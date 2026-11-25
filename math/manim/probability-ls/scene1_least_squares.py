"""第 7 章 · 计数原理、概率测度空间与统计线性逼近 —— 场景：最小二乘与样本空间

第一幕：二维散点云。一条绕样本中心 (x̄,ȳ) 转动的直线，每个数据点到直线的竖直残差
         用红线段画出，并把 |残差| 画成小正方形 —— 正方形面积之和就是残差平方和。
         转到回归斜率时面积之和全局最小。
第二幕：样本空间 Ω（矩形）中圈出子集 A；把 Ω 之外的部分淡去、A 放大充满画面，
         演示条件概率 P(B|A) 是「样本空间缩小到 A 后重新归一化」。

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene1_least_squares.py LeastSquaresAndSampleSpace

字体：中文统一 Noto Sans Mono CJK SC；数学一律 MathTex（原始字符串）。
"""

from manim import *
import numpy as np

FONT_NAME = "Noto Sans Mono CJK SC"

PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"
RED_H = "#FF5252"
GRAY = "#9A9A9A"


class LeastSquaresAndSampleSpace(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        self._act_one()
        self._act_two()

    # ================= 第一幕 =================
    def _act_one(self):
        title = Text(
            "1. 最小二乘：让残差平方和最小的那条线",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.2)

        axes = Axes(
            x_range=[-0.5, 6.5, 1],
            y_range=[-0.5, 6.5, 1],
            x_length=6.6,
            y_length=5.6,
            axis_config={"include_tip": True, "color": WHITE, "stroke_width": 2},
        ).shift(LEFT * 1.6 + DOWN * 0.3)

        xs = np.array([1.0, 1.6, 2.2, 2.9, 3.5, 4.1, 4.9, 5.6])
        ys = np.array([1.3, 2.1, 2.5, 3.3, 3.1, 4.5, 4.7, 5.5])
        xbar, ybar = float(xs.mean()), float(ys.mean())
        b = float(((xs - xbar) * (ys - ybar)).sum() / ((xs - xbar) ** 2).sum())
        a = ybar - b * xbar

        self.xs, self.ys = xs, ys
        self.xbar, self.ybar, self.b, self.a = xbar, ybar, b, a
        self.axes = axes
        self.m = ValueTracker(0.15)

        pts = VGroup(*[
            Dot(axes.c2p(float(x), float(y)), radius=0.08, color=PRIMARY)
            for x, y in zip(xs, ys)
        ])
        center = Dot(axes.c2p(xbar, ybar), radius=0.09, color=ACCENT)
        center_lab = Text("样本中心", font=FONT_NAME, font_size=18, color=ACCENT)
        center_lab.next_to(center, UP + RIGHT, buff=0.12)

        fit_line = always_redraw(lambda: self._fit_line(b, a))
        rot_line = always_redraw(lambda: self._rot_line())
        resid = always_redraw(lambda: self._residuals())

        formula = MathTex(
            rf"\hat{{y}}={b:.3f}x{'+' if a >= 0 else '-'}{abs(a):.3f}",
            font_size=26, color=SECONDARY,
        )
        formula.to_edge(RIGHT, buff=0.6).shift(UP * 1.5)
        through = Text("必过样本中心 (x̄, ȳ)", font=FONT_NAME,
                       font_size=18, color=GRAY)
        through.next_to(formula, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(Create(axes), run_time=1.3)
        self.play(FadeIn(pts), FadeIn(center), Write(center_lab), run_time=1.2)
        self.wait(0.5)

        cap1 = Text(
            "让直线绕样本中心转动：黄色方块 = 各点竖直残差的平方",
            font=FONT_NAME, font_size=19, color=GRAY,
        ).to_edge(DOWN, buff=0.35)
        self.play(Write(cap1), Create(rot_line), FadeIn(resid), run_time=1.4)

        self.play(self.m.animate.set_value(1.5), run_time=3.4,
                  rate_func=there_and_back)
        self.wait(0.6)

        cap2 = Text(
            "方块面积之和在回归斜率处达到全局最小",
            font=FONT_NAME, font_size=20, color=ACCENT,
        ).to_edge(DOWN, buff=0.35)
        self.play(ReplacementTransform(cap1, cap2), run_time=0.8)
        self.play(self.m.animate.set_value(b), run_time=1.4,
                  rate_func=smooth)
        self.play(FadeOut(rot_line), FadeOut(resid), run_time=0.8)
        self.play(Create(fit_line), Write(formula), Write(through),
                  run_time=1.4)
        self.wait(1.2)

        note = Text(
            "几何本质：找使 Σ(yᵢ−ŷᵢ)² 最小的投影方向",
            font=FONT_NAME, font_size=19, color=GRAY,
        ).to_edge(DOWN, buff=0.35)
        self.play(Write(note), run_time=1.2)
        self.wait(2.0)

        self.act1 = VGroup(title, axes, pts, center, center_lab,
                           fit_line, formula, through, note, cap2)
        self.play(FadeOut(self.act1), run_time=1.2)

    # ================= 第二幕 =================
    def _act_two(self):
        title = Text(
            "2. 条件概率：把样本空间缩小到事件 A 再重新归一化",
            font=FONT_NAME, font_size=24, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.2)

        # 样本空间 Ω：6.4 x 4.0 的矩形，随机撒 18 个点
        omega = Rectangle(width=6.4, height=4.0, color=WHITE,
                          stroke_width=3, fill_color="#2A2A2A",
                          fill_opacity=0.6)
        omega.shift(LEFT * 1.2 + DOWN * 0.4)

        rng = np.random.default_rng(7)
        dots = VGroup(*[
            Dot(omega.get_center() +
                np.array([rng.uniform(-3.0, 3.0), rng.uniform(-1.8, 1.8), 0.0]),
                radius=0.075, color=PRIMARY)
            for _ in range(18)
        ])

        om_lab = MathTex(r"\Omega", font_size=30, color=WHITE)
        om_lab.next_to(omega, UP, buff=0.15)

        # 事件 A：左侧子矩形
        A_rect = Rectangle(width=2.1, height=4.0, color=ACCENT,
                           stroke_width=4, fill_color=ACCENT,
                           fill_opacity=0.16)
        A_rect.align_to(omega, LEFT).align_to(omega, DOWN)
        A_lab = MathTex(r"A", font_size=28, color=ACCENT)
        A_lab.next_to(A_rect, UP, buff=0.12)

        inner = [d for d in dots
                 if A_rect.get_left()[0] <= d.get_center()[0] <= A_rect.get_right()[0]]
        assert len(inner) > 0, "事件 A 内没有样本点，无法演示条件概率"
        n_b = min(5, len(inner))   # B ⊂ A：A 内前 n_b 个点；分子由实际计数得到
        rel = [((d.get_center()[0] - A_rect.get_left()[0]) / A_rect.width,
                (d.get_center()[1] - A_rect.get_bottom()[1]) / A_rect.height)
               for d in inner]

        p_a = MathTex(
            rf"P(A)=\frac{{\mu(A)}}{{\mu(\Omega)}}=\frac{{{len(inner)}}}{{18}}",
            font_size=25, color=ACCENT,
        )
        p_a.to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
        p_ba = MathTex(
            rf"P(B\mid A)=\frac{{\mu(B)}}{{\mu(A)}}=\frac{{{n_b}}}{{{len(inner)}}}",
            font_size=25, color=RED_H,
        )
        p_ba.next_to(p_a, DOWN, buff=0.35, aligned_edge=LEFT)

        self.play(Create(omega), Write(om_lab), run_time=1.2)
        self.play(FadeIn(dots), run_time=1.2)
        self.play(Create(A_rect), Write(A_lab), run_time=1.2)
        self.wait(0.5)
        self.play(Write(p_a), run_time=1.2)
        self.wait(0.6)

        cap1 = Text(
            "条件概率不是新东西：把 Ω 扔出画面，只留下 A 当新的全集",
            font=FONT_NAME, font_size=19, color=GRAY,
        ).to_edge(DOWN, buff=0.35)
        self.play(Write(cap1), run_time=1.2)

        # ---- 重建：A 成为新的样本空间 ----
        new_A = Rectangle(width=4.0, height=6.0, color=ACCENT,
                          stroke_width=4, fill_color=ACCENT,
                          fill_opacity=0.14)
        new_A.move_to(np.array([-2.3, 0.0, 0.0]))
        new_lab = VGroup(
            MathTex(r"A", font_size=28, color=ACCENT),
            Text("（新的样本空间）", font=FONT_NAME, font_size=18, color=GRAY),
        ).arrange(RIGHT, buff=0.15)
        new_lab.next_to(new_A, UP, buff=0.12)
        new_dots = VGroup(*[
            Dot(np.array([new_A.get_left()[0] + rx * new_A.width,
                          new_A.get_bottom()[1] + ry * new_A.height, 0.0]),
                radius=0.10, color=PRIMARY)
            for rx, ry in rel
        ])
        # B ⊂ A：A 内前 n_b 个点标红
        B_dots = VGroup(*list(new_dots)[:n_b])
        B_dots.set_color(RED_H)
        B_lab = MathTex(r"B\subset A", font_size=24, color=RED_H)
        B_lab.move_to(new_A.get_center() + UP * 2.5 + RIGHT * 0.9)

        self.play(
            FadeOut(omega), FadeOut(om_lab), FadeOut(dots),
            FadeOut(A_rect), FadeOut(A_lab), FadeOut(cap1),
            run_time=1.2,
        )
        self.play(Create(new_A), Write(new_lab), FadeIn(new_dots), run_time=1.6)
        self.wait(0.6)

        cap2 = Text(
            "在缩小的样本空间里重新归一化：P(B|A) = μ(B) / μ(A)",
            font=FONT_NAME, font_size=20, color=ACCENT,
        ).to_edge(DOWN, buff=0.35)
        self.play(Write(cap2), run_time=1.0)
        self.play(FadeIn(B_dots), Write(B_lab), Write(p_ba), run_time=1.4)
        self.wait(1.0)

        final = Text(
            "全概率公式与贝叶斯公式：都是同一套「划分 → 缩小 → 归一」",
            font=FONT_NAME, font_size=20, color=SECONDARY,
        ).to_edge(DOWN, buff=0.35)
        self.play(ReplacementTransform(cap2, final), run_time=1.0)
        self.wait(4.0)

    # ---------- 第一幕辅助 ----------
    def _c2p(self, x, y):
        return self.axes.c2p(float(x), float(y))

    def _rot_line(self):
        m = float(self.m.get_value())
        c = self.ybar - m * self.xbar
        x1, x2 = -0.5, 6.5
        return Line(self._c2p(x1, m * x1 + c), self._c2p(x2, m * x2 + c),
                    color=ACCENT, stroke_width=4)

    def _fit_line(self, b, a):
        x1, x2 = -0.5, 6.5
        return Line(self._c2p(x1, b * x1 + a), self._c2p(x2, b * x2 + a),
                    color=SECONDARY, stroke_width=5)

    def _residuals(self):
        m = float(self.m.get_value())
        c = self.ybar - m * self.xbar
        items = []
        for x, y in zip(self.xs, self.ys):
            foot_y = m * float(x) + c
            r = float(y) - foot_y
            p = self._c2p(float(x), float(y))
            f = self._c2p(float(x), foot_y)
            items.append(Line(p, f, color=RED_H, stroke_width=3))
            side = max(abs(r), 1e-3)
            sq = Rectangle(width=side, height=side, color=ACCENT,
                           fill_color=ACCENT, fill_opacity=0.42,
                           stroke_width=1.5)
            sq.move_to((p + f) / 2)
            items.append(sq)
        return VGroup(*items)
