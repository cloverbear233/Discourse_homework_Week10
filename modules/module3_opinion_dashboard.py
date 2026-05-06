import random
from typing import Any, Dict, List, Tuple

import plotly.graph_objects as go
import streamlit as st

from services.sentiment_service import analyze_sentiment

# 候选池略大于 15 条，便于随机抽样出 10–15 条不重复的模拟评论
_MOCK_REVIEW_POOL: List[str] = [
    "发货神速，包装完好，耳机降噪效果惊艳，已经推荐给朋友了！",
    "屏幕色彩通透，系统流畅，这个价格买到很值，全五星。",
    "客服耐心解答，退换货流程顺畅，购物体验超出预期。",
    "做工扎实，续航一整天没问题，拍照夜景也很干净。",
    "性价比很高，学生党预算有限也能入手，日常够用。",
    "商品与描述一致，没有惊喜也没有踩雷，算是中规中矩。",
    "功能该有的都有，外观普通，属于无功无过的水平。",
    "等了三天才揽收，到货后外包装有点瘪，但机器还能用。",
    "说明书印刷模糊，不过不影响使用，整体凑合。",
    "音质一般，低音有点闷，听个响还行，别指望发烧级。",
    "到货外壳划痕明显，联系客服推诿，体验非常差，考虑维权。",
    "用了两周频繁死机，售后检测说要自费维修，坚决差评。",
    "广告宣传夸大，实际续航不到半天，感觉被忽悠了。",
    "充电头发烫严重，担心安全隐患，已申请退货。",
    "软件广告推送太多，关都关不掉，严重影响使用心情。",
    "拍照发黄严重，跟店里演示完全不一样，要求退款。",
    "物流暴力分拣，盒子破了，里面屏幕也有细纹，失望。",
    "耳机一边声音偏小，品控堪忧，不会再买这个牌子。",
    "更新系统后卡顿明显，官方迟迟不出补丁，很不负责任。",
    "号称防水结果进水了不保修，条款全是坑，差评。",
]


def _generate_mock_reviews(rng: random.Random) -> List[str]:
    k = rng.randint(10, 15)
    if k > len(_MOCK_REVIEW_POOL):
        k = len(_MOCK_REVIEW_POOL)
    return rng.sample(_MOCK_REVIEW_POOL, k)


