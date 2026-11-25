"""第 2 章 · 三角与复平面旋转 —— 场景 2：乘以 i 秒杀诱导公式

叙事：复平面单位圆上第一象限向量 z = cosθ + i sinθ（横坐标蓝、纵坐标绿）
      → 乘 i = 乘 e^{iπ/2}，绕原点逆时针精确转 90°（标直角符号与 90° 弧）
      → 绿线倒向实轴负半轴成 -sinθ，蓝线竖到虚轴正半轴成 cosθ
      → 定格诱导公式 cos(θ+π/2) = -sinθ，sin(θ+π/2) = cosθ。

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene2_multiply_by_i.py MultiplyByIInduction
字体：中文统一 Noto Sans Mono CJK SC；数学一律 MathTex（原始字符串）。
"""

from manim import *
import numpy as np

FONT_NAME = "Noto Sans Mono CJK SC"
BG = "#1C1C1C"
PRIMARY = "#58C4DD"     # 蓝：cosθ
SECONDARY = "#83C167"   # 绿：sinθ
ACCENT = "#FFFF00"


def rot2(p, a):
    """把二维点 p 绕原点逆时针旋转角度 a，返回三维向量"""
    c, s = np.cos(a), np.sin(a)
    return np.array([c * p[0] - s * p[1], s * p[0] + c * p[1], 0.0])


