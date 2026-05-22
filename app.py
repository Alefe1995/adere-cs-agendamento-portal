import streamlit as st
from components.ui import setup_page, header, kpi_card, panel
from services.data_loader import load_data, filter_bar
from utils.kpis import main_kpis, top_counts
from utils.charts import bar_count, line_by_period

setup_page("Dashboard")
df = load_data()
header("Dashboard", "Visão executiva do portal de agendamentos")
f = filter_bar(df)
k = main_kpis(f)

c = st.columns(6)
with c[0]: kpi_card("📄", "Total de NFs", f"{k['total']:,}".replace(",","."), "↑ 12,5% vs período anterior", "blue")
with c[1]: kpi_card("🕘", "Agendamentos Pendentes", k["pendentes"], "↑ 8,3% vs período anterior", "warn")
with c[2]: kpi_card("📅", "Entregas Agendadas", k["agendados"], "↑ 15,7% vs período anterior", "good")
with c[3]: kpi_card("🔄", "Reagendamentos", k["reag"], "↑ 10,6% vs período anterior", "purple")
with c[4]: kpi_card("⚠️", "Atrasos", k["atrasos"], "↑ 25,0% vs período anterior", "bad")
with c[5]: kpi_card("🎯", "SLA de Agendamento", f"{k['sla']}%", "↑ 4,2 p.p. vs período anterior", "blue")

left, right = st.columns([.78,.22])
with left:
    g1, g2 = st.columns([.45,.55])
    with g1: st.plotly_chart(bar_count(f, "UF", "Agendamentos por UF"), use_container_width=True)
    with g2: st.plotly_chart(line_by_period(f, "Data Envio de agendamento", "Evolução semanal de agendamentos"), use_container_width=True)
    st.markdown("### Fluxo operacional")
    cols = st.columns(5)
    stages = ["A Enviar", "Aguardando Cliente", "Confirmada", "Atrasada", "Entregue"]
    for col, s in zip(cols, stages):
        with col:
            qtd = int((f["Status"] == s).sum())
            sample = f[f["Status"] == s].head(2)
            body = "".join([f"<div class='alert blue'><b>NF {r.NF}</b><br>{r.Cliente}<br><span class='muted'>{r.Transportadora}</span></div>" for _, r in sample.iterrows()])
            panel(f"{s} <span class='chip blue'>{qtd}</span>", body or "<span class='muted'>Sem registros</span>")
    st.markdown("### Agendamentos")
    cols_view = ["Cliente","CNPJ Cliente","NF","Destino","UF","Transportadora","RC","Coordenador","Data Envio de agendamento","Data Agendada","Reagendamento?","Data Entrerga","Analista","Status"]
    st.dataframe(f[[c for c in cols_view if c in f.columns]].head(200), use_container_width=True, hide_index=True)
with right:
    panel("Alertas e Insights", "")
    panel("5 entregas vencidas", "<div class='alert red'>Confira entregas com atraso superior a 24h.<br><span class='small-link'>Ver detalhes →</span></div>")
    panel("NFs sem data agendada", "<div class='alert orange'>NFs aguardando agendamento há mais de 48h.<br><span class='small-link'>Ver detalhes →</span></div>")
    top_transp = top_counts(f, "Transportadora", 1)
    txt = top_transp.iloc[0,0] if len(top_transp) else "-"
    panel("Transportadora com maior volume", f"<div class='alert blue'><b>{txt}</b><br>{int(top_transp.iloc[0,1]) if len(top_transp) else 0} agendamentos</div>")
