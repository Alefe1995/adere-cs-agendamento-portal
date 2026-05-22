"""Componentes visuais reutilizáveis: setup de página, sidebar, cards, painéis."""
from pathlib import Path
import streamlit as st

ASSETS_CSS = Path(__file__).resolve().parent.parent / "assets" / "style.css"

# A primeira entrada é a Home (app.py). Streamlit trata a Home de forma especial:
# st.page_link("app.py", ...) lança erro. Usamos o nome da entrada da Home como caminho ".".
MENU = [
    ("Dashboard",       None,                              "🏠"),  # Home
    ("Agendamentos",    "pages/1_Agendamentos.py",         "📅"),
    ("Pendências",      "pages/2_Pendencias.py",           "⚠️"),
    ("Reagendamentos",  "pages/3_Reagendamentos.py",       "🔄"),
    ("Transportadoras", "pages/4_Transportadoras.py",      "🚚"),
    ("Clientes",        "pages/5_Clientes.py",             "👥"),
    ("Relatórios",      "pages/6_Relatorios.py",           "📊"),
    ("Configurações",   "pages/7_Configuracoes.py",        "⚙️"),
]


def load_css() -> None:
    """Injeta o CSS uma única vez por sessão para evitar reflows."""
    if st.session_state.get("_css_loaded"):
        return
    try:
        css = ASSETS_CSS.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        st.session_state["_css_loaded"] = True
    except FileNotFoundError:
        st.warning(f"Arquivo de estilos não encontrado em `{ASSETS_CSS}`.")


def setup_page(title: str) -> None:
    st.set_page_config(
        page_title=f"{title} | Portal de Agendamentos",
        page_icon="📦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    load_css()
    sidebar()


def sidebar() -> None:
    with st.sidebar:
        st.markdown(
            '<div class="nav-title">Portal de<br>Agendamentos<br>de Entrega</div>',
            unsafe_allow_html=True,
        )
        for label, path, icon in MENU:
            if path is None:
                st.page_link("app.py", label=f"{icon}  {label}")
            else:
                st.page_link(path, label=f"{icon}  {label}")


def header(title: str, subtitle: str = "Última atualização automática pela planilha") -> None:
    c1, c2 = st.columns([0.78, 0.22], vertical_alignment="center")
    with c1:
        st.markdown(
            f'<div class="page-title">{title}</div>'
            f'<div class="page-subtitle">{subtitle}</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown('<div class="updated">Última atualização: dados da planilha</div>', unsafe_allow_html=True)
        st.download_button(
            "⇩ Exportar",
            data="Exportação completa disponível na tela Relatórios.",
            file_name="exportacao.txt",
            mime="text/plain",
            use_container_width=True,
        )


def kpi_card(icon: str, title: str, value, delta: str = "", color: str = "good") -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
          <div class="kpi-icon {color}">{icon}</div>
          <div class="kpi-title">{title}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-delta {color}">{delta}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def panel(title: str, body: str = "") -> None:
    st.markdown(
        f'<div class="panel"><h3>{title}</h3>{body}</div>',
        unsafe_allow_html=True,
    )


def status_chip(value) -> str:
    v = str(value)
    color = "gray"
    if v in ["Entregue", "Confirmada", "Agendado", "Agendada", "Faturada", "Dentro SLA"]:
        color = "green"
    elif v in ["Atrasada", "Crítica", "Vencido", "Fora SLA"]:
        color = "red"
    elif v in ["Aguardando Cliente", "Em Contato", "Reagendar", "Em Transporte", "Alta", "Atenção"]:
        color = "orange"
    elif v in ["A Enviar", "Média"]:
        color = "blue"
    return f'<span class="chip {color}">{v}</span>'


def format_df_for_display(df):
    out = df.copy()
    for col in ["Status", "Prioridade", "SLAStatus"]:
        if col in out.columns:
            out[col] = out[col].apply(status_chip)
    return out
