"""
Camada de leitura, normalização e filtragem dos dados.
- Não assume colunas que podem não existir.
- Tolera valores nulos em datas (NaT) e DataFrames vazios.
- Cache invalidado quando o arquivo da planilha muda (mtime).
"""
from pathlib import Path
from datetime import date
import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "agendamentos.xlsx"

DATE_COLS = [
    "Data Envio de agendamento",
    "Data Sugerida de agendamento",
    "Data Agendada",
    "Data Cobrada",
    "Data Envio a Transportadora",
    "Data Entrerga",
    "DataUltimaAtualizacaoStatus",
    "DataPrimeiroEnvioTransportadora",
    "Data_Faturamento",
    "Data_Agendada",
]

TEXT_COLS = [
    "Cliente", "UF", "Transportadora", "Coordenador", "Analista",
    "Status", "Prioridade", "TipoPendencia", "MotivoPendencia",
    "MotivoReagendamento", "ResponsavelAcao", "Destino", "Cidade",
    "CNPJ Cliente", "RC",
]

BOOL_COLS = ["Atrasado", "Reagendamento?"]


def _file_signature(path: Path) -> tuple:
    """Assinatura de invalidação de cache. Se o arquivo muda, o cache cai."""
    try:
        stat = path.stat()
        return (str(path), stat.st_mtime_ns, stat.st_size)
    except FileNotFoundError:
        return (str(path), 0, 0)


@st.cache_data(show_spinner="Carregando planilha...")
def _read_excel(path_str: str, signature: tuple) -> pd.DataFrame:
    """O parâmetro `signature` força o cache a recarregar quando o arquivo muda.

    Lê a aba `agendamentos` sem depender de maiúsculas/minúsculas.
    Se a aba não existir, usa a primeira aba do arquivo.
    """
    xls = pd.ExcelFile(path_str)
    sheet = next((s for s in xls.sheet_names if s.strip().lower() == "agendamentos"), xls.sheet_names[0])
    df = pd.read_excel(path_str, sheet_name=sheet)
    df.columns = [str(c).strip() for c in df.columns]

    for c in DATE_COLS:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")

    for c in TEXT_COLS:
        if c in df.columns:
            df[c] = df[c].fillna("Não informado").astype(str).str.strip()

    for c in BOOL_COLS:
        if c in df.columns:
            df[c] = df[c].astype(str).str.lower().isin(["sim", "true", "1", "yes", "s"])

    # Períodos derivados apenas quando a base existir
    if "Data Envio de agendamento" in df.columns:
        df["Mes"] = df["Data Envio de agendamento"].dt.to_period("M").astype(str)
        df["Semana"] = df["Data Envio de agendamento"].dt.to_period("W").astype(str)
    else:
        df["Mes"] = ""
        df["Semana"] = ""

    return df


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    if not path.exists():
        st.error(
            f"Arquivo de dados não encontrado: `{path}`. "
            "Coloque sua planilha em `data/agendamentos.xlsx` ou ajuste o caminho."
        )
        st.stop()
    return _read_excel(str(path), _file_signature(path))


def _safe_unique(df: pd.DataFrame, col: str) -> list:
    if col not in df.columns:
        return []
    return sorted(df[col].dropna().astype(str).unique().tolist())


def _safe_date_bounds(df: pd.DataFrame, col: str):
    """Retorna (min, max) seguro mesmo com NaT ou DataFrame vazio."""
    today = date.today()
    if col not in df.columns or df[col].dropna().empty:
        return today, today
    s = df[col].dropna()
    return s.min().date(), s.max().date()


def filter_data(df, cliente="Todos", uf="Todos", transportadora="Todos",
                analista="Todos", status="Todos", periodo=None) -> pd.DataFrame:
    f = df
    if cliente != "Todos" and "Cliente" in f.columns:
        f = f[f["Cliente"] == cliente]
    if uf != "Todos" and "UF" in f.columns:
        f = f[f["UF"] == uf]
    if transportadora != "Todos" and "Transportadora" in f.columns:
        f = f[f["Transportadora"] == transportadora]
    if analista != "Todos" and "Analista" in f.columns:
        f = f[f["Analista"] == analista]
    if status != "Todos" and "Status" in f.columns:
        f = f[f["Status"] == status]
    if periodo and "Data Envio de agendamento" in f.columns:
        ini, fim = periodo
        col = f["Data Envio de agendamento"]
        mask = col.notna() & (col.dt.date >= ini) & (col.dt.date <= fim)
        f = f[mask]
    return f


def filter_bar(df: pd.DataFrame) -> pd.DataFrame:
    """Barra de filtros padronizada. Cada coluna é renderizada só se existir."""
    c1, c2, c3, c4, c5, c6 = st.columns([1.3, 0.8, 1.2, 1.0, 1.0, 1.2])

    with c1:
        cliente = st.selectbox("Cliente", ["Todos"] + _safe_unique(df, "Cliente"))
    with c2:
        uf = st.selectbox("UF", ["Todos"] + _safe_unique(df, "UF"))
    with c3:
        transp = st.selectbox("Transportadora", ["Todos"] + _safe_unique(df, "Transportadora"))
    with c4:
        analista = st.selectbox("Analista", ["Todos"] + _safe_unique(df, "Analista"))
    with c5:
        status = st.selectbox("Status", ["Todos"] + _safe_unique(df, "Status"))

    min_d, max_d = _safe_date_bounds(df, "Data Envio de agendamento")
    with c6:
        periodo = st.date_input(
            "Período",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
        )

    # st.date_input devolve uma única data enquanto o usuário ainda não escolheu o fim.
    if not isinstance(periodo, tuple) or len(periodo) != 2:
        periodo = (min_d, max_d)

    return filter_data(df, cliente, uf, transp, analista, status, periodo)
