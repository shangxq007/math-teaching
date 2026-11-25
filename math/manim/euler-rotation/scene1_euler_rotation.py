"""第 2 章 · 三角与复平面旋转 —— 场景 1：复平面旋转与两角和公式

叙事：复平面单位圆上的绿色向量 z1 = e^{iα}（α = 30°）向实轴、虚轴作虚线投影，
      标出坐标 (cos α, sin α)
      → 乘上旋转因子 e^{iβ}（β = 40°），向量绕原点逆时针旋转，黄色扇形弧标角，
        落成橙色向量 z2 = e^{i(α+β)}
      → 从 z2 端点向两轴作垂线，高亮 cos(α+β)（红）与 sin(α+β)（青）；
        右栏同步展开 (cos α + i sin α)(cos β + i sin β) 并对比实部与虚部，
        定格两角和公式。

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene1_euler_rotation.py EulerRotationSumFormula
字体：中文统一 Noto Sans Mono CJK SC；数学一律 MathTex（原始字符串）。
"""

from manim import *
import numpy as np

FONT_NAME = "Noto Sans Mono CJK SC"
BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"
RED_H = "#FF5252"      # 实部 / cos(α+β) 高亮
CYAN_H = "#00E5FF"     # 虚部 / sin(α+β) 高亮


