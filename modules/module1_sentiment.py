import os

import streamlit as st

from modules.sentiment_viz import build_confidence_gauge
from services.sentiment_service import analyze_sentiment
from theme import render_week10_intro

EXAMPLE_REVIEWS = {
    "明显好评": "物流超快，包装严实，手机续航和拍照都超预期，五星好评，会回购！",
    "明显差评": "到货外壳刮花严重，客服推诿不处理，用了三天就死机，非常失望，坚决退货。",
    "中性评价": "商品与描述基本一致，价格适中，没有惊喜也没有大问题，算是中规中矩。",
    "阴阳怪气": "挺好的，也就是等了半个月才发货，坏了两次而已，客服回复挺“及时”的（三天回一句）。",
}


def _apply_example_review() -> None:
    selected = st.session_state.get("m1_example_select", "明显好评")
    st.session_state["m1_review_text"] = EXAMPLE_REVIEWS.get(selected, EXAMPLE_REVIEWS["明显好评"])


def render_module1_sentiment() -> None:
    st.title("Week10 细粒度情感分析与舆情监测平台")
    st.caption("模块1：单条中文评论的情感极性与置信度量化。")
    render_week10_intro()

    if "m1_review_text" not in st.session_state:
        st.session_state["m1_review_text"] = EXAMPLE_REVIEWS["明显好评"]

    left, right = st.columns([1, 1])
    with left:
        st.selectbox(
            "示例评论",
            list(EXAMPLE_REVIEWS.keys()),
            key="m1_example_select",
            on_change=_apply_example_review,
            help="切换后将自动填充下方输入框，便于课堂对比观察。",
        )
        text = st.text_area("中文商品评论", key="m1_review_text", height=220)
        st.caption(
            "运行环境：建议在 conda **base** 中启动（`conda activate base`），并在该环境下 "
            "`pip install -r requirements.txt`。首次运行会从镜像下载模型，可能需要数十秒至数分钟。"
        )
        st.caption(
            "模型下载 endpoint："
            f"HF_ENDPOINT={os.environ.get('HF_ENDPOINT', '未设置')}；"
            f"HUGGINGFACE_HUB_BASE_URL={os.environ.get('HUGGINGFACE_HUB_BASE_URL', '未设置')}"
        )
        run = st.button("分析情感", use_container_width=True)

    with right:
        st.markdown("**分析结果**")
        if not run:
            st.markdown(
                '<div class="result-box">输入评论并点击「分析情感」，将显示极性、置信度仪表盘与三类概率。</div>',
                unsafe_allow_html=True,
            )
            return

        if not text.strip():
            st.warning("请先输入非空评论。")
            return

        with st.spinner("模型推理中..."):
            result = analyze_sentiment(text)

        if result.get("ok") != "true":
            st.error(result.get("error", "分析失败。"))
            if result.get("detail"):
                st.caption(f"错误详情：{result['detail']}")
            return

        top_en = result.get("top_label_en", "")
        top_zh = result.get("top_label_zh", "")
        top_score = float(result.get("top_score", "0"))
        pct = max(0.0, min(100.0, top_score * 100.0))

        st.success(f"**情感极性：** {top_en}（{top_zh}）")
        st.metric("置信度（预测类别概率）", f"{pct:.2f}%")

        fig = build_confidence_gauge(top_en, pct)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            f'<div class="small-note">模型：{result.get("model", "")} ｜ '
            f'本次推理耗时：{result.get("elapsed_ms", "?")} ms（重复分析通常会更快）</div>',
            unsafe_allow_html=True,
        )

        all_scores = result.get("all_scores") or []
        with st.expander("查看三类概率分布（课堂观察）", expanded=True):
            st.markdown(
                "当多个类别的概率接近时，说明模型「不那么确定」——工程上常结合阈值、人工复核或二次模型处理。"
            )
            rows = []
            for row in sorted(all_scores, key=lambda x: float(x["score"]), reverse=True):
                rows.append(
                    {
                        "极性": f"{row['label_en']}（{row['label_zh']}）",
                        "概率": f"{float(row['score']):.4f}",
                    }
                )
            st.table(rows)

            for row in sorted(all_scores, key=lambda x: float(x["score"]), reverse=True):
                st.caption(f"{row['label_en']} · {float(row['score']):.2%}")
                st.progress(float(row["score"]))

        with st.expander("为什么要同时看「标签」和「置信度」？"):
            st.markdown(
                "- **阈值与风控**：低置信样本可触发告警、转人工或请求更多信息，而不是直接自动化处置。"
            )
            st.markdown(
                "- **误差形态**：标签可能在边界样本上不稳定；概率刻画了模型内在的不确定性（并非等同真实校准，但仍是实用信号）。"
            )
            st.markdown(
                "- **业务决策**：同样的「负面」标签，0.51 与 0.97 的业务含义完全不同；仪表盘让差异一目了然。"
            )
