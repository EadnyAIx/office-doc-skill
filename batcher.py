"""批量处理器：对目录下的文档递归执行解析/摘要/转换。"""

import traceback
from pathlib import Path

from parser import parse_document, format_plain
from converter import convert_file
from summarizer import summarize_document, format_result


SUPPORTED_EXT = {".pdf", ".docx", ".doc", ".md", ".markdown", ".txt"}


def batch_process(directory: str, action: str, **kwargs) -> str:
    """批量处理目录下的所有文档。

    Args:
        directory: 目录路径
        action: 操作 (parse / summarize / convert)
        **kwargs: 附加参数（to=目标格式等）

    Returns:
        处理报告
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return f"❌ 目录不存在: {directory}"
    if not dir_path.is_dir():
        return f"❌ 不是目录: {directory}"

    files = _collect_files(dir_path)
    if not files:
        return f"📭 目录下没有支持的文档（{', '.join(sorted(SUPPORTED_EXT))}）"

    results = []
    success = 0
    failed = 0

    for f in files:
        try:
            if action == "parse":
                parsed = parse_document(str(f))
                output = format_plain(parsed)
                results.append(f"✅ {f.name} (解析成功)")
            elif action == "summarize":
                result = summarize_document(str(f), points=kwargs.get("points"))
                output = format_result(result)
                results.append(f"✅ {f.name} (摘要生成)")
            elif action == "convert":
                to_fmt = kwargs.get("to", "html")
                out_path = convert_file(str(f), to_fmt)
                results.append(f"✅ {f.name} → {Path(out_path).name}")
            else:
                return f"❌ 不支持的操作: {action}"
            success += 1
        except Exception as e:
            failed += 1
            results.append(f"❌ {f.name}: {e}")
            if kwargs.get("verbose"):
                traceback.print_exc()

    report = [
        f"📦 批量处理报告 ({action})",
        "=" * 50,
        f"处理文件: {len(files)} 个",
        f"成功: {success} 个",
        f"失败: {failed} 个",
        "",
        "明细:",
    ]
    report.extend(f"  {r}" for r in results)
    return "\n".join(report)


def _collect_files(dir_path: Path) -> list:
    """收集目录下所有支持的文档。"""
    files = []
    for f in sorted(dir_path.rglob("*")):
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXT:
            files.append(f)
    return files
