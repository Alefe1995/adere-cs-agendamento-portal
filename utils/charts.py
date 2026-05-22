"""Gráficos Plotly. Toda função aceita DataFrame vazio sem estourar."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.kpis import top_counts

BLUE = "#0F6CBD"
GREEN = "#16A34A"
ORANGE = "#F97316"
RED = "#E11D48"
PURPLE = "#6D28D9"


def _empty_fig(title: str):
    fig = go.Figure()
    fig.add_annotation(
        text="Sem dados para exibir",
        showarrow=False,
        font=dict(size=14, color="#667085"),
    )
    fig.update_layout(
        title=title, height=330,
        margin=dict(l=10, r=10, t=45, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(visible=False), yaxis=dict(visible=False),
    )
    return fig


def bar_count(df: pd.DataFrame, col: str, title: str, n: int = 10, horizontal: bool = False):
    if col not in df.columns or df.empty:
        return _empty_fig(title)
    data = top_counts(df, col, n)
    if data.empty:
        return _empty_fig(title)

    if horizontal:
        fig = px.bar(
            data.sort_values("Quantidade"),
            x="Quantidade", y=col, orientation="h", text="Quantidade",
        )
    else:
        fig = px.bar(data, x=col, y="Quantidade", text="Quantidade")
    fig.update_traces(marker_color=BLUE, textposition="outside", cliponaxis=False)
    fig.update_layout(
        title=title, height=330,
        margin=dict(l=10, r=10, t=45, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
    )
    return fig


def line_by_period(df: pd.DataFrame, date_col: str, title: str, freq: str = "W"):
    if date_col not in df.columns:
        return _empty_fig(title)
    tmp = df.dropna(subset=[date_col]).copy()
    if tmp.empty:
        return _empty_fig(title)
    tmp["Periodo"] = tmp[date_col].dt.to_period(freq).astype(str)
    data = tmp.groupby("Periodo").size().reset_index(name="Quantidade")
    fig = px.line(data, x="Periodo", y="Quantidade", markers=True, text="Quantidade")
    fig.update_traces(line_color=BLUE, marker_color=BLUE, textposition="top center")
    fig.update_layout(
        title=title, height=330,
        margin=dict(l=10, r=10, t=45, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
    )
    return fig


def donut(df: pd.DataFrame, col: str, title: str):
    if col not in df.columns or df.empty:
        return _empty_fig(title)
    data = top_counts(df, col, 8)
    if data.empty:
        return _empty_fig(title)
    fig = px.pie(data, values="Quantidade", names=col, hole=0.55)
    fig.update_layout(
        title=title, height=330,
        margin=dict(l=10, r=10, t=45, b=10), paper_bgcolor="white",
    )
    return fig


def scatter_sla_volume(df: pd.DataFrame):
    title = "SLA x Volume"
    needed = {"Cliente", "NF", "SLAStatus"}
    if not needed.issubset(df.columns) or df.empty:
        return _empty_fig(title)
    data = (
        df.groupby("Cliente")
        .agg(Volume=("NF", "count"),
             SLA=("SLAStatus", lambda x: round(x.eq("Dentro SLA").mean() * 100, 1)))
        .reset_index()
    )
    if data.empty:
        return _empty_fig(title)
    fig = px.scatter(data, x="Volume", y="SLA", hover_name="Cliente", size="Volume")
    fig.update_traces(marker_color=BLUE)
    fig.update_layout(
        title=title, height=330,
        margin=dict(l=10, r=10, t=45, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
    )
    return fig
