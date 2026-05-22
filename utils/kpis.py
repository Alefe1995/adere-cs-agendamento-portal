import pandas as pd
import numpy as np

def pct(n, d):
    return 0 if d == 0 else round((n / d) * 100, 1)

def main_kpis(df):
    total = len(df)
    pendentes = df["Status"].isin(["Aguardando Cliente", "Atrasada", "Pendente", "Em Contato", "A Enviar", "Reagendar"]).sum() if "Status" in df else 0
    agendados = df["Data Agendada"].notna().sum() if "Data Agendada" in df else 0
    reag = df["Reagendamento?"].sum() if "Reagendamento?" in df else 0
    atrasos = df["Atrasado"].sum() if "Atrasado" in df else 0
    sla = pct((df["SLAStatus"].eq("Dentro SLA")).sum(), total) if "SLAStatus" in df else 0
    return {"total": total, "pendentes": int(pendentes), "agendados": int(agendados), "reag": int(reag), "atrasos": int(atrasos), "sla": sla}

def top_counts(df, col, n=10):
    if col not in df: return pd.DataFrame({col:[], "Quantidade":[]})
    return df[col].value_counts().head(n).rename_axis(col).reset_index(name="Quantidade")

def status_order():
    return ["A Enviar", "Em Contato", "Aguardando Cliente", "Confirmada", "Faturada", "Atrasada", "Entregue"]
