"""Clientes: carteira, volume, SLA e risco por cliente."""
import streamlit as st

from components.ui import setup_page, header, kpi_card, panel
from services.data_loader import load_data, filter_bar
from utils.charts import bar_count, scatter_sla_volume

setup_page("Clientes")
df = load_data()
header("Clientes", "Carteira, volume, SLA e risco por cliente")

f = filter_bar(df)

needed = {"Cliente", "CNPJ Cliente", "UF", "NF"}
if needed.issubset(f.columns) and not f.empty:
    aggs = {"Volume de NFs": ("NF", "count")}
    if "Atrasado" in f.columns:
        aggs["Pendências"] = ("Atrasado", "sum")
    if "Reagendamento?" in f.columns:
        aggs["Reagendamentos"] = ("Reagendamento?", "sum")
    if "SLAStatus" in f.columns:
        aggs["SLA"] = ("SLAStatus", lambda x: round(x.eq("Dentro SLA").mean() * 100, 1))
    if "Data Agendada" in f.columns:
        aggs["Último agendamento"] = ("Data Agendada", "max")
    if "Analista" in f.columns:
        aggs["Analista responsável"] = ("Analista", "first")

    cli = (
        f.groupby(["Cliente", "CNPJ Cliente", "UF"])
        .agg(**aggs)
        .reset_index()
        .sort_values("Volume de NFs", ascending=False)
    )
else:
    cli = f.iloc[0:0]

cs = st.columns(5)
with cs[0]:
    kpi_card("👥", "Clientes ativos",
             cli["Cliente"].nunique() if len(cli) else 0, "↑ 8,2%", "blue")
with cs[1]:
    if len(cli):
        kpi_card("🚚", "Maior volume", str(cli.iloc[0]["Cliente"]), "Top cliente", "good")
    else:
        kpi_card("🚚", "Maior volume", "-", "Sem dados", "good")
with cs[2]:
    com_pend = int((cli["Pendências"] > 0).sum()) if "Pendências" in cli.columns else 0
    kpi_card("⚠️", "Com pendências", com_pend, "↑ 15,6%", "bad")
with cs[3]:
    melhor_sla = int((cli["SLA"] >= 90).sum()) if "SLA" in cli.columns else 0
    kpi_card("🏅", "SLA ≥ 90%", melhor_sla, "↑ 6,7%", "purple")
with cs[4]:
    if "SLA_Dias" in f.columns and f["SLA_Dias"].notna().any():
        kpi_card("🕒", "Tempo médio", f"{f['SLA_Dias'].mean():.1f} dias", "↓ 5,3%", "blue")
    else:
        kpi_card("🕒", "Tempo médio", "-", "Sem dados", "blue")

c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(bar_count(f, "Cliente", "Volume por cliente"), use_container_width=True)
with c2:
    st.plotly_chart(scatter_sla_volume(f), use_container_width=True)

st.markdown("### Contas prioritárias")
if len(cli):
    for col, (_, r) in zip(st.columns(5), cli.head(5).iterrows()):
        with col:
            sla_val = r.get("SLA", "-")
            panel(
                str(r["Cliente"]),
                f"{r.get('UF','-')}<br><b>{int(r['Volume de NFs'])}</b> NFs/mês"
                f"<br>SLA: <b>{sla_val}%</b>",
            )
else:
    st.info("Sem clientes no período filtrado.")

st.dataframe(cli, use_container_width=True, hide_index=True)
