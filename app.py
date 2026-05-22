import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Portal CS ADERE",
    layout="wide"
)

# carregar CSS
with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.title("📦 Portal Customer Service - ADERE")

st.write("Sistema carregado")

try:

    df = pd.read_csv(
        "data/agendamentos.csv"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

except:

    st.warning(
        "Base não encontrada"
    )
