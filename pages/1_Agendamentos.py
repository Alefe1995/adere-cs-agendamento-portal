"""Tela operacional de agendamentos: lista, kanban e calendário."""
from datetime import date
import streamlit as st

from components.ui import setup_page, header, kpi_card
from services.data_loader import load_data, filter_bar
from utils.kpis import main_kpis

setup_page("Agendamentos")
df = load_data()
header("Agendamentos", "Tela operacional com lista, kanban e calendário")

f = filter_bar(df)
k = main_kpis(f)

# ---- KPIs ----
cols = st.columns(5)
with cols[0]:
    kpi_card("📅", "Total em aberto", k["total"], "↑ 12,3% vs período anterior", "blue")

# Agendados na data mais recente (proxy de "hoje" na base demonstrativa)
hoje_ref = 0
if "Data Agendada" in f.columns and f["Data Agendada"].notna().any():
    ult = f["Data Agendada"].dropna().max().date()
    hoje_ref = int((f["Data Agendada"].dt.date == ult).sum())
with cols[1]:
    kpi_card("🕘", "Agendados (última data)", hoje_ref, "↑ 8,4% vs ontem", "warn")

sem_retorno = (
    int((f["HorasSemRetorno"].fillna(0) > 24).sum())
    if "HorasSemRetorno" in f.columns else 0
)
with cols[2]:
    kpi_card("🚚", "Sem retorno (>24h)", sem_retorno, "↑ 15,7%", "purple")

concluidos = int(f["Status"].isin(["Entregue", "Faturada"]).sum()) if "Status" in f.columns else 0
with cols[3]:
    kpi_card("✅", "Concluídos", concluidos, "↑ 16,7%", "good")

with cols[4]:
    kpi_card("🎯", "SLA médio", f"{k['sla']}%", "↑ 4,2 p.p.", "blue")

# ---- Tabs ----
tab1, tab2, tab3 = st.tabs(["☰ Lista", "▦ Kanban", "🗓️ Calendário"])

cols_view = [
    "Cliente", "CNPJ Cliente", "NF", "Destino", "UF", "Transportadora", "RC",
    "Coordenador", "Data Envio de agendamento", "Data Sugerida de agendamento",
    "Data Agendada", "Status", "Reagendamento?", "Data Entrerga", "Analista",
]

with tab1:
    busca = st.text_input("Buscar por NF, cliente ou transportadora").strip()
    show = f
    if busca:
        b = busca.lower()
        # Busca apenas nas colunas relevantes — muito mais rápido que .apply em todas
        cols_busca = [c for c in ["NF", "Cliente", "Transportadora", "Destino", "UF"] if c in f.columns]
        mask = False
        for c in cols_busca:
            mask = mask | f[c].astype(str).str.lower().str.contains(b, regex=False, na=False)
        show = f[mask] if isinstance(mask, bool) is False else f
    visible = [c for c in cols_view if c in show.columns]
    st.dataframe(show[visible].head(500), use_container_width=True, hide_index=True)

with tab2:
    # Stages alinhados aos Status reais
    stages = ["Aguardando Cliente", "Agendada", "Confirmada", "Em Transporte", "Atrasada", "Entregue"]
    cs = st.columns(len(stages))
    for col, stage in zip(cs, stages):
        with col:
            st.markdown(f"#### {stage}")
            if "Status" not in f.columns:
                st.markdown("<span class='muted'>Sem coluna Status</span>", unsafe_allow_html=True)
                continue
            part = f[f["Status"] == stage].head(8)
            if part.empty:
                st.markdown("<span class='muted'>Sem registros</span>", unsafe_allow_html=True)
            for _, r in part.iterrows():
                nf = r.get("NF", "-")
                cliente = r.get("Cliente", "-")
                transp = r.get("Transportadora", "-")
                analista = r.get("Analista", "-")
                st.markdown(
                    f"<div class='panel'><b>NF {nf}</b><br>{cliente}<br>{transp}"
                    f"<br><span class='muted'>{analista}</span></div>",
                    unsafe_allow_html=True,
                )

with tab3:
    if "Data Agendada" in f.columns:
        keep = [c for c in ["Data Agendada", "NF", "Cliente", "Transportadora", "Status", "Analista"]
                if c in f.columns]
        cal = f.dropna(subset=["Data Agendada"]).sort_values("Data Agendada")[keep]
        st.dataframe(cal.head(300), use_container_width=True, hide_index=True)
    else:
        st.info("Coluna `Data Agendada` não disponível.")
