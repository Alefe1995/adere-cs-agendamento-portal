"""Gráficos Plotly com aparência executiva e tratamento defensivo."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.kpis import top_counts

BLUE = "#0B63F6"
GREEN = "#16A34A"
ORANGE = "#F97316"
RED = "#E11D48"
PURPLE = "#6D28D9"
GRID = "#E8EEF7"
TEXT = "#071B4D"
MUTED = "#667085"


def _base_layout(fig, title: str, height: int = 330):
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color=TEXT, family="Inter", weight=800), x=0.02),
        height=height,
        margin=dict(l=16, r=16, t=54, b=22),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, Segoe UI, Arial", size=12, color=TEXT),
        hovermode="x unified",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, color="#344054")
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False, color="#344054")
    return fig


def _empty_fig(title: str):
    fig = go.Figure()
    fig.add_annotation(text="Sem dados para exibir", showarrow=False, font=dict(size=14, color=MUTED))
    fig.update_layout(title=dict(text=title, font=dict(size=15, color=TEXT)), height=330,
                      margin=dict(l=16, r=16, t=54, b=22), plot_bgcolor="white", paper_bgcolor="white",
                      xaxis=dict(visible=False), yaxis=dict(visible=False))
    return fig


def bar_count(df: pd.DataFrame, col: str, title: str, n: int = 10, horizontal: bool = False):
    if col not in df.columns or df.empty:
        return _empty_fig(title)
    data = top_counts(df, col, n)
    if data.empty:
        return _empty_fig(title)
    if horizontal:
        fig = px.bar(data.sort_values("Quantidade"), x="Quantidade", y=col, orientation="h", text="Quantidade")
        fig.update_traces(marker_color=BLUE, textposition="outside", cliponaxis=False, width=0.55)
    else:
        fig = px.bar(data, x=col, y="Quantidade", text="Quantidade")
        fig.update_traces(marker_color=BLUE, textposition="outside", cliponaxis=False, width=0.55)
    _base_layout(fig, title)
    fig.update_layout(showlegend=False)
    return fig


def line_by_period(df: pd.DataFrame, date_col: str, title: str, freq: str = "W"):
    if date_col not in df.columns:
        return _empty_fig(title)
    tmp = df.dropna(subset=[date_col]).copy()
    if tmp.empty:
        return _empty_fig(title)
    tmp["Periodo"] = tmp[date_col].dt.to_period(freq).astype(str)
    data = tmp.groupby("Periodo").size().reset_index(name="Quantidade")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["Periodo"], y=data["Quantidade"], mode="lines+markers+text",
        text=data["Quantidade"], textposition="top center", name="Agendamentos",
        line=dict(color=BLUE, width=3), marker=dict(color=BLUE, size=8),
        fill="tozeroy", fillcolor="rgba(11,99,246,0.10)"
    ))
    _base_layout(fig, title)
    fig.update_layout(showlegend=False)
    return fig


def donut(df: pd.DataFrame, col: str, title: str):
    if col not in df.columns or df.empty:
        return _empty_fig(title)
    data = top_counts(df, col, 8)
    if data.empty:
        return _empty_fig(title)
    palette = [BLUE, "#1D4ED8", "#60A5FA", PURPLE, ORANGE, GREEN, RED, "#94A3B8"]
    fig = px.pie(data, values="Quantidade", names=col, hole=0.62, color_discrete_sequence=palette)
    fig.update_traces(textposition="inside", textinfo="percent", marker=dict(line=dict(color="white", width=2)))
    _base_layout(fig, title)
    fig.update_layout(legend=dict(orientation="v", y=.5, x=1.02), margin=dict(l=16, r=16, t=54, b=22))
    return fig


def scatter_sla_volume(df: pd.DataFrame):
    title = "SLA x Volume"
    needed = {"Cliente", "NF", "SLAStatus"}
    if not needed.issubset(df.columns) or df.empty:
        return _empty_fig(title)
    data = (df.groupby("Cliente")
            .agg(Volume=("NF", "count"), SLA=("SLAStatus", lambda x: round(x.eq("Dentro SLA").mean() * 100, 1)))
            .reset_index())
    if data.empty:
        return _empty_fig(title)
    fig = px.scatter(data, x="Volume", y="SLA", hover_name="Cliente", size="Volume")
    fig.update_traces(marker=dict(color=BLUE, opacity=.85, line=dict(color="white", width=1)))
    _base_layout(fig, title)
    fig.update_layout(showlegend=False)
    return fig
