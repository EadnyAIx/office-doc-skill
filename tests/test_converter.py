"""converter 单元测试。"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from converter import convert_file, ConvertError


def test_md_to_html():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src = tmp / "note.md"
        src.write_text("# 标题\n\n正文", encoding="utf-8")
        out = convert_file(str(src), "html")
        content = Path(out).read_text(encoding="utf-8")
        assert "<h1>" in content
        assert "正文" in content


def test_md_to_txt_unsupported():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src = tmp / "note.md"
        src.write_text("test", encoding="utf-8")
        try:
            convert_file(str(src), "txt")
            assert False
        except ConvertError as e:
            assert "不支持" in str(e)


def test_md_to_docx():
    try:
        import docx  # noqa
    except ImportError:
        return
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src = tmp / "note.md"
        src.write_text("# 标题\n\n正文内容", encoding="utf-8")
        out = convert_file(str(src), "docx")
        assert Path(out).exists()
        assert Path(out).suffix == ".docx"


def test_invalid_target():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src = tmp / "note.md"
        src.write_text("test", encoding="utf-8")
        try:
            convert_file(str(src), "exe")
            assert False
        except ConvertError as e:
            assert "不支持" in str(e)
