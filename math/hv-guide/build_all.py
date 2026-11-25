#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四合一多版本一键编译（hv-guide）

用法：
    python3 build_all.py            # 编译四种版本，产物在 dist/
    python3 build_all.py --demo     # 额外编译一份挂载示范章节的「完整教师版」
    python3 build_all.py --only student_basic

原理：为每种版本生成一个极薄的包装 .tex（内容仅为导言区 + 两行开关），
再 \\input{main_body}，因此源文件只有一份，永远不会有副本漂移。
手动改版本：直接编辑 main.tex 顶部「版本切换面板」的两行，然后 latexmk -xelatex main。
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

WRAPPER_HEAD = """% 本文件由 build_all.py 自动生成，请勿手工编辑
\\documentclass[cn,11pt,color=cyan,math=newtx,normal]{elegantnote}

\\input{../common/preamble}
\\input{../common/macros}
\\input{../common/envs}
\\usetikzlibrary{decorations.pathmorphing}
\\input{versions}

"""

WRAPPER_TAIL = "\n\\input{main_body}\n"

DEMO_LINE_OFF = r"\demomodefalse"   # 关闭示范章节
DEMO_LINE_ON = r"\demomodetrue"    # 开启示范章节

# (目录名, 教师开关, 基础开关, 中文副标题)
MODES = [
    ("01_teacher_full",  r"\teachertrue",  r"\basicfalse", "① 完整教师版"),
    ("02_student_full",  r"\teacherfalse", r"\basicfalse", "② 完整学生版"),
    ("03_teacher_basic", r"\teachertrue",  r"\basictrue",  "③ 薄弱生教师版"),
    ("04_student_basic", r"\teacherfalse", r"\basictrue",  "④ 薄弱生学生版"),
]


def build(name: str, teacher: str, basic: str, demo: bool) -> tuple[int, str, int, int]:
    """编译一个版本，返回 (exit_code, 日志路径, 页数)。"""
    tag = f"{name}_demo" if demo else name
    wrapper = ROOT / f"_variant_{tag}.tex"
    wrapper.write_text(
        WRAPPER_HEAD + teacher + "\n" + basic + "\n"
        + (DEMO_LINE_ON if demo else DEMO_LINE_OFF) + "\n" + WRAPPER_TAIL,
        encoding="utf-8",
    )
    jobname = f"hvguide_{tag}"
    cmd = ["latexmk", "-xelatex", "-g", f"-jobname={jobname}", wrapper.name]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)

    log_path = ROOT / f"{jobname}.log"
    errors = 0
    if log_path.exists():
        errors = sum(1 for ln in log_path.read_text(errors="ignore").splitlines()
                     if ln.startswith("!"))

    pages = -1
    try:
        out = subprocess.run(["pdfinfo", str(ROOT / f"{jobname}.pdf")],
                             capture_output=True, text=True).stdout
        for ln in out.splitlines():
            if ln.startswith("Pages:"):
                pages = int(ln.split()[-1])
                break
    except Exception:
        pass

    return proc.returncode, str(log_path), errors, pages


def main() -> None:
    args = [a for a in sys.argv[1:]]
    demo = "--demo" in args
    only = None
    for a in args:
        if a.startswith("--only"):
            only = a.split("=", 1)[-1] if "=" in a else a

    jobs = list(MODES)
    if demo:
        jobs.append(("05_demo_teacher_full", r"\teachertrue", r"\basicfalse",
                     "示范章节 · 完整教师版"))
    if only:
        jobs = [j for j in jobs if only in j[0]]

    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)

    print(f"{'版本':<24}{'EXIT':>6}{'error':>7}{'页数':>7}  产物")
    print("-" * 72)
    failures = []
    for name, teacher, basic, label in jobs:
        rc, log, errors, pages = build(name, teacher, basic, demo=("demo" in name))
        tag = f"{name}_demo" if "demo" in name else name
        src = ROOT / f"hvguide_{tag}.pdf"
        dst = dist / f"{label.replace(' ', '_')}.pdf"
        if src.exists():
            shutil.copy2(src, dst)
        print(f"{label:<22}{rc:>6}{errors:>7}{pages:>7}  {dst.name}")
        if rc != 0 or errors:
            failures.append((label, log))

    print("-" * 72)
    if failures:
        print("存在失败/报错的版本：")
        for label, log in failures:
            print(f"  - {label}：{log}")
        sys.exit(1)
    print("全部版本编译通过（0 error）。产物目录：hv-guide/dist/")


if __name__ == "__main__":
    main()
