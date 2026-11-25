"""第 2 章 · 三角与复平面旋转 —— 场景 3：虚数单位 i 与欧拉公式的诞生

叙事：一维实数轴上，绿色单位向量 1 乘 -1 逆时针转 180°（半圆弧标注），
      再乘一次回到 1 —— 提出问题：什么数能只转 90°？
      → 乘 i 逆时针转 90°，虚轴 Im 动态生长，落点标 i；再乘 i 落回 -1，
        浮现 i×i = -1
      → 淡入灰色虚线单位圆，向量回到 (1,0)，橙色切线速度箭头 +i 与位置垂直；
        θ 从 0 到 2π 匀速旋转并留下轨迹，速度箭头始终垂直；
        右上角同步写 e^{iθ}=cosθ+i sinθ；在 θ=π 处暂停弹出 e^{iπ}+1=0。

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene3_imaginary_genesis.py ImaginaryAndEulerGenesis
字体：中文统一 Noto Sans Mono CJK SC；数学一律 MathTex（原始字符串）。
"""

from manim import *
import numpy as np

FONT_NAME = "Noto Sans Mono CJK SC"
BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"


class ImaginaryAndEulerGenesis(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ======================================================
        # 第一幕：一维实数轴 —— 乘 -1 就是逆时针转 180°
        # ======================================================
        title1 = Text(
            "1. 实数轴上的乘法：乘以负一就是掉头",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=1.2)
        self.wait(0.5)

        line = NumberLine(
            x_range=[-3.5, 3.5, 1],
            length=7.0,
            include_numbers=True,
            include_tip=True,
            label_direction=DOWN,
            color=WHITE,
            stroke_width=2,
        ).shift(DOWN * 0.2)
        origin = line.n2p(0)
        ulen = line.n2p(1)[0] - origin[0]

        self.play(Create(line), run_time=1.4)
        self.play(Write(line.numbers), run_time=0.9)
        self.wait(0.4)

        ang = ValueTracker(0.0)

        def tip_now():
            a = ang.get_value()
            return origin + ulen * (np.cos(a) * RIGHT + np.sin(a) * UP)

        vec = always_redraw(lambda: Arrow(
            origin, tip_now(), buff=0, color=SECONDARY, stroke_width=6,
        ))
        arc = always_redraw(lambda: Arc(
            radius=0.55, start_angle=0, angle=max(ang.get_value(), 1e-3),
            color=ACCENT, stroke_width=4, arc_center=origin,
        ))
        self.add(vec, arc)
        self.wait(0.5)

        # 第一次乘 -1：逆时针转 180°
        self.play(ang.animate.set_value(PI), run_time=2.6, rate_func=linear)
        deg180 = MathTex(r"180^\circ", font_size=22, color=ACCENT)
        deg180.move_to(origin + UP * 0.85)
        self.play(Write(deg180), run_time=0.8)
        self.wait(1.2)

        # 再乘一次 -1：继续逆时针转 180°，回到 1
        self.play(ang.animate.set_value(2 * PI), run_time=2.6, rate_func=linear)
        self.wait(1.0)

        question = Text(
            "乘 -1 转 180°，那什么数能只转 90°？",
            font=FONT_NAME, font_size=24, color=ACCENT,
        ).move_to((0, 2.9, 0))
        self.play(Write(question), run_time=1.4)
        self.wait(2.2)

        # ======================================================
        # 第二幕：乘 i 转 90° —— 虚轴诞生，张开二维复平面
        # ======================================================
        title2 = Text(
            "2. 乘虚数单位 i：转出直角，张开虚轴",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(
            FadeOut(arc), FadeOut(deg180), FadeOut(question),
            ReplacementTransform(title1, title2),
            run_time=1.0,
        )

        ang.set_value(0.0)      # 2π 与 0 同位置，无跳跃
        mult_txt = Text(
            "乘以 i：向量绕原点逆时针旋转",
            font=FONT_NAME, font_size=24, color=WHITE,
        ).move_to((0, 2.9, 0))
        self.play(Write(mult_txt), run_time=1.2)

        arc2 = always_redraw(lambda: Arc(
            radius=0.55, start_angle=0, angle=max(ang.get_value(), 1e-3),
            color=ACCENT, stroke_width=4, arc_center=origin,
        ))
        deg90 = MathTex(r"90^\circ", font_size=20, color=ACCENT)
        deg90.add_updater(lambda m: m.move_to(
            origin + 0.82 * np.cos(ang.get_value() / 2) * RIGHT
            + 0.82 * np.sin(ang.get_value() / 2) * UP
        ))
        self.add(arc2, deg90)
        self.wait(0.4)

        self.play(ang.animate.set_value(PI / 2), run_time=2.4, rate_func=linear)

        # 直角符号（实轴正方向与虚轴正方向之间）
        sq = VGroup(
            Line(
                origin + 0.4 * RIGHT, origin + 0.4 * (RIGHT + UP),
                color=ACCENT, stroke_width=3,
            ),
            Line(
                origin + 0.4 * (RIGHT + UP), origin + 0.4 * UP,
                color=ACCENT, stroke_width=3,
            ),
        )
        self.play(Create(sq), run_time=0.8)

        # 虚轴生长出来，一维数轴张开成二维复平面
        im_axis = DoubleArrow(
            origin + DOWN * 2.2, origin + UP * 2.2,
            color=WHITE, stroke_width=2, tip_length=0.16,
        )
        im_label = MathTex(r"\mathrm{Im}", font_size=24, color=WHITE).next_to(
            im_axis.get_end(), RIGHT, buff=0.12,
        )
        re_label = MathTex(r"\mathrm{Re}", font_size=24, color=WHITE).next_to(
            line.get_end(), RIGHT + UP, buff=0.1,
        )
        self.play(Create(im_axis), run_time=1.4)
        self.play(Write(im_label), Write(re_label), run_time=0.9)

        i_dot = Dot(origin + UP * ulen, radius=0.07, color=SECONDARY)
        i_label = MathTex(r"i", font_size=30, color=SECONDARY).next_to(
            i_dot, LEFT, buff=0.18,
        )
        self.play(FadeIn(i_dot), Write(i_label), run_time=0.9)
        self.wait(1.2)

        # 再乘一次 i：从 i 继续逆时针转 90°，落回 -1
        self.play(ang.animate.set_value(PI), run_time=2.4, rate_func=linear)
        i2_eq = MathTex(
            r"i\times i=-1\ \Longrightarrow\ i^2=-1",
            font_size=30, color=ACCENT,
        ).move_to((0, 2.8, 0))
        self.play(FadeOut(mult_txt), run_time=0.5)
        self.play(Write(i2_eq), run_time=1.4)
        self.wait(2.0)

        # ======================================================
        # 第三幕：切线速度始终垂直 —— 欧拉公式诞生
        # ======================================================
        title3 = Text(
            "3. 切线速度始终垂直：欧拉公式诞生",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(
            FadeOut(arc2), FadeOut(deg90), FadeOut(sq),
            FadeOut(i2_eq), FadeOut(i_dot), FadeOut(i_label),
            ReplacementTransform(title2, title3),
            run_time=1.0,
        )

        # 继续逆时针转回起点 (1, 0)
        self.play(ang.animate.set_value(2 * PI), run_time=1.8, rate_func=linear)
        ang.set_value(0.0)

        unit_circle = DashedVMobject(
            Circle(radius=ulen, color=GRAY, stroke_width=2), num_dashes=48,
        ).move_to(origin)
        self.play(FadeIn(unit_circle), run_time=1.2)

        vel_caption = Text(
            "切线速度始终垂直于位置向量",
            font=FONT_NAME, font_size=24, color=WHITE,
        ).move_to((0, 2.9, 0))
        self.play(Write(vel_caption), run_time=1.2)
        self.wait(0.8)

        # 位置向量 + 轨迹 + 切线速度箭头（始终垂直）
        trail = always_redraw(lambda: Arc(
            radius=ulen, start_angle=0, angle=max(ang.get_value(), 1e-3),
            color=PRIMARY, stroke_width=4, arc_center=origin,
        ))

        def vel_end():
            a = ang.get_value()
            t = tip_now()
            return t + 0.6 * ulen * (-np.sin(a) * RIGHT + np.cos(a) * UP)

        vel = always_redraw(lambda: Arrow(
            tip_now(), vel_end(), buff=0, color=ORANGE, stroke_width=5,
        ))
        # “+i” 只在起点处标注（此时速度方向确实为 +i），旋转开始后淡出
        vel_lab = MathTex(r"+i", font_size=24, color=ORANGE).move_to(
            origin + ulen * RIGHT + 0.6 * ulen * UP + RIGHT * 0.3
        )
        self.add(trail, vel, vel_lab)

        euler_formula = MathTex(
            r"e^{i\theta}=\cos\theta+i\sin\theta",
            font_size=26, color=WHITE,
        ).to_corner(UR, buff=0.35)
        self.play(Write(euler_formula), run_time=1.4)
        self.wait(0.8)
        self.play(FadeOut(vel_lab), run_time=0.6)

        # θ：0 → π
        self.play(ang.animate.set_value(PI), run_time=4.5, rate_func=linear)
        self.wait(0.8)
        identity = MathTex(r"e^{i\pi}+1=0", font_size=32, color=ACCENT).move_to((0, 2.7, 0))
        self.play(Write(identity), run_time=1.2)
        self.wait(2.0)
        self.play(FadeOut(identity), run_time=0.6)

        # θ：π → 2π，完成整圈
        self.play(ang.animate.set_value(2 * PI), run_time=4.5, rate_func=linear)
        self.wait(2.5)
