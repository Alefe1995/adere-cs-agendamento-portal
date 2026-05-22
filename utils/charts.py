import plotly.express as px
import plotly.graph_objects as go
from utils.kpis import top_counts

BLUE = "#0F6CBD"
GREEN = "#16A34A"
ORANGE = "#F97316"
RED = "#E11D48"
PURPLE = "#6D28D9"

def bar_count(df, col, title, n=10, horizontal=False):
    data = top_counts(df, col, n)
    if horizontal:
        fig = px.bar(data.sort_values("Quantidade"), x="Quantidade", y=col, orientation="h", text="Quantidade")
    else:
        fig = px.bar(data, x=col, y="Quantidade", text="Quantidade")
    fig.update_traces(marker_color=BLUE, textposition="outside")
    fig.update_layout(title=title, height=330, margin=dict(l=10,r=10,t=45,b=10), plot_bgcolor="white", paper_bgcolor="white")
    return fig

def line_by_period(df, date_col, title, freq="W"):
    tmp = df.dropna(subset=[date_col]).copy()
    tmp["Periodo"] = tmp[date_col].dt.to_period(freq).astype(str)
    data = tmp.groupby("Periodo").size().reset_index(name="Quantidade")
    fig = px.line(data, x="Periodo", y="Quantidade", markers=True, text="Quantidade")
    fig.update_traces(line_color=BLUE, marker_color=BLUE, textposition="top center")
    fig.update_layout(title=title, height=330, margin=dict(l=10,r=10,t=45,b=10), plot_bgcolor="white", paper_bgcolor="white")
    return fig

def donut(df, col, title):
    data = top_counts(df, col, 8)
    fig = px.pie(data, values="Quantidade", names=col, hole=.55)
    fig.update_layout(title=title, height=330, margin=dict(l=10,r=10,t=45,b=10), paper_bgcolor="white")
    return fig

def scatter_sla_volume(df):
    data = df.groupby("Cliente").agg(Volume=("NF","count"), SLA=("SLAStatus", lambda x: (x.eq("Dentro SLA").mean()*100))).reset_index()
    fig = px.scatter(data, x="Volume", y="SLA", hover_name="Cliente", size="Volume")
    fig.update_traces(marker_color=BLUE)
    fig.update_layout(title="SLA x Volume", height=330, margin=dict(l=10,r=10,t=45,b=10), plot_bgcolor="white", paper_bgcolor="white")
    return fig
