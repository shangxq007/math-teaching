# -*- coding: utf-8 -*-
"""换基底与相似互换律：同一线性变换在不同基底下的矩阵满足 A' = P^{-1} A P。

例：标准基下 A = [[2,1],[0,1]]，v=(2,1) -> (5,1)。
新基 u1=(1,1), u2=(-1,1)（P = [[1,-1],[1,1]]）：
[v]_B' = (3/2, -1/2)，[T(v)]_B' = (3, -2)，A' = P^{-1}AP = [[2,0],[-1,1]]。
"""
from manim import *

FONT_NAME = "Noto Sans Mono CJK SC"


class ChangeBasisSimilarity(Scene):
    def construct(self):
        title = Text(
            "换基底与相似互换律：A' = P⁻¹ A P",
            font=FONT_NAME,
            font_size=25,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(
            x_range=[-2.5, 6.2, 1],
            y_range=[-2.6, 3.2, 1],
            x_length=10.2,
            y_length=4.9,
            axis_config={"include_tip": True, "font_size": 18},
        ).shift(UP * 0.15)
        self.play(Create(axes))

        e1 = np.array([1.0, 0.0])
        e2 = np.array([0.0, 1.0])
        v = np.array([2.0, 1.0])
        w = np.array([5.0, 1.0])  # T(v) = A v
        u1 = np.array([1.0, 1.0])
        u2 = np.array([-1.0, 1.0])

        # ---------- 幕一：标准基下的线性变换 ----------
        note0 = Text(
            "标准基下：T(v) = A v，其中 A = [[2,1],[0,1]]，v = (2,1)",
            font=FONT_NAME,
            font_size=20,
        ).to_edge(DOWN, buff=0.25)
        ar_e1 = Arrow(ORIGIN, axes.c2p(*e1), buff=0, color=GRAY, stroke_width=3)
        ar_e2 = Arrow(ORIGIN, axes.c2p(*e2), buff=0, color=GRAY, stroke_width=3)
        lab_e1 = MathTex(r"e_1", font_size=22, color=GRAY).next_to(ar_e1, DOWN, buff=0.05)
        lab_e2 = MathTex(r"e_2", font_size=22, color=GRAY).next_to(ar_e2, RIGHT, buff=0.05)
        ar_v = Arrow(ORIGIN, axes.c2p(*v), buff=0, color=TEAL, stroke_width=5)
        lab_v = MathTex(r"v=(2,1)", font_size=22, color=TEAL).next_to(
            axes.c2p(*v), LEFT, buff=0.08
        )
        ar_w = Arrow(ORIGIN, axes.c2p(*w), buff=0, color=PURPLE, stroke_width=5)
        lab_w = MathTex(r"T(v)=(5,1)", font_size=22, color=PURPLE).next_to(
            axes.c2p(*w), RIGHT, buff=0.08
        )
        mat_a = MathTex(
            r"A=\begin{pmatrix}2&1\\0&1\end{pmatrix}", font_size=26, color=YELLOW
        ).move_to(axes.c2p(-1.9, 2.7))
        self.play(Write(note0))
        self.play(Create(ar_e1), Create(ar_e2), Write(lab_e1), Write(lab_e2))
        self.play(Create(ar_v), Write(lab_v))
        self.play(Create(ar_w), Write(lab_w), Write(mat_a))
        self.wait(1.2)

        # ---------- 幕二：换上新基底，读出同一向量的坐标 ----------
        note1 = Text(
            "换基底 u1=(1,1), u2=(-1,1)：坐标系转动，图形一动不动，读数全变",
            font=FONT_NAME,
            font_size=20,
            color=ORANGE,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeOut(note0))
        self.play(Write(note1))

        ar_u1 = Arrow(ORIGIN, axes.c2p(*u1), buff=0, color=ORANGE, stroke_width=5)
        ar_u2 = Arrow(ORIGIN, axes.c2p(*u2), buff=0, color=ORANGE, stroke_width=5)
        lab_u1 = MathTex(r"u_1=(1,1)", font_size=22, color=ORANGE).next_to(
            axes.c2p(*u1), UP, buff=0.05
        )
        lab_u2 = MathTex(r"u_2=(-1,1)", font_size=22, color=ORANGE).next_to(
            axes.c2p(*u2), UP, buff=0.05
        )
        # v = (3/2) u1 - (1/2) u2 的分解辅助线
        p1 = 1.5 * u1
        d1 = DashedLine(axes.c2p(*p1), axes.c2p(*v), color=ORANGE, stroke_width=3)
        ar_p1 = Arrow(ORIGIN, axes.c2p(*p1), buff=0, color=ORANGE, stroke_width=3)
        self.play(Create(ar_u1), Create(ar_u2), Write(lab_u1), Write(lab_u2))
        self.play(Create(ar_p1), Create(d1))
        read_v = MathTex(
            r"[v]_{\mathcal{B}'}=\left(\tfrac{3}{2},-\tfrac{1}{2}\right)",
            font_size=24,
            color=ORANGE,
        ).move_to(axes.c2p(-1.9, 2.7))
        self.play(FadeTransform(mat_a, read_v))
        self.wait(1.2)

        # ---------- 幕三：T(v) 在新基下的读数与互换律 ----------
        note2 = Text(
            "像向量同步换尺子：[T(v)]_B' = (3,-2)，所用的矩阵不再是 A",
            font=FONT_NAME,
            font_size=20,
            color=PURPLE,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeOut(note1))
        self.play(Write(note2))

        q1 = 3.0 * u1
        d2 = DashedLine(axes.c2p(*q1), axes.c2p(*w), color=PURPLE, stroke_width=3)
        ar_q1 = Arrow(ORIGIN, axes.c2p(*q1), buff=0, color=PURPLE, stroke_width=3)
        read_w = MathTex(
            r"[T(v)]_{\mathcal{B}'}=(3,-2)", font_size=24, color=PURPLE
        ).move_to(axes.c2p(-1.9, 2.7))
        self.play(FadeTransform(read_v, read_w))
        self.play(Create(ar_q1), Create(d2))
        self.wait(0.8)

        rule = VGroup(
            MathTex(
                r"A'=P^{-1}AP=\begin{pmatrix}2&0\\-1&1\end{pmatrix}",
                font_size=25,
                color=YELLOW,
            ),
            Text(
                "同一个线性变换：换基底只是换读数（坐标），变换本身纹丝不动",
                font=FONT_NAME,
                font_size=19,
            ),
        ).arrange(DOWN, buff=0.15)
        rule.to_edge(DOWN, buff=0.18)
        self.play(FadeTransform(note2, rule))
        self.wait(2.4)
