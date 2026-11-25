"""第 3 章 · 平面向量与空间向量 —— 场景 2：数量积的几何意义（投影）

叙事：画 b（橙）与 a（青），夹角 θ
      → 从 a 的端点向 b 所在直线作垂线，高亮投影段（红）并标 proj_b a
      → θ 从锐角 → 直角 → 钝角，投影方向翻转（钝角时投影为负）
      → 定格 a·b = |a||b|cosθ 与投影公式

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene2_dot_projection.py DotProductProjection
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


class DotProductProjection(Scene):
    def construct(self):
        self.camera.background_color = BG

        b_ang = 18 * DEGREES
        b_len = 1.60
        a_len = 1.70

        # ======================================================
        # 第一幕：a、b 与夹角 θ，作出投影
        # ======================================================
        title1 = Text(
            "1. 数量积的几何意义：投影",
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
            return origin + unit * (x * RIGHT + y * UP)

        b_hat = np.array([np.cos(b_ang), np.sin(b_ang)])
        b_tip = cpt(*(b_len * b_hat))
        b_arrow = Arrow(origin, b_tip, buff=0, color=ORANGE, stroke_width=6)
        b_lab = MathTex(r"\vec b", font_size=24, color=ORANGE)
        b_lab.next_to(b_tip, UP + RIGHT, buff=0.16)

        self.play(Create(axes), run_time=1.2)
        self.play(Create(b_arrow), Write(b_lab), run_time=1.1)
        self.wait(1.4)

        a_angle = ValueTracker(75 * DEGREES)

        def state():
            """返回 (a 端点场景坐标, 垂足场景坐标, 带符号投影长度（数据单位）)"""
            a = a_angle.get_value()
            tip_d = np.array([a_len * np.cos(a), a_len * np.sin(a)])
            s = float(np.dot(tip_d, b_hat))
            return cpt(*tip_d), cpt(*(s * b_hat)), s

        a_arrow = always_redraw(
            lambda: Arrow(origin, state()[0], buff=0, color=PRIMARY, stroke_width=6)
        )
        perp = always_redraw(
            lambda: DashedLine(state()[0], state()[1], color=GRAY, stroke_width=2)
        )
        proj_seg = always_redraw(
            lambda: Line(origin, state()[1], color=RED_H, stroke_width=10)
        )
        theta_arc = always_redraw(
            lambda: Arc(
                radius=0.80, start_angle=b_ang,
                angle=a_angle.get_value() - b_ang,
                arc_center=origin, color=WHITE, stroke_width=3,
            )
        )

        def right_angle_marker():
            tip_s, f_s, _ = state()
            v = tip_s - f_s
            n = float(np.linalg.norm(v))
            if n < 1e-4:
                return VMobject()
            vhat = v / n
            sz = 0.26
            b_hat3 = np.array([b_hat[0], b_hat[1], 0.0])
            pts = [f_s, f_s + sz * b_hat3,
                   f_s + sz * b_hat3 + sz * vhat, f_s + sz * vhat]
            return Polygon(*pts, color=WHITE, stroke_width=2, fill_opacity=0)

        ra_mark = always_redraw(right_angle_marker)

        a_lab = always_redraw(
            lambda: MathTex(r"\vec a", font_size=24, color=PRIMARY).next_to(
                state()[0], UP + LEFT, buff=0.14,
            )
        )
        theta_lab = always_redraw(
            lambda: MathTex(r"\theta", font_size=24, color=WHITE).move_to(
                origin + unit * 1.22 * np.array([
                    np.cos((a_angle.get_value() + b_ang) / 2),
                    np.sin((a_angle.get_value() + b_ang) / 2),
                    0.0,
                ])
            )
        )
        proj_lab = always_redraw(
            lambda: MathTex(
                r"\mathrm{proj}_{\vec b}\vec a", font_size=22, color=RED_H,
            ).move_to(
                (origin + state()[1]) / 2
                + 0.55 * np.array([-np.sin(b_ang), -np.cos(b_ang), 0.0])
            )
        )

        self.play(Create(a_arrow), run_time=1.1)
        self.play(Create(perp), Create(proj_seg), run_time=1.1)
        self.play(Create(theta_arc), run_time=0.9)
        self.play(Write(a_lab), Write(theta_lab), Write(proj_lab), run_time=1.0)
        self.play(Create(ra_mark), run_time=0.7)
        self.wait(2.6)

        # 右栏：数量积公式
        dot_eq = MathTex(
            r"\vec a\cdot\vec b=|\vec a||\vec b|\cos\theta",
            font_size=29, color=ACCENT,
        ).move_to((3.05, 2.45, 0))
        self.play(Write(dot_eq), run_time=1.6)
        self.wait(1.6)

        status1 = Text(
            "锐角：投影为正，与 b 同向",
            font=FONT_NAME, font_size=22, color=SECONDARY,
        ).move_to((3.05, 0.55, 0))
        self.play(Write(status1), run_time=1.0)
        self.wait(1.8)

        # ======================================================
        # 第二幕：θ → 90°，投影收缩为零
        # ======================================================
        title2 = Text(
            "2. θ 变成直角：投影收缩为零",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=1.0)

        status2 = Text(
            "直角：投影长度为零",
            font=FONT_NAME, font_size=22, color=ACCENT,
        ).move_to((3.05, 0.55, 0))
        self.play(ReplacementTransform(status1, status2), run_time=0.9)

        self.play(a_angle.animate.set_value(108 * DEGREES), run_time=3.2)
        self.wait(2.4)

        # ======================================================
        # 第三幕：θ → 钝角，投影翻转为负
        # ======================================================
        title3 = Text(
            "3. θ 变成钝角：投影翻转为负",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title2, title3), run_time=1.0)

        status3 = Text(
            "钝角：投影为负，与 b 反向",
            font=FONT_NAME, font_size=22, color=RED_H,
        ).move_to((3.05, 0.55, 0))
        self.play(ReplacementTransform(status2, status3), run_time=0.9)

        self.play(a_angle.animate.set_value(148 * DEGREES), run_time=3.2)
        self.wait(2.4)

        # ======================================================
        # 定格：投影公式
        # ======================================================
        proj_eq = MathTex(
            r"\mathrm{proj}_{\vec b}\vec a=\frac{\vec a\cdot\vec b}{|\vec b|^2}\vec b",
            font_size=26, color=RED_H,
        ).move_to((3.05, 1.40, 0))
        self.play(FadeOut(status3), run_time=0.5)
        self.play(Write(proj_eq), run_time=1.6)
        self.wait(1.2)

        caption = Text(
            "投影是带符号的：θ 为钝角时 cosθ < 0",
            font=FONT_NAME, font_size=22, color=ACCENT,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(caption), run_time=1.4)
        self.wait(5.0)
