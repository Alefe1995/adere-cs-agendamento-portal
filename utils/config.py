# ============================================================
# ADERE Produtos Auto Adesivos
# Configuração Central de Identidade Visual
# ============================================================
# Para alterar qualquer cor do sistema, edite APENAS este arquivo.
# Todas as partes do portal lêem as configurações daqui.

# --- PALETA PRINCIPAL ADERE ---
BRAND = {
    # Cores primárias da marca
    "primary":         "#E30613",   # Vermelho ADERE (cor dominante oficial)
    "primary_dark":    "#B8000F",   # Vermelho escuro (hover, pressão)
    "primary_light":   "#FF1A2E",   # Vermelho claro (destaque)
    "primary_muted":   "#FDECEA",   # Vermelho suave (backgrounds)

    # Neutros corporativos
    "black":           "#1A1A1A",   # Preto corporativo
    "gray_dark":       "#2D2D2D",   # Cinza escuro (sidebar, header)
    "gray_mid":        "#6B6B6B",   # Cinza médio (textos secundários)
    "gray_light":      "#D1D1D1",   # Cinza claro (bordas)
    "gray_bg":         "#F5F5F5",   # Cinza fundo geral
    "white":           "#FFFFFF",   # Branco

    # Cores funcionais (status)
    "success":         "#1E8449",   # Verde sucesso / entregue
    "warning":         "#D4AC0D",   # Amarelo atenção / aguardando
    "alert":           "#E67E22",   # Laranja risco / reagendada
    "critical":        "#C0392B",   # Vermelho crítico / atrasada
    "info":            "#2471A3",   # Azul informação / faturada
    "neutral":         "#6B6B6B",   # Cinza neutro

    # Empresa
    "company_name":    "ADERE",
    "company_full":    "ADERE Produtos Auto Adesivos",
    "company_tagline": "Colou, tá colado.",
    "system_name":     "Portal CS | Agendamentos",
    "system_version":  "v1.0.0",
}

# --- MAPEAMENTO DE STATUS ---
STATUS_CONFIG = {
    "Faturada": {
        "color":      "#2471A3",
        "bg":         "#EBF5FB",
        "border":     "#AED6F1",
        "icon":       "📄",
        "priority":   1,
        "severity":   "info",
    },
    "Aguardando contato": {
        "color":      "#B7950B",
        "bg":         "#FEFDE8",
        "border":     "#F9E79F",
        "icon":       "⏳",
        "priority":   2,
        "severity":   "warning",
    },
    "Contato realizado": {
        "color":      "#6C3483",
        "bg":         "#F4ECF7",
        "border":     "#C39BD3",
        "icon":       "📞",
        "priority":   3,
        "severity":   "info",
    },
    "Aguardando cliente": {
        "color":      "#B7950B",
        "bg":         "#FEFDE8",
        "border":     "#F9E79F",
        "icon":       "🔔",
        "priority":   4,
        "severity":   "warning",
    },
    "Agendada": {
        "color":      "#1E8449",
        "bg":         "#EAFAF1",
        "border":     "#A9DFBF",
        "icon":       "📅",
        "priority":   5,
        "severity":   "success",
    },
    "Confirmada": {
        "color":      "#145A32",
        "bg":         "#D5F5E3",
        "border":     "#82E0AA",
        "icon":       "✅",
        "priority":   6,
        "severity":   "success",
    },
    "Em transporte": {
        "color":      "#1A5276",
        "bg":         "#EBF5FB",
        "border":     "#85C1E9",
        "icon":       "🚚",
        "priority":   7,
        "severity":   "info",
    },
    "Entregue": {
        "color":      "#0B5345",
        "bg":         "#D5F5E3",
        "border":     "#52BE80",
        "icon":       "✔️",
        "priority":   8,
        "severity":   "success",
    },
    "Reagendada": {
        "color":      "#A04000",
        "bg":         "#FEF5E7",
        "border":     "#F0B27A",
        "icon":       "🔄",
        "priority":   9,
        "severity":   "alert",
    },
    "Atrasada": {
        "color":      "#922B21",
        "bg":         "#FDEBD0",
        "border":     "#F1948A",
        "icon":       "⚠️",
        "priority":   10,
        "severity":   "critical",
    },
    "Crítica": {
        "color":      "#7B241C",
        "bg":         "#FDEDEC",
        "border":     "#E74C3C",
        "icon":       "🚨",
        "priority":   11,
        "severity":   "critical",
    },
    "Cliente recusou": {
        "color":      "#922B21",
        "bg":         "#FDEDEC",
        "border":     "#F1948A",
        "icon":       "❌",
        "priority":   12,
        "severity":   "critical",
    },
}

# --- PLOTLY TEMA CORES ---
PLOTLY_COLORS = [
    "#E30613",  # Vermelho ADERE
    "#2D2D2D",  # Cinza escuro
    "#2471A3",  # Azul
    "#1E8449",  # Verde
    "#E67E22",  # Laranja
    "#D4AC0D",  # Amarelo
    "#6C3483",  # Roxo
    "#B8000F",  # Vermelho escuro
    "#1A5276",  # Azul escuro
    "#0B5345",  # Verde escuro
]

# --- PLOTLY LAYOUT PADRÃO ---
PLOTLY_LAYOUT = {
    "font":        {"family": "Segoe UI, Helvetica Neue, Arial", "color": "#1A1A1A"},
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor":  "rgba(0,0,0,0)",
    "margin":      {"t": 40, "b": 40, "l": 40, "r": 20},
    "title":       {"font": {"size": 14, "color": "#1A1A1A", "family": "Segoe UI"}},
    "legend":      {"bgcolor": "rgba(255,255,255,0.8)", "bordercolor": "#D1D1D1", "borderwidth": 1},
}

# --- CONFIGURAÇÕES DE NEGÓCIO ---
BUSINESS = {
    "sla_dias_alerta":   3,    # Dias para alertar sobre SLA
    "sla_dias_critico":  7,    # Dias para status crítico
    "registros_por_pagina": 25,
    "max_historico_dias": 90,
    "fuso_horario": "America/Sao_Paulo",
}
