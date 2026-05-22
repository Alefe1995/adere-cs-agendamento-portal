"""Transportadoras: volume, SLA e desempenho por parceiro logístico."""
import streamlit as st

from components.ui import setup_page, header, kpi_card, panel
from services.data_loader import load_data, filter_bar
from utils.charts import bar_count

setup_page("Transportadoras")
df = load_data()
header("Transportadoras", "Volume, SLA e desempenho por parceiro logístico")

f = filter_bar(df)

if "Transportadora" in f.columns and not f.empty:
    rank = (
        f.groupby("Transportadora")
        .agg(**{
            "Volume de NFs": ("NF", "count") if "NF" in f.columns else ("Transportadora", "size"),
            "Entregas agendadas": ("Data Agendada", lambda x: x.notna().sum())
                if "Data Agendada" in f.columns else ("Transportadora", "size"),
            "Atrasos": ("Atrasado", "sum") if "Atrasado" in f.columns else ("Transportadora", "size"),
            "SLA": ("SLAStatus", lambda x: round(x.eq("Dentro SLA").mean() * 100, 1))
                if "SLAStatus" in f.columns else ("Transportadora", "size"),
            "Reagendamentos": ("Reagendamento?", "sum")
                if "Reagendamento?" in f.columns else ("Transportadora", "size"),
            "Último envio": ("Data Envio de agendamento", "max")
                if "Data Envio de agendamento" in f.columns else ("Transportadora", "first"),
        })
        .reset_index()
        .sort_values("Volume de NFs", ascending=False)
    )
else:
    rank = f.iloc[0:0]

cs = st.columns(5)
with cs[0]:
    kpi_card("🚚", "Transportadoras ativas",
             rank["Transportadora"].nunique() if len(rank) else 0,
             "↑ 2,4%", "blue")
with cs[1]:
    if len(rank):
        top = rank.iloc[0]
        kpi_card("📊", "Maior volume", str(top["Transportadora"]),
                 f"{int(top['Volume de NFs'])} NFs", "warn")
    else:
        kpi_card("📊", "Maior volume", "-", "Sem dados", "warn")
with cs[2]:
    sla_medio = f"{rank['SLA'].mean():.1f}%" if len(rank) and "SLA" in rank.columns else "0%"
    kpi_card("✅", "SLA médio", sla_medio, "↑ 2,8%", "good")
with cs[3]:
    atrasos = int(f["Atrasado"].sum()) if "Atrasado" in f.columns else 0
    kpi_card("⚠️", "Atrasos", atrasos, "↑ 15,3%", "bad")
with cs[4]:
    reag = int(f["Reagendamento?"].sum()) if "Reagendamento?" in f.columns else 0
    kpi_card("🔄", "Reagendamentos", reag, "↑ 8,6%", "purple")

c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(
        bar_count(f, "Transportadora", "Ranking por volume", horizontal=True),
        use_container_width=True,
    )
with c2:
    if "SLAStatus" in f.columns:
        st.plotly_chart(
            bar_count(f[f["SLAStatus"].ne("Dentro SLA")], "Transportadora",
                      "SLA abaixo da meta", horizontal=True),
            use_container_width=True,
        )
    else:
        st.info("Coluna `SLAStatus` não disponível para este gráfico.")

st.markdown("### Cards de transportadoras")
if len(rank):
    for col, (_, r) in zip(st.columns(4), rank.head(4).iterrows()):
        with col:
            sla_val = r.get("SLA", "-")
            panel(
                str(r["Transportadora"]),
                f"<b>{int(r['Volume de NFs'])}</b> NFs"
                f"<br>Performance SLA: <b>{sla_val}%</b>",
            )
else:
    st.info("Sem transportadoras no período filtrado.")

st.dataframe(rank, use_container_width=True, hide_index=True)
