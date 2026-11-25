"""第 5 章 · 数列与离散动态系统 —— 场景 1：蛛网迭代与特征方向

叙事：坐标平面画 y=f(x)=1/2 x+1/2 与 y=x，标出不动点 x*=1，
      在 x* 处用斜率三角形标出切线斜率 λ=f'(x*)=1/2（特征方向）
      → 从 x0=0 出发的蛛网阶梯，逐步逼近不动点（偏差每步缩小 λ 倍）
      → 换成 g(x)=2x-1（同一不动点 x*=1，λ=2>1），阶梯发散逃离
      → 定格稳定性判据：|λ|<1 吸引，|λ|>1 排斥

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene1_cobweb.py CobwebAndEigenEvolution
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


class CobwebAndEigenEvolution(Scene):
    def construct(self):
        self.camera.background_color = BG
        XSTAR = 1.0

        axes = Axes(
            x_range=[-1, 3, 1],
            y_range=[-1, 3, 1],
            x_length=4.8,
            y_length=4.8,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "color": GRAY,
                "stroke_width": 2,
            },
        ).shift(LEFT * 2.3 + DOWN * 0.55)
        origin = axes.c2p(0, 0)
        unit = axes.c2p(1, 0)[0] - origin[0]

        def cpt(x, y):
            """数据坐标 → 场景坐标（统一 3D）"""
            return origin + unit * np.array([x, y, 0.0])

        def cobweb(func, x0, nsteps, color):
            """蛛网阶梯：竖直撞曲线、水平反射回 y=x"""
            lines = VGroup()
            x = x0
            dot = Dot(cpt(x, 0), radius=0.07, color=ACCENT)
            self.play(FadeIn(dot), run_time=0.5)
            for i in range(nsteps):
                xn = func(x)
                y0 = x if i > 0 else 0.0
                v = Line(cpt(x, y0), cpt(x, xn), color=color, stroke_width=2.5)
                h = Line(cpt(x, xn), cpt(xn, xn), color=color, stroke_width=2.5)
                self.play(Create(v), dot.animate.move_to(cpt(x, xn)),
                          run_time=0.7)
                self.play(Create(h), dot.animate.move_to(cpt(xn, xn)),
                          run_time=0.7)
                lines.add(v, h)
                x = xn
            return lines, dot

        # ======================================================
        # 第一幕：不动点与特征方向（切线斜率 λ）
        # ======================================================
        title1 = Text(
            "1. 不动点：曲线 y=f(x) 与直线 y=x 的交点",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=1.1)
        self.wait(0.4)

        f_curve = axes.plot(lambda x: 0.5 * x + 0.5, x_range=[-1, 3],
                            color=PRIMARY, stroke_width=3)
        diag = DashedLine(cpt(-1, -1), cpt(3, 3), color=GRAY, stroke_width=2)
        fp = Dot(cpt(XSTAR, XSTAR), radius=0.09, color=ACCENT)
        fp_label = MathTex(r"x^*=1", font_size=24, color=ACCENT)
        # 放在不动点正下方：该处两条曲线都不经过，蛛网阶梯也不占用
        fp_label.next_to(fp, DOWN + RIGHT, buff=0.34)
        # 加深色底衬，保证标签压在蛛网竖边/曲线上时仍清晰可读
        fp_bg = BackgroundRectangle(
            fp_label, color="#1C1C1C", fill_opacity=0.92, buff=0.1,
        )

        f_label = MathTex(r"f(x)=\frac{1}{2}x+\frac{1}{2}",
                          font_size=21, color=PRIMARY)
        f_label.move_to(cpt(-0.8, 0.62))
        diag_label = MathTex(r"y=x", font_size=21, color=GRAY)
        diag_label.move_to(cpt(2.5, 2.8))

        self.play(Create(axes), run_time=1.3)
        self.play(Create(f_curve), Create(diag), run_time=1.2)
        self.play(FadeIn(fp), FadeIn(fp_bg), Write(fp_label), run_time=0.9)
        self.play(Write(f_label), Write(diag_label), run_time=1.0)
        self.wait(0.5)

        # 斜率三角形：在 x* 处标出切线斜率 λ = f'(x*)
        tri_run = Line(cpt(1, 1), cpt(2.1, 1), color=SECONDARY, stroke_width=3)
        tri_rise = Line(cpt(2.1, 1), cpt(2.1, 1.55), color=SECONDARY,
                        stroke_width=3)
        lam_label = MathTex(r"\lambda=\frac{1}{2}", font_size=22,
                            color=SECONDARY)
        lam_label.move_to(cpt(2.1, 1.27) + RIGHT * 0.5)
        self.play(Create(tri_run), Create(tri_rise), run_time=1.0)
        self.play(Write(lam_label), run_time=0.9)
        self.wait(0.5)

        panel1 = VGroup(
            VGroup(Text("不动点方程", font=FONT_NAME, font_size=21,
                        color=PRIMARY),
                   MathTex(r"x^*=f(x^*)", font_size=24, color=WHITE)
                   ).arrange(RIGHT, buff=0.22),
            MathTex(r"x^*=\frac{1}{2}x^*+\frac{1}{2}\ \Rightarrow\ x^*=1",
                    font_size=24, color=WHITE),
            VGroup(Text("切线斜率", font=FONT_NAME, font_size=21,
                        color=SECONDARY),
                   MathTex(r"\lambda=f'(x^*)=\frac{1}{2}", font_size=24,
                           color=SECONDARY)).arrange(RIGHT, buff=0.22),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        panel1.move_to((1.2, 1.35, 0), aligned_edge=LEFT)
        self.play(Write(panel1), run_time=1.5)
        self.wait(3.0)

        # ======================================================
        # 第二幕：蛛网阶梯收敛（|λ|<1）
        # ======================================================
        title2 = Text(
            "2. 蛛网迭代：阶梯式逼近不动点（|λ|<1）",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=1.0)

        panel2 = VGroup(
            MathTex(r"x_{n+1}-x^*=\lambda\,(x_n-x^*)", font_size=25,
                    color=WHITE),
            Text("偏差每步缩小为 λ 倍", font=FONT_NAME, font_size=21,
                 color=SECONDARY),
            MathTex(r"x_0=0,\ x_1=\frac{1}{2},\ x_2=\frac{3}{4},\ \cdots",
                    font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        panel2.move_to((1.2, 1.5, 0), aligned_edge=LEFT)

        self.play(FadeOut(panel1), run_time=0.6)
        self.play(Write(panel2), run_time=1.3)
        self.wait(0.5)

        cw_lines, cw_dot = cobweb(lambda x: 0.5 * x + 0.5, 0.0, 5, PRIMARY)
        self.wait(0.8)

        conv_arrow = Arrow(cpt(0.2, 0.2), cpt(0.92, 0.92), buff=0,
                           color=ACCENT, stroke_width=3,
                           tip_length=0.18)
        conv_label = Text("阶梯收缩", font=FONT_NAME, font_size=20,
                          color=ACCENT)
        conv_label.move_to(cpt(0.15, 0.62))
        self.play(Create(conv_arrow), Write(conv_label), run_time=1.1)
        self.wait(2.6)

        # ======================================================
        # 第三幕：换成扩张映射（|λ|>1），定格稳定性判据
        # ======================================================
        title3 = Text(
            "3. 对比：|λ|>1 时间阶梯发散，定格稳定性判据",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title2, title3), run_time=1.0)

        self.play(
            FadeOut(panel2), FadeOut(conv_arrow), FadeOut(conv_label),
            FadeOut(cw_lines), FadeOut(cw_dot),
            FadeOut(f_curve), FadeOut(f_label), FadeOut(lam_label),
            FadeOut(tri_run), FadeOut(tri_rise),
            run_time=0.8,
        )

        g_curve = axes.plot(lambda x: 2 * x - 1, x_range=[0, 2],
                            color=RED_H, stroke_width=3)
        g_label = MathTex(r"g(x)=2x-1", font_size=21, color=RED_H)
        g_label.move_to(cpt(1.2, 1.2) + RIGHT * 0.55)
        tri2_run = Line(cpt(1, 1), cpt(1.5, 1), color=RED_H, stroke_width=3)
        tri2_rise = Line(cpt(1.5, 1), cpt(1.5, 2), color=RED_H, stroke_width=3)
        lam2_label = MathTex(r"\lambda=2", font_size=22, color=RED_H)
        lam2_label.move_to(cpt(1.5, 2.0) + RIGHT * 0.4)

        self.play(Create(g_curve), run_time=1.2)
        self.play(Write(g_label), run_time=0.9)
        self.play(Create(tri2_run), Create(tri2_rise), run_time=0.9)
        self.play(Write(lam2_label), run_time=0.9)
        self.wait(0.5)

        cw2_lines, cw2_dot = cobweb(lambda x: 2 * x - 1, 1.2, 3, RED_H)
        self.wait(0.6)

        panel3 = VGroup(
            VGroup(MathTex(r"|\lambda|<1", font_size=24, color=SECONDARY),
                   Text("吸引不动点：阶梯收缩", font=FONT_NAME,
                        font_size=21, color=SECONDARY)).arrange(
                       RIGHT, buff=0.25),
            VGroup(MathTex(r"|\lambda|>1", font_size=24, color=RED_H),
                   Text("排斥不动点：阶梯放大", font=FONT_NAME,
                        font_size=21, color=RED_H)).arrange(
                       RIGHT, buff=0.25),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        panel3.move_to((1.2, 1.2, 0), aligned_edge=LEFT)
        box3 = SurroundingRectangle(panel3, color=ACCENT, buff=0.22,
                                    stroke_width=3)

        self.play(Write(panel3), run_time=1.5)
        self.play(Create(box3), run_time=0.9)
        self.wait(0.8)

        caption = Text(
            "不动点是否稳定，取决于 |f'(x*)| 与 1 的大小",
            font=FONT_NAME, font_size=22, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(caption), run_time=1.3)
        self.wait(4.5)
