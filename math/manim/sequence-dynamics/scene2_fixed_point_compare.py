"""第 5 章 · 数列与离散动态系统 —— 场景 2：不动点稳定性对比

叙事：两条一阶递推并排对比稳定性（不动点不同）
        左：压缩型 a_{n+1}=1/2 a_n+1，|f'|=1/2<1，真不动点 x*=2，蛛网收拢
        右：扩张型 a_{n+1}=2a_n-1，|g'|=2>1，真不动点 x*=1，蛛网远离
      数列项用点列在各自数轴上跳动
      → 定格：不动点是否吸引，取决于 |f'(x*)| 与 1 的关系

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene2_fixed_point_compare.py FixedPointStabilityComparison
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


class FixedPointStabilityComparison(Scene):
    def construct(self):
        self.camera.background_color = BG
        XSTAR_L = 2.0   # f(x)=x/2+1 的不动点：x*=x/2+1 ⇒ x*=2
        XSTAR_R = 1.0   # g(x)=2x-1 的不动点：x*=2x*-1 ⇒ x*=1

        def make_axes(center):
            return Axes(
                x_range=[-1, 3, 1],
                y_range=[-1, 3, 1],
                x_length=4.4,
                y_length=4.4,
                axis_config={
                    "include_tip": True,
                    "include_numbers": False,
                    "color": GRAY,
                    "stroke_width": 2,
                },
            ).shift(center)

        left_axes = make_axes(LEFT * 3.55 + UP * 0.6)
        right_axes = make_axes(RIGHT * 3.55 + UP * 0.6)

        def cpt(ax, x, y):
            o = ax.c2p(0, 0)
            u = ax.c2p(1, 0)[0] - o[0]
            return o + u * np.array([x, y, 0.0])

        # ======================================================
        # 第一幕：两个递推、各自不动点不同，稳定性相反
        # ======================================================
        title1 = Text(
            "1. 左 x*=2 压缩型 vs 右 x*=1 扩张型",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=1.1)
        self.wait(0.4)

        f_curve = left_axes.plot(lambda x: 0.5 * x + 1, x_range=[-1, 3],
                                 color=PRIMARY, stroke_width=3)
        g_curve = right_axes.plot(lambda x: 2 * x - 1, x_range=[0, 2],
                                  color=RED_H, stroke_width=3)
        diag_l = DashedLine(cpt(left_axes, -1, -1), cpt(left_axes, 3, 3),
                            color=GRAY, stroke_width=2)
        diag_r = DashedLine(cpt(right_axes, -1, -1), cpt(right_axes, 3, 3),
                            color=GRAY, stroke_width=2)

        fp_l = Dot(cpt(left_axes, XSTAR_L, XSTAR_L), radius=0.09, color=ACCENT)
        fp_r = Dot(cpt(right_axes, XSTAR_R, XSTAR_R), radius=0.09, color=ACCENT)
        fp_lbl_l = MathTex(r"x^*=2", font_size=22, color=ACCENT)
        fp_lbl_l.next_to(fp_l, UP + RIGHT, buff=0.1)
        fp_lbl_r = MathTex(r"x^*=1", font_size=22, color=ACCENT)
        fp_lbl_r.next_to(fp_r, UP + LEFT, buff=0.1)

        f_label = MathTex(r"f(x)=\frac{1}{2}x+1", font_size=20,
                          color=PRIMARY)
        f_label.move_to(cpt(left_axes, -0.8, 0.72))
        g_label = MathTex(r"g(x)=2x-1", font_size=20, color=RED_H)
        g_label.move_to(cpt(right_axes, 0.2, -0.72))

        left_pt = VGroup(
            Text("压缩型", font=FONT_NAME, font_size=20, color=SECONDARY),
            MathTex(r"|f'(x^*)|=\frac{1}{2}<1", font_size=20,
                    color=SECONDARY),
        ).arrange(RIGHT, buff=0.15)
        left_pt.move_to((-3.55, 3.0, 0))
        right_pt = VGroup(
            Text("扩张型", font=FONT_NAME, font_size=20, color=RED_H),
            MathTex(r"|g'(x^*)|=2>1", font_size=20, color=RED_H),
        ).arrange(RIGHT, buff=0.15)
        right_pt.move_to((3.55, 3.0, 0))

        self.play(Create(left_axes), Create(right_axes), run_time=1.4)
        self.play(Create(f_curve), Create(g_curve),
                  Create(diag_l), Create(diag_r), run_time=1.4)
        self.play(FadeIn(fp_l), FadeIn(fp_r), Write(fp_lbl_l),
                  Write(fp_lbl_r), run_time=1.0)
        self.play(Write(f_label), Write(g_label), run_time=1.0)
        self.play(Write(left_pt), Write(right_pt), run_time=1.2)
        self.wait(0.6)

        # 数轴：数列项跳动
        left_nl = NumberLine(x_range=[-1, 3, 1], length=4.4,
                             include_numbers=True, font_size=15,
                             color=GRAY).move_to((-3.55, -2.15, 0))
        right_nl = NumberLine(x_range=[-1, 3, 1], length=4.4,
                              include_numbers=True, font_size=15,
                              color=GRAY).move_to((3.55, -2.15, 0))
        left_nl_lbl = Text("数列 {a_n}", font=FONT_NAME, font_size=18,
                           color=PRIMARY).move_to((-3.55, -1.72, 0))
        right_nl_lbl = Text("数列 {b_n}", font=FONT_NAME, font_size=18,
                            color=RED_H).move_to((3.55, -1.72, 0))

        self.play(Create(left_nl), Create(right_nl), run_time=1.1)
        self.play(Write(left_nl_lbl), Write(right_nl_lbl), run_time=0.9)
        self.wait(2.6)

        # ======================================================
        # 第二幕：同步蛛网 + 数轴点列
        # ======================================================
        title2 = Text(
            "2. 蛛网对比：一个向不动点收拢，一个远离",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=1.0)

        lx, rx = -0.5, 1.1
        dot_l = Dot(cpt(left_axes, lx, 0), radius=0.07, color=ACCENT)
        dot_r = Dot(cpt(right_axes, rx, 0), radius=0.07, color=ACCENT)
        nl_dot_l = Dot(left_nl.n2p(lx), radius=0.07, color=PRIMARY)
        nl_dot_r = Dot(right_nl.n2p(rx), radius=0.07, color=RED_H)
        self.play(FadeIn(dot_l), FadeIn(dot_r), FadeIn(nl_dot_l),
                  FadeIn(nl_dot_r), run_time=0.6)

        for i in range(4):
            xn_l = 0.5 * lx + 1
            xn_r = 2 * rx - 1
            v_l = Line(cpt(left_axes, lx, lx if i > 0 else 0),
                       cpt(left_axes, lx, xn_l),
                       color=PRIMARY, stroke_width=2.5)
            h_l = Line(cpt(left_axes, lx, xn_l),
                       cpt(left_axes, xn_l, xn_l),
                       color=PRIMARY, stroke_width=2.5)
            v_r = Line(cpt(right_axes, rx, rx if i > 0 else 0),
                       cpt(right_axes, rx, xn_r),
                       color=RED_H, stroke_width=2.5)
            h_r = Line(cpt(right_axes, rx, xn_r),
                       cpt(right_axes, xn_r, xn_r),
                       color=RED_H, stroke_width=2.5)
            trail_l = Dot(left_nl.n2p(xn_l), radius=0.045, color=PRIMARY)
            trail_r = Dot(right_nl.n2p(xn_r), radius=0.045, color=RED_H)

            self.play(Create(v_l), Create(v_r),
                      dot_l.animate.move_to(cpt(left_axes, lx, xn_l)),
                      dot_r.animate.move_to(cpt(right_axes, rx, xn_r)),
                      run_time=0.7)
            self.play(Create(h_l), Create(h_r),
                      dot_l.animate.move_to(cpt(left_axes, xn_l, xn_l)),
                      dot_r.animate.move_to(cpt(right_axes, xn_r, xn_r)),
                      nl_dot_l.animate.move_to(left_nl.n2p(xn_l)),
                      nl_dot_r.animate.move_to(right_nl.n2p(xn_r)),
                      FadeIn(trail_l), FadeIn(trail_r),
                      run_time=0.7)
            lx, rx = xn_l, xn_r

        self.wait(0.8)

        left_concl = Text("台阶变小，收拢到 x*=2", font=FONT_NAME,
                          font_size=19, color=SECONDARY)
        left_concl.move_to((-3.55, -2.75, 0))
        right_concl = Text("台阶变大，逃离 x*=1", font=FONT_NAME,
                           font_size=19, color=RED_H)
        right_concl.move_to((3.55, -2.75, 0))
        self.play(Write(left_concl), Write(right_concl), run_time=1.2)
        self.wait(2.6)

        # ======================================================
        # 第三幕：定格判据
        # ======================================================
        title3 = Text(
            "3. 定格：不动点是否吸引，取决于 |f'(x*)| 与 1 的关系",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title2, title3), run_time=1.0)

        self.play(FadeOut(left_concl), FadeOut(right_concl),
                  FadeOut(left_nl_lbl), FadeOut(right_nl_lbl),
                  run_time=0.6)

        crit = VGroup(
            VGroup(MathTex(r"|f'(x^*)|<1", font_size=24, color=SECONDARY),
                   Text("吸引不动点：数列收拢", font=FONT_NAME,
                        font_size=21, color=SECONDARY)).arrange(
                       RIGHT, buff=0.25),
            VGroup(MathTex(r"|f'(x^*)|>1", font_size=24, color=RED_H),
                   Text("排斥不动点：数列远离", font=FONT_NAME,
                        font_size=21, color=RED_H)).arrange(
                       RIGHT, buff=0.25),
        ).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
        crit.move_to((0, -3.3, 0))
        box = SurroundingRectangle(crit, color=ACCENT, buff=0.22,
                                   stroke_width=3)

        self.play(Write(crit), run_time=1.6)
        self.play(Create(box), run_time=0.9)
        self.wait(4.5)
