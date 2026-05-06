# Sentiment Analysis & Opinion Mining Dashboard

基于 **Streamlit**、**Hugging Face Transformers**（DistilBERT 多语种情感）与 **Plotly** 的中文电商评论分析演示应用：单条情感与置信度仪表盘、显式/隐式表述对照、批量模拟舆情与饼图大屏。

## 环境

建议使用 conda `base`（或独立 venv）与 Python 3.10+。

```bash
conda activate base
cd /path/to/this-repo
pip install -r requirements.txt
```

## 运行

```bash
streamlit run app.py
```

首次运行会从镜像拉取模型到本地 `.hf_cache/`（已加入 `.gitignore`），需可访问外网或已配置 `HF_ENDPOINT` 等镜像变量。

## 模块说明

| 模块 | 功能概要 |
|------|----------|
| 1 | 单条中文评论：Positive / Negative / Neutral + 半圆置信度仪表盘 |
| 2 | 「显式情感」与「隐式客观描述」双框对照推理 |
| 3 | 随机生成 10–15 条模拟评论，批量推理并展示舆情饼图 |

## 许可证

课堂 / 个人学习用途请遵循所在课程要求；开源分发时请自行补充许可证文件。
