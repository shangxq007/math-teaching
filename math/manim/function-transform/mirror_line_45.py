# -*- coding: utf-8 -*-
"""45° 镜面反射定律：y=x+b 的坐标互换规律 + 指对同构交点秒杀。

第一幕：对称轴 y=x 与平移后的 y=x+1，展示 (x,y) -> (y-b, x+b) 的干净互换。
第二幕：y=e^x 与 y=ln x 关于 y=x 对称，被斜率 -1 的直线 x+y=4 所截，
        两交点关于 y=x 对称 => x1 + x2 = 4（无需解超越方程）。
"""
from manim import *
import numpy as np

FONT_NAME = "Noto Sans Mono CJK SC"


class MirrorLine45Symmetry(Scene):
    def construct(self):
        title = Text(
            "45° 镜面反射定律：对称轴 y = ±x + b",
            font=FONT_NAME,
            font_size=25,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # ==========================================================
        # 第一幕：y = x 与 y = x + b 的坐标互换本质
        # ==========================================================
        axes1 = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            x_length=8.6,
            y_length=5.4,
            axis_config={"include_tip": True, "font_size": 18},
        ).shift(DOWN * 0.55 + LEFT * 0.5)

        line_yx = axes1.plot(lambda x: x, x_range=[-1, 4.2], color=BLUE, stroke_width=3.5)
        lab_yx = MathTex(r"y=x", font_size=24, color=BLUE).next_to(
            axes1.c2p(4.0, 4.0), UP, buff=0.12
        )

        note1 = Text(
            "第一幕：关于 y = x 对称 = 横纵坐标直接互换",
            font=FONT_NAME,
            font_size=20,
            color=GRAY,
        ).next_to(title, DOWN, aligned_edge=RIGHT, buff=0.06)

        self.play(Create(axes1), Create(line_yx), Write(lab_yx), Write(note1))
        self.wait(0.5)

        # 点 P(1,3) -> P'(3,1)：沿垂直于 y=x 的方向翻转
        P = axes1.c2p(1, 3)
        Pp = axes1.c2p(3, 1)
        seg = DashedLine(P, Pp, color=YELLOW, stroke_width=3)
        dotP = Dot(P, radius=0.09, color=YELLOW)
        dotPp = Dot(Pp, radius=0.09, color=ORANGE)
        tagP = MathTex("P(1,3)", font_size=22, color=YELLOW).next_to(dotP, UL, buff=0.12)
        tagPp = MathTex("P'(3,1)", font_size=22, color=ORANGE).next_to(dotPp, DR, buff=0.12)
        map1 = MathTex(r"(x,y)\mapsto(y,x)", font_size=26, color=YELLOW).to_edge(
            DOWN, buff=0.3
        )
        mid1 = Dot(axes1.c2p(2, 2), radius=0.06, color=WHITE)
        tagMid1 = MathTex("M(2,2)", font_size=20, color=WHITE).next_to(mid1, UR, buff=0.1)

        self.play(Create(seg), FadeIn(dotP), Write(tagP))
        self.wait(0.4)
        self.play(
            dotP.animate.move_to(Pp),
            Transform(tagP, MathTex("P'(3,1)", font_size=22, color=YELLOW).next_to(dotPp, DR, buff=0.12)),
            run_time=1.4,
        )
        self.play(FadeIn(dotPp), FadeIn(mid1), Write(tagMid1), Write(map1))
        self.wait(1.0)

        # 镜面平移为 y = x + 1
        line_yxb = axes1.plot(
            lambda x: x + 1, x_range=[-1.6, 3.4], color=ORANGE, stroke_width=3.5
        )
        lab_yxb = MathTex(r"y=x+1", font_size=24, color=ORANGE).next_to(
            axes1.c2p(3.2, 4.2), UP, buff=0.12
        )
        self.play(FadeOut(note1), Create(line_yxb), Write(lab_yxb))
        self.wait(0.6)

        # 回到原像 P(1,3)，演示它关于镜面和 y=x+1 的对称点 P''=(2,2)
        # （若误用像点 P'(3,1) 作输入将得到 (0,4)，这是常见错因，故必须换回原像）
        self.play(
            FadeOut(dotP), FadeOut(dotPp), FadeOut(tagP),
            FadeOut(mid1), FadeOut(tagMid1), FadeOut(seg), FadeOut(map1),
        )
        P0 = axes1.c2p(1, 3)
        Ppb = axes1.c2p(2, 2)
        M2 = axes1.c2p(1.5, 2.5)
        seg2 = DashedLine(P0, Ppb, color=ORANGE, stroke_width=3)
        dotP0 = Dot(P0, radius=0.09, color=YELLOW)
        tagP0 = MathTex("P(1,3)", font_size=22, color=YELLOW).next_to(dotP0, UL, buff=0.12)
        dotPpb = Dot(Ppb, radius=0.09, color=ORANGE)
        tagPpb = MathTex("P''(2,2)", font_size=22, color=ORANGE).next_to(
            dotPpb, DR, buff=0.12
        )
        dotM2 = Dot(M2, radius=0.06, color=WHITE)
        tagM2 = MathTex(r"M(\tfrac{3}{2},\tfrac{5}{2})", font_size=20, color=WHITE).next_to(
            dotM2, LEFT, buff=0.08
        )
        map2 = MathTex(
            r"(x,y)\mapsto(y-b,\;x+b)", font_size=26, color=ORANGE
        ).to_edge(DOWN, buff=0.3)
        check = MathTex(r"3-1=2,\quad 1+1=2", font_size=24, color=GRAY).next_to(
            map2, UP, buff=0.15
        )

        self.play(
            FadeIn(dotP0), Write(tagP0), Create(seg2),
            FadeIn(dotPpb), Write(tagPpb), FadeIn(dotM2), Write(tagM2),
        )
        self.wait(0.4)
        self.play(Write(map2), Write(check))
        self.wait(1.2)

        keyline = Text(
            "唯有 k = ±1 的镜面，能保持横纵坐标的干净线性互换！",
            font=FONT_NAME,
            font_size=19,
            color=YELLOW,
        ).next_to(title, DOWN, aligned_edge=RIGHT, buff=0.22)
        self.play(Write(keyline))
        self.wait(1.0)

        # ==========================================================
        # 第二幕：指对同构交点秒杀（x + y = 4）
        # ==========================================================
        group1 = VGroup(
            axes1, line_yx, lab_yx, line_yxb, lab_yxb, note1, seg, seg2,
            dotP, dotPp, tagP, mid1, tagMid1, map1,
            dotP0, tagP0, dotPpb, tagPpb, dotM2, tagM2,
            map2, check, keyline,
        )
        self.play(FadeOut(group1))

        axes2 = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            x_length=8.6,
            y_length=5.4,
            axis_config={"include_tip": True, "font_size": 18},
        ).shift(DOWN * 0.55 + LEFT * 0.5)

        curve_e = axes2.plot(
            lambda x: np.exp(x), x_range=[-1, 1.2], color=GREEN, stroke_width=4
        )
        curve_ln = axes2.plot(
            lambda x: np.log(x), x_range=[0.09, 4.8], color=BLUE, stroke_width=4
        )
        sym = axes2.plot(lambda x: x, x_range=[-1, 4.2], color=YELLOW, stroke_width=2.5)
        sym_dashed = DashedLine(
            axes2.c2p(-1, -1), axes2.c2p(4.2, 4.2), color=YELLOW, stroke_width=2.5
        )

        lab_e = MathTex(r"y=e^x", font_size=22, color=GREEN).next_to(
            axes2.c2p(0.9, 2.6), LEFT, buff=0.1
        )
        lab_ln = MathTex(r"y=\ln x", font_size=22, color=BLUE).next_to(
            axes2.c2p(4.0, 1.4), RIGHT, buff=0.1
        )

        cond = MathTex(
            r"e^{x_1}+x_1=4 \Rightarrow e^{x_1}=4-x_1",
            r"\ln x_2+x_2=4 \Rightarrow \ln x_2=4-x_2",
            font_size=22,
            color=WHITE,
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title, DOWN, aligned_edge=LEFT, buff=0.22)

        self.play(
            Create(axes2), Create(curve_e), Create(curve_ln),
            Create(sym_dashed), Write(lab_e), Write(lab_ln),
            Write(cond),
        )
        self.wait(0.6)

        # 红色直线 x + y = 4，与 y = x 垂直相交于 M(2,2)
        cut = axes2.plot(
            lambda x: 4 - x, x_range=[-0.8, 4.8], color=RED, stroke_width=4
        )
        lab_cut = MathTex(r"x+y=4", font_size=22, color=RED).next_to(
            axes2.c2p(3.9, 0.35), DOWN, buff=0.08
        )
        M = Dot(axes2.c2p(2, 2), radius=0.1, color=YELLOW)
        tagM = MathTex("M(2,2)", font_size=24, color=WHITE).next_to(M, UL, buff=0.12)
        perp = MathTex(r"(-1)\times1=-1", font_size=20, color=GRAY).next_to(
            axes2.c2p(2.4, 1.7), DR, buff=0.05
        )

        self.play(Create(cut), Write(lab_cut), FadeIn(M), Write(tagM), Write(perp))
        self.wait(0.8)

        # 两个交点 A(1.07, 2.93) 与 B(2.93, 1.07)
        xA = 1.07
        yA = 4 - xA
        A = Dot(axes2.c2p(xA, yA), radius=0.1, color=RED)
        B = Dot(axes2.c2p(yA, xA), radius=0.1, color=RED)
        tagA = MathTex(r"A(x_1,y_1)", font_size=23, color=RED).next_to(A, UL, buff=0.1)
        tagB = MathTex(r"B(y_1,x_1)", font_size=23, color=RED).next_to(B, DR, buff=0.1)
        segAB = DashedLine(A.get_center(), B.get_center(), color=ORANGE, stroke_width=2.5)

        self.play(FadeIn(A), Write(tagA), FadeIn(B), Write(tagB), Create(segAB))
        self.wait(0.8)

        reason = Text(
            "A 与 B 关于 y = x 对称：x₂ = y₁，且 y₁ = 4 − x₁",
            font=FONT_NAME,
            font_size=21,
            color=ORANGE,
        ).to_edge(DOWN, buff=0.75)
        result = MathTex(
            r"x_1+x_2 = x_1+y_1 = 4", font_size=30, color=YELLOW
        ).to_edge(DOWN, buff=0.3)
        tail = Text(
            "无需硬解超越方程，3 秒出答案！",
            font=FONT_NAME,
            font_size=20,
            color=GREEN,
        ).next_to(result, RIGHT, buff=0.4)

        self.play(Write(reason))
        self.wait(0.4)
        self.play(Write(result), Write(tail))
        self.wait(2.2)
