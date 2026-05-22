import streamlit as st
from components.ui import setup_page, header, kpi_card, panel
from services.data_loader import load_data, filter_bar
from utils.charts import bar_count, scatter_sla_volume

setup_page("Clientes")
df=load_data(); header("Clientes", "Carteira, volume, SLA e risco por cliente")
f=filter_bar(df)
cli=f.groupby(["Cliente","CNPJ Cliente","UF"]).agg(**{"Volume de NFs":("NF","count"),"Pendências":("Atrasado","sum"),"Reagendamentos":("Reagendamento?","sum"),"SLA":("SLAStatus",lambda x: round(x.eq("Dentro SLA").mean()*100,1)),"Último agendamento":("Data Agendada","max"),"Analista responsável":("Analista","first")}).reset_index().sort_values("Volume de NFs",ascending=False)
cs=st.columns(5)
with cs[0]: kpi_card("👥","Clientes ativos", cli["Cliente"].nunique(), "↑ 8,2%", "blue")
with cs[1]: kpi_card("🚚","Maior volume", cli.iloc[0]["Cliente"] if len(cli) else "-", "Top cliente", "good")
with cs[2]: kpi_card("⚠️","Mais pendências", int((cli["Pendências"]>0).sum()), "↑ 15,6%", "bad")
with cs[3]: kpi_card("🏅","Melhor SLA", int((cli["SLA"]>=90).sum()), "↑ 6,7%", "purple")
with cs[4]: kpi_card("🕒","Tempo médio", f"{f['SLA_Dias'].mean():.1f} dias" if "SLA_Dias" in f else "-", "↓ 5,3%", "blue")
c1,c2=st.columns(2)
with c1: st.plotly_chart(bar_count(f,"Cliente","Volume por cliente"), use_container_width=True)
with c2: st.plotly_chart(scatter_sla_volume(f), use_container_width=True)
st.markdown("### Contas prioritárias")
for col, (_, r) in zip(st.columns(5), cli.head(5).iterrows()):
    with col: panel(str(r["Cliente"]), f"{r['UF']}<br><b>{int(r['Volume de NFs'])}</b> NFs/mês<br>SLA: <b>{r['SLA']}%</b>")
st.dataframe(cli, use_container_width=True, hide_index=True)
