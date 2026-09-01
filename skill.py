"""办公文档助手 - CLI 入口。

用法:
    python skill.py parse <文件路径> [--json]
    python skill.py summarize <文件路径> [--points N]
    python skill.py convert <文件路径> --to html|docx|txt [--out 输出路径]
    python skill.py batch <目录> --parse|--summarize|--convert --to 格式
"""

import argparse
import sys

from parser import parse_document, format_plain, format_json, ParseError
from converter import convert_file, ConvertError
from summarizer import summarize_document, format_result, SummarizeError
from batcher import batch_process


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="skill", description="办公文档助手 Skill")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # parse
    p = sub.add_parser("parse", help="解析文档")
    p.add_argument("path", help="文档路径")
    p.add_argument("--json", action="store_true", help="输出 JSON")

    # summarize
    s = sub.add_parser("summarize", help="生成摘要")
    s.add_argument("path", help="文档路径")
    s.add_argument("--points", type=int, default=None, help="要点数量")

    # convert
    c = sub.add_parser("convert", help="格式转换")
    c.add_argument("path", help="源文件路径")
    c.add_argument("--to", required=True, help="目标格式: html/docx/txt")
    c.add_argument("--out", default=None, help="输出路径")

    # batch
    b = sub.add_parser("batch", help="批量处理")
    b.add_argument("directory", help="目录路径")
    action = b.add_mutually_exclusive_group(required=True)
    action.add_argument("--parse", action="store_true", help="批量解析")
    action.add_argument("--summarize", action="store_true", help="批量摘要")
    action.add_argument("--convert", action="store_true", help="批量转换")
    b.add_argument("--to", default="html", help="转换目标格式（--convert 时使用）")
    b.add_argument("--points", type=int, default=None, help="要点数量")
    b.add_argument("--verbose", action="store_true", help="显示详细错误")

    return parser


def main():
    args = build_parser().parse_args()

    try:
        if args.cmd == "parse":
            parsed = parse_document(args.path)
            print(format_json(parsed) if args.json else format_plain(parsed))

        elif args.cmd == "summarize":
            result = summarize_document(args.path, points=args.points)
            print(format_result(result))

        elif args.cmd == "convert":
            out = convert_file(args.path, args.to, args.out)
            print(f"✅ 转换完成: {out}")

        elif args.cmd == "batch":
            if args.parse:
                action = "parse"
            elif args.summarize:
                action = "summarize"
            else:
                action = "convert"
            print(batch_process(
                args.directory,
                action,
                to=args.to,
                points=args.points,
                verbose=args.verbose,
            ))

    except (ParseError, ConvertError, SummarizeError) as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 未知错误: {type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
