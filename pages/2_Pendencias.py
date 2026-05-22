"""Pendências: priorização, aging e responsáveis."""
import streamlit as st

from components.ui import setup_page, header, kpi_card, panel
from services.data_loader import load_data, filter_bar
from utils.charts import bar_count, line_by_period

setup_page("Pendências")
df = load_data()
header("Pendências", "Priorização de exceções e aging")

f = filter_bar(df)

# Monta o filtro de pendência sem assumir colunas
mask = False
if "Atrasado" in f.columns:
    mask = mask | f["Atrasado"].fillna(False).astype(bool)
if "Prioridade" in f.columns:
    mask = mask | f["Prioridade"].isin(["Crítica", "Alta"])
if "Status" in f.columns:
    mask = mask | f["Status"].isin(["Aguardando Cliente", "Atrasada"])
pend = f[mask] if not isinstance(mask, bool) else f.iloc[0:0]

cs = st.columns(5)
with cs[0]:
    qtd_critica = int((pend["Prioridade"] == "Crítica").sum()) if "Prioridade" in pend.columns else 0
    kpi_card("⚠️", "Pendências críticas", qtd_critica, "↑ 18,7%", "bad")
with cs[1]:
    sem_data = int(pend["Data Agendada"].isna().sum()) if "Data Agendada" in pend.columns else 0
    kpi_card("📆", "Sem data agendada", sem_data, "↑ 22,1%", "warn")
with cs[2]:
    aguard = int((pend["Status"] == "Aguardando Cliente").sum()) if "Status" in pend.columns else 0
    kpi_card("🔄", "Aguardando retorno", aguard, "↑ 14,3%", "blue")
with cs[3]:
    bloq = (
        int(pend["TipoPendencia"].astype(str)
            .str.contains("Bloqueio|Transportadora", case=False, na=False).sum())
        if "TipoPendencia" in pend.columns else 0
    )
    kpi_card("🔒", "Bloqueios de entrega", bloq, "↓ 5,6%", "purple")
with cs[4]:
    if "DiasEmAberto" in pend.columns and len(pend) and pend["DiasEmAberto"].notna().any():
        media = f"{pend['DiasEmAberto'].mean():.1f} dias"
    else:
        media = "0 dias"
    kpi_card("🕒", "Tempo médio", media, "↑ 0,4 dia", "good")

left, right = st.columns([0.73, 0.27])

with left:
    st.markdown("### Matriz de prioridades")
    cols = st.columns(4)
    for col, pri in zip(cols, ["Crítica", "Alta", "Média", "Baixa"]):
        with col:
            if "Prioridade" not in pend.columns:
                panel(pri, "<span class='muted'>Sem coluna Prioridade</span>")
                continue
            part = pend[pend["Prioridade"] == pri].head(5)
            cor = "red" if pri == "Crítica" else "orange" if pri == "Alta" else "blue"
            cards = []
            for _, r in part.iterrows():
                nf = r.get("NF", "-")
                cliente = r.get("Cliente", "-")
                motivo = r.get("MotivoPendencia", "-")
                cards.append(
                    f"<div class='alert {cor}'><b>NF {nf}</b>"
                    f"<br>{cliente}<br>{motivo}</div>"
                )
            corpo = "".join(cards) or "<span class='muted'>Sem registros</span>"
            panel(f"{pri} <span class='chip {cor}'>{len(part)}</span>", corpo)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            bar_count(pend, "MotivoPendencia", "Pendências por motivo", horizontal=True),
            use_container_width=True,
        )
    with c2:
        st.plotly_chart(
            line_by_period(f, "Data Envio de agendamento", "Evolução de pendências"),
            use_container_width=True,
        )

    cols_tabela = [
        "NF", "Cliente", "MotivoPendencia", "Transportadora",
        "ResponsavelAcao", "DiasEmAberto", "ProximaAcao", "Status",
    ]
    visible = [c for c in cols_tabela if c in pend.columns]
    st.dataframe(pend[visible].head(300), use_container_width=True, hide_index=True)

with right:
    panel("Alertas e insights", "")
    panel("NFs há mais de 48h",
          "<div class='alert red'>Casos sem agendamento exigem ação imediata.</div>")
    panel("Clientes aguardando retorno",
          "<div class='alert orange'>Revise a carteira de clientes em aberto.</div>")
    panel("Pendências por transportadora",
          "<div class='alert blue'>Ranking ajuda a priorizar contatos.</div>")
