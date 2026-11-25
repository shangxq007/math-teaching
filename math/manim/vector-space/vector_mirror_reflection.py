# -*- coding: utf-8 -*-
"""向量的镜面反射：以 b 所在直线为镜面，a 的反射像 a' = 2 proj_b a - a。

例：a=(2.5,1.5)，b=(3,1)，proj_b a = (2.7,0.9)，a' = (2.9,0.3)。
"""
from manim import *

FONT_NAME = "Noto Sans Mono CJK SC"


class VectorMirrorReflection(Scene):
    def construct(self):
        title = Text(
            "向量镜面反射：a 关于 b 所在直线的对称向量",
            font=FONT_NAME,
            font_size=25,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(
            x_range=[-1.0, 6.0, 1],
            y_range=[-1.2, 3.4, 1],
            x_length=10.0,
            y_length=4.8,
            axis_config={"include_tip": True, "font_size": 18},
        ).shift(UP * 0.15)
        self.play(Create(axes))

        a = np.array([2.5, 1.5])
        b = np.array([3.0, 1.0])
        t = float(np.dot(a, b) / np.dot(b, b))
        foot = t * b
        ap = 2 * foot - a

        # 镜面所在的直线（虚线双向延长）
        line = DashedLine(axes.c2p(-1.5 * b[0], -1.5 * b[1]), axes.c2p(2.6 * b[0], 2.6 * b[1]),
                          color=ORANGE, stroke_width=3)
        ar_b = Arrow(ORIGIN, axes.c2p(*b), buff=0, color=ORANGE, stroke_width=5)
        lab_b = MathTex(r"b=(3,1)", font_size=22, color=ORANGE).next_to(
            axes.c2p(*b), RIGHT, buff=0.06
        )
        note0 = Text(
            "镜面是 b 所在的整条直线，而不只是向量 b",
            font=FONT_NAME,
            font_size=20,
            color=ORANGE,
        ).to_edge(DOWN, buff=0.25)
        self.play(Create(line), Create(ar_b), Write(lab_b), Write(note0))
        self.wait(1.0)

        # 原向量与投影
        ar_a = Arrow(ORIGIN, axes.c2p(*a), buff=0, color=TEAL, stroke_width=5)
        lab_a = MathTex(r"a=(2.5,1.5)", font_size=22, color=TEAL).next_to(
            axes.c2p(*a), LEFT, buff=0.08
        )
        foot_dot = Dot(axes.c2p(*foot), radius=0.08, color=RED)
        ar_proj = Arrow(ORIGIN, axes.c2p(*foot), buff=0, color=RED, stroke_width=5)
        lab_proj = MathTex(
            r"\mathrm{proj}_b a=\frac{a\cdot b}{b\cdot b}\,b=(2.7,0.9)",
            font_size=22,
            color=RED,
        ).move_to(axes.c2p(0.4, -1.1))
        note1 = Text(
            "先投影：从 a 的终点向镜面作垂线，垂足即 proj_b a",
            font=FONT_NAME,
            font_size=20,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeOut(note0))
        self.play(Write(note1))
        self.play(Create(ar_a), Write(lab_a))
        self.play(Create(ar_proj), FadeIn(foot_dot), Write(lab_proj))
        self.wait(1.2)

        # 反射像
        ar_ap = Arrow(ORIGIN, axes.c2p(*ap), buff=0, color=PURPLE, stroke_width=5)
        lab_ap = MathTex(r"a'=(2.9,0.3)", font_size=22, color=PURPLE).next_to(
            axes.c2p(*ap), RIGHT, buff=0.08
        )
        path = DashedLine(axes.c2p(*a), axes.c2p(*foot), color=WHITE, stroke_width=3)
        path2 = DashedLine(axes.c2p(*foot), axes.c2p(*ap), color=WHITE, stroke_width=3)
        rule = VGroup(
            MathTex(r"a'=2\,\mathrm{proj}_b a-a", font_size=26, color=YELLOW),
            Text(
                "镜面是 a 与 a' 连线的垂直平分线；proj_b a 恰好是中点",
                font=FONT_NAME,
                font_size=19,
            ),
        ).arrange(DOWN, buff=0.15)
        rule.to_edge(DOWN, buff=0.18)
        note2 = Text(
            "再镜像：越过镜面走同样远，a' = 2 proj_b a - a",
            font=FONT_NAME,
            font_size=20,
            color=PURPLE,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeOut(note1))
        self.play(Write(note2))
        self.play(Create(path), Create(path2))
        self.play(Create(ar_ap), Write(lab_ap))
        self.wait(1.0)
        self.play(FadeTransform(note2, rule))
        self.wait(2.4)
