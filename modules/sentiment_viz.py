import plotly.graph_objects as go


def gauge_color(label_en: str) -> str:
    if label_en == "Positive":
        return "#10b981"
    if label_en == "Negative":
        return "#f43f5e"
    if label_en == "Neutral":
        return "#64748b"
    return "#7dd3fc"


def build_confidence_gauge(label_en: str, confidence_pct: float, height: int = 340) -> go.Figure:
    bar = gauge_color(label_en)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=confidence_pct,
            number={"suffix": "%", "valueformat": ".1f"},
            title={"text": f"预测置信度<br><span style='font-size:0.85em;color:#64748b'>{label_en}</span>"},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94a3b8"},
                "bar": {"color": bar},
                "bgcolor": "rgba(255,255,255,0.65)",
                "borderwidth": 2,
                "bordercolor": "rgba(125, 211, 252, 0.55)",
                "shape": "angular",
                "steps": [
                    {"range": [0, 33], "color": "rgba(248, 250, 252, 0.35)"},
                    {"range": [33, 66], "color": "rgba(241, 245, 249, 0.35)"},
                    {"range": [66, 100], "color": "rgba(226, 232, 240, 0.35)"},
                ],
            },
        )
    )
    fig.update_layout(
        height=height,
        margin=dict(l=24, r=24, t=40, b=16),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "PingFang SC, Microsoft YaHei, sans-serif", "color": "#0f172a"},
    )
    return fig
