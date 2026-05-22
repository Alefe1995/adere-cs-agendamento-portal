import streamlit as st
from components.ui import setup_page, header, kpi_card, panel
from services.data_loader import load_data, filter_bar
from utils.charts import bar_count, line_by_period

setup_page("Pendências")
df = load_data(); header("Pendências", "Priorização de exceções e aging")
f = filter_bar(df)
pend = f[(f["Atrasado"]) | (f["Prioridade"].isin(["Crítica","Alta"])) | (f["Status"].isin(["Aguardando Cliente","Atrasada"]))]
cs = st.columns(5)
with cs[0]: kpi_card("⚠️", "Pendências críticas", int((pend["Prioridade"]=="Crítica").sum()), "↑ 18,7%", "bad")
with cs[1]: kpi_card("📆", "Sem data agendada", int(pend["Data Agendada"].isna().sum()), "↑ 22,1%", "warn")
with cs[2]: kpi_card("🔄", "Aguardando retorno", int((pend["Status"]=="Aguardando Cliente").sum()), "↑ 14,3%", "blue")
with cs[3]: kpi_card("🔒", "Bloqueios de entrega", int((pend["TipoPendencia"].str.contains("Bloqueio|Transportadora", case=False, na=False)).sum()), "↓ 5,6%", "purple")
with cs[4]: kpi_card("🕒", "Tempo médio", f"{pend['DiasEmAberto'].mean():.1f} dias" if len(pend) else "0 dias", "↑ 0,4 dia", "good")
left, right = st.columns([.73,.27])
with left:
    st.markdown("### Matriz de prioridades")
    cols = st.columns(4)
    for col, pri in zip(cols, ["Crítica","Alta","Média","Baixa"]):
        with col:
            part = pend[pend["Prioridade"]==pri].head(5)
            cards = "".join([f"<div class='alert {'red' if pri=='Crítica' else 'orange'}'><b>NF {r.NF}</b><br>{r.Cliente}<br>{r.MotivoPendencia}</div>" for _, r in part.iterrows()])
            panel(f"{pri} <span class='chip red'>{len(part)}</span>", cards or "<span class='muted'>Sem registros</span>")
    c1,c2 = st.columns(2)
    with c1: st.plotly_chart(bar_count(pend, "MotivoPendencia", "Pendências por motivo", horizontal=True), use_container_width=True)
    with c2: st.plotly_chart(line_by_period(f, "Data Envio de agendamento", "Evolução de pendências"), use_container_width=True)
    st.dataframe(pend[["NF","Cliente","MotivoPendencia","Transportadora","ResponsavelAcao","DiasEmAberto","ProximaAcao","Status"]].head(300), use_container_width=True, hide_index=True)
with right:
    panel("Alertas e insights", "")
    panel("NFs há mais de 48h", "<div class='alert red'>Casos sem agendamento exigem ação imediata.</div>")
    panel("Clientes aguardando retorno", "<div class='alert orange'>Revise a carteira de clientes em aberto.</div>")
    panel("Pendências por transportadora", "<div class='alert blue'>Ranking ajuda a priorizar contatos.</div>")
