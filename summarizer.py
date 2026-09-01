"""LLM 摘要器：长文档自动生成摘要和核心要点，超长文本分块处理。"""

from typing import List

from config import Config
from parser import parse_document


class SummarizeError(Exception):
    """摘要异常。"""


class LLMClient:
    """轻量 LLM 客户端封装（OpenAI 兼容）。"""

    def __init__(self):
        if not Config.has_llm():
            raise SummarizeError(
                "未配置 OPENAI_API_KEY，请复制 .env.example 为 .env 并填入 API Key"
            )
        try:
            from openai import OpenAI
        except ImportError:
            raise SummarizeError("未安装 openai，请运行 pip install openai")

        self.client = OpenAI(
            api_key=Config.OPENAI_API_KEY,
            base_url=Config.OPENAI_BASE_URL if Config.OPENAI_BASE_URL else None,
        )
        self.model = Config.CHAT_MODEL

    def chat(self, system: str, user: str) -> str:
        """调用对话模型。"""
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip()


def summarize_document(path: str, points: int = None, max_chars: int = None) -> dict:
    """对文档生成摘要和要点。

    Args:
        path: 文档路径
        points: 要点数量
        max_chars: 单块最大字符数

    Returns:
        dict: {"title", "summary", "points", "used_llm"}
    """
    parsed = parse_document(path)
    content = parsed["content"]
    points = points or Config.DEFAULT_POINTS
    max_chars = max_chars or Config.SUMMARY_CHAR_LIMIT

    if not content.strip():
        raise SummarizeError("文档内容为空，无法生成摘要")

    llm = LLMClient()

    # 超长文本分块
    chunks = _chunk_text(content, max_chars)

    if len(chunks) == 1:
        summary, point_list = _summarize_chunk(llm, chunks[0], parsed["title"], points)
    else:
        # 多块：先分别摘要，再合并
        chunk_summaries = []
        for i, chunk in enumerate(chunks, 1):
            s, _ = _summarize_chunk(llm, chunk, f"{parsed['title']} (第{i}部分)", max(2, points))
            chunk_summaries.append(s)
        combined = "\n".join(chunk_summaries)
        summary, point_list = _summarize_chunk(llm, combined, parsed["title"], points)

    return {
        "title": parsed["title"],
        "type": parsed["type"],
        "summary": summary,
        "points": point_list,
        "chunks": len(chunks),
        "used_llm": True,
    }


def _summarize_chunk(llm: LLMClient, content: str, title: str, points: int) -> tuple:
    """对单个文本块生成摘要和要点。"""
    system = "你是一个专业的文档摘要助手，用中文输出。"
    user = (
        f"请对以下文档《{title}》生成摘要和核心要点。\n"
        f"要求：\n"
        f"1. 摘要 100-200 字，概括主要内容\n"
        f"2. 列出 {points} 个核心要点，每条一句话\n\n"
        f"输出格式：\n"
        f"【摘要】\n...\n\n【要点】\n- ...\n- ...\n\n"
        f"文档内容：\n{content}"
    )
    resp = llm.chat(system, user)
    return _parse_response(resp)


def _parse_response(text: str) -> tuple:
    """解析 LLM 输出为摘要和要点列表。"""
    summary = text
    points = []

    # 尝试分割
    if "【要点】" in text:
        parts = text.split("【要点】")
        summary = parts[0].replace("【摘要】", "").strip()
        points = [
            p.strip().lstrip("-*• ").strip()
            for p in parts[1].splitlines()
            if p.strip().startswith(("-", "*", "•"))
        ]
    elif "**要点**" in text:
        parts = text.split("**要点**")
        summary = parts[0].replace("**摘要**", "").strip()
        points = [p.strip().lstrip("-*• ").strip() for p in parts[1].splitlines() if p.strip()]

    if not points:
        # 兜底：把响应按行拆
        points = [line.strip().lstrip("-*• ") for line in text.splitlines() if line.strip()][1:]
    if not points:
        points = ["（未能提取要点）"]

    return summary, points


def _chunk_text(text: str, max_chars: int) -> List[str]:
    """按最大字符数切分文本，尽量在段落边界切。"""
    if len(text) <= max_chars:
        return [text]

    chunks = []
    current = ""
    for para in text.split("\n\n"):
        if len(current) + len(para) + 2 <= max_chars:
            current = current + "\n\n" + para if current else para
        else:
            if current:
                chunks.append(current)
            if len(para) > max_chars:
                # 超长段落按字符硬切
                for i in range(0, len(para), max_chars):
                    chunks.append(para[i:i + max_chars])
                current = ""
            else:
                current = para
    if current:
        chunks.append(current)
    return chunks


def format_result(result: dict) -> str:
    """格式化摘要结果为易读文本。"""
    lines = [
        f"📄 文档摘要: {result['title']}",
        "=" * 50,
        f"{result['summary']}",
        "",
        "🔑 核心要点:",
    ]
    for i, p in enumerate(result["points"], 1):
        lines.append(f"  {i}. {p}")
    if result["chunks"] > 1:
        lines.append(f"\n（文档较长，分 {result['chunks']} 块处理）")
    return "\n".join(lines)