class MultiplyByIInduction(Scene):
    def construct(self):
        self.camera.background_color = BG
        th = PI / 5       # 36°，第一象限任意角

        # ======================================================
        # 第一幕：单位向量 z = cosθ + i sinθ 的两段坐标
        # ======================================================
        title1 = Text(
            "1. 复平面单位圆上的任意向量",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=1.2)
        self.wait(0.5)

        axes = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=4.6,
            y_length=4.6,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "color": WHITE,
                "stroke_width": 2,
            },
        ).shift(LEFT * 1.75 + DOWN * 0.3)
        origin = axes.c2p(0, 0)
        unit = axes.c2p(1, 0)[0] - origin[0]

        def cpt(x, y):
            return origin + unit * (x * RIGHT + y * UP)

        re_label = MathTex(r"\mathrm{Re}", font_size=24, color=WHITE).next_to(
            axes.x_axis.get_end(), RIGHT + DOWN, buff=0.08,
        )
        im_label = MathTex(r"\mathrm{Im}", font_size=24, color=WHITE).next_to(
            axes.y_axis.get_end(), LEFT + UP, buff=0.08,
        )

        circle = Circle(radius=unit, color=PRIMARY, stroke_width=3).move_to(origin)

        tip = cpt(np.cos(th), np.sin(th))
        z0 = Arrow(origin, tip, buff=0, color=WHITE, stroke_width=6)
        tip_dot = Dot(tip, radius=0.06, color=WHITE)

        seg_blue0 = Line(origin, cpt(np.cos(th), 0), color=PRIMARY, stroke_width=9)
        seg_green0 = Line(cpt(np.cos(th), 0), tip, color=SECONDARY, stroke_width=9)

        cos_lab0 = MathTex(r"\cos\theta", font_size=24, color=PRIMARY)
        cos_lab0.move_to(cpt(0.5 * np.cos(th), 0) + DOWN * 0.38)
        sin_lab0 = MathTex(r"\sin\theta", font_size=24, color=SECONDARY)
        sin_lab0.move_to(cpt(np.cos(th), 0.5 * np.sin(th)) + RIGHT * 0.55)

        z_label = MathTex(
            r"z=\cos\theta+i\sin\theta", font_size=24, color=WHITE,
        ).move_to(cpt(0.0, 1.72))

        self.play(Create(axes), run_time=1.4)
        self.play(Write(re_label), Write(im_label), run_time=0.8)
        self.play(Create(circle), run_time=1.2)
        self.play(Create(z0), FadeIn(tip_dot), run_time=1.2)
        self.play(Create(seg_blue0), Create(seg_green0), run_time=1.2)
        self.play(Write(cos_lab0), Write(sin_lab0), run_time=1.0)
        self.play(Write(z_label), run_time=1.0)
        self.wait(1.2)

        # ======================================================
        # 第二幕：乘 i —— 逆时针精确旋转 90°
        # ======================================================
        title2 = Text(
            "2. 乘以 i：逆时针精确旋转 90°",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=0.9)

        op1 = MathTex(
            r"i\cdot z=e^{i\frac{\pi}{2}}\cdot e^{i\theta}", font_size=26,
        ).move_to((3.7, 2.55, 0))
        op2 = MathTex(
            r"=e^{i(\theta+\frac{\pi}{2})}", font_size=26,
        ).move_to((3.7, 2.02, 0))
        self.play(Write(op1), run_time=1.2)
        self.play(Write(op2), run_time=1.2)

        # 原位置退成淡影，作为旋转前参照
        self.play(
            z0.animate.set_opacity(0.3),
            tip_dot.animate.set_opacity(0.3),
            FadeOut(seg_blue0), FadeOut(seg_green0),
            FadeOut(cos_lab0), FadeOut(sin_lab0),
            run_time=0.7,
        )

        t_rot = ValueTracker(0.0)

        def rot_pt(base, a):
            return origin + unit * rot2(np.array(base, dtype=float), a)

        z_rot = always_redraw(lambda: Arrow(
            origin, rot_pt([np.cos(th), np.sin(th)], t_rot.get_value()),
            buff=0, color=ORANGE, stroke_width=6,
        ))
        seg_b = always_redraw(lambda: Line(
            origin, rot_pt([np.cos(th), 0.0], t_rot.get_value()),
            color=PRIMARY, stroke_width=9,
        ))
        seg_g = always_redraw(lambda: Line(
            rot_pt([np.cos(th), 0.0], t_rot.get_value()),
            rot_pt([np.cos(th), np.sin(th)], t_rot.get_value()),
            color=SECONDARY, stroke_width=9,
        ))
        arc_rot = always_redraw(lambda: Arc(
            radius=0.42 * unit, start_angle=th,
            angle=max(t_rot.get_value(), 1e-3),
            color=ACCENT, stroke_width=4, arc_center=origin,
        ))
        deg_label = MathTex(r"90^\circ", font_size=20, color=ACCENT)

        def deg_pos():
            a = th + t_rot.get_value() / 2
            return cpt(0.68 * np.cos(a), 0.68 * np.sin(a))

        deg_label.add_updater(lambda m: m.move_to(deg_pos()))

        # 直角符号：夹在初始方向与旋转后方向之间
        L = 0.3
        square = VGroup(
            Line(
                rot_pt([L, 0.0], th), rot_pt([L, L], th),
                color=ACCENT, stroke_width=3,
            ),
            Line(
                rot_pt([L, L], th), rot_pt([0.0, L], th),
                color=ACCENT, stroke_width=3,
            ),
        )

        self.add(z_rot, seg_b, seg_g, arc_rot, deg_label)
        self.wait(0.4)
        self.play(
            t_rot.animate.set_value(PI / 2),
            run_time=3.2, rate_func=linear,
        )
        self.play(Create(square), run_time=0.8)
        self.wait(1.2)

        # ======================================================
        # 第三幕：读出新坐标 —— 诱导公式
        # ======================================================
        deg_label.clear_updaters()
        self.play(
            FadeOut(arc_rot), FadeOut(deg_label), FadeOut(square),
            FadeOut(z0), FadeOut(tip_dot),
            run_time=0.7,
        )

        tip_new = cpt(-np.sin(th), np.cos(th))
        proj_x = DashedLine(tip_new, cpt(-np.sin(th), 0), color=GRAY, stroke_width=2)
        proj_y = DashedLine(tip_new, cpt(0, np.cos(th)), color=GRAY, stroke_width=2)

        seg_green_ax = Line(
            origin, cpt(-np.sin(th), 0), color=SECONDARY, stroke_width=9,
        )
        neg_sin_lab = MathTex(r"-\sin\theta", font_size=24, color=SECONDARY)
        neg_sin_lab.move_to(cpt(-0.5 * np.sin(th), 0) + DOWN * 0.38)

        cos_lab_new = MathTex(r"\cos\theta", font_size=24, color=PRIMARY)
        cos_lab_new.move_to(cpt(0, 0.5 * np.cos(th)) + RIGHT * 0.62)

        self.play(Create(proj_x), Create(proj_y), run_time=1.0)
        self.play(Create(seg_green_ax), Write(neg_sin_lab), run_time=1.2)
        self.play(Write(cos_lab_new), run_time=0.9)
        self.wait(0.5)

        form1 = MathTex(
            r"\cos(\theta+\frac{\pi}{2})=-\sin\theta",
            font_size=26, color=PRIMARY,
        ).move_to((3.7, 0.85, 0))
        form2 = MathTex(
            r"\sin(\theta+\frac{\pi}{2})=\cos\theta",
            font_size=26, color=SECONDARY,
        ).move_to((3.7, 0.1, 0))

        self.play(Write(form1), run_time=1.4)
        self.play(Write(form2), run_time=1.4)
        self.wait(1.0)

        caption = Text(
            "乘以 i = 逆时针转 90°：诱导公式一眼读出",
            font=FONT_NAME, font_size=22, color=ACCENT,
        ).to_edge(DOWN, buff=0.45)
        self.play(Write(caption), run_time=1.2)
        self.wait(2.0)
