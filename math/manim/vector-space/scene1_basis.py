"""第 3 章 · 平面向量与空间向量 —— 场景 1：平面向量基本定理（基底分解）

叙事：坐标平面内画出一组斜交基底 e1（青）、e2（橙）
      → 任取向量 a（黄）
      → 从 a 的端点作两条与基底平行的虚线，把 a「拉开」成平行四边形
      → 高亮两个分量 x·e1（青）与 y·e2（橙）
      → 定格 a = x·e1 + y·e2；右栏写基本定理；底部写「基底选得巧，计算就少」

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene1_basis.py BasisDecomposition
字体：中文统一 Noto Sans Mono CJK SC；数学一律 MathTex（原始字符串）。
"""

from manim import *
import numpy as np

FONT_NAME = "Noto Sans Mono CJK SC"
BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"
RED_H = "#FF5252"


class BasisDecomposition(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ======================================================
        # 第一幕：斜交基底 e1、e2 与任意向量 a
        # ======================================================
        title1 = Text(
            "1. 斜交基底：把向量「拉开」",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=1.2)
        self.wait(0.6)

        axes = Axes(
            x_range=[-1.6, 1.6, 1],
            y_range=[-1.6, 1.6, 1],
            x_length=5.0,
            y_length=5.0,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "color": WHITE,
                "stroke_width": 2,
            },
        ).shift(LEFT * 3.3 + DOWN * 0.3)
        origin = axes.c2p(0, 0)
        unit = axes.c2p(1, 0)[0] - origin[0]

        def cpt(x, y):
            """数据坐标 → 场景坐标"""
            return origin + unit * (x * RIGHT + y * UP)

        # 斜交基底与待分解的向量（数据坐标）
        e1 = np.array([1.0, 0.32])
        e2 = np.array([-0.32, 1.0])
        x_coef, y_coef = 1.5, 0.95
        P1 = x_coef * e1            # x·e1 的端点
        Q = y_coef * e2             # y·e2 的端点
        P2 = P1 + Q                 # a 的端点

        e1_arrow = Arrow(origin, cpt(*e1), buff=0, color=PRIMARY, stroke_width=5)
        e2_arrow = Arrow(origin, cpt(*e2), buff=0, color=ORANGE, stroke_width=5)
        e1_lab = MathTex(r"\vec e_1", font_size=24, color=PRIMARY)
        e1_lab.move_to(cpt(0.45, 0.14) + UP * 0.36)
        e2_lab = MathTex(r"\vec e_2", font_size=24, color=ORANGE)
        e2_lab.move_to(cpt(-0.14, 0.45) + LEFT * 0.60)

        self.play(Create(axes), run_time=1.2)
        self.play(Create(e1_arrow), Create(e2_arrow), run_time=1.2)
        self.play(Write(e1_lab), Write(e2_lab), run_time=0.9)
        self.wait(1.6)

        a_arrow = Arrow(origin, cpt(*P2), buff=0, color=ACCENT, stroke_width=6)
        a_dot = Dot(cpt(*P2), radius=0.055, color=ACCENT)
        a_lab = MathTex(r"\vec a", font_size=26, color=ACCENT)
        a_lab.move_to(cpt(*P2) + UP * 0.32)

        self.play(Create(a_arrow), FadeIn(a_dot), run_time=1.1)
        self.play(Write(a_lab), run_time=0.7)
        self.wait(2.2)

        # ======================================================
        # 第二幕：沿基底方向拉开成平行四边形
        # ======================================================
        title2 = Text(
            "2. 沿基底方向「拉开」：平行四边形",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=1.0)

        para_fill = Polygon(
            origin, cpt(*P1), cpt(*P2), cpt(*Q),
            color=PRIMARY, fill_opacity=0.10, stroke_opacity=0,
        )
        dash1 = DashedLine(cpt(*P2), cpt(*P1), color=GRAY, stroke_width=2)
        dash2 = DashedLine(cpt(*P2), cpt(*Q), color=GRAY, stroke_width=2)
        foot1 = Dot(cpt(*P1), radius=0.05, color=WHITE)
        foot2 = Dot(cpt(*Q), radius=0.05, color=WHITE)

        self.play(Create(dash1), Create(dash2), run_time=1.2)
        self.play(FadeIn(foot1), FadeIn(foot2), run_time=0.6)
        self.wait(1.4)

        comp1 = Arrow(origin, cpt(*P1), buff=0, color=PRIMARY, stroke_width=10)
        comp1_lab = MathTex(r"x\vec e_1", font_size=24, color=PRIMARY)
        comp1_lab.move_to(cpt(0.75, 0.24) + DOWN * 0.45)

        self.play(Create(comp1), run_time=1.1)
        self.play(Write(comp1_lab), run_time=0.8)
        self.wait(0.8)

        comp2 = Arrow(cpt(*P1), cpt(*P2), buff=0, color=ORANGE, stroke_width=10)
        comp2_lab = MathTex(r"y\vec e_2", font_size=24, color=ORANGE)
        comp2_lab.move_to(cpt(1.35, 0.96) + RIGHT * 0.80)

        self.play(Create(comp2), run_time=1.1)
        self.play(Write(comp2_lab), run_time=0.8)
        self.wait(0.6)
        self.play(FadeIn(para_fill), run_time=0.9)
        self.wait(2.2)

        # ======================================================
        # 第三幕：定格基本定理
        # ======================================================
        title3 = Text(
            "3. 定格：平面向量基本定理",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title2, title3), run_time=1.0)

        eq = MathTex(
            r"\vec a=x\vec e_1+y\vec e_2", font_size=32, color=ACCENT,
        )
        line2 = Text(
            "平面内任一向量都可唯一分解",
            font=FONT_NAME, font_size=22, color=WHITE,
        )
        line3 = Text(
            "基底：不共线的一组向量",
            font=FONT_NAME, font_size=22, color=SECONDARY,
        )
        panel = VGroup(eq, line2, line3).arrange(DOWN, buff=0.38)
        panel.move_to((3.05, 1.35, 0))

        self.play(Write(eq), run_time=1.5)
        self.play(Write(line2), run_time=1.1)
        self.play(Write(line3), run_time=1.1)
        self.wait(1.2)

        caption = Text(
            "基底选得巧，计算就少",
            font=FONT_NAME, font_size=26, color=ACCENT,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(caption), run_time=1.3)
        self.wait(5.0)