class EulerRotationSumFormula(Scene):
    def construct(self):
        self.camera.background_color = BG
        alpha = PI / 6          # 30°
        beta = 2 * PI / 9       # 40°

        # ======================================================
        # 第一幕：复平面单位圆与 z1 = e^{iα} 的投影
        # ======================================================
        title1 = Text(
            "1. 复平面单位圆：单位向量的坐标投影",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=1.2)
        self.wait(0.6)

        axes = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=4.8,
            y_length=4.8,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "color": WHITE,
                "stroke_width": 2,
            },
        ).shift(LEFT * 3.45 + DOWN * 0.25)
        origin = axes.c2p(0, 0)
        unit = axes.c2p(1, 0)[0] - origin[0]

        def cpt(x, y):
            """复平面直角坐标 → 场景坐标"""
            return origin + unit * (x * RIGHT + y * UP)

        re_label = MathTex(r"\mathrm{Re}", font_size=24, color=WHITE).next_to(
            axes.x_axis.get_end(), RIGHT + DOWN, buff=0.08,
        )
        im_label = MathTex(r"\mathrm{Im}", font_size=24, color=WHITE).next_to(
            axes.y_axis.get_end(), LEFT + UP, buff=0.08,
        )

        circle = Circle(radius=unit, color=PRIMARY, stroke_width=3).move_to(origin)

        tip1 = cpt(np.cos(alpha), np.sin(alpha))
        z1 = Arrow(origin, tip1, buff=0, color=SECONDARY, stroke_width=6)
        tip_dot1 = Dot(tip1, radius=0.06, color=SECONDARY)
        proj_x1 = DashedLine(tip1, cpt(np.cos(alpha), 0), color=GRAY, stroke_width=2)
        proj_y1 = DashedLine(tip1, cpt(0, np.sin(alpha)), color=GRAY, stroke_width=2)

        coord_label = MathTex(
            r"(\cos\alpha,\ \sin\alpha)", font_size=24, color=WHITE,
        ).next_to(tip1, UP + RIGHT, buff=0.2)

        z1_label = MathTex(r"z_1=e^{i\alpha}", font_size=24, color=SECONDARY)
        # 标签放在单位圆左上方空白处，避免与 z2 标签互相压盖
        z1_label.move_to(cpt(-1.32, 1.15))

        alpha_arc = Arc(
            radius=0.42 * unit, start_angle=0, angle=alpha,
            color=WHITE, stroke_width=3, arc_center=origin,
        )
        alpha_label = MathTex(r"\alpha=30^\circ", font_size=20, color=WHITE)
        alpha_label.move_to(cpt(0.62 * np.cos(alpha / 2), 0.62 * np.sin(alpha / 2)))

        self.play(Create(axes), run_time=1.4)
        self.play(Write(re_label), Write(im_label), run_time=0.8)
        self.play(Create(circle), run_time=1.2)
        self.wait(0.6)
        self.play(Create(z1), FadeIn(tip_dot1), run_time=1.2)
        self.play(Create(proj_x1), Create(proj_y1), run_time=1.0)
        self.play(Write(coord_label), Write(z1_label), run_time=1.2)
        self.play(Create(alpha_arc), Write(alpha_label), run_time=1.2)
        self.wait(3.5)

        # ======================================================
        # 第二幕：乘上 e^{iβ} —— 绕原点逆时针旋转 β 角
        # ======================================================
        title2 = Text(
            "2. 乘上旋转因子：向量绕原点逆时针旋转",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=1.0)

        eq = MathTex(
            r"z_1\cdot e^{i\beta}=e^{i\alpha}\cdot e^{i\beta}=e^{i(\alpha+\beta)}",
            font_size=25, color=WHITE,
        ).move_to((3.0, 2.95, 0))
        self.play(Write(eq), run_time=1.4)

        # 原向量退成幽灵，作为旋转前的参照
        self.play(
            z1.animate.set_opacity(0.3),
            tip_dot1.animate.set_opacity(0.3),
            z1_label.animate.set_opacity(0.3),
            run_time=0.8,
        )
        self.wait(0.5)

        theta = ValueTracker(alpha)

        def tip_now():
            t = theta.get_value()
            return cpt(np.cos(t), np.sin(t))

        z2 = always_redraw(lambda: Arrow(
            origin, tip_now(), buff=0, color=ORANGE, stroke_width=6,
        ))
        beta_arc = always_redraw(lambda: Arc(
            radius=0.5 * unit, start_angle=alpha,
            angle=max(theta.get_value() - alpha, 1e-3),
            color=ACCENT, stroke_width=4, arc_center=origin,
        ))
        beta_label = MathTex(r"\beta=40^\circ", font_size=20, color=ACCENT)
        beta_label.add_updater(lambda m: m.move_to(
            cpt(0.95 * np.cos(alpha + (theta.get_value() - alpha) / 2),
                0.95 * np.sin(alpha + (theta.get_value() - alpha) / 2))
        ))
        self.add(z2, beta_arc, beta_label)
        self.wait(0.4)

        self.play(
            theta.animate.set_value(alpha + beta),
            run_time=4.0, rate_func=linear,
        )
        self.wait(3.5)

        # ======================================================
        # 第三幕：z2 的投影 与 代数展开对照 —— 两角和公式
        # ======================================================
        title3 = Text(
            "3. 几何投影对照代数展开：两角和公式",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title2, title3), run_time=1.0)

        # 清理上一幕的临时对象
        beta_label.clear_updaters()
        self.play(
            FadeOut(beta_arc), FadeOut(beta_label),
            FadeOut(proj_x1), FadeOut(proj_y1),
            run_time=0.8,
        )

        total = alpha + beta
        tip2 = cpt(np.cos(total), np.sin(total))
        z2_label = MathTex(r"z_2=e^{i(\alpha+\beta)}", font_size=24, color=ORANGE)
        # 与 z1 标签同列竖排，保证两者不重叠
        z2_label.move_to(cpt(-1.32, 0.55))
        proj_x2 = DashedLine(tip2, cpt(np.cos(total), 0), color=GRAY, stroke_width=2)
        proj_y2 = DashedLine(tip2, cpt(0, np.sin(total)), color=GRAY, stroke_width=2)
        cos_seg = Line(
            origin, cpt(np.cos(total), 0), color=RED_H, stroke_width=9,
        )
        sin_seg = Line(
            cpt(np.cos(total), 0), tip2, color=CYAN_H, stroke_width=9,
        )
        cos_lab = MathTex(r"\cos(\alpha+\beta)", font_size=24, color=RED_H)
        cos_lab.move_to(cpt(0.5 * np.cos(total), 0) + DOWN * 0.38)
        sin_lab = MathTex(r"\sin(\alpha+\beta)", font_size=24, color=CYAN_H)
        sin_lab.move_to(
            cpt(np.cos(total), 0.5 * np.sin(total)) + RIGHT * 1.05
        )

        self.play(Write(z2_label), run_time=0.9)
        self.play(Create(proj_x2), Create(proj_y2), run_time=1.0)
        self.play(Create(cos_seg), Write(cos_lab), run_time=1.1)
        self.play(Create(sin_seg), Write(sin_lab), run_time=1.1)
        self.wait(1.5)

        # 右栏：代数展开，与左侧投影同色呼应
        alg1 = MathTex(
            r"(\cos\alpha+i\sin\alpha)(\cos\beta+i\sin\beta)", font_size=24,
        )
        alg2 = MathTex(
            r"=", r"\cos\alpha\cos\beta-\sin\alpha\sin\beta", font_size=24,
        )
        alg2[1].set_color(RED_H)
        alg3 = MathTex(
            r"+i(", r"\sin\alpha\cos\beta+\cos\alpha\sin\beta", r")", font_size=24,
        )
        alg3[1].set_color(CYAN_H)
        alg_group = VGroup(alg1, alg2, alg3).arrange(
            DOWN, buff=0.32, aligned_edge=LEFT,
        )
        alg_group.move_to((-0.35, 1.75, 0), aligned_edge=LEFT)

        self.play(Write(alg1), run_time=1.2)
        self.play(Write(alg2), run_time=1.2)
        self.play(Write(alg3), run_time=1.2)
        self.wait(0.8)

        re_tag = Text("实部", font=FONT_NAME, font_size=21, color=RED_H)
        cos_line = MathTex(
            r"\cos(\alpha+\beta)=\cos\alpha\cos\beta-\sin\alpha\sin\beta",
            font_size=24, color=RED_H,
        )
        re_row = VGroup(re_tag, cos_line).arrange(RIGHT, buff=0.28)
        re_row.move_to((3.0, 0.15, 0))

        im_tag = Text("虚部", font=FONT_NAME, font_size=21, color=CYAN_H)
        sin_line = MathTex(
            r"\sin(\alpha+\beta)=\sin\alpha\cos\beta+\cos\alpha\sin\beta",
            font_size=24, color=CYAN_H,
        )
        im_row = VGroup(im_tag, sin_line).arrange(RIGHT, buff=0.28)
        im_row.move_to((3.0, -0.62, 0))

        self.play(Write(re_row), run_time=1.4)
        self.play(Write(im_row), run_time=1.4)
        self.wait(1.0)

        caption = Text(
            "一次复数乘法 = 旋转 + 投影：两角和公式自然诞生",
            font=FONT_NAME, font_size=22, color=ACCENT,
        ).to_edge(DOWN, buff=0.45)
        self.play(Write(caption), run_time=1.4)
        self.wait(5.0)
