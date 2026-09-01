"""batcher 单元测试。"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from batcher import batch_process


def test_batch_parse():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "a.txt").write_text("文件A内容", encoding="utf-8")
        (tmp / "b.md").write_text("# 文件B\n\n内容B", encoding="utf-8")
        report = batch_process(str(tmp), "parse")
        assert "成功: 2" in report
        assert "a.txt" in report
        assert "b.md" in report


def test_batch_empty_dir():
    with tempfile.TemporaryDirectory() as tmp:
        report = batch_process(str(tmp), "parse")
        assert "没有支持" in report


def test_batch_convert():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "a.md").write_text("# 标题\n\n正文", encoding="utf-8")
        report = batch_process(str(tmp), "convert", to="html")
        assert "成功: 1" in report
        # 检查输出文件生成
        out_files = list((tmp / "output").glob("*.html"))
        assert len(out_files) == 1
