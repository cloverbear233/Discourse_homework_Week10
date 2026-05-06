import streamlit as st

from modules.module1_sentiment import render_module1_sentiment
from modules.module2_explicit_implicit import render_module2_explicit_implicit
from modules.module3_opinion_dashboard import render_module3_opinion_dashboard
from theme import inject_week10_theme, render_footer_attribution


st.set_page_config(
    page_title="Week10 电商评论情感分析与舆情监测",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    inject_week10_theme()

    st.sidebar.title("模块导航")
    tab = st.sidebar.radio(
        "请选择模块",
        ["模块1：情感极性与置信度", "模块2：显式 vs 隐式情感", "模块3：舆情挖掘与可视化仪表盘"],
        label_visibility="collapsed",
    )

    if tab.startswith("模块1"):
        render_module1_sentiment()
    elif tab.startswith("模块2"):
        render_module2_explicit_implicit()
    else:
        render_module3_opinion_dashboard()

    render_footer_attribution()


if __name__ == "__main__":
    main()
