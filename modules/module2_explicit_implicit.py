import streamlit as st

from modules.sentiment_viz import build_confidence_gauge
from services.sentiment_service import analyze_sentiment


PAIR_PRESETS = {
    "自定义（不覆盖）": None,
    "观察任务·屏幕（显式负面 vs 隐式负面）": (
        "这屏幕画质太垃圾了",
        "在太阳底下根本看不清屏幕上的字",
    ),
    "显式好评 vs 隐式好评倾向": (
        "太棒了，手感无敌，我愿意给满分！",
        "同事看我用了两周也来问链接，已经推荐给项目组了。",
    ),
    "显式差评 vs 客观陈述（耗电）": (
        "这续航简直灾难级，谁买谁后悔。",
        "手机玩游戏半小时就没电了，得一直插着充电器。",
    ),
}

M2_PRESET_KEYS = list(PAIR_PRESETS.keys())
# 默认选中「观察任务」配对，与课堂观察示例一致
M2_DEFAULT_PRESET_INDEX = M2_PRESET_KEYS.index("观察任务·屏幕（显式负面 vs 隐式负面）")


def _apply_pair_preset() -> None:
    name = st.session_state.get("m2_preset_select", "自定义（不覆盖）")
    pair = PAIR_PRESETS.get(name)
    if pair is None:
        return
    explicit, implicit = pair
    st.session_state["m2_explicit_text"] = explicit
    st.session_state["m2_implicit_text"] = implicit


def _render_result_block(result: dict, heading: str, gauge_height: int = 300) -> None:
    st.markdown(f"**{heading}**")
    if result.get("ok") != "true":
        st.error(result.get("error", "分析失败。"))
        if result.get("detail"):
            st.caption(f"错误详情：{result['detail']}")
        return

    top_en = result.get("top_label_en", "")
    top_zh = result.get("top_label_zh", "")
    top_score = float(result.get("top_score", "0"))
    pct = max(0.0, min(100.0, top_score * 100.0))

    st.success(f"情感极性：**{top_en}**（{top_zh}）")
    st.metric("置信度", f"{pct:.2f}%")
    fig = build_confidence_gauge(top_en, pct, height=gauge_height)
    st.plotly_chart(fig, use_container_width=True)

    all_scores = result.get("all_scores") or []
    with st.expander("三类概率", expanded=False):
        for row in sorted(all_scores, key=lambda x: float(x["score"]), reverse=True):
            st.caption(f"{row['label_en']} · {float(row['score']):.2%}")
            st.progress(float(row["score"]))


def render_module2_explicit_implicit() -> None:
    st.header("模块2：显式情感 vs. 隐式情感识别")
    st.caption("对照课件：显式情感（Explicit）与隐式情感（Implicit）。")

    st.markdown(
        """
        <div class="wk10_intro">
          <strong>什么是显式情感？</strong>
          文本里直接出现明显的褒贬词或强烈态度，例如「太棒了」「垃圾」「失望透顶」——情感倾向往往一目了然。<br><br>
          <strong>什么是隐式情感？</strong>
          表面上是客观描述事实或现象，未必带情感词，但读者能推断态度。例如「手机玩游戏半小时就没电了」常隐含对续航的不满；
          「在太阳底下根本看不清屏幕上的字」常隐含对户外可视性的负面评价。
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "m2_explicit_text" not in st.session_state:
        pair0 = PAIR_PRESETS[M2_PRESET_KEYS[M2_DEFAULT_PRESET_INDEX]]
        if pair0 is not None:
            st.session_state["m2_explicit_text"], st.session_state["m2_implicit_text"] = pair0
        else:
            st.session_state["m2_explicit_text"] = ""
            st.session_state["m2_implicit_text"] = ""

    st.selectbox(
        "一键填入课堂示例（左右两框会同时更新）",
        M2_PRESET_KEYS,
        index=M2_DEFAULT_PRESET_INDEX,
        key="m2_preset_select",
        on_change=_apply_pair_preset,
    )

    c_left, c_right = st.columns(2)
    with c_left:
        explicit_text = st.text_area(
            "显式情感评价",
            key="m2_explicit_text",
            height=160,
            help="带有明显情感词或态度词的表述。",
        )
    with c_right:
        implicit_text = st.text_area(
            "隐式客观描述",
            key="m2_implicit_text",
            height=160,
            help="尽量不带明显褒贬词，用事实或现象传递态度。",
        )

    run = st.button("分别分析两条文本", use_container_width=True, key="m2_run")

    st.divider()
    st.markdown("##### 模型输出对比")

    with st.expander("课堂观察：隐式句模型能「听懂」吗？", expanded=True):
        st.markdown(
            "- 请尝试左侧输入**显式负面**（如「这屏幕画质太垃圾了」），右侧输入**隐式负面**（如「在太阳底下根本看不清屏幕上的字」）。"
        )
        st.markdown(
            "- **对比维度**：两侧是否都被判为 Negative？隐式句的置信度是否明显更低、或被判成 Neutral？"
        )
        st.markdown(
            "- **原因直觉**：轻量模型多依赖表层词线索；隐式评价需要世界知识与推理，仍是难点，工程上往往需要更强模型、观点抽取或人机协同。"
        )

    if not run:
        st.info("输入两侧文本后，点击「分别分析两条文本」查看情感模型对显式 / 隐式表述的差异。")
        return

    if not explicit_text.strip() and not implicit_text.strip():
        st.warning("请至少在其中一个输入框中填写文本。")
        return

    res_explicit = None
    res_implicit = None
    if explicit_text.strip():
        with st.spinner("分析「显式情感评价」…"):
            res_explicit = analyze_sentiment(explicit_text)
    if implicit_text.strip():
        with st.spinner("分析「隐式客观描述」…"):
            res_implicit = analyze_sentiment(implicit_text)

    out_l, out_r = st.columns(2)
    with out_l:
        if res_explicit is None:
            st.markdown("**显式情感评价 · 结果**")
            st.caption("（该侧为空，未调用模型）")
        else:
            _render_result_block(res_explicit, "显式情感评价 · 结果")

    with out_r:
        if res_implicit is None:
            st.markdown("**隐式客观描述 · 结果**")
            st.caption("（该侧为空，未调用模型）")
        else:
            _render_result_block(res_implicit, "隐式客观描述 · 结果")
