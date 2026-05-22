"""Cálculo dos KPIs principais. Tudo defensivo contra colunas ausentes/DF vazio."""
import pandas as pd


def pct(n, d) -> float:
    return 0.0 if not d else round((n / d) * 100, 1)


def _safe_sum_bool(df: pd.DataFrame, col: str) -> int:
    if col not in df.columns:
        return 0
    return int(df[col].fillna(False).astype(bool).sum())


def _safe_isin_count(df: pd.DataFrame, col: str, values) -> int:
    if col not in df.columns:
        return 0
    return int(df[col].isin(values).sum())


def main_kpis(df: pd.DataFrame) -> dict:
    total = len(df)
    pendentes = _safe_isin_count(
        df, "Status",
        ["Aguardando Cliente", "Atrasada", "Pendente", "Em Contato", "A Enviar", "Reagendar"],
    )
    agendados = int(df["Data Agendada"].notna().sum()) if "Data Agendada" in df.columns else 0
    reag = _safe_sum_bool(df, "Reagendamento?")
    atrasos = _safe_sum_bool(df, "Atrasado")
    sla = pct((df["SLAStatus"].eq("Dentro SLA")).sum(), total) if "SLAStatus" in df.columns else 0.0
    return {
        "total": int(total),
        "pendentes": pendentes,
        "agendados": agendados,
        "reag": reag,
        "atrasos": atrasos,
        "sla": sla,
    }


def top_counts(df: pd.DataFrame, col: str, n: int = 10) -> pd.DataFrame:
    if col not in df.columns or df.empty:
        return pd.DataFrame({col: [], "Quantidade": []})
    return (
        df[col].value_counts().head(n)
        .rename_axis(col).reset_index(name="Quantidade")
    )


def status_order():
    # Lista canônica — útil em ordenações
    return [
        "A Enviar", "Em Contato", "Aguardando Cliente",
        "Confirmada", "Agendada", "Faturada", "Em Transporte",
        "Atrasada", "Crítica", "Entregue",
    ]
