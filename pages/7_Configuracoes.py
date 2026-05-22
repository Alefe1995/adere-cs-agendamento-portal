import streamlit as st
from components.ui import setup_page, header, panel
from services.data_loader import load_data

setup_page("Configurações")
df=load_data(); header("Configurações", "Parâmetros fictícios para apresentação")
left,right=st.columns([.72,.28])
with left:
    st.markdown("### Usuários e perfis")
    users=df.groupby("Analista").agg(Equipe=("Transportadora","first"),Ultimo_acesso=("DataUltimaAtualizacaoStatus","max"),Registros=("NF","count")).reset_index().rename(columns={"Analista":"Nome"})
    users["Perfil"]="Analista"; users["Status"]="Ativo"
    st.dataframe(users[["Nome","Perfil","Equipe","Ultimo_acesso","Status","Registros"]], use_container_width=True, hide_index=True)
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown("#### Parâmetros de SLA")
        st.number_input("Prazo para alerta de atraso (h)", value=24)
        st.number_input("Prazo para considerar atraso (h)", value=48)
        st.toggle("Considerar finais de semana")
        st.toggle("Considerar feriados", value=True)
    with c2:
        st.markdown("#### Motivos de pendência")
        st.multiselect("Motivos", sorted(df["MotivoPendencia"].dropna().unique()), default=sorted(df["MotivoPendencia"].dropna().unique())[:3])
        st.toggle("Permitir motivo personalizado", value=True)
    with c3:
        st.markdown("#### Motivos de reagendamento")
        st.multiselect("Motivos", sorted(df["MotivoReagendamento"].dropna().unique()), default=sorted(df["MotivoReagendamento"].dropna().unique())[:3])
        st.toggle("Permitir motivo personalizado", value=True)
    st.markdown("#### Integrações e notificações")
    st.checkbox("E-mail", value=True); st.checkbox("Portal", value=True); st.checkbox("Microsoft Teams"); st.checkbox("SMS")
with right:
    panel("Últimas alterações", "<div class='alert green'>Mariana alterou parâmetros de SLA</div><div class='alert blue'>João adicionou usuário</div>")
    panel("Boas práticas", "Revise perfis de acesso, mantenha SLA alinhado e padronize motivos para indicadores melhores.")
