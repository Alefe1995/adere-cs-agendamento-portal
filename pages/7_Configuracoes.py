"""Configurações (parâmetros demonstrativos da apresentação)."""
import streamlit as st

from components.ui import setup_page, header, panel
from services.data_loader import load_data

setup_page("Configurações")
df = load_data()
header("Configurações", "Parâmetros fictícios para apresentação")

left, right = st.columns([0.72, 0.28])

with left:
    st.markdown("### Usuários e perfis")
    if "Analista" in df.columns:
        aggs = {}
        if "Transportadora" in df.columns:
            aggs["Equipe"] = ("Transportadora", "first")
        if "DataUltimaAtualizacaoStatus" in df.columns:
            aggs["Ultimo_acesso"] = ("DataUltimaAtualizacaoStatus", "max")
        if "NF" in df.columns:
            aggs["Registros"] = ("NF", "count")
        users = (
            df.groupby("Analista").agg(**aggs).reset_index()
            .rename(columns={"Analista": "Nome"})
        )
        users["Perfil"] = "Analista"
        users["Status"] = "Ativo"
        cols_show = [c for c in ["Nome", "Perfil", "Equipe", "Ultimo_acesso", "Status", "Registros"]
                     if c in users.columns]
        st.dataframe(users[cols_show], use_container_width=True, hide_index=True)
    else:
        st.info("Coluna `Analista` não encontrada.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### Parâmetros de SLA")
        st.number_input("Prazo para alerta de atraso (h)", value=24, min_value=0, step=1)
        st.number_input("Prazo para considerar atraso (h)", value=48, min_value=0, step=1)
        st.toggle("Considerar finais de semana", key="sla_fds")
        st.toggle("Considerar feriados", value=True, key="sla_feriados")

    with c2:
        st.markdown("#### Motivos de pendência")
        if "MotivoPendencia" in df.columns:
            opts = sorted(df["MotivoPendencia"].dropna().unique().tolist())
            st.multiselect("Motivos", opts, default=opts[:3] if opts else [], key="mp")
        else:
            st.info("Sem dados de `MotivoPendencia`.")
        st.toggle("Permitir motivo personalizado", value=True, key="mp_custom")

    with c3:
        st.markdown("#### Motivos de reagendamento")
        if "MotivoReagendamento" in df.columns:
            opts = sorted(df["MotivoReagendamento"].dropna().unique().tolist())
            st.multiselect("Motivos", opts, default=opts[:3] if opts else [], key="mr")
        else:
            st.info("Sem dados de `MotivoReagendamento`.")
        st.toggle("Permitir motivo personalizado", value=True, key="mr_custom")

    st.markdown("#### Integrações e notificações")
    nc1, nc2, nc3, nc4 = st.columns(4)
    with nc1:
        st.checkbox("E-mail", value=True, key="not_email")
    with nc2:
        st.checkbox("Portal", value=True, key="not_portal")
    with nc3:
        st.checkbox("Microsoft Teams", key="not_teams")
    with nc4:
        st.checkbox("SMS", key="not_sms")

with right:
    panel(
        "Últimas alterações",
        "<div class='alert green'>Mariana alterou parâmetros de SLA</div>"
        "<div class='alert blue'>João adicionou usuário</div>",
    )
    panel(
        "Boas práticas",
        "Revise perfis de acesso, mantenha SLA alinhado e padronize motivos para indicadores melhores.",
    )
