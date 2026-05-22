"""Dashboard principal do Portal de Agendamentos."""
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
with c[0]:
    kpi_card("📄", "Total de NFs", f"{k['total']:,}".replace(",", "."),
             "↑ 12,5% vs período anterior", "blue")
with c[1]:
    kpi_card("🕘", "Agendamentos Pendentes", k["pendentes"],
             "↑ 8,3% vs período anterior", "warn")
with c[2]:
    kpi_card("📅", "Entregas Agendadas", k["agendados"],
             "↑ 15,7% vs período anterior", "good")
with c[3]:
    kpi_card("🔄", "Reagendamentos", k["reag"],
             "↑ 10,6% vs período anterior", "purple")
with c[4]:
    kpi_card("⚠️", "Atrasos", k["atrasos"],
             "↑ 25,0% vs período anterior", "bad")
with c[5]:
    kpi_card("🎯", "SLA de Agendamento", f"{k['sla']}%",
             "↑ 4,2 p.p. vs período anterior", "blue")

left, right = st.columns([0.78, 0.22])

with left:
    g1, g2 = st.columns([0.45, 0.55])
    with g1:
        st.plotly_chart(
            bar_count(f, "UF", "Agendamentos por UF"),
            use_container_width=True,
        )
    with g2:
        st.plotly_chart(
            line_by_period(f, "Data Envio de agendamento", "Evolução semanal de agendamentos"),
            use_container_width=True,
        )

    st.markdown("### Fluxo operacional")
    # Stages alinhados aos Status realmente presentes na planilha
    stages = ["Aguardando Cliente", "Agendada", "Confirmada", "Em Transporte", "Atrasada", "Entregue"]
    cols = st.columns(len(stages))
    for col, s in zip(cols, stages):
        with col:
            if "Status" not in f.columns:
                panel(s, "<span class='muted'>Coluna Status não encontrada</span>")
                continue
            qtd = int((f["Status"] == s).sum())
            sample = f[f["Status"] == s].head(2)
            cards = []
            for _, r in sample.iterrows():
                nf = r.get("NF", "-")
                cliente = r.get("Cliente", "-")
                transp = r.get("Transportadora", "-")
                cards.append(
                    f"<div class='alert blue'><b>NF {nf}</b><br>{cliente}"
                    f"<br><span class='muted'>{transp}</span></div>"
                )
            body = "".join(cards) or "<span class='muted'>Sem registros</span>"
            panel(f"{s} <span class='chip blue'>{qtd}</span>", body)

    st.markdown("### Agendamentos")
    cols_view = [
        "Cliente", "CNPJ Cliente", "NF", "Destino", "UF", "Transportadora",
        "RC", "Coordenador", "Data Envio de agendamento", "Data Agendada",
        "Reagendamento?", "Data Entrerga", "Analista", "Status",
    ]
    visible = [c for c in cols_view if c in f.columns]
    st.dataframe(f[visible].head(200), use_container_width=True, hide_index=True)

with right:
    panel("Alertas e Insights", "")
    panel(
        "Entregas vencidas",
        "<div class='alert red'>Confira entregas com atraso superior a 24h."
        "<br><span class='small-link'>Ver detalhes →</span></div>",
    )
    panel(
        "NFs sem data agendada",
        "<div class='alert orange'>NFs aguardando agendamento há mais de 48h."
        "<br><span class='small-link'>Ver detalhes →</span></div>",
    )
    top_transp = top_counts(f, "Transportadora", 1)
    if len(top_transp):
        nome = top_transp.iloc[0, 0]
        qtd = int(top_transp.iloc[0, 1])
        panel(
            "Transportadora com maior volume",
            f"<div class='alert blue'><b>{nome}</b><br>{qtd} agendamentos</div>",
        )
    else:
        panel(
            "Transportadora com maior volume",
            "<div class='alert blue'>Sem dados no período</div>",
        )
