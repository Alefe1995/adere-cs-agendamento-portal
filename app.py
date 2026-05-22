import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="ADERE Customer Service",
    page_icon="📦",
    layout="wide"
)

# ==================================================
# CSS
# ==================================================

css_file=Path("assets/style.css")

if css_file.exists():

    with open(css_file,encoding="utf-8") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ==================================================
# BASE
# ==================================================

arquivo=Path("data/agendamentos.xlsx")

df=pd.read_excel(arquivo)

# converter datas

datas=[

"Data_Faturamento",
"Data_Agendada",
"Data Entrerga",
"Data Envio de agendamento"

]

for c in datas:

    if c in df.columns:

        df[c]=pd.to_datetime(
            df[c],
            errors="coerce"
        )

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🔎 Filtros")

cliente=st.sidebar.multiselect(
    "Cliente",
    sorted(df["Cliente"].unique())
)

uf=st.sidebar.multiselect(
    "UF",
    sorted(df["UF"].unique())
)

analista=st.sidebar.multiselect(
    "Analista",
    sorted(df["Analista"].unique())
)

status=st.sidebar.multiselect(
    "Status",
    sorted(df["Status"].unique())
)

if cliente:
    df=df[df["Cliente"].isin(cliente)]

if uf:
    df=df[df["UF"].isin(uf)]

if analista:
    df=df[df["Analista"].isin(analista)]

if status:
    df=df[df["Status"].isin(status)]

# ==================================================
# HEADER
# ==================================================

st.markdown("""
<div style='padding:20px;
background:linear-gradient(90deg,#111,#222);
border-radius:15px;
margin-bottom:20px;'>

<h1 style='color:white'>
📦 ADERE Customer Service Dashboard
</h1>

<p style='color:lightgray'>

Monitoramento operacional de agendamentos

</p>

</div>
""",unsafe_allow_html=True)

# ==================================================
# KPI'S
# ==================================================

total_nf=len(df)

reag=len(
    df[df["Reagendamento?"]=="Sim"]
)

atrasadas=len(
    df[df["Atrasado"]=="Sim"]
)

criticas=len(
    df[df["Prioridade"]=="Crítica"]
)

sla=round(
    df["SLA_Dias"].mean(),
    1
)

tempo=round(
    df["Tempo_Parado_Dias"].mean(),
    1
)

c1,c2,c3,c4,c5,c6=st.columns(6)

c1.metric(
    "NF Total",
    total_nf
)

c2.metric(
    "Reagendamentos",
    reag
)

c3.metric(
    "Atrasadas",
    atrasadas
)

c4.metric(
    "Críticas",
    criticas
)

c5.metric(
    "SLA Médio",
    sla
)

c6.metric(
    "Tempo Parado",
    tempo
)

st.write("")

# ==================================================
# LINHA SUPERIOR
# ==================================================

col1,col2=st.columns([3,1])

with col1:

    evolucao=(
        df.groupby(
            "Data_Faturamento"
        )
        .size()
        .reset_index()
    )

    evolucao.columns=[
        "Data",
        "Quantidade"
    ]

    fig=px.line(
        evolucao,
        x="Data",
        y="Quantidade",
        title="Evolução de Agendamentos"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader(
        "📌 Insights"
    )

    st.info(
        f"""
        NFs críticas: {criticas}
        """
    )

    st.warning(
        f"""
        Reagendamentos: {reag}
        """
    )

    st.error(
        f"""
        Atrasadas: {atrasadas}
        """
    )

# ==================================================
# SEGUNDA LINHA
# ==================================================

g1,g2,g3=st.columns(3)

with g1:

    fig=px.pie(
        df,
        names="Status",
        title="Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with g2:

    transp=(
        df[
            "Transportadora"
        ]
        .value_counts()
        .reset_index()
    )

    transp.columns=[
        "Transportadora",
        "Qtd"
    ]

    fig=px.bar(
        transp,
        x="Transportadora",
        y="Qtd",
        title="Transportadoras"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with g3:

    top=(
        df[
            "Cliente"
        ]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top.columns=[
        "Cliente",
        "Qtd"
    ]

    fig=px.bar(
        top,
        x="Qtd",
        y="Cliente",
        orientation="h",
        title="Top Clientes"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# TABELA
# ==================================================

st.subheader(
    "📋 Operação"
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    height=500
)
