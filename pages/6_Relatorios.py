import streamlit as st
from io import BytesIO
from components.ui import setup_page, header, kpi_card, panel
from services.data_loader import load_data, filter_bar
from utils.charts import bar_count, line_by_period
from utils.kpis import main_kpis

setup_page("Relatórios")
df=load_data(); header("Relatórios", "Indicadores consolidados e exportações")
f=filter_bar(df); k=main_kpis(f)
cs=st.columns(5)
with cs[0]: kpi_card("📋","Relatórios salvos", 24, "↑ 14,3%", "blue")
with cs[1]: kpi_card("🕘","Última atualização", "Automática", "pela planilha Excel", "warn")
with cs[2]: kpi_card("📈","Métricas", 18, "↑ 12,5%", "good")
with cs[3]: kpi_card("🔄","SLA consolidado", f"{k['sla']}%", "↑ 3,1 p.p.", "purple")
with cs[4]: kpi_card("📈","Tendência", "Positiva", "Melhoria consistente", "bad")
colA,colB,colC=st.columns(3)
with colA: st.plotly_chart(line_by_period(f,"Data Envio de agendamento","Performance operacional"), use_container_width=True)
with colB: st.plotly_chart(bar_count(f,"Cliente","SLA por Cliente"), use_container_width=True)
with colC: st.plotly_chart(bar_count(f,"Transportadora","SLA por Transportadora", horizontal=True), use_container_width=True)
st.markdown("### Resumo comparativo")
resumo=f.groupby("Mes").agg(Agendamentos=("NF","count"),Atrasos=("Atrasado","sum"),Reagendamentos=("Reagendamento?","sum"),SLA=("SLAStatus",lambda x: round(x.eq("Dentro SLA").mean()*100,1))).reset_index()
st.dataframe(resumo, use_container_width=True, hide_index=True)
buf=BytesIO(); f.to_excel(buf,index=False)
st.download_button("⬇️ Baixar Excel filtrado", data=buf.getvalue(), file_name="relatorio_agendamentos.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
