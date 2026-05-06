import os
import time
from typing import Any, Dict, List, Tuple

import streamlit as st

os.environ.setdefault("TRANSFORMERS_NO_TF", "1")
os.environ.setdefault("TRANSFORMERS_NO_FLAX", "1")
os.environ.setdefault("USE_TF", "0")
os.environ.setdefault("USE_FLAX", "0")

HF_MIRROR_ENDPOINT = "https://hf-mirror.com"
os.environ["HF_ENDPOINT"] = HF_MIRROR_ENDPOINT
os.environ["HF_HUB_ENDPOINT"] = HF_MIRROR_ENDPOINT
os.environ["HUGGINGFACE_HUB_BASE_URL"] = HF_MIRROR_ENDPOINT

from transformers import pipeline  # noqa: E402
from huggingface_hub import snapshot_download  # noqa: E402

MODEL_NAME = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
MAX_INPUT_CHARS = 2000
LOCAL_MODEL_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".hf_cache", "distilbert-multilingual-sentiments-student")
)

_WEIGHT_FILES = {
    "pytorch_model.bin",
    "model.safetensors",
    "tf_model.h5",
    "tf_model.h5.index",
    "model.ckpt.index",
    "flax_model.msgpack",
}


def _local_model_has_weights(model_dir: str) -> bool:
    if not os.path.exists(os.path.join(model_dir, "config.json")):
        return False
    for name in _WEIGHT_FILES:
        if os.path.exists(os.path.join(model_dir, name)):
            return True
    for root, _, files in os.walk(model_dir):
        for f in files:
            if f in _WEIGHT_FILES:
                return True
    return False


def _canonical_label(raw: str) -> Tuple[str, str]:
    """
    将 HF 模型返回的 label 规范为展示用英文与中文说明。
    """
    r = raw.strip().lower()
    if "positive" in r or r in ("pos", "label_2"):
        return "Positive", "正面"
    if "negative" in r or r in ("neg", "label_0"):
        return "Negative", "负面"
    if "neutral" in r or r in ("neu", "label_1"):
        return "Neutral", "中性"
    title = raw.replace("_", " ").strip().title() or raw
    return title, title


def _normalize_scores(raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """合并同一 canonical 标签的多条输出（若存在），按 score 降序。"""
    merged: Dict[str, Dict[str, Any]] = {}
    for it in raw_items:
        raw_label = str(it.get("label", ""))
        score = float(it.get("score", 0.0))
        en, zh = _canonical_label(raw_label)
        if en not in merged or score > merged[en]["score"]:
            merged[en] = {
                "label_en": en,
                "label_zh": zh,
                "score": score,
                "raw_label": raw_label,
            }
    out = sorted(merged.values(), key=lambda x: x["score"], reverse=True)
    return out


@st.cache_resource(show_spinner=False)
def get_sentiment_classifier():
    os.makedirs(LOCAL_MODEL_DIR, exist_ok=True)
    if _local_model_has_weights(LOCAL_MODEL_DIR):
        return pipeline(
            "sentiment-analysis",
            model=LOCAL_MODEL_DIR,
            framework="pt",
        )

    try:
        snapshot_download(
            repo_id=MODEL_NAME,
            endpoint=HF_MIRROR_ENDPOINT,
            local_dir=LOCAL_MODEL_DIR,
            etag_timeout=20,
        )
    except Exception:
        try:
            return pipeline(
                "sentiment-analysis",
                model=MODEL_NAME,
                framework="pt",
                model_kwargs={"local_files_only": True},
            )
        except Exception as exc:
            raise RuntimeError(
                "情感模型权重缺失，且无法从 hf-mirror 下载到本地。"
                "请确认网络可用，或将模型预先下载到本地缓存。"
            ) from exc

    if not _local_model_has_weights(LOCAL_MODEL_DIR):
        raise RuntimeError(
            "模型权重仍未在本地目录找到。请确认网络可用并重试；必要时删除本目录后重新下载。"
        )

    return pipeline(
        "sentiment-analysis",
        model=LOCAL_MODEL_DIR,
        framework="pt",
    )


def analyze_sentiment(text: str) -> Dict[str, Any]:
    cleaned = text.strip()
    if not cleaned:
        return {"ok": "false", "error": "请输入评论文本后再进行分析。"}
    if len(cleaned) > MAX_INPUT_CHARS:
        return {"ok": "false", "error": f"输入过长（>{MAX_INPUT_CHARS} 字符），请缩短后重试。"}

    t0 = time.perf_counter()
    try:
        clf = get_sentiment_classifier()
        raw_out = clf(cleaned, truncation=True, max_length=512, top_k=3)
    except Exception as exc:
        return {
            "ok": "false",
            "error": (
                "模型加载或推理失败。请确认网络可用，并已在 conda base 环境安装 "
                "transformers、torch、sentencepiece、plotly 后重试（可先执行 conda activate base）。"
            ),
            "detail": str(exc),
        }

    elapsed_ms = int((time.perf_counter() - t0) * 1000)

    if isinstance(raw_out, dict):
        raw_items = [raw_out]
    elif isinstance(raw_out, list) and raw_out and isinstance(raw_out[0], list):
        raw_items = raw_out[0]
    elif isinstance(raw_out, list) and raw_out and isinstance(raw_out[0], dict):
        raw_items = raw_out
    else:
        return {
            "ok": "false",
            "error": "模型返回格式异常，请更换输入或检查 transformers 版本。",
            "detail": str(raw_out)[:500],
        }

    all_scores = _normalize_scores(raw_items)
    if not all_scores:
        return {"ok": "false", "error": "模型未返回有效概率分布。"}

    top = all_scores[0]
    return {
        "ok": "true",
        "model": MODEL_NAME,
        "elapsed_ms": str(elapsed_ms),
        "top_label_en": top["label_en"],
        "top_label_zh": top["label_zh"],
        "top_score": str(top["score"]),
        "all_scores": all_scores,
    }
