# -*- coding: utf-8 -*-
"""非线性算子：函数值平方 y=[f(x)]^2 与函数值倒数 y=1/f(x)（母曲线 f=x^2-2x）。

对应 hv-guide 第 1 章 §1.6「三级变换总表 · 非线性算子」与「倒数五铁律」。
"""
from manim import *

FONT_NAME = "Noto Sans Mono CJK SC"


class SquareAndReciprocal(Scene):
    def construct(self):
        title = Text(
            "非线性算子：函数值平方与函数值倒数",
            font=FONT_NAME,
            font_size=26,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(
            x_range=[-2.0, 4.2, 1],
            y_range=[-2.8, 4.2, 1],
            x_length=9.4,
            y_length=4.7,
            axis_config={"include_tip": True, "font_size": 18},
        ).shift(DOWN * 0.62)
        self.play(Create(axes))

        def f(x):
            return x ** 2 - 2 * x

        fc = axes.plot(f, x_range=[-1.2, 3.2], color=GREEN, stroke_width=5)
        flab = MathTex(r"f(x)=x^2-2x", font_size=26, color=GREEN).move_to(
            axes.c2p(0.9, 3.35)
        )
        z1 = Dot(axes.c2p(0, 0), radius=0.07, color=YELLOW)
        z2 = Dot(axes.c2p(2, 0), radius=0.07, color=YELLOW)
        vz = Dot(axes.c2p(1, -1), radius=0.08, color=YELLOW)
        vlab = MathTex(r"(1,-1)", font_size=24, color=YELLOW).next_to(vz, DOWN, buff=0.06)

        note0 = Text(
            "母曲线 f(x)=x^2-2x = x(x-2)：零点 0、2，极小值 -1",
            font=FONT_NAME,
            font_size=21,
        ).to_edge(DOWN, buff=0.25)
        self.play(Create(fc), Write(flab))
        self.play(FadeIn(z1), FadeIn(z2), FadeIn(vz), Write(vlab))
        self.play(Write(note0))
        self.wait(1.2)

        # ---------- 幕二：函数值平方 ----------
        note1 = Text(
            "平方算子：纵坐标 y 变为 y^2，负部翻折向上",
            font=FONT_NAME,
            font_size=21,
            color=ORANGE,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeOut(note0))
        self.play(Write(note1))

        f2 = axes.plot(
            lambda x: f(x) ** 2, x_range=[-0.72, 2.72], color=ORANGE, stroke_width=5
        )
        f2lab = MathTex(r"y=[f(x)]^2", font_size=26, color=ORANGE).move_to(
            axes.c2p(2.3, 3.45)
        )
        arrows = VGroup(
            *[
                Arrow(
                    axes.c2p(x, f(x)),
                    axes.c2p(x, f(x) ** 2),
                    buff=0.02,
                    color=YELLOW,
                    stroke_width=3,
                    tip_length=0.16,
                )
                for x in (-0.7, 0.6, 1.0, 1.5, 2.2)
            ]
        )
        vp2 = Dot(axes.c2p(1, 1), radius=0.08, color=ORANGE)
        vp2lab = MathTex(r"(1,1)", font_size=24, color=ORANGE).next_to(vp2, UP, buff=0.06)
        self.play(Create(f2), Write(f2lab))
        self.play(FadeIn(vp2), Write(vp2lab))
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25, run_time=2.2)
        )
        self.wait(0.8)

        key1 = Text(
            "负部翻折向上：零点 0、2 变为水平相切的偶重零点；(1,-1) 升到 (1,1) 成为极大值",
            font=FONT_NAME,
            font_size=20,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeOut(note1))
        self.play(Write(key1))
        self.wait(1.6)

        # ---------- 幕三：函数值倒数 ----------
        self.play(
            FadeOut(f2),
            FadeOut(f2lab),
            FadeOut(arrows),
            FadeOut(vz),
            FadeOut(vlab),
            FadeOut(vp2),
            FadeOut(vp2lab),
        )
        note2 = Text(
            "倒数算子：纵坐标 y 变为 1/y，零点撕成竖直渐近线",
            font=FONT_NAME,
            font_size=21,
            color=BLUE_B,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeOut(key1))
        self.play(Write(note2))

        r1 = axes.plot(lambda x: 1 / f(x), x_range=[-1.2, -0.35], color=BLUE_B, stroke_width=5)
        r2 = axes.plot(lambda x: 1 / f(x), x_range=[0.35, 1.65], color=BLUE_B, stroke_width=5)
        r3 = axes.plot(lambda x: 1 / f(x), x_range=[2.35, 3.2], color=BLUE_B, stroke_width=5)
        rg = VGroup(r1, r2, r3)
        asyms = VGroup(
            DashedLine(axes.c2p(0, -2.6), axes.c2p(0, 4.0), color=RED, stroke_width=3.5),
            DashedLine(axes.c2p(2, -2.6), axes.c2p(2, 4.0), color=RED, stroke_width=3.5),
        )
        alab1 = MathTex(r"x=0", font_size=24, color=RED).next_to(asyms[0], UP, buff=0.05)
        alab2 = MathTex(r"x=2", font_size=24, color=RED).next_to(asyms[1], UP, buff=0.05)
        rlab = MathTex(r"y=\frac{1}{f(x)}", font_size=26, color=BLUE_B).move_to(
            axes.c2p(-0.85, 2.75)
        )
        rdot = Dot(axes.c2p(1, -1), radius=0.08, color=YELLOW)
        rlab2 = MathTex(r"(1,-1)", font_size=24, color=YELLOW).next_to(rdot, LEFT, buff=0.12)

        self.play(Create(rg), Create(asyms), Write(alab1), Write(alab2))
        self.play(Write(rlab), FadeIn(rdot), Write(rlab2))
        self.wait(1.2)

        concl = VGroup(
            Text(
                "倒数五铁律：符号不变 · 零点撕裂 · 无穷变零 · 单调反转 · 极值互换",
                font=FONT_NAME,
                font_size=20,
            ),
            Text(
                "y = 1 与 y = -1 处纹丝不动（真正的不动点）",
                font=FONT_NAME,
                font_size=20,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.15)
        concl.to_edge(DOWN, buff=0.22)
        self.play(FadeOut(note2))
        self.play(FadeIn(concl))
        self.wait(2.6)
