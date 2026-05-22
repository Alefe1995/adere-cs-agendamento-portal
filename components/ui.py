import streamlit as st

MENU = [
    ("Dashboard", "app.py", "🏠"),
    ("Agendamentos", "pages/1_Agendamentos.py", "📅"),
    ("Pendências", "pages/2_Pendencias.py", "⚠️"),
    ("Reagendamentos", "pages/3_Reagendamentos.py", "🔄"),
    ("Transportadoras", "pages/4_Transportadoras.py", "🚚"),
    ("Clientes", "pages/5_Clientes.py", "👥"),
    ("Relatórios", "pages/6_Relatorios.py", "📊"),
    ("Configurações", "pages/7_Configuracoes.py", "⚙️"),
]

def load_css():
    with open("assets/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def setup_page(title: str):
    st.set_page_config(page_title=f"{title} | Portal de Agendamentos", page_icon="📦", layout="wide")
    load_css()
    sidebar()

def sidebar():
    with st.sidebar:
        st.markdown('<div class="nav-title">Portal de<br>Agendamentos<br>de Entrega</div>', unsafe_allow_html=True)
        for label, path, icon in MENU:
            st.page_link(path, label=f"{icon}  {label}")
        st.markdown('<div class="nav-card"><b>JS</b><br>João Silva<br><span style="font-size:12px;opacity:.8">Analista Sênior</span></div>', unsafe_allow_html=True)

def header(title, subtitle="Última atualização: automática pela planilha"):
    c1, c2 = st.columns([0.76, 0.24], vertical_alignment="center")
    with c1:
        st.markdown(f'<div class="page-title">{title}</div><div class="muted">{subtitle}</div>', unsafe_allow_html=True)
    with c2:
        st.download_button("⬇️ Exportar dados", data="Exportação disponível na tela Relatórios", file_name="exportacao.txt")

def kpi_card(icon, title, value, delta="", color="good"):
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-icon {color}">{icon}</div>
      <div class="kpi-title">{title}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-delta {color}">{delta}</div>
    </div>""", unsafe_allow_html=True)

def panel(title, body=""):
    st.markdown(f'<div class="panel"><h3>{title}</h3>{body}</div>', unsafe_allow_html=True)

def status_chip(value):
    v = str(value)
    color = "gray"
    if v in ["Entregue", "Confirmada", "Agendado", "Faturada", "Dentro SLA"]: color="green"
    elif v in ["Atrasada", "Crítica", "Vencido"]: color="red"
    elif v in ["Aguardando Cliente", "Em Contato", "Reagendar", "Alta", "Atenção"]: color="orange"
    elif v in ["A Enviar", "Média"]: color="blue"
    return f'<span class="chip {color}">{v}</span>'

def format_df_for_display(df):
    out = df.copy()
    for col in ["Status", "Prioridade", "SLAStatus"]:
        if col in out.columns:
            out[col] = out[col].apply(status_chip)
    return out
