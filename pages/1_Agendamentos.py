import streamlit as st
from components.ui import setup_page, header, kpi_card
from services.data_loader import load_data, filter_bar
from utils.kpis import main_kpis

setup_page("Agendamentos")
df = load_data(); header("Agendamentos", "Tela operacional com lista, kanban e calendário")
f = filter_bar(df); k = main_kpis(f)
cols = st.columns(5)
with cols[0]: kpi_card("📅", "Total em aberto", k["total"], "↑ 12,3% vs período anterior", "blue")
with cols[1]: kpi_card("🕘", "Agendados hoje", int((f["Data Agendada"].dt.date == f["Data Agendada"].max().date()).sum()) if f["Data Agendada"].notna().any() else 0, "↑ 8,4% vs ontem", "warn")
with cols[2]: kpi_card("🚚", "Sem retorno", int((f["HorasSemRetorno"] > 24).sum()) if "HorasSemRetorno" in f else 0, "↑ 15,7%", "purple")
with cols[3]: kpi_card("✅", "Concluídos", int((f["Status"].isin(["Entregue","Faturada"])).sum()), "↑ 16,7%", "good")
with cols[4]: kpi_card("🎯", "SLA médio", f"{k['sla']}%", "↑ 4,2 p.p.", "blue")

tab1, tab2, tab3 = st.tabs(["☰ Lista", "▦ Kanban", "🗓️ Calendário"])
cols_view = ["Cliente","CNPJ Cliente","NF","Destino","UF","Transportadora","RC","Coordenador","Data Envio de agendamento","Data Sugerida de agendamento","Data Agendada","Status","Reagendamento?","Data Entrerga","Analista"]
with tab1:
    busca = st.text_input("Buscar por NF, cliente ou transportadora")
    show = f.copy()
    if busca:
        b = busca.lower()
        show = show[show.astype(str).apply(lambda row: row.str.lower().str.contains(b, regex=False).any(), axis=1)]
    st.dataframe(show[[c for c in cols_view if c in show.columns]].head(500), use_container_width=True, hide_index=True)
with tab2:
    stages = ["A Enviar", "Aguardando Cliente", "Confirmada", "Atrasada", "Entregue"]
    cs = st.columns(len(stages))
    for col, stage in zip(cs, stages):
        with col:
            st.markdown(f"#### {stage}")
            part = f[f["Status"] == stage].head(8)
            for _, r in part.iterrows():
                st.markdown(f"<div class='panel'><b>NF {r.NF}</b><br>{r.Cliente}<br>{r.Transportadora}<br><span class='muted'>{r.Analista}</span></div>", unsafe_allow_html=True)
with tab3:
    cal = f.dropna(subset=["Data Agendada"]).sort_values("Data Agendada")[["Data Agendada","NF","Cliente","Transportadora","Status","Analista"]]
    st.dataframe(cal.head(300), use_container_width=True, hide_index=True)
