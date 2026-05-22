from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st

DATA_PATH = Path("data/agendamentos.xlsx")
DATE_COLS = [
    "Data Envio de agendamento","Data Sugerida de agendamento","Data Agendada","Data Cobrada",
    "Data Envio a Transportadora","Data Entrerga","DataUltimaAtualizacaoStatus",
    "DataPrimeiroEnvioTransportadora","Data_Faturamento","Data_Agendada"
]

@st.cache_data(show_spinner=False)
def load_data(path: str = str(DATA_PATH)) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="agendamentos")
    df.columns = [str(c).strip() for c in df.columns]
    for c in DATE_COLS:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    text_cols = ["Cliente","UF","Transportadora","Coordenador","Analista","Status","Prioridade","TipoPendencia","MotivoPendencia","MotivoReagendamento","ResponsavelAcao"]
    for c in text_cols:
        if c in df.columns:
            df[c] = df[c].fillna("Não informado").astype(str).str.strip()
    bool_cols = ["Atrasado", "Reagendamento?"]
    for c in bool_cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.lower().isin(["sim","true","1","yes"])
    df["Mes"] = df["Data Envio de agendamento"].dt.to_period("M").astype(str) if "Data Envio de agendamento" in df else ""
    df["Semana"] = df["Data Envio de agendamento"].dt.to_period("W").astype(str) if "Data Envio de agendamento" in df else ""
    return df

def filter_data(df, cliente="Todos", uf="Todos", transportadora="Todos", analista="Todos", status="Todos", periodo=None):
    f = df.copy()
    if cliente != "Todos": f = f[f["Cliente"] == cliente]
    if uf != "Todos": f = f[f["UF"] == uf]
    if transportadora != "Todos": f = f[f["Transportadora"] == transportadora]
    if analista != "Todos": f = f[f["Analista"] == analista]
    if status != "Todos": f = f[f["Status"] == status]
    if periodo and "Data Envio de agendamento" in f:
        ini, fim = periodo
        f = f[(f["Data Envio de agendamento"].dt.date >= ini) & (f["Data Envio de agendamento"].dt.date <= fim)]
    return f

def filter_bar(df):
    c1,c2,c3,c4,c5,c6 = st.columns([1.3,.8,1.2,1,1,1.2])
    with c1: cliente = st.selectbox("Cliente", ["Todos"] + sorted(df["Cliente"].dropna().unique().tolist()))
    with c2: uf = st.selectbox("UF", ["Todos"] + sorted(df["UF"].dropna().unique().tolist()))
    with c3: transp = st.selectbox("Transportadora", ["Todos"] + sorted(df["Transportadora"].dropna().unique().tolist()))
    with c4: analista = st.selectbox("Analista", ["Todos"] + sorted(df["Analista"].dropna().unique().tolist()))
    with c5: status = st.selectbox("Status", ["Todos"] + sorted(df["Status"].dropna().unique().tolist()))
    min_d = df["Data Envio de agendamento"].min().date(); max_d = df["Data Envio de agendamento"].max().date()
    with c6: periodo = st.date_input("Período", value=(min_d, max_d), min_value=min_d, max_value=max_d)
    if not isinstance(periodo, tuple) or len(periodo) != 2:
        periodo = (min_d, max_d)
    return filter_data(df, cliente, uf, transp, analista, status, periodo)
