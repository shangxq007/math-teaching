"""第 9 章 · 不动点：迭代、方程与几何变换的交汇 —— 场景 1：蛛网法

叙事：以 a_{n+1}=1/2 a_n+1, a_0=0 为例。
      数列是 N→R 的函数，递推 = 映射 F(x)=x/2+1 的自迭代
      → 数值感知：a_1=1, a_2=3/2, a_3=7/4, a_4=15/8，节节逼近 2
      → 几何翻译：曲线 y=F(x) 与对角线 y=x 的交点即不动点，
        解 x*=F(x*) 得 x*=2；蛛网阶梯从 a_0=0 出发螺旋收拢
      → 定格稳定性判据：|F'(x*)|=1/2<1 收缩（稳定）；>1 扩张；=1 临界
        并提醒：不动点存在 ≠ 轨道收敛（反例 a_{n+1}=-a_n）

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene1_cobweb.py CobwebFixedPoint
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


class CobwebFixedPoint(Scene):
    def construct(self):
        self.camera.background_color = BG
        XSTAR = 2.0

        # ======================================================
        # 第一幕：数列 = 函数的迭代
        # ======================================================
        title1 = Text(
            "1. 数列是函数的迭代：a_{n+1}=F(a_n)",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=1.1)
        self.wait(0.4)

        view = VGroup(
            Text("数列 {a_n} 是 N→R 的函数", font=FONT_NAME, font_size=21,
                 color=WHITE),
            Text("一阶递推 = 映射 F 的自迭代", font=FONT_NAME,
                 font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        view.move_to(UP * 2.2 + LEFT * 3.2)
        self.play(Write(view), run_time=1.2)
        self.wait(0.5)

        rec = MathTex(r"a_{n+1}=\frac{1}{2}a_n+1,\qquad a_0=0",
                      font_size=30, color=ACCENT).move_to(UP * 0.9)
        terms = MathTex(
            r"a_1=1,\quad a_2=\frac32,\quad a_3=\frac74,\quad "
            r"a_4=\frac{15}{8},\quad \cdots",
            font_size=26, color=WHITE).move_to(UP * 0.0)
        guess = Text("数值节节逼近 2？", font=FONT_NAME, font_size=21,
                     color=SECONDARY).move_to(DOWN * 0.8)
        self.play(Write(rec), run_time=1.3)
        self.play(Write(terms), run_time=1.4)
        self.play(FadeIn(guess), run_time=0.9)
        self.wait(2.4)

        # ======================================================
        # 第二幕：几何翻译 + 蛛网阶梯
        # ======================================================
        title2 = Text(
            "2. 几何翻译：曲线 y=F(x) 与对角线 y=x 的交点",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=1.0)
        self.play(FadeOut(view), FadeOut(rec), FadeOut(terms),
                  FadeOut(guess), run_time=0.6)

        axes = Axes(
            x_range=[-1, 3, 1],
            y_range=[-1, 3, 1],
            x_length=4.9, y_length=4.9,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "color": GRAY,
                "stroke_width": 2,
            },
        ).shift(LEFT * 2.85 + DOWN * 0.55)

        def cpt(x, y):
            o = axes.c2p(0, 0)
            u = axes.c2p(1, 0)[0] - o[0]
            v = axes.c2p(0, 1)[1] - o[1]
            return o + np.array([u * x, v * y, 0.0])

        f_curve = axes.plot(lambda x: 0.5 * x + 1, x_range=[-1, 3],
                            color=PRIMARY, stroke_width=3)
        diag = DashedLine(cpt(-1, -1), cpt(3, 3), color=GRAY,
                          stroke_width=2)
        fp = Dot(cpt(XSTAR, XSTAR), radius=0.09, color=ACCENT)
        fp_lbl = MathTex(r"x^*=2", font_size=22, color=ACCENT)
        fp_lbl.next_to(fp, UP + RIGHT, buff=0.16)
        fp_bg = BackgroundRectangle(fp_lbl, color="#1C1C1C",
                                    fill_opacity=0.92, buff=0.1)
        f_lbl = MathTex(r"F(x)=\frac12 x+1", font_size=20,
                        color=PRIMARY)
        f_lbl.move_to(cpt(-0.85, 0.7))
        diag_lbl = MathTex(r"y=x", font_size=20, color=GRAY)
        diag_lbl.move_to(cpt(2.55, 2.8))

        self.play(Create(axes), run_time=1.2)
        self.play(Create(f_curve), Create(diag), run_time=1.2)
        self.play(FadeIn(fp), FadeIn(fp_bg), Write(fp_lbl), Write(f_lbl),
                  Write(diag_lbl), run_time=1.1)
        self.wait(0.6)

        panel_eq = VGroup(
            VGroup(Text("不动点方程 ", font=FONT_NAME, font_size=20,
                        color=WHITE),
                   MathTex(r"x^*=F(x^*)", font_size=23,
                           color=WHITE)).arrange(RIGHT, buff=0.18),
            MathTex(r"x^*=\frac12 x^*+1\ \Rightarrow\ x^*=2",
                    font_size=23, color=ACCENT),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        panel_eq.move_to((3.4, 1.5, 0))
        self.play(Write(panel_eq), run_time=1.4)
        self.wait(2.2)

        # 蛛网阶梯：从 a0=0 出发
        x = 0.0
        dot = Dot(cpt(x, 0), radius=0.07, color=ACCENT)
        self.play(FadeIn(dot), run_time=0.5)
        step_lbls = VGroup()
        trail = VGroup()
        dirs = [UP + RIGHT, DOWN + RIGHT]
        for i in range(4):
            xn = 0.5 * x + 1
            y0 = x if i > 0 else 0.0
            v = Line(cpt(x, y0), cpt(x, xn), color=PRIMARY,
                     stroke_width=2.5)
            h = Line(cpt(x, xn), cpt(xn, xn), color=PRIMARY,
                     stroke_width=2.5)
            self.play(Create(v), dot.animate.move_to(cpt(x, xn)),
                      run_time=0.7)
            if i < 2:
                lab = MathTex("a_%d" % (i + 1), font_size=18,
                              color=ACCENT)
                lab.next_to(cpt(xn, xn), dirs[i], buff=0.12)
                self.play(Create(h), dot.animate.move_to(cpt(xn, xn)),
                          FadeIn(lab), run_time=0.7)
                step_lbls.add(lab)
            else:
                self.play(Create(h), dot.animate.move_to(cpt(xn, xn)),
                          run_time=0.7)
            trail.add(v, h)
            x = xn
        self.wait(0.8)

        shrink = Text("台阶一级级变小，收拢到 x*=2",
                      font=FONT_NAME, font_size=20, color=SECONDARY)
        shrink.move_to((3.4, 0.15, 0))
        self.play(Write(shrink), run_time=1.1)
        self.wait(2.6)

        # ======================================================
        # 第三幕：稳定性判据定格
        # ======================================================
        title3 = Text(
            "3. 定格：|F'(x*)| 与 1 比大小",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title2, title3), run_time=1.0)
        self.play(FadeOut(panel_eq), FadeOut(shrink), run_time=0.6)

        tri_run = Line(cpt(2, 2), cpt(3, 2), color=SECONDARY,
                       stroke_width=3)
        tri_rise = Line(cpt(3, 2), cpt(3, 2.5), color=SECONDARY,
                        stroke_width=3)
        lam_lbl = MathTex(r"F'(x^*)=\frac12", font_size=21,
                          color=SECONDARY)
        lam_lbl.next_to(tri_rise, RIGHT, buff=0.18)
        self.play(Create(tri_run), Create(tri_rise), run_time=1.0)
        self.play(Write(lam_lbl), run_time=0.9)
        self.wait(0.6)

        crit = VGroup(
            VGroup(MathTex(r"|F'(x^*)|<1", font_size=23, color=SECONDARY),
                   Text("收缩：阶梯收拢", font=FONT_NAME, font_size=20,
                        color=SECONDARY)).arrange(RIGHT, buff=0.22),
            VGroup(MathTex(r"|F'(x^*)|>1", font_size=23, color=RED_H),
                   Text("扩张：阶梯弹开", font=FONT_NAME, font_size=20,
                        color=RED_H)).arrange(RIGHT, buff=0.22),
            VGroup(MathTex(r"|F'(x^*)|=1", font_size=23, color=GRAY),
                   Text("临界：看高阶项", font=FONT_NAME, font_size=20,
                        color=GRAY)).arrange(RIGHT, buff=0.22),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        crit.move_to((3.4, 1.2, 0))
        box = SurroundingRectangle(crit, color=ACCENT, buff=0.24,
                                   stroke_width=3)
        self.play(Write(crit), run_time=1.6)
        self.play(Create(box), run_time=0.9)
        self.wait(0.8)

        warn = Text("注意：不动点存在 ≠ 轨道收敛（反例 a_{n+1}=-a_n）",
                    font=FONT_NAME, font_size=19, color=ACCENT)
        warn.move_to((3.4, 0.15, 0))
        self.play(Write(warn), run_time=1.2)
        self.wait(4.0)
