import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================
# CONFIGURAÇÕES DA PÁGINA
# ==========================

st.set_page_config(
    page_title="Portal Customer Service ADERE",
    page_icon="📦",
    layout="wide"
)

# ==========================
# CSS CUSTOMIZADO
# ==========================

css_file = Path("assets/style.css")

if css_file.exists():

    with open(css_file, encoding="utf-8") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ==========================
# CARREGAMENTO DA BASE
# ==========================

arquivo = Path("data/agendamentos.xlsx")

if not arquivo.exists():

    st.error(
        "Arquivo data/agendamentos.xlsx não encontrado"
    )

    st.stop()

try:

    df = pd.read_excel(arquivo)

except Exception as e:

    st.error(
        f"Erro ao carregar Excel: {e}"
    )

    st.stop()

# ==========================
# VALIDAR COLUNAS
# ==========================

colunas_necessarias = [

    "NF",
    "Status",
    "Cliente",
    "Transportadora",
    "Analista",
    "SLA_Dias"

]

for coluna in colunas_necessarias:

    if coluna not in df.columns:

        st.error(
            f"Coluna ausente: {coluna}"
        )

        st.stop()

# ==========================
# SIDEBAR FILTROS
# ==========================

st.sidebar.title("🔎 Filtros")

status = st.sidebar.multiselect(
    "Status",
    sorted(df["Status"].dropna().unique())
)

cliente = st.sidebar.multiselect(
    "Cliente",
    sorted(df["Cliente"].dropna().unique())
)

transportadora = st.sidebar.multiselect(
    "Transportadora",
    sorted(df["Transportadora"].dropna().unique())
)

analista = st.sidebar.multiselect(
    "Analista",
    sorted(df["Analista"].dropna().unique())
)

# Aplicar filtros

if status:

    df=df[df["Status"].isin(status)]

if cliente:

    df=df[df["Cliente"].isin(cliente)]

if transportadora:

    df=df[df["Transportadora"].isin(transportadora)]

if analista:

    df=df[df["Analista"].isin(analista)]

# ==========================
# CABEÇALHO
# ==========================

st.markdown(
"""
<h1 style='text-align:center'>
📦 ADERE - Customer Service Portal
</h1>
""",
unsafe_allow_html=True
)

st.write("")

# ==========================
# KPI'S
# ==========================

total_nf=len(df)

agendadas=len(
    df[df["Status"]=="Agendada"]
)

atrasadas=len(
    df[df["Status"]=="Atrasada"]
)

entregues=len(
    df[df["Status"]=="Entregue"]
)

sla=round(
    df["SLA_Dias"].mean(),
    1
)

c1,c2,c3,c4,c5=st.columns(5)

c1.metric(
    "Total NF",
    total_nf
)

c2.metric(
    "Agendadas",
    agendadas
)

c3.metric(
    "Atrasadas",
    atrasadas
)

c4.metric(
    "Entregues",
    entregues
)

c5.metric(
    "SLA Médio",
    sla
)

st.divider()

# ==========================
# TABS
# ==========================

dashboard,dados=st.tabs(
[
"📊 Dashboard",
"📋 Dados"
]
)

# ==========================
# DASHBOARD
# ==========================

with dashboard:

    col1,col2=st.columns(2)

    with col1:

        fig1=px.pie(
            df,
            names="Status",
            title="Entregas por Status"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col2:

        trans=(
            df["Transportadora"]
            .value_counts()
            .reset_index()
        )

        trans.columns=[
            "Transportadora",
            "Quantidade"
        ]

        fig2=px.bar(
            trans,
            x="Quantidade",
            y="Transportadora",
            orientation="h",
            title="Entregas por Transportadora"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.write("")

    fig3=px.histogram(
        df,
        x="SLA_Dias",
        title="Distribuição SLA"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ==========================
# DADOS
# ==========================

with dados:

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇ Exportar Excel",
        data=df.to_csv(index=False),
        file_name="exportacao.csv",
        mime="text/csv"
    )
