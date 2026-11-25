"""第 5 章 · 数列与离散动态系统 —— 场景 3：特征方向与不动点的同构

叙事：二维线性系统 v_{n+1}=M v_n，M = [[5/4,3/4],[3/4,5/4]]
      两条特征方向：(1,1) 对应 λ1=2（拉伸），(1,-1) 对应 λ2=1/2（压缩）
      → 取 v0=(0.4,0.1) 分解为 c1(1,1)+c2(1,-1)，逐次迭代，
        沿每个特征方向的分量就是等比数列 c_i·λ_i^n
      → 定格：特征向量 = 射影意义下的不动点方向，特征值 = 放大率；
        二阶线性递推 a_{n+2}=p a_{n+1}+q a_n 与矩阵 [[0,1],[q,p]] 同构

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene3_eigen_fixed_point.py EigenvectorToFixedPoint
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
ORANGE_H = "#FF9E40"
GRAY = "#9E9E9E"


class EigenvectorToFixedPoint(Scene):
    def construct(self):
        self.camera.background_color = BG

        axes = Axes(
            x_range=[-2, 3, 1],
            y_range=[-2, 3, 1],
            x_length=5.2,
            y_length=5.2,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "color": GRAY,
                "stroke_width": 2,
            },
        ).shift(LEFT * 1.85 + DOWN * 0.35)
        origin = axes.c2p(0, 0)
        unit = axes.c2p(1, 0)[0] - origin[0]

        def cpt(x, y):
            return origin + unit * np.array([x, y, 0.0])

        # v0 = (0.4, 0.1) = c1*(1,1) + c2*(1,-1)
        C1, C2 = 0.25, 0.15
        LAM1, LAM2 = 2.0, 0.5

        def vseq(n):
            return np.array([C1 * LAM1 ** n + C2 * LAM2 ** n,
                             C1 * LAM1 ** n - C2 * LAM2 ** n])

        # ======================================================
        # 第一幕：矩阵 M 的两个特征方向
        # ======================================================
        title1 = Text(
            "1. 矩阵 M 的两个特征方向：一个拉伸，一个压缩",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=1.1)
        self.wait(0.4)

        eigen1 = Line(cpt(-2, -2), cpt(3, 3), color=SECONDARY, stroke_width=3)
        eigen2 = Line(cpt(-2, 2), cpt(2.2, -2.2), color=ORANGE_H,
                      stroke_width=3)

        lam1_lbl = VGroup(
            MathTex(r"\lambda_1=2", font_size=21, color=SECONDARY),
            Text("拉伸", font=FONT_NAME, font_size=19, color=SECONDARY),
        ).arrange(RIGHT, buff=0.12)
        lam1_lbl.move_to(cpt(-1.55, -1.55) + DOWN * 0.38)
        lam2_lbl = VGroup(
            MathTex(r"\lambda_2=\frac{1}{2}", font_size=21, color=ORANGE_H),
            Text("压缩", font=FONT_NAME, font_size=19, color=ORANGE_H),
        ).arrange(RIGHT, buff=0.12)
        lam2_lbl.move_to(cpt(1.7, -1.7) + DOWN * 0.38)

        self.play(Create(axes), run_time=1.3)
        self.play(Create(eigen1), Create(eigen2), run_time=1.2)
        self.play(Write(lam1_lbl), Write(lam2_lbl), run_time=1.0)
        self.wait(0.5)

        panel1 = VGroup(
            MathTex(r"M=\begin{pmatrix}\frac54&\frac34\\[2pt]"
                    r"\frac34&\frac54\end{pmatrix}", font_size=26,
                    color=WHITE),
            MathTex(r"M\binom{1}{1}=2\binom{1}{1}", font_size=22,
                    color=SECONDARY),
            MathTex(r"M\binom{1}{-1}=\frac12\binom{1}{-1}", font_size=22,
                    color=ORANGE_H),
            Text("特征方向不变，仅长度伸缩", font=FONT_NAME, font_size=20,
                 color=GRAY),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        panel1.move_to((1.2, 1.45, 0), aligned_edge=LEFT)
        self.play(Write(panel1), run_time=1.5)
        self.wait(3.0)

        # ======================================================
        # 第二幕：迭代轨迹沿特征方向分解
        # ======================================================
        title2 = Text(
            "2. 迭代轨迹沿特征方向分解：沿特征方向就是等比数列",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=1.0)

        panel2 = VGroup(
            MathTex(r"v_n=c_1\lambda_1^n\binom{1}{1}"
                    r"+c_2\lambda_2^n\binom{1}{-1}", font_size=23,
                    color=WHITE),
            MathTex(r"c_1\lambda_1^n:\ 0.25,\ 0.5,\ 1,\ 2,\ 4,\cdots",
                    font_size=21, color=SECONDARY),
            MathTex(r"c_2\lambda_2^n:\ 0.15,\ 0.075,\ 0.0375,\ \cdots",
                    font_size=21, color=ORANGE_H),
            Text("两个分量各自是等比数列", font=FONT_NAME, font_size=20,
                 color=GRAY),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        panel2.move_to((1.2, 1.55, 0), aligned_edge=LEFT)

        self.play(FadeOut(panel1), run_time=0.6)
        self.play(Write(panel2), run_time=1.4)
        self.wait(0.5)

        # v0 的平行四边形分解
        v0 = cpt(0.4, 0.1)
        comp1 = cpt(C1, C1)
        comp2 = cpt(C2, -C2)
        d1 = DashedLine(comp1, v0, color=SECONDARY, stroke_width=2)
        d2 = DashedLine(comp2, v0, color=ORANGE_H, stroke_width=2)
        dot_comp1 = Dot(comp1, radius=0.055, color=SECONDARY)
        dot_comp2 = Dot(comp2, radius=0.055, color=ORANGE_H)
        dot_v0 = Dot(v0, radius=0.07, color=ACCENT)
        c1_lbl = MathTex(r"0.25\binom{1}{1}", font_size=18,
                         color=SECONDARY)
        c1_lbl.move_to(comp1 + LEFT * 0.12 + DOWN * 0.3)
        c2_lbl = MathTex(r"0.15\binom{1}{-1}", font_size=18,
                         color=ORANGE_H)
        c2_lbl.move_to(comp2 + RIGHT * 0.05 + DOWN * 0.3)

        self.play(Create(d1), Create(d2), run_time=1.0)
        self.play(FadeIn(dot_comp1), FadeIn(dot_comp2), FadeIn(dot_v0),
                  run_time=0.8)
        self.play(Write(c1_lbl), Write(c2_lbl), run_time=1.0)
        self.wait(0.6)

        # 逐次迭代 v0 → v1 → v2 → v3
        pts = [vseq(n) for n in range(4)]
        traj_dots = VGroup()
        traj_arrows = VGroup()
        ghost_lines = VGroup()
        for n, p in enumerate(pts):
            traj_dots.add(Dot(cpt(p[0], p[1]), radius=0.065,
                              color=ACCENT))
        for n in range(3):
            a, b = pts[n], pts[n + 1]
            traj_arrows.add(Arrow(cpt(a[0], a[1]), cpt(b[0], b[1]), buff=0,
                                  color=PRIMARY, stroke_width=3,
                                  tip_length=0.16))
        for n in range(1, 4):
            p = pts[n]
            ghost_lines.add(DashedLine(cpt(0, 0), cpt(p[0], p[1]),
                                       color=GRAY, stroke_width=1.5))

        self.play(FadeIn(traj_dots[1]), FadeIn(traj_dots[2]),
                  FadeIn(traj_dots[3]), run_time=0.8)
        self.play(Create(traj_arrows), run_time=1.6)
        self.play(Create(ghost_lines), run_time=1.2)
        self.wait(0.6)

        align_lbl = Text("方向趋于特征方向 (1,1)", font=FONT_NAME,
                         font_size=19, color=ACCENT)
        align_lbl.move_to(cpt(2.2, 1.35))
        self.play(Write(align_lbl), run_time=1.1)
        self.wait(2.6)

        # ======================================================
        # 第三幕：定格同构
        # ======================================================
        title3 = Text(
            "3. 定格：特征向量 = 方向不动点，特征值 = 放大率",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title2, title3), run_time=1.0)

        self.play(
            FadeOut(panel2), FadeOut(d1), FadeOut(d2),
            FadeOut(dot_comp1), FadeOut(dot_comp2), FadeOut(dot_v0),
            FadeOut(c1_lbl), FadeOut(c2_lbl),
            FadeOut(traj_dots), FadeOut(traj_arrows),
            FadeOut(ghost_lines), FadeOut(align_lbl),
            run_time=0.8,
        )

        panel3 = VGroup(
            Text("特征向量 = 射影意义下的不动点方向", font=FONT_NAME,
                 font_size=22, color=PRIMARY),
            Text("特征值 λ = 该方向的放大率（等比公比）", font=FONT_NAME,
                 font_size=22, color=SECONDARY),
            MathTex(r"a_{n+2}=p a_{n+1}+q a_n\ \longleftrightarrow\ "
                    r"\begin{pmatrix}0&1\\q&p\end{pmatrix}",
                    font_size=24, color=WHITE),
            VGroup(Text("特征方程", font=FONT_NAME, font_size=20,
                        color=GRAY),
                   MathTex(r"\lambda^2-p\lambda-q=0", font_size=22,
                           color=ACCENT)).arrange(RIGHT, buff=0.2),
            MathTex(r"M:\ \lambda^2-\tfrac52\lambda+1=0\ "
                    r"\Rightarrow\ p=\tfrac52,\ q=-1",
                    font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        panel3.move_to((1.2, 1.3, 0), aligned_edge=LEFT)
        box3 = SurroundingRectangle(panel3, color=ACCENT, buff=0.22,
                                    stroke_width=3)

        self.play(Write(panel3), run_time=1.8)
        self.play(Create(box3), run_time=0.9)
        self.wait(0.8)

        caption = Text(
            "沿特征方向的运动就是等比数列：特征值即公比",
            font=FONT_NAME, font_size=22, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(caption), run_time=1.3)
        self.wait(4.5)
