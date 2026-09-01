# office-doc-skill

办公文档助手 Skill：多格式文档解析、摘要要点、格式转换、批量处理。

## 触发条件

当用户需要处理日常文档任务时调用本 Skill：
- 读取/解析 PDF、Word、Markdown、TXT 文档内容
- 对长文档生成摘要和核心要点
- 文档格式互转（Markdown↔HTML、TXT→Word）
- 对整个文件夹的文档进行批量处理

## 使用方式

本 Skill 通过 CLI 入口 `skill.py` 提供服务：

```bash
# 解析提取
python skill.py parse <文件路径>            # 提取标题/正文/表格
python skill.py parse <路径> --json         # 输出结构化 JSON

# 摘要要点（需要 OPENAI_API_KEY）
python skill.py summarize <文件路径>        # 生成摘要和核心要点
python skill.py summarize <文件路径> --points 5

# 格式转换
python skill.py convert 笔记.md --to html   # MD → HTML
python skill.py convert 笔记.md --to docx   # MD → Word
python skill.py convert 草稿.txt --to docx  # TXT → Word

# 批量处理
python skill.py batch <目录> --parse        # 批量解析
python skill.py batch <目录> --summarize    # 批量摘要
python skill.py batch <目录> --to html      # 批量转换
```

## 配置

摘要功能需要 LLM，请在 `.env` 中配置：

```
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1
CHAT_MODEL=gpt-4o-mini
```

解析、转换、批量（非摘要）功能完全离线可用。

## 子功能说明

### 1. 解析提取 (parse)
- 统一接口解析 PDF / Word (.docx) / Markdown / TXT
- 自动识别文档类型，提取标题、正文、表格
- 支持 JSON 结构化输出

### 2. 摘要要点 (summarize)
- 长文档自动生成摘要（100-200字）和核心要点列表
- 可指定要点数量
- 基于 LLM 生成，自动处理超长文本（分块）

### 3. 格式转换 (convert)
- Markdown → HTML（保留标题/列表/代码块/表格）
- Markdown → Word (.docx)
- TXT → Word (.docx)

### 4. 批量处理 (batch)
- 对整个目录递归处理
- 支持批量解析/摘要/转换
- 自动生成处理报告

## 设计要点

- 多格式统一解析接口，新增格式只需注册解析器
- 摘要功能对超长文本自动分块，避免超 token 限制
- 所有文件操作有明确的错误处理和提示
- 输出文件默认放在同目录 `output/` 下
