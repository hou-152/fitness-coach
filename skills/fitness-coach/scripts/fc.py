#!/usr/bin/env python3
"""fitness-coach 统一入口：ask（知识检索）/ quota（配额计算）/ notes（笔记检索）。

自动发现同机安装的 fitness-kb 与 diet-plan 两个引擎 Skill；
notes 子命令直接检索知识库研究层的 76 个内容单元。

用法:
  fc.py ask "词根1" "词根2" [--cards]
  fc.py quota --gender male --weight 70 --height 175 --goal fat-loss --training strength
  fc.py notes "关键词"
"""
import argparse
import glob
import os
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
SUMMARY_URL = "https://xcn2zcuh5uow.feishu.cn/docx/XMo3dOlfZoLq7mxiou7crB4tnug"


def discover_kb():
    """自动发现知识库：Documents 下带 SOURCE_OF_TRUTH.md 且含研究工程/derived 标志物的目录。"""
    env = os.environ.get("FITNESS_KB_ROOT")
    if env:
        return Path(env)
    for cand in sorted(glob.glob(str(HOME / "Documents/*/SOURCE_OF_TRUTH.md"))):
        d = Path(cand).parent
        if (d / "研究工程").is_dir() and (d / "derived").is_dir() and (d / "raw").is_dir():
            return d
    return None


KB_ROOT = discover_kb()


def find_engine(skill, script):
    """在已知宿主 skills 目录里定位引擎脚本。"""
    for host in (HOME / ".zcode/skills", HOME / ".agents/skills",
                 HOME / ".claude/skills", HOME / ".codex/skills", HOME / ".grok/skills"):
        p = host / skill / "scripts" / script
        if p.exists():
            return str(p)
    return None


def run(cmd):
    r = subprocess.run(cmd)
    sys.exit(r.returncode)


def cmd_ask(args):
    kb = args.kb or str(KB_ROOT or "")
    s = find_engine("fitness-kb", "kb_search.py")
    if s:
        run([sys.executable, s, *args.terms, "--kb", kb, "--max", str(args.max)]
            + (["--cards"] if args.cards else []))
    else:
        print("未找到 fitness-kb 引擎（kb_search.py）。请安装 fitness-kb Skill。", file=sys.stderr)
        sys.exit(2)


def cmd_quota(args):
    s = find_engine("diet-plan", "diet_plan.py")
    if not s:
        print("未找到 diet-plan 引擎（diet_plan.py）。请安装 diet-plan Skill。", file=sys.stderr)
        sys.exit(2)
    run([sys.executable, s, "--gender", args.gender, "--weight", str(args.weight),
         "--height", str(args.height), "--goal", args.goal, "--training", args.training])


def cmd_notes(args):
    if KB_ROOT is None:
        print("错误：未发现知识库（用 --kb 或 FITNESS_KB_ROOT 指定）", file=sys.stderr); sys.exit(2)
    units = KB_ROOT / "研究工程/02-内容单元库"
    if not units.is_dir():
        print(f"错误：研究层不存在 {units}", file=sys.stderr)
        sys.exit(2)
    kw = args.keyword
    hits = []
    for f in units.rglob("*.md"):
        text = f.read_text(encoding="utf-8", errors="replace")
        if kw in text:
            title = re.search(r"^title: (.+)$", text, re.M)
            hits.append((f.name, title.group(1).strip() if title else f.name))
    if not hits:
        print(f"研究层无「{kw}」命中单元。试试 ask 子命令检索原始文本层。")
        sys.exit(1)
    print(f"研究层命中 {len(hits)} 个单元（关键词：{kw}）：\n")
    for name, title in sorted(hits):
        print(f"  {name}  —  {title}")
    print(f"\n飞书课程笔记汇总：{SUMMARY_URL}")
    sys.exit(0)


import re  # noqa: E402  （notes 解析用）

def main():
    ap = argparse.ArgumentParser(prog="fc", description="fitness-coach 统一入口")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_ask = sub.add_parser("ask", help="知识检索（自动展开 ASR 变体）")
    p_ask.add_argument("terms", nargs="+")
    p_ask.add_argument("--kb")
    p_ask.add_argument("--cards", action="store_true")
    p_ask.add_argument("--max", type=int, default=6)
    p_q = sub.add_parser("quota", help="碳蛋脂配额计算")
    for flag in ("--gender", "--weight", "--height", "--goal", "--training"):
        p_q.add_argument(flag, required=True)
    p_n = sub.add_parser("notes", help="研究层单元检索")
    p_n.add_argument("keyword")
    args = ap.parse_args()
    if args.cmd == "ask":
        args.cards = getattr(args, "cards", False)
        cmd_ask(args)
    elif args.cmd == "quota":
        cmd_quota(args)
    elif args.cmd == "notes":
        cmd_notes(args)


if __name__ == "__main__":
    main()
