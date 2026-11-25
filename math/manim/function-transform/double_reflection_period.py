# -*- coding: utf-8 -*-
"""双镜像反射生成周期平移：连续两次平行镜像反射 = 一次刚体平移 T = 2(b-a)。"""
from manim import *
import numpy as np

FONT_NAME = "Noto Sans Mono CJK SC"


def reflect(mob, a):
    """把 mobject 关于竖直直线 x = a 作真实镜像（仅几何形状，文字请另行添加）。"""
    return mob.copy().apply_function(
        lambda p: np.array([2 * a - p[0], p[1], p[2]], dtype=float)
    )


class DoubleReflectionToPeriod(Scene):
    def construct(self):
        A, B = 1.0, 3.5
        d = B - A

        title = Text(
            "抽象函数周期之源：连续两次镜像反射 = 刚体平移",
            font=FONT_NAME,
            font_size=26,
        ).to_edge(UP, buff=0.35)
        self.play(Write(title))

        axes = Axes(
            x_range=[-2, 8, 1],
            y_range=[-1.6, 3.6, 1],
            x_length=9.6,
            y_length=4.4,
            axis_config={"include_tip": True, "font_size": 18},
        ).shift(DOWN * 0.55)
        self.play(Create(axes))

        mirror1 = DashedLine(
            axes.c2p(A, -1.4), axes.c2p(A, 3.4),
            color=BLUE, stroke_width=3.5,
        )
        mirror2 = DashedLine(
            axes.c2p(B, -1.4), axes.c2p(B, 3.4),
            color=ORANGE, stroke_width=3.5,
        )
        lab1 = MathTex(r"x=a", font_size=26, color=BLUE).next_to(mirror1, UP, buff=0.12)
        lab2 = MathTex(r"x=b", font_size=26, color=ORANGE).next_to(mirror2, UP, buff=0.12)

        brace = BraceBetweenPoints(
            axes.c2p(A, -1.25), axes.c2p(B, -1.25), direction=DOWN, color=GREY_BROWN
        )
        blab = MathTex(r"d=b-a", font_size=24, color=GREY_BROWN).next_to(brace, DOWN, buff=0.1)
        self.play(Create(mirror1), Create(mirror2), Write(lab1), Write(lab2))
        self.play(Create(brace), Write(blab))
        self.wait(0.6)

        def f(x):
            return 1.5 * np.exp(-3 * (x + 0.1) ** 2) + 0.6 * x + 0.8

        wave0 = axes.plot(f, x_range=[-0.7, 0.7], color=GREEN, stroke_width=5)
        dot0 = Dot(axes.c2p(0, f(0)), radius=0.08, color=YELLOW)
        tag0 = MathTex(r"P(x)", font_size=24, color=YELLOW).next_to(dot0, UL, buff=0.12)
        shape0 = VGroup(wave0, dot0)

        note1 = Text(
            "第 1 次反射：关于 x = a 轴对称（左右朝向反转）",
            font=FONT_NAME, font_size=22, color=BLUE,
        ).to_edge(DOWN, buff=0.25)

        self.play(Create(wave0), FadeIn(dot0), Write(tag0))
        self.wait(0.7)
        self.play(Write(note1))

        # 幕一：关于 x = A 反射
        shape1 = reflect(shape0, A)
        gA = shape0.copy()
        tag1 = MathTex(r"P_1(2a-x)", font_size=24, color=BLUE_B).next_to(
            axes.c2p(2 * A, f(0)), UR, buff=0.12
        )
        self.play(Transform(gA, shape1), run_time=1.5)
        self.play(Write(tag1))
        self.wait(0.7)

        # 幕二：关于 x = B 再反射一次
        note2 = Text(
            "第 2 次反射：关于 x = b 轴对称（再次反转，朝向复原）",
            font=FONT_NAME, font_size=22, color=ORANGE,
        ).to_edge(DOWN, buff=0.25)
        self.play(ReplacementTransform(note1, note2))

        shape2 = reflect(shape1, B)
        gB = gA.copy()
        tag2 = MathTex(r"P_2\bigl(x+2(b-a)\bigr)", font_size=24, color=GREEN).next_to(
            axes.c2p(2 * B - 2 * A, f(0)), UR, buff=0.12
        )
        self.play(Transform(gB, shape2), run_time=1.5)
        self.play(Write(tag2))
        self.wait(0.8)

        # 收尾：初态与末态的纯粹平移关系
        arrow = Arrow(
            dot0.get_center(), axes.c2p(2 * B - 2 * A, f(0)),
            buff=0.12, color=RED, stroke_width=4,
        )
        concl = VGroup(
            MathTex(r"T=2|b-a|", font_size=30, color=RED),
            Text("朝向复原，只剩平移：周期出现", font=FONT_NAME, font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.2)
        concl.to_corner(UR, buff=0.5)
        self.play(GrowArrow(arrow))
        self.play(FadeIn(concl))
        self.wait(2.2)
