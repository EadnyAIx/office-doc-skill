# 办公文档助手 Skill

> 多格式文档解析、摘要要点、格式转换、批量处理，一个技能搞定日常文档杂活。

## ✨ 功能特性

### 📄 解析提取
- 统一接口解析 PDF / Word (.docx) / Markdown / TXT
- 自动识别文档类型，提取标题、正文、表格
- 支持 JSON 结构化输出

### ✂️ 摘要要点
- 长文档自动生成摘要和核心要点（LLM）
- 可指定要点数量
- 超长文本自动分块处理

### 🔄 格式转换
- Markdown → HTML / Word
- TXT → Word

### 📦 批量处理
- 递归处理整个目录
- 批量解析 / 摘要 / 转换
- 自动生成处理报告

## 🏗️ 架构

```
skill.py (CLI 入口)
 ├── parser.py      多格式解析统一接口
 ├── summarizer.py  LLM 摘要/要点
 ├── converter.py   格式转换
 └── batcher.py     批量处理
```

## 📦 安装

```bash
git clone <repo-url>
cd office-doc-skill
pip install -r requirements.txt
cp .env.example .env   # 摘要功能需要配置 OPENAI_API_KEY
```

## 🚀 使用方法

### 解析文档

```bash
python skill.py parse 报告.pdf
python skill.py parse 论文.docx
python skill.py parse 笔记.md --json
```

### 生成摘要

```bash
python skill.py summarize 论文.docx
python skill.py summarize 报告.pdf --points 5
```

### 格式转换

```bash
python skill.py convert 笔记.md --to html
python skill.py convert 笔记.md --to docx
python skill.py convert 草稿.txt --to docx
```

### 批量处理

```bash
python skill.py batch ./docs --parse
python skill.py batch ./docs --summarize
python skill.py batch ./docs --to html
```

## 🧪 测试

```bash
python -m pytest tests/ -v
```

## 📁 项目结构

```
office-doc-skill/
├── SKILL.md
├── skill.py              # CLI 入口
├── parser.py             # 多格式解析
├── summarizer.py         # LLM 摘要
├── converter.py          # 格式转换
├── batcher.py            # 批量处理
├── config.py             # 配置
├── requirements.txt
├── .env.example
├── .gitignore
└── tests/
    ├── test_parser.py
    ├── test_converter.py
    └── test_batcher.py
```

## 📄 License

MIT
