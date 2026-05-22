import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="ADERE Customer Service",
    layout="wide"
)

# CSS
with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# Base
df=pd.read_excelv("data/agendamentos.xlsx")

# SIDEBAR
st.sidebar.title("Filtros")

status=st.sidebar.multiselect(
    "Status",
    df["Status"].unique()
)

cliente=st.sidebar.multiselect(
    "Cliente",
    df["Cliente"].unique()
)

if status:
    df=df[df["Status"].isin(status)]

if cliente:
    df=df[df["Cliente"].isin(cliente)]

# HEADER

st.markdown("""
<div class='adere-header'>
<div>
<h2 style='color:white'>
ADERE Portal Customer Service
</h2>
</div>
</div>
""",unsafe_allow_html=True)

# KPIS

col1,col2,col3,col4,col5=st.columns(5)

total=len(df)

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
    df["SLA_Dias"].mean(),1
)

col1.metric(
    "Total NFs",
    total
)

col2.metric(
    "Agendadas",
    agendadas
)

col3.metric(
    "Atrasadas",
    atrasadas
)

col4.metric(
    "Entregues",
    entregues
)

col5.metric(
    "SLA Médio",
    sla
)

st.divider()

aba1,aba2,aba3=st.tabs([
"Dashboard",
"Análise",
"Dados"
])

with aba1:

    c1,c2=st.columns(2)

    with c1:

        fig=px.pie(
            df,
            names="Status",
            title="Entregas por Status"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        fig2=px.bar(
            df["Transportadora"]
            .value_counts()
            .reset_index(),
            x="count",
            y="Transportadora",
            orientation="h",
            title="Transportadoras"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

with aba2:

    fig3=px.histogram(
        df,
        x="SLA_Dias",
        title="Distribuição SLA"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with aba3:

    st.dataframe(
        df,
        use_container_width=True
    )
