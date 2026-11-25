"""第 0 章 · 逻辑演算与证明武器库 —— 场景 2：数学归纳法（多米诺骨牌）

叙事：N* 数轴 + 一排骨牌 → 条件 1∈S（奠基）、k∈S⇒k+1∈S（递推）
      → 骨牌依次倒下、S 逐步扩张覆盖整条数轴 → S=N*
      → 结论：归纳公理（有限步征服无穷）+ 最小反例原理。

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh -ql scene2_induction.py InductionDominoes
字体：中文统一 Noto Sans Mono CJK SC；数学一律 MathTex（原始字符串）。
"""

from manim import *

FONT_NAME = "Noto Sans Mono CJK SC"
BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"


class InductionDominoes(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ===================== 标题 =====================
        title1 = Text(
            "1. 摆好骨牌：给正整数排队",
            font=FONT_NAME, font_size=27, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=1.2)
        self.wait(0.5)

        # ===================== 第一幕：N* 数轴与一排骨牌 =====================
        line = NumberLine(
            x_range=[0.6, 7.6, 1],
            length=6.8,
            include_numbers=True,
            numbers_to_include=[1, 2, 3, 4, 5, 6],
            font_size=26,
            include_tip=True,
            color=WHITE,
            label_direction=DOWN,
        ).shift(DOWN * 1.5)
        ns_lab = MathTex(
            r"\mathbb{N}^*", font_size=26, color=GRAY,
        ).move_to((-3.75, -2.0, 0))
        dots_lab = MathTex(
            r"\cdots", font_size=30, color=GRAY,
        ).move_to(line.n2p(7.35) + UP * 0.28)

        self.play(Create(line), Write(line.numbers), run_time=1.3)
        self.play(Write(ns_lab), Write(dots_lab), run_time=0.7)

        def make_domino(i, ghost=False):
            d = RoundedRectangle(
                width=0.5, height=1.9, corner_radius=0.06,
                color=GRAY if ghost else PRIMARY,
                stroke_width=2 if ghost else 3,
                fill_color=GRAY if ghost else PRIMARY,
                fill_opacity=0.10 if ghost else 0.20,
            )
            d.move_to(line.n2p(i) + UP * 0.95)
            return d

        dominoes = [make_domino(i) for i in range(1, 7)]
        ghost = make_domino(7, ghost=True)

        self.play(
            LaggedStart(*[FadeIn(d) for d in dominoes], lag_ratio=0.35),
            run_time=1.8,
        )
        self.play(FadeIn(ghost), run_time=0.5)
        self.wait(1.0)

        # ===================== 第二幕：奠基 与 递推 =====================
        title2 = Text(
            "2. 两个条件：奠基 与 递推",
            font=FONT_NAME, font_size=27, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=0.8)

        cond_y = line.n2p(1)[1] + 2.75  # 条件标注的高度（数轴上方）

        self.play(
            dominoes[0].animate.set_color(SECONDARY).set_fill(SECONDARY, 0.35),
            run_time=0.8,
        )
        base_lab = MathTex(
            r"1\in S", font_size=30, color=SECONDARY,
        ).move_to((line.n2p(1)[0], cond_y, 0))
        base_cn = Text(
            "奠基", font=FONT_NAME, font_size=20, color=GRAY,
        ).next_to(base_lab, DOWN, buff=0.12)
        self.play(Write(base_lab), Write(base_cn), run_time=0.9)

        arr = Arrow(
            line.n2p(2) + UP * 2.75, line.n2p(3) + UP * 2.75,
            buff=0.25, color=ACCENT, stroke_width=3,
        )
        step_lab = MathTex(
            r"k\in S\ \Rightarrow\ k+1\in S", font_size=28, color=ACCENT,
        ).move_to((line.n2p(2.5)[0], cond_y + 0.8, 0))
        step_cn = Text(
            "递推", font=FONT_NAME, font_size=20, color=GRAY,
        ).next_to(step_lab, DOWN, buff=0.12)
        self.play(Create(arr), Write(step_lab), Write(step_cn), run_time=1.0)
        self.wait(1.4)

        # ===================== 第三幕：依次倒下，S 覆盖数轴 =====================
        title3 = Text(
            "3. 依次倒下：S 覆盖整条数轴",
            font=FONT_NAME, font_size=27, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title2, title3), run_time=0.8)

        cap = Text(
            "每倒一张，S 就向右扩张一格",
            font=FONT_NAME, font_size=20, color=GRAY,
        ).move_to((0, -2.6, 0))
        self.play(Write(cap), run_time=0.7)

        # S 的扩张条：从 1 开始向右生长
        bar_left = line.n2p(1)[0]
        bar = Rectangle(
            width=0.02, height=0.16,
            fill_color=SECONDARY, fill_opacity=0.95, stroke_width=0,
        ).move_to((bar_left + 0.01, -2.05, 0))
        self.play(FadeIn(bar), run_time=0.4)

        for idx, d in enumerate(dominoes):
            pivot = d.get_bottom() + RIGHT * 0.25
            w = line.n2p(idx + 2)[0] - bar_left
            self.play(
                d.animate.rotate(-PI / 2, about_point=pivot),
                bar.animate.stretch_to_fit_width(w, about_edge=LEFT),
                run_time=0.55,
            )
            self.wait(0.15)

        w_end = line.n2p(7.6)[0] - bar_left
        self.play(
            bar.animate.stretch_to_fit_width(w_end, about_edge=LEFT),
            run_time=1.0,
        )
        s_full = MathTex(
            r"S=\mathbb{N}^*", font_size=32, color=ACCENT,
        ).move_to((3.0, 2.5, 0))
        self.play(Write(s_full), run_time=1.0)
        self.wait(1.6)

        # ===================== 第四幕：结论 =====================
        title4 = Text(
            "4. 结论：有限步征服无穷",
            font=FONT_NAME, font_size=27, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(
            ReplacementTransform(title3, title4),
            FadeOut(cap), FadeOut(base_lab), FadeOut(base_cn),
            FadeOut(arr), FadeOut(step_lab), FadeOut(step_cn),
            run_time=0.9,
        )
        self.play(
            *[d.animate.set_fill(opacity=0.06).set_stroke(opacity=0.25)
              for d in dominoes],
            ghost.animate.set_fill(opacity=0.04).set_stroke(opacity=0.15),
            run_time=0.8,
        )

        concl1 = Text(
            "数学归纳法 = 皮亚诺归纳公理",
            font=FONT_NAME, font_size=24, color=PRIMARY,
        ).move_to((0, -2.55, 0))
        concl2 = Text(
            "有限步征服无穷",
            font=FONT_NAME, font_size=22, color=ACCENT,
        ).move_to((0, -2.95, 0))
        min_cn = Text(
            "最小反例原理：若中途断了，设最小断点为 k",
            font=FONT_NAME, font_size=20, color=GRAY,
        ).move_to((0, -3.35, 0))
        min_math = MathTex(
            r"k-1\in S\ \Rightarrow\ k\in S", font_size=24, color=RED,
        ).move_to((-0.55, -3.72, 0))
        min_cn2 = Text(
            "矛盾", font=FONT_NAME, font_size=20, color=RED,
        ).next_to(min_math, RIGHT, buff=0.3)

        self.play(Write(concl1), Write(concl2), run_time=1.2)
        self.play(Write(min_cn), Write(min_math), Write(min_cn2), run_time=1.2)
        self.wait(2.8)
