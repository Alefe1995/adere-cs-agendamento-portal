import streamlit as st
from components.ui import setup_page, header, kpi_card, panel
from services.data_loader import load_data, filter_bar
from utils.charts import donut, line_by_period

setup_page("Reagendamentos")
df = load_data(); header("Reagendamentos", "Controle de solicitações e alterações de datas")
f = filter_bar(df); reag = f[(f["Reagendamento?"]) | (f["QtdReagendamentos"] > 0)]
cs=st.columns(5)
with cs[0]: kpi_card("📅", "Reagendamentos", len(reag), "↑ 18,7%", "good")
with cs[1]: kpi_card("⚠️", "Críticos", int((reag["Prioridade"]=="Crítica").sum()), "↑ 8,3%", "bad")
with cs[2]: kpi_card("👤", "Por solicitação", int(reag["MotivoReagendamento"].str.contains("cliente|indisponível",case=False,na=False).sum()), "↑ 12,6%", "blue")
with cs[3]: kpi_card("⚙️", "Falha operacional", int(reag["MotivoReagendamento"].str.contains("falha|capacidade",case=False,na=False).sum()), "↑ 24,5%", "bad")
with cs[4]: kpi_card("✅", "Taxa de sucesso", "92,4%", "↑ 4,2 p.p.", "blue")
c1,c2=st.columns([.35,.65])
with c1: st.plotly_chart(donut(reag,"MotivoReagendamento","Motivos de reagendamento"), use_container_width=True)
with c2: st.plotly_chart(line_by_period(reag,"Data Agendada","Reagendamentos por semana"), use_container_width=True)
st.markdown("### Workflow")
for col, status in zip(st.columns(5), ["Solicitado","Em análise","Nova data proposta","Confirmado","Concluído"]):
    with col: panel(status, "<div class='alert blue'>Casos simulados pelo status operacional da planilha.</div>")
st.dataframe(reag[["NF","Cliente","MotivoReagendamento","Data Sugerida de agendamento","Data Agendada","QtdReagendamentos","Transportadora","ResponsavelAcao","Status"]].head(300), use_container_width=True, hide_index=True)
