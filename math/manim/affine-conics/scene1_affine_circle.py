"""第 4 章 · 立体几何与圆锥曲线 —— 场景 1：仿射压缩把圆变成椭圆

叙事：坐标系中画半径 a=3 的蓝色圆 x^2+y^2=9，及其内接最大面积的黄色正三角形，
      右栏标出 S_max = (3√3/4)a²
      → 施加仿射压缩 [[1,0],[0,0.6]]（b/a = 0.6），圆平滑压成
        长半轴 3、短半轴 1.8 的绿色椭圆，内部三角形同步变形
      → 高亮仿射不变量 S_ell = (b/a)·S_circ = (3√3/4)ab
      → 定格：仿射变换保持共线、平行、中点与面积比

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene1_affine_circle.py AffineCircleToEllipse
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


class AffineCircleToEllipse(Scene):
    def construct(self):
        self.camera.background_color = BG
        A = 3.0                 # 圆的半径 a
        RATIO = 0.6             # b / a

        # ----------------------------------------------------------
        # 布局：左侧坐标系（圆 + 内接正三角形），右侧公式面板
        # ----------------------------------------------------------
        axes = Axes(
            x_range=[-3.3, 3.3, 1],
            y_range=[-3.3, 3.3, 1],
            x_length=5.2,
            y_length=5.2,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "color": GRAY,
                "stroke_width": 2,
            },
        ).shift(LEFT * 1.35 + DOWN * 0.25)
        origin = axes.c2p(0, 0)
        unit = axes.c2p(1, 0)[0] - origin[0]

        def cpt(x, y):
            """数据坐标 → 场景坐标（统一 3D）"""
            return origin + unit * (np.array([x, y, 0.0]))

        # ==========================================================
        # 第一幕：圆与它的内接最大面积正三角形
        # ==========================================================
        title1 = Text(
            "1. 半径 a=3 的圆：内接正三角形面积最大",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=1.1)
        self.wait(0.5)

        circle = Circle(radius=A * unit, color=PRIMARY, stroke_width=4).move_to(origin)

        # 内接正三角形：顶点取 90° / 210° / 330°
        tri_angles = [PI / 2, PI / 2 + TAU / 3, PI / 2 + 2 * TAU / 3]
        tri_pts = [cpt(A * np.cos(t), A * np.sin(t)) for t in tri_angles]
        triangle = Polygon(
            *tri_pts, color=ACCENT, stroke_width=4, fill_opacity=0.10,
        )

        # ==========================================================
        # 第一幕：圆与它的内接最大面积正三角形
        # ==========================================================
        self.play(Create(axes), run_time=1.3)
        self.play(Create(circle), run_time=1.4)
        self.wait(0.5)

        panel1 = VGroup(
            VGroup(Text("圆", font=FONT_NAME, font_size=22, color=PRIMARY),
                   MathTex(r"x^2+y^2=a^2=9", font_size=24, color=WHITE)
                   ).arrange(RIGHT, buff=0.18),
            Text("内接正三角形面积最大", font=FONT_NAME,
                 font_size=22, color=SECONDARY),
            MathTex(r"S_{\max}=\dfrac{3\sqrt{3}}{4}a^2=\dfrac{27\sqrt{3}}{4}",
                    font_size=24, color=ACCENT),
        ).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        panel1.move_to((2.20, 1.15, 0), aligned_edge=LEFT)
        self.play(Write(panel1), run_time=1.5)
        self.wait(0.6)

        self.play(Create(triangle), run_time=1.4)
        self.wait(3.0)

        # ==========================================================
        # 第二幕：施加仿射压缩 y → 0.6y
        # ==========================================================
        title2 = Text(
            "2. 仿射压缩：y 变为 0.6y（b/a = 0.6）",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=1.0)

        mat = MathTex(
            r"\begin{pmatrix}1&0\\[2pt]0&0.6\end{pmatrix}",
            font_size=30, color=WHITE,
        )
        mat_caption = VGroup(
            Text("仿射矩阵", font=FONT_NAME, font_size=21, color=GRAY),
            mat,
        ).arrange(RIGHT, buff=0.22)
        mat_row = VGroup(
            mat_caption,
            MathTex(r"b=0.6a=1.8,\quad \frac{b}{a}=0.6", font_size=24, color=ACCENT),
        ).arrange(DOWN, buff=0.28)
        mat_row.move_to((2.20, 1.35, 0), aligned_edge=LEFT)

        self.play(FadeOut(panel1), run_time=0.6)
        self.play(Write(mat_row), run_time=1.4)
        self.wait(0.8)

        # 形变动画：关于原点沿 y 方向压缩到 0.6，圆变绿
        self.play(
            circle.animate.stretch(RATIO, dim=1, about_point=origin),
            circle.animate.set_color(SECONDARY),
            triangle.animate.stretch(RATIO, dim=1, about_point=origin),
            run_time=3.4, rate_func=smooth,
        )
        self.wait(0.6)

        ellipse_eq = VGroup(
            Text("椭圆", font=FONT_NAME, font_size=22, color=SECONDARY),
            MathTex(r"\frac{x^2}{9}+\frac{y^2}{3.24}=1", font_size=24, color=WHITE),
        ).arrange(RIGHT, buff=0.18)
        semi_lab = VGroup(
            MathTex(r"a=3,\ b=1.8", font_size=24, color=ACCENT),
        )
        ellipse_row = VGroup(ellipse_eq, semi_lab).arrange(
            DOWN, buff=0.26, aligned_edge=LEFT,
        )
        ellipse_row.move_to((2.20, -0.35, 0), aligned_edge=LEFT)
        self.play(Write(ellipse_row), run_time=1.3)
        self.wait(2.6)

        # ==========================================================
        # 第三幕：仿射不变量 —— 面积比等于 b/a
        # ==========================================================
        title3 = Text(
            "3. 仿射不变量：面积比 = b/a",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title2, title3), run_time=1.0)

        self.play(FadeOut(mat_row), FadeOut(ellipse_row), run_time=0.6)

        inv1 = MathTex(
            r"S_{\text{ell}}=\frac{b}{a}\,S_{\text{circ}}",
            font_size=30, color=WHITE,
        )
        inv2 = MathTex(
            r"S_{\text{ell}}=\frac{3\sqrt{3}}{4}\,ab",
            font_size=30, color=ACCENT,
        )
        inv_note = Text(
            "同步缩放，面积比不变",
            font=FONT_NAME, font_size=20, color=SECONDARY,
        )
        inv_group = VGroup(inv1, inv2, inv_note).arrange(
            DOWN, buff=0.34, aligned_edge=LEFT,
        )
        inv_group.move_to((2.20, 0.95, 0), aligned_edge=LEFT)
        inv_box = SurroundingRectangle(inv_group, color=ACCENT,
                                       buff=0.22, stroke_width=3)

        self.play(Write(inv1), run_time=1.3)
        self.play(Write(inv2), run_time=1.3)
        self.play(Write(inv_note), run_time=1.2)
        self.play(Create(inv_box), run_time=0.9)
        self.wait(3.2)

        # ==========================================================
        # 第四幕：定格 —— 仿射变换保持什么
        # ==========================================================
        title4 = Text(
            "4. 定格：仿射变换保持共线、平行、中点与面积比",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title3, title4), run_time=1.0)

        self.play(FadeOut(inv_group), run_time=0.6)

        keep_rows = VGroup(
            VGroup(Text("共线", font=FONT_NAME, font_size=22, color=SECONDARY),
                   Text("共线的点仍共线", font=FONT_NAME,
                        font_size=21, color=WHITE)).arrange(RIGHT, buff=0.28),
            VGroup(Text("平行", font=FONT_NAME, font_size=22, color=SECONDARY),
                   Text("平行线仍平行", font=FONT_NAME,
                        font_size=21, color=WHITE)).arrange(RIGHT, buff=0.28),
            VGroup(Text("中点", font=FONT_NAME, font_size=22, color=SECONDARY),
                   Text("线段中点仍是中点", font=FONT_NAME,
                        font_size=21, color=WHITE)).arrange(RIGHT, buff=0.28),
            VGroup(Text("面积比", font=FONT_NAME, font_size=22, color=SECONDARY),
                   Text("任意两图形面积比不变", font=FONT_NAME,
                        font_size=21, color=WHITE)).arrange(RIGHT, buff=0.28),
        ).arrange(DOWN, buff=0.30, aligned_edge=LEFT)
        keep_rows.move_to((2.20, 1.10, 0), aligned_edge=LEFT)

        self.play(Write(keep_rows), run_time=1.8)
        self.wait(1.0)

        caption = Text(
            "仿射变换保持共线、平行、中点与面积比",
            font=FONT_NAME, font_size=24, color=ACCENT,
        ).to_edge(DOWN, buff=0.45)
        self.play(Write(caption), run_time=1.3)
        self.wait(4.0)
