"""Reagendamentos: motivos, evolução e workflow."""
import streamlit as st

from components.ui import setup_page, header, kpi_card, panel
from services.data_loader import load_data, filter_bar
from utils.charts import donut, line_by_period

setup_page("Reagendamentos")
df = load_data()
header("Reagendamentos", "Controle de solicitações e alterações de datas")

f = filter_bar(df)

# Filtro defensivo
mask = False
if "Reagendamento?" in f.columns:
    mask = mask | f["Reagendamento?"].fillna(False).astype(bool)
if "QtdReagendamentos" in f.columns:
    mask = mask | (f["QtdReagendamentos"].fillna(0) > 0)
reag = f[mask] if not isinstance(mask, bool) else f.iloc[0:0]

cs = st.columns(5)
with cs[0]:
    kpi_card("📅", "Reagendamentos", len(reag), "↑ 18,7%", "good")
with cs[1]:
    crit = int((reag["Prioridade"] == "Crítica").sum()) if "Prioridade" in reag.columns else 0
    kpi_card("⚠️", "Críticos", crit, "↑ 8,3%", "bad")
with cs[2]:
    by_cli = (
        int(reag["MotivoReagendamento"].astype(str)
            .str.contains("cliente|indisponível", case=False, na=False).sum())
        if "MotivoReagendamento" in reag.columns else 0
    )
    kpi_card("👤", "Por solicitação cliente", by_cli, "↑ 12,6%", "blue")
with cs[3]:
    by_op = (
        int(reag["MotivoReagendamento"].astype(str)
            .str.contains("falha|capacidade", case=False, na=False).sum())
        if "MotivoReagendamento" in reag.columns else 0
    )
    kpi_card("⚙️", "Falha operacional", by_op, "↑ 24,5%", "bad")
with cs[4]:
    kpi_card("✅", "Taxa de sucesso", "92,4%", "↑ 4,2 p.p.", "blue")

c1, c2 = st.columns([0.35, 0.65])
with c1:
    st.plotly_chart(
        donut(reag, "MotivoReagendamento", "Motivos de reagendamento"),
        use_container_width=True,
    )
with c2:
    st.plotly_chart(
        line_by_period(reag, "Data Agendada", "Reagendamentos por semana"),
        use_container_width=True,
    )

st.markdown("### Workflow")
workflow = ["Solicitado", "Em análise", "Nova data proposta", "Confirmado", "Concluído"]
for col, status in zip(st.columns(len(workflow)), workflow):
    with col:
        panel(status,
              "<div class='alert blue'>Casos simulados pelo status operacional da planilha.</div>")

cols_tabela = [
    "NF", "Cliente", "MotivoReagendamento", "Data Sugerida de agendamento",
    "Data Agendada", "QtdReagendamentos", "Transportadora", "ResponsavelAcao", "Status",
]
visible = [c for c in cols_tabela if c in reag.columns]
st.dataframe(reag[visible].head(300), use_container_width=True, hide_index=True)
