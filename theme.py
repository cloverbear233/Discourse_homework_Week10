import streamlit as st


def inject_week10_theme() -> None:
    st.markdown(
        """
        <style>
        :root{
            --accent: #7dd3fc;
            --bg0: #fffbeb;
            --bg1: #fafefe;
            --panel: rgba(241, 250, 255, 0.88);
            --text: #0f172a;
            --muted: #475569;
            --border: rgba(125, 211, 252, 0.22);
            --card-border: rgba(125, 211, 252, 0.42);
            --card-bg: linear-gradient(160deg, rgba(186, 230, 253, 0.36) 0%, rgba(224, 242, 254, 0.55) 38%, rgba(255, 255, 255, 0.98) 100%);
            --card-shadow: 0 6px 20px rgba(125, 211, 252, 0.12);
            --tab-active-bg: linear-gradient(135deg, rgba(254, 243, 199, 0.82) 0%, rgba(224, 242, 254, 0.86) 100%);
            --week10-st-topbar-safe: max(4.25rem, calc(2.75rem + env(safe-area-inset-top, 0px)));
        }

        html, body, [data-testid="stAppViewContainer"]{
            font-family: "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(180deg, var(--bg0) 0%, var(--bg1) 100%);
            color: var(--text);
            font-size: 18px;
        }
        section.stMain > div.block-container, section.stMain .block-container{
            padding-top: calc(1rem + var(--week10-st-topbar-safe));
            padding-bottom: 2.2rem;
        }
        section[data-testid="stSidebar"]{
            background: var(--panel);
            border-right: 1px solid var(--border);
        }
        section[data-testid="stSidebar"] > div.block-container{
            padding-top: calc(1rem + var(--week10-st-topbar-safe));
        }
        section[data-testid="stSidebar"] h1{
            font-size: 2rem !important;
            font-weight: 740 !important;
            color: #334155;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"]{
            display: flex;
            flex-direction: column;
            gap: 0.45rem;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label{
            width: 100%;
            border-radius: 12px;
            border: 1px solid rgba(186, 230, 253, 0.7);
            background: rgba(255, 255, 255, 0.84);
            padding: 0.7rem 0.85rem;
            min-height: 3.1rem;
            font-size: 1.15rem !important;
            font-weight: 560;
            transition: all 150ms ease;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{
            transform: translateX(3px);
            box-shadow: 0 8px 18px rgba(125, 211, 252, 0.16);
            border-color: rgba(125, 211, 252, 0.88);
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){
            background: var(--tab-active-bg);
            border-color: rgba(125, 211, 252, 0.92);
            font-weight: 650;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label p{
            font-size: 1.15rem !important;
        }
        section.stMain h1{
            font-size: 2.2rem;
            font-weight: 760;
            color: #0f172a;
            border-bottom: 2px solid rgba(186, 230, 253, 0.65);
            padding-bottom: 0.45rem;
            margin-bottom: 0.35rem;
        }
        section.stMain h2, section.stMain h3{
            color: #1e293b;
            font-weight: 660;
            font-size: 1.45rem;
        }
        div[data-testid="stMetric"]{
            border-radius: 12px;
            border: 2px solid var(--card-border);
            background: var(--card-bg);
            box-shadow: var(--card-shadow);
            padding: 0.65rem 0.8rem;
        }
        div[data-testid="stAlert"]{
            border-radius: 12px;
            border: 1px solid rgba(186, 230, 253, 0.7);
            box-shadow: 0 2px 10px rgba(148, 163, 184, 0.08);
        }
        div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea, div[data-testid="stSelectbox"] > div{
            border-radius: 10px !important;
            border-color: rgba(186, 230, 253, 0.85) !important;
            font-size: 1.02rem !important;
        }
        .result-box {
            border: 1px solid rgba(186, 230, 253, 0.7);
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.82);
            box-shadow: 0 2px 10px rgba(148, 163, 184, 0.08);
            padding: 12px;
            min-height: 120px;
            line-height: 1.7;
            white-space: pre-wrap;
        }
        .small-note { color: #475569; font-size: 0.9rem; }
        .wk10_intro{
            border-radius: 12px;
            border: 2px solid rgba(125, 211, 252, 0.38);
            background: linear-gradient(165deg, rgba(254, 243, 199, 0.86) 0%, rgba(224, 242, 254, 0.62) 48%, rgba(255, 255, 255, 0.98) 100%);
            padding: 0.9rem 1rem;
            color: #1f2937;
            box-shadow: 0 8px 20px rgba(125, 211, 252, 0.1);
            margin: 0.25rem 0 0.75rem 0;
            font-size: 1.06rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_week10_intro() -> None:
    st.markdown(
        """
        <div class="wk10_intro">
          <strong>课堂实验目标：</strong>将电商/社媒评论转化为可量化的情感极性与置信度，
          理解「分类标签 + 概率」在舆情监测与商业决策中的意义。
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer_attribution() -> None:
    st.caption("NLP Week10 · Streamlit · Transformers · Plotly · 细粒度情感分析与舆情监测")
