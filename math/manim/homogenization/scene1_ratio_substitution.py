"""第 8 章 · 齐次化：把二元问题压成一元比例 —— 场景 1：t = y/x 代换

叙事：已知 x>0, y>0, 2x+y=1，求 xy 的最大值。
      利用约束「2x+y=1」把目标写成二元分式 xy/(2x+y)^2
      → 几何观察：点 (x,y) 落在过原点的射线 y=tx 上；(x,y) 与 (λx,λy)
        只是同一条射线上的不同代表。分子分母同为二次，分式是 0 次齐次，
        λ² 上下对消，取值只依赖比值 t=y/x
      → 同除 x²：xy/(2x+y)^2 → (y/x)/(2+y/x)² → t/(2+t)²
        （二元分式压成一元分式）
      → 一元函数 g(t)=t/(2+t)² 的图象：最大值在 t=2，g=1/8；
        几何回扣：最优射线 y=2x 与直线 2x+y=1 的交点正是 (1/4, 1/2)

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene1_ratio_substitution.py RatioSubstitution
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
GRAY = "#9E9E9E"


class RatioSubstitution(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ======================================================
        # 第一幕：问题登场——目标是二元分式
        # ======================================================
        title1 = Text(
            "1. 问题：两个变量的最值，怎么下手？",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=1.1)
        self.wait(0.4)

        cond = MathTex(r"x>0,\quad y>0,\quad 2x+y=1", font_size=30,
                       color=WHITE)
        goal = MathTex(r"\max\ xy", font_size=30, color=ACCENT)
        pg = VGroup(cond, goal).arrange(RIGHT, buff=0.7)
        pg.move_to(UP * 1.95)
        self.play(Write(pg), run_time=1.2)
        self.wait(0.6)

        eq = MathTex(r"\frac{xy}{(2x+y)^2}=\frac{xy}{1}=xy",
                     font_size=32, color=WHITE).move_to(UP * 0.75)
        self.play(Write(eq), run_time=1.4)
        self.wait(0.5)

        note = Text("二元分式：x 与 y 纠缠在一起，配方、不等式都用不上",
                    font=FONT_NAME, font_size=21, color=RED_H)
        note.next_to(eq, DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=0.9)
        self.wait(1.8)

        # ======================================================
        # 第二幕：齐次性——取值只认比例 t=y/x
        # ======================================================
        title2 = Text(
            "2. 关键观察：齐次式的取值只认比例 t=y/x",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=1.0)
        self.play(FadeOut(pg), FadeOut(eq), FadeOut(note), run_time=0.6)

        axes = Axes(
            x_range=[-0.2, 1.2, 0.5],
            y_range=[-0.2, 2.2, 0.5],
            x_length=4.6, y_length=4.6,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "color": GRAY,
                "stroke_width": 2,
            },
        ).shift(LEFT * 3.35 + DOWN * 0.55)

        def cpt(x, y):
            o = axes.c2p(0, 0)
            u = axes.c2p(1, 0)[0] - o[0]
            v = axes.c2p(0, 1)[1] - o[1]
            return o + np.array([u * x, v * y, 0.0])

        self.play(Create(axes), run_time=1.2)

        ray = Line(cpt(-0.05, -0.1), cpt(1.15, 2.3), color=SECONDARY,
                   stroke_width=3)
        seg = Line(cpt(0, 1), cpt(0.5, 0), color=PRIMARY, stroke_width=3.5)
        ray_lbl = MathTex(r"y=tx", font_size=21, color=SECONDARY)
        ray_lbl.move_to(cpt(1.02, 2.32))
        seg_lbl = MathTex(r"2x+y=1", font_size=19, color=PRIMARY)
        seg_lbl.move_to(cpt(0.36, 1.14))

        dotP = Dot(cpt(0.25, 0.5), radius=0.09, color=ACCENT)
        dotP2 = Dot(cpt(0.5, 1.0), radius=0.08, color=SECONDARY)
        lblP = MathTex(r"\left(\tfrac14,\tfrac12\right)", font_size=17,
                       color=ACCENT)
        lblP.next_to(dotP, DOWN + RIGHT, buff=0.16)
        lblP2 = MathTex(r"\left(\tfrac12,1\right)", font_size=17,
                        color=SECONDARY)
        lblP2.next_to(dotP2, UP + RIGHT, buff=0.12)

        self.play(Create(ray), Create(seg), run_time=1.2)
        self.play(Write(ray_lbl), Write(seg_lbl), run_time=0.9)
        self.play(FadeIn(dotP), FadeIn(dotP2), Write(lblP), Write(lblP2),
                  run_time=1.0)
        self.wait(0.5)

        scale_arrow = Arrow(dotP, dotP2, buff=0.1, color=ACCENT,
                            stroke_width=3, tip_length=0.16)
        scale_lbl = Text("(x,y) 与 (2x,2y)：同一条射线上的不同代表",
                         font=FONT_NAME, font_size=19, color=ACCENT)
        scale_lbl.move_to(cpt(0.62, 1.86))
        self.play(Create(scale_arrow), Write(scale_lbl), run_time=1.1)
        self.wait(0.6)

        panel = VGroup(
            Text("分子、分母都是 2 次", font=FONT_NAME, font_size=20,
                 color=WHITE),
            MathTex(r"Q(\lambda x,\lambda y)=Q(x,y)", font_size=22,
                    color=WHITE),
            Text("λ² 上下对消：取值与点在射线上的位置无关",
                 font=FONT_NAME, font_size=19, color=SECONDARY),
            VGroup(Text("只剩一个自由度 ", font=FONT_NAME, font_size=20,
                        color=WHITE),
                   MathTex(r"t=\frac{y}{x}", font_size=24,
                           color=ACCENT)).arrange(RIGHT, buff=0.2),
            MathTex(r"Q(x,y)=g(t)", font_size=24, color=ACCENT),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        panel.move_to((3.25, 0.55, 0))
        self.play(Write(panel), run_time=1.8)
        self.wait(2.6)

        # ======================================================
        # 第三幕：同除 x²——二元分式压成一元分式
        # ======================================================
        title3 = Text(
            "3. 同除 x²：二元分式 → 一元分式",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title2, title3), run_time=1.0)
        self.play(
            FadeOut(axes), FadeOut(ray), FadeOut(seg),
            FadeOut(ray_lbl), FadeOut(seg_lbl),
            FadeOut(dotP), FadeOut(dotP2), FadeOut(lblP), FadeOut(lblP2),
            FadeOut(scale_arrow), FadeOut(scale_lbl), FadeOut(panel),
            run_time=0.7,
        )

        tag0 = Text("二元分式：x、y 两个变量", font=FONT_NAME, font_size=20,
                    color=RED_H).move_to(UP * 2.6)
        L0 = MathTex(r"\frac{xy}{(2x+y)^2}", font_size=40,
                     color=WHITE).move_to(UP * 1.55)
        op1 = Text("分子分母同除 x²（次数差不变）", font=FONT_NAME,
                   font_size=19, color=GRAY).move_to(DOWN * 0.35)
        L1 = MathTex(r"\frac{xy\div x^{2}}{(2x+y)^{2}\div x^{2}}",
                     font_size=34, color=WHITE).move_to(UP * 1.55)
        op2 = Text("把 y/x 记为 t", font=FONT_NAME, font_size=19,
                   color=GRAY).move_to(DOWN * 0.35)
        L2 = MathTex(r"\frac{\dfrac{y}{x}}{\left(2+\dfrac{y}{x}\right)^{2}}",
                     font_size=34, color=WHITE).move_to(UP * 1.55)
        tag3 = Text("一元分式：只有 t", font=FONT_NAME, font_size=20,
                    color=SECONDARY).move_to(UP * 2.6)
        L3 = MathTex(r"\frac{t}{(2+t)^{2}}", font_size=42,
                     color=ACCENT).move_to(UP * 1.55)

        self.play(Write(tag0), Write(L0), run_time=1.2)
        self.wait(1.4)
        self.play(ReplacementTransform(L0, L1), Write(op1), run_time=1.4)
        self.wait(1.6)
        self.play(ReplacementTransform(L1, L2), FadeOut(op1),
                  Write(op2), run_time=1.4)
        self.wait(1.6)
        self.play(ReplacementTransform(L2, L3), FadeOut(op2),
                  ReplacementTransform(tag0, tag3), run_time=1.5)
        self.wait(2.8)

        # ======================================================
        # 第四幕：一元函数 g(t)=t/(2+t)² 的最值
        # ======================================================
        title4 = Text(
            "4. 一元函数：g(t)=t/(2+t)² 的最值",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title3, title4), run_time=1.0)
        self.play(FadeOut(L3), FadeOut(tag3), run_time=0.6)

        ax2 = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 0.16, 0.05],
            x_length=5.4, y_length=4.2,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "color": GRAY,
                "stroke_width": 2,
            },
        ).shift(LEFT * 2.7 + DOWN * 0.7)

        def c2(x, y):
            o = ax2.c2p(0, 0)
            u = ax2.c2p(1, 0)[0] - o[0]
            v = ax2.c2p(0, 1)[1] - o[1]
            return o + np.array([u * x, v * y, 0.0])

        gcurve = ax2.plot(lambda t: t / (2 + t) ** 2, x_range=[0.01, 5],
                          color=PRIMARY, stroke_width=3)
        peak = Dot(c2(2, 0.125), radius=0.09, color=ACCENT)
        vline = DashedLine(c2(2, 0), c2(2, 0.125), color=ACCENT,
                           stroke_width=2)
        peak_lbl = MathTex(r"\left(2,\tfrac18\right)", font_size=20,
                           color=ACCENT)
        peak_lbl.next_to(peak, UP + LEFT, buff=0.14)
        t_lbl = MathTex(r"t=2", font_size=19, color=ACCENT)
        t_lbl.next_to(c2(2, 0), DOWN, buff=0.18)
        g_lbl = MathTex(r"g(t)=\frac{t}{(2+t)^2}", font_size=20,
                        color=PRIMARY)
        g_lbl.move_to(c2(0.4, 0.135))

        self.play(Create(ax2), run_time=1.2)
        self.play(Create(gcurve), run_time=1.4)
        self.play(FadeIn(peak), Create(vline), Write(peak_lbl),
                  Write(t_lbl), Write(g_lbl), run_time=1.2)
        self.wait(0.8)

        panel4 = VGroup(
            MathTex(r"(t+2)^2\ge 8t", font_size=23, color=WHITE),
            MathTex(r"\Rightarrow\ g(t)=\frac{t}{(2+t)^2}\le\frac18",
                    font_size=23, color=WHITE),
            VGroup(Text("等号当 ", font=FONT_NAME, font_size=19,
                        color=WHITE),
                   MathTex(r"t=2", font_size=22, color=ACCENT),
                   Text("，即 ", font=FONT_NAME, font_size=19,
                        color=WHITE),
                   MathTex(r"y=2x", font_size=22, color=ACCENT)).arrange(
                       RIGHT, buff=0.14),
            VGroup(Text("此时 ", font=FONT_NAME, font_size=19,
                        color=WHITE),
                   MathTex(r"x=\tfrac14,\ y=\tfrac12", font_size=21,
                           color=ACCENT)).arrange(RIGHT, buff=0.14),
            MathTex(r"\max\ xy=\frac18", font_size=24, color=ACCENT),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        panel4.move_to((3.5, 0.35, 0))
        self.play(Write(panel4), run_time=1.8)
        self.wait(1.2)

        caption = Text(
            "几何回扣：射线 y=2x 与直线 2x+y=1 的交点，正是最优点",
            font=FONT_NAME, font_size=20, color=ACCENT,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(caption), run_time=1.3)
        self.wait(4.0)