def _inject_dashboard_style() -> None:
    st.markdown(
        """
        <style>
        .m3-dash-wrap{
            background: linear-gradient(145deg, #0b1220 0%, #111827 42%, #0f172a 100%);
            border-radius: 18px;
            padding: 1.35rem 1.45rem 1.55rem 1.45rem;
            margin: 0.5rem 0 1.1rem 0;
            border: 1px solid rgba(56, 189, 248, 0.28);
            box-shadow:
                0 0 0 1px rgba(15, 23, 42, 0.6) inset,
                0 12px 40px rgba(8, 47, 73, 0.35),
                0 0 48px rgba(56, 189, 248, 0.08);
        }
        .m3-dash-title{
            color: #e0f2fe;
            font-size: 1.35rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            margin: 0 0 0.35rem 0;
            text-shadow: 0 0 18px rgba(56, 189, 248, 0.35);
        }
        .m3-dash-sub{
            color: #94a3b8;
            font-size: 0.98rem;
            margin: 0 0 1rem 0;
            line-height: 1.55;
        }
        .m3-kpi-row{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: space-between;
            margin-top: 0.5rem;
        }
        .m3-kpi{
            flex: 1 1 140px;
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(56, 189, 248, 0.18);
            border-radius: 12px;
            padding: 0.75rem 1rem;
            box-shadow: 0 0 24px rgba(56, 189, 248, 0.06) inset;
        }
        .m3-kpi-label{ color: #94a3b8; font-size: 0.88rem; letter-spacing: 0.06em; }
        .m3-kpi-val{ font-size: 1.65rem; font-weight: 780; margin-top: 0.2rem; font-variant-numeric: tabular-nums; }
        .m3-kpi-total .m3-kpi-val{ color: #7dd3fc; }
        .m3-kpi-pos .m3-kpi-val{ color: #34d399; text-shadow: 0 0 12px rgba(52, 211, 153, 0.35); }
        .m3-kpi-neg .m3-kpi-val{ color: #fb7185; text-shadow: 0 0 12px rgba(251, 113, 133, 0.35); }
        .m3-kpi-neu .m3-kpi-val{ color: #cbd5e1; }
        div[data-testid="stPlotlyChart"]{
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid rgba(56, 189, 248, 0.22);
            box-shadow: 0 14px 36px rgba(15, 23, 42, 0.22);
            margin-top: 0.35rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _build_opinion_pie(counts: Dict[str, int]) -> go.Figure:
    order = [("Positive", "正面", "#34d399"), ("Negative", "负面", "#fb7185"), ("Neutral", "中性", "#94a3b8")]
    labels: List[str] = []
    values: List[int] = []
    colors: List[str] = []
    for key, zh, col in order:
        v = int(counts.get(key, 0))
        if v > 0:
            labels.append(f"{zh} {key}")
            values.append(v)
            colors.append(col)

    if not values:
        labels = ["暂无数据"]
        values = [1]
        colors = ["#475569"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.58,
                marker=dict(colors=colors, line=dict(color="#020617", width=2)),
                textinfo="label+percent",
                textposition="outside",
                textfont=dict(size=14, color="#e2e8f0"),
                insidetextorientation="radial",
                hovertemplate="%{label}<br>条数: %{value}<br>占比: %{percent}<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#cbd5e1", family="PingFang SC, Microsoft YaHei, sans-serif"),
        title=dict(
            text="整体口碑比例 · Sentiment Mix",
            x=0.5,
            xanchor="center",
            font=dict(size=18, color="#7dd3fc"),
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.12,
            x=0.5,
            xanchor="center",
            font=dict(size=13, color="#94a3b8"),
        ),
        margin=dict(t=54, b=72, l=28, r=28),
        height=440,
        annotations=[
            dict(
                text="OPINION<br>MINING",
                x=0.5,
                y=0.5,
                font_size=13,
                font_color="rgba(148,163,184,0.55)",
                showarrow=False,
            )
        ],
    )
    return fig


def render_module3_opinion_dashboard() -> None:
    st.header("模块3：舆情挖掘与可视化仪表盘")
    st.caption("对应课件：意见挖掘与大规模情感分析的应用。")

    st.markdown(
        """
        <div class="wk10_intro">
          <strong>本模块做什么？</strong>
          将单句情感分类扩展到一批模拟电商评论：自动生成测试语料、批量推理、汇总极性分布，
          用图表呈现「宏观口碑结构」，支撑产品改进与舆情预警等决策场景。
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "m3_rng_seed" not in st.session_state:
        st.session_state["m3_rng_seed"] = 2026
    if "m3_reviews" not in st.session_state:
        st.session_state["m3_reviews"] = []
    if "m3_batch_rows" not in st.session_state:
        st.session_state["m3_batch_rows"] = []

    col_a, col_b, col_c = st.columns([1, 1, 2])
    with col_a:
        gen = st.button("生成测试舆情数据", use_container_width=True, key="m3_gen")
    with col_b:
        run_batch = st.button("批量情感分析", use_container_width=True, key="m3_batch")

    if gen:
        st.session_state["m3_rng_seed"] = st.session_state["m3_rng_seed"] + 1
        rng = random.Random(st.session_state["m3_rng_seed"])
        st.session_state["m3_reviews"] = _generate_mock_reviews(rng)
        st.session_state["m3_batch_rows"] = []
        st.success(f"已生成 {len(st.session_state['m3_reviews'])} 条模拟评价（批次 seed={st.session_state['m3_rng_seed']}）。")

    reviews: List[str] = st.session_state["m3_reviews"]

    if not reviews:
        st.info("请先点击「生成测试舆情数据」，系统将随机抽取 10–15 条模拟商品评价（含好、中、差各类表述）。")
        return

    with st.expander(f"当前批次预览（共 {len(reviews)} 条）", expanded=False):
        for i, r in enumerate(reviews, start=1):
            st.markdown(f"{i}. {r}")

    if run_batch:
        rows: List[Dict[str, Any]] = []
        prog = st.progress(0.0)
        status = st.empty()
        status.caption("批量推理中…")
        for idx, text in enumerate(reviews):
            result = analyze_sentiment(text)
            row: Dict[str, Any] = {"序号": idx + 1, "评论摘要": text[:80] + ("…" if len(text) > 80 else ""), "全文": text}
            if result.get("ok") == "true":
                row["极性"] = result.get("top_label_en", "")
                row["置信度"] = f"{float(result.get('top_score', 0)):.2%}"
            else:
                row["极性"] = "ERROR"
                row["置信度"] = "-"
                row["错误"] = result.get("error", "")
            rows.append(row)
            prog.progress((idx + 1) / max(len(reviews), 1))
            status.caption(f"已分析 {idx + 1}/{len(reviews)}")
        prog.empty()
        status.empty()
        st.session_state["m3_batch_rows"] = rows

    rows_out: List[Dict[str, Any]] = st.session_state.get("m3_batch_rows") or []

    if not rows_out:
        st.warning("已有模拟数据，请点击「批量情感分析」生成宏观图表与统计。")
        return

    counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    errors = 0
    for row in rows_out:
        lab = row.get("极性", "")
        if lab in counts:
            counts[lab] += 1
        elif lab == "ERROR":
            errors += 1

    _inject_dashboard_style()
    total = len(rows_out)
    st.markdown(
        f"""
        <div class="m3-dash-wrap">
          <p class="m3-dash-title">舆情监测大屏 · Opinion Mining Dashboard</p>
          <p class="m3-dash-sub">基于当前批次的批量情感推理结果，聚合 Positive / Negative / Neutral 分布。
          （轻量模型 + 模拟数据，仅供课堂演示。）</p>
          <div class="m3-kpi-row">
            <div class="m3-kpi m3-kpi-total">
              <div class="m3-kpi-label">TOTAL · 总条数</div>
              <div class="m3-kpi-val">{total}</div>
            </div>
            <div class="m3-kpi m3-kpi-pos">
              <div class="m3-kpi-label">POSITIVE · 正面</div>
              <div class="m3-kpi-val">{counts["Positive"]}</div>
            </div>
            <div class="m3-kpi m3-kpi-neg">
              <div class="m3-kpi-label">NEGATIVE · 负面</div>
              <div class="m3-kpi-val">{counts["Negative"]}</div>
            </div>
            <div class="m3-kpi m3-kpi-neu">
              <div class="m3-kpi-label">NEUTRAL · 中性</div>
              <div class="m3-kpi-val">{counts["Neutral"]}</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if errors:
        st.error(f"本批次有 {errors} 条推理失败，已计入表格，但未纳入饼图统计。")

    pie = _build_opinion_pie(counts)
    st.plotly_chart(pie, use_container_width=True)

    with st.expander("查看每条评论的标注明细", expanded=False):
        display_rows = []
        for row in rows_out:
            display_rows.append(
                {
                    "序号": row["序号"],
                    "极性": row["极性"],
                    "置信度": row["置信度"],
                    "评论摘要": row["评论摘要"],
                }
            )
        st.dataframe(display_rows, use_container_width=True, hide_index=True)

    with st.expander("课堂观察：从单句到大规模意见挖掘", expanded=True):
        st.markdown(
            "- **宏观涌现**：单条评论对应模块 1 的「针尖」判断；批量汇总后得到的是「海面」结构——占比变化对运营与产品路线更有解释力。"
        )
        st.markdown(
            "- **商业联想**：负面占比异常升高可触发危机预警与溯源；中性堆积可能提示「卖点不突出」或「期待管理」问题；正面主导则可提炼传播话术。"
        )
        st.markdown(
            "- **现实约束**：真实舆情数据存在抽样偏差、刷单与水军；生产环境还需时间维度、主题建模与人机复核，本仪表盘演示的是技术链路的核心一环。"
        )
