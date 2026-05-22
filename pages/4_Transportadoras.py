import streamlit as st
from components.ui import setup_page, header, kpi_card, panel
from services.data_loader import load_data, filter_bar
from utils.charts import bar_count

setup_page("Transportadoras")
df=load_data(); header("Transportadoras", "Volume, SLA e desempenho por parceiro logístico")
f=filter_bar(df)
rank=f.groupby("Transportadora").agg(**{"Volume de NFs":("NF","count"),"Entregas agendadas":("Data Agendada",lambda x:x.notna().sum()),"Atrasos":("Atrasado","sum"),"SLA":("SLAStatus",lambda x: round(x.eq("Dentro SLA").mean()*100,1)),"Reagendamentos":("Reagendamento?","sum"),"Último envio":("Data Envio de agendamento","max")}).reset_index().sort_values("Volume de NFs",ascending=False)
cs=st.columns(5)
with cs[0]: kpi_card("🚚","Transportadoras ativas", rank["Transportadora"].nunique(), "↑ 2,4%", "blue")
with cs[1]: kpi_card("📊","Maior volume", rank.iloc[0]["Transportadora"] if len(rank) else "-", f"{int(rank.iloc[0]['Volume de NFs']) if len(rank) else 0} NFs", "warn")
with cs[2]: kpi_card("✅","SLA médio", f"{rank['SLA'].mean():.1f}%" if len(rank) else "0%", "↑ 2,8%", "good")
with cs[3]: kpi_card("⚠️","Atrasos", int(f["Atrasado"].sum()), "↑ 15,3%", "bad")
with cs[4]: kpi_card("🔄","Reagendamentos", int(f["Reagendamento?"].sum()), "↑ 8,6%", "purple")
c1,c2=st.columns(2)
with c1: st.plotly_chart(bar_count(f,"Transportadora","Ranking por volume", horizontal=True), use_container_width=True)
with c2: st.plotly_chart(bar_count(f[f["SLAStatus"].ne("Dentro SLA")],"Transportadora","SLA abaixo da meta", horizontal=True), use_container_width=True)
st.markdown("### Cards de transportadoras")
for col, (_, r) in zip(st.columns(4), rank.head(4).iterrows()):
    with col: panel(str(r["Transportadora"]), f"<b>{int(r['Volume de NFs'])}</b> NFs<br>Performance SLA: <b>{r['SLA']}%</b>")
st.dataframe(rank, use_container_width=True, hide_index=True)
