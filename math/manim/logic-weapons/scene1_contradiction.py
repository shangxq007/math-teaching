"""第 0 章 · 逻辑演算与证明武器库 —— 场景 1：反证法（集合包含版）

叙事：要证 A⊆B → 反设 ∃x∈A 且 x∉B（红块 A∩∁_U B + 红点 x）
      → 由条件与 B 的定义推出 P(x)∧¬P(x) ⇒ 0=1（矛盾）
      → 红块收缩、变色、消失 → 结论 A⊆B ⟺ A∩∁_U B=∅（正难则反）。

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh -ql scene1_contradiction.py ProofByContradictionSets
字体：中文统一 Noto Sans Mono CJK SC；数学一律 MathTex（原始字符串）。
"""

from manim import *

FONT_NAME = "Noto Sans Mono CJK SC"
BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"


class ProofByContradictionSets(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ===================== 标题 =====================
        title1 = Text(
            "1. 反证法：要证 A 包含于 B，先假设它不成立",
            font=FONT_NAME, font_size=27, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=1.2)
        self.wait(0.6)

        # ===================== 第一幕：全集 U、集合 B、集合 A =====================
        u_box = RoundedRectangle(
            width=9.6, height=4.6, corner_radius=0.25,
            color=GRAY, stroke_width=3,
        ).shift(DOWN * 0.05)
        u_label = MathTex("U", font_size=34, color=GRAY).move_to(
            u_box.get_corner(UL) + RIGHT * 0.45 + DOWN * 0.35
        )

        b_circ = Circle(
            radius=2.15, color=SECONDARY, stroke_width=4,
            fill_color=BG, fill_opacity=1.0,
        ).shift(LEFT * 0.8 + DOWN * 0.05)
        b_label = MathTex("B", font_size=36, color=SECONDARY).move_to(
            b_circ.get_center() + LEFT * 1.15 + DOWN * 1.35
        )

        a_circ = Circle(
            radius=1.4, color=PRIMARY, stroke_width=4,
            fill_color=PRIMARY, fill_opacity=0.18,
        ).shift(RIGHT * 0.95 + UP * 0.10)
        a_label = MathTex("A", font_size=36, color=PRIMARY).move_to(
            a_circ.get_center() + RIGHT * 1.05 + DOWN * 0.30
        )

        # 红块：A 的复制品（先透明）。B 的不透明填充会盖住 A∩B，只露出 A\B 新月形。
        a_red = a_circ.copy().set_fill(RED, 0.0).set_stroke(opacity=0)

        self.play(Create(u_box), Write(u_label), run_time=1.0)
        self.play(Create(a_circ), Write(a_label), run_time=1.0)
        self.add(a_red)
        self.play(Create(b_circ), Write(b_label), run_time=1.0)
        self.wait(1.4)

        # ===================== 第二幕：反设 ∃x∈A 且 x∉B =====================
        title2 = Text(
            "2. 反设：存在 x 在 A 中，却不在 B 中",
            font=FONT_NAME, font_size=27, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=0.8)

        dot = Dot(point=(1.95, 0.45, 0), radius=0.10, color=RED)
        x_lab = MathTex("x", font_size=34, color=WHITE).next_to(dot, UP, buff=0.12)
        assume = Text(
            "反设：存在 x 属于 A，但不属于 B",
            font=FONT_NAME, font_size=24, color=ACCENT,
        ).move_to((0, -3.05, 0))

        self.play(a_red.animate.set_fill(opacity=0.55), run_time=0.9)
        self.play(FadeIn(dot), Write(x_lab), run_time=0.7)
        self.play(Write(assume), run_time=1.0)
        self.wait(2.0)

        # ===================== 第三幕：推出矛盾，红块收缩消失 =====================
        title3 = Text(
            "3. 推出矛盾：假设的那块正在收缩",
            font=FONT_NAME, font_size=27, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title2, title3), FadeOut(assume), run_time=0.8)

        caption = Text(
            "由已知条件与 B 的定义，逐步推出矛盾：",
            font=FONT_NAME, font_size=20, color=GRAY,
        ).move_to((0, -2.55, 0))
        l1 = MathTex(
            r"x\in A\ \Rightarrow\ P(x)", font_size=25, color=WHITE,
        ).move_to((0, -2.95, 0))
        l2 = MathTex(
            r"x\notin B\ \Leftrightarrow\ \neg P(x)", font_size=25, color=WHITE,
        ).move_to((0, -3.33, 0))
        l3 = MathTex(
            r"P(x)\wedge\neg P(x)\ \Rightarrow\ 0=1", font_size=25, color=RED,
        ).move_to((0, -3.71, 0))
        contra = Text(
            "矛盾！", font=FONT_NAME, font_size=22, color=RED,
        ).next_to(l3, RIGHT, buff=0.3)

        self.play(Write(caption), run_time=0.8)
        self.play(Write(l1), run_time=0.7)
        self.wait(0.5)
        self.play(Write(l2), run_time=0.7)
        self.wait(0.5)
        self.play(Write(l3), Write(contra), run_time=0.9)
        self.wait(0.8)

        # A（连同红块与 x）被矛盾挤进 B：新月形逐渐收缩、变色、消失
        group_a = VGroup(a_circ, a_label)
        self.play(
            group_a.animate.move_to(b_circ.get_center()),
            a_red.animate.move_to(b_circ.get_center()).set_fill(GRAY, 0.35),
            dot.animate.move_to(
                b_circ.get_center() + RIGHT * 1.0 + UP * 0.30
            ).set_opacity(0).scale(0.3),
            x_lab.animate.move_to(
                b_circ.get_center() + RIGHT * 1.0 + UP * 0.55
            ).set_opacity(0),
            run_time=2.8,
        )
        self.play(FadeOut(a_red), run_time=0.6)

        empty_label = MathTex(
            r"A\cap\complement_U B=\emptyset", font_size=26, color=SECONDARY,
        ).move_to((2.6, 0.9, 0))
        self.play(Write(empty_label), run_time=0.9)
        self.wait(1.6)

        # ===================== 第四幕：结论 =====================
        title4 = Text(
            "4. 结论：正难则反",
            font=FONT_NAME, font_size=27, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title3, title4), run_time=0.8)
        self.play(
            FadeOut(caption), FadeOut(l1), FadeOut(l2), FadeOut(l3),
            FadeOut(contra), FadeOut(empty_label),
            run_time=0.7,
        )
        # 揭开 B 的遮盖：A 已完全落入 B 内
        self.play(b_circ.animate.set_fill(opacity=0.0), run_time=1.0)

        concl_cn = Text(
            "要证 A 包含于 B，只需证 A 与 B 的补集不相交",
            font=FONT_NAME, font_size=23, color=PRIMARY,
        ).move_to((0, -2.75, 0))
        concl_math = MathTex(
            r"A\subseteq B\ \iff\ A\cap\complement_U B=\emptyset",
            font_size=28, color=WHITE,
        ).move_to((0, -3.2, 0))
        zhengnan = Text(
            "正难则反", font=FONT_NAME, font_size=30, color=ACCENT,
        ).move_to((0, -3.65, 0))

        self.play(Write(concl_cn), Write(concl_math), run_time=1.4)
        self.play(Write(zhengnan), run_time=0.8)
        self.wait(3.5)
