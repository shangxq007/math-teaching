"""第 1 章 · 函数的概念引入（二）：从无序到有序 —— 图像线

只讲一件事：图像上的次序是怎么长出来的。
    幕 1  矩形区域里随手撒一把点：每个 x 拖着一大段 y —— 无序，无法预测
    幕 2  立规矩：每条竖线只留一个点 —— 确定了，但点列仍在乱跳
    幕 3  离散到连续的过渡：点越密，跳动的点列糊成一条粗壮的「黑带」
    幕 4  压扁：带的厚度收敛到 0，剩下的那条线就是函数图像 —— 有序，可计算

配套概念线见 scene1_concept.py（一般关系 → 函数）。

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene2_order.py GraphOrderFromChaos

字体：中文统一 Noto Sans Mono CJK SC；数学一律 MathTex（原始字符串，不含中文）。
"""

from manim import *
import numpy as np

FONT_NAME = "Noto Sans Mono CJK SC"

BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"
RED_H = "#FF5252"
GRAY = "#9A9A9A"

XMIN, XMAX = -2.2, 2.2
BLOCK_W, BLOCK_H = 6.6, 4.0          # 矩形「黑块」
BLOCK_C = np.array([0.0, -0.1, 0.0])


def f(x):
    return 0.5 * x ** 2 - 1.0


class GraphOrderFromChaos(Scene):
    def construct(self):
        self.camera.background_color = BG
        self._act_one()
        self._act_two()
        self._act_three()

    # ---------------- 公共：坐标与矩形黑块 ----------------
    def _block(self):
        rect = Rectangle(width=BLOCK_W, height=BLOCK_H, color=GRAY,
                         stroke_width=3, fill_color="#262626", fill_opacity=0.85)
        rect.move_to(BLOCK_C)
        lab = Text("平面上一块区域", font=FONT_NAME, font_size=18, color=GRAY)
        lab.next_to(rect, DOWN, buff=0.2)
        return rect, lab

    # ================= 幕 1：无序 =================
    def _act_one(self):
        title = Text(
            "1. 无序：随手撒一把点，谁也说不清下一个在哪",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.2)

        rect, lab = self._block()
        self.play(Create(rect), Write(lab), run_time=1.0)

        rng = np.random.default_rng(11)
        pts = VGroup(*[
            Dot(np.array([rng.uniform(-BLOCK_W / 2 + 0.15, BLOCK_W / 2 - 0.15),
                          rng.uniform(-BLOCK_H / 2 + 0.15, BLOCK_H / 2 - 0.15), 0.0])
                + BLOCK_C,
                 radius=0.045, color="#4FA8C8", fill_opacity=0.75)
            for _ in range(1400)
        ])
        self.play(FadeIn(pts), run_time=1.8)
        self.wait(0.6)

        cap = Text(
            "随便取一个 x，正上方拖着一大段 y —— 有无穷多种可能",
            font=FONT_NAME, font_size=21, color=ACCENT,
        ).to_edge(DOWN, buff=0.9)
        self.play(Write(cap), run_time=1.2)
        self.wait(1.2)

        # 抽一条竖线，直观看到「一列点」
        xline = -0.6
        col = Line(np.array([xline, -BLOCK_H / 2, 0]) + BLOCK_C,
                   np.array([xline, BLOCK_H / 2, 0]) + BLOCK_C,
                   color=RED_H, stroke_width=3)
        col_lab = Text("一个 x", font=FONT_NAME, font_size=18, color=RED_H)
        col_lab.next_to(col.get_top(), RIGHT, buff=0.15)
        self.play(Create(col), Write(col_lab), run_time=1.0)
        self.wait(1.5)

        self.title1, self.rect, self.lab, self.pts = title, rect, lab, pts
        self.cap1, self.col, self.col_lab = cap, col, col_lab

    # ================= 幕 2：立规矩（每列只留一点） =================
    def _act_two(self):
        title2 = Text(
            "2. 立规矩：同一条竖线上只许留一个点",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(self.title1, title2), run_time=0.8)
        self.play(FadeOut(self.cap1), FadeOut(self.col_lab), run_time=0.6)

        scan = Line(np.array([-BLOCK_W / 2, -BLOCK_H / 2, 0]) + BLOCK_C,
                    np.array([-BLOCK_W / 2, BLOCK_H / 2, 0]) + BLOCK_C,
                    color=RED_H, stroke_width=3)
        self.play(Create(scan), run_time=0.5)
        self.play(scan.animate.move_to(BLOCK_C + RIGHT * (BLOCK_W / 2)),
                  run_time=2.2, rate_func=linear)
        self.play(FadeOut(scan), FadeOut(self.col), run_time=0.6)

        # 每列只留一个（这里取该列里随机一个）——点列仍高低跳动
        rng = np.random.default_rng(23)
        keep_pts = VGroup(*[
            Dot(np.array([x, f(x) + rng.uniform(-0.85, 0.85), 0.0]),
                radius=0.07, color=ACCENT)
            for x in np.linspace(XMIN, XMAX, 26)
        ])
        cap2 = VGroup(
            Text("每个 x 只有一个 y 了，但点列还在乱跳 —— 确定了，却还没有次序",
                 font=FONT_NAME, font_size=20, color=GRAY),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.75)

        self.play(ReplacementTransform(self.pts, keep_pts), run_time=1.6)
        self.play(Write(cap2), run_time=1.2)
        self.wait(1.4)

        self.title2, self.keep_pts, self.cap2 = title2, keep_pts, cap2

    # ================= 幕 3-4：密化成带 → 压扁成线 =================
    def _act_three(self):
        title3 = Text(
            "3. 离散到连续：点越密，跳动的点列糊成一条粗壮的带",
            font=FONT_NAME, font_size=24, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(self.title2, title3), run_time=0.8)
        self.play(FadeOut(self.cap2), FadeOut(self.keep_pts), run_time=0.8)

        n = 600
        rng = np.random.default_rng(37)
        xs = np.linspace(XMIN, XMAX, n)
        jitter = rng.uniform(-1.0, 1.0, n)
        self.thick = ValueTracker(1.0)

        band = always_redraw(lambda: self._band(xs, jitter, self.thick.get_value()))
        self.add(band)
        self.wait(0.8)

        cap3 = Text(
            "带还有厚度：一个 x 仍然对应着上下好几个 y",
            font=FONT_NAME, font_size=21, color=ACCENT,
        ).to_edge(DOWN, buff=0.75)
        self.play(Write(cap3), run_time=1.2)
        self.wait(1.0)

        # 压扁
        title4 = Text(
            "4. 压扁：厚度归零 —— 剩下的那条线就是函数图像",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        cap4 = Text(
            "有序：按 x 排好队，且每个 x 只剩唯一的一个 y",
            font=FONT_NAME, font_size=21, color=SECONDARY,
        ).to_edge(DOWN, buff=0.75)

        self.play(ReplacementTransform(title3, title4),
                  ReplacementTransform(cap3, cap4), run_time=1.0)
        self.play(self.thick.animate.set_value(0.0), run_time=3.2,
                  rate_func=smooth)
        self.wait(0.6)

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-1.6, 2.0, 1],
            x_length=6.4, y_length=4.0,
            axis_config={"include_tip": True, "color": WHITE, "stroke_width": 2},
        ).move_to(BLOCK_C + DOWN * 0.15)
        curve = axes.plot(f, x_range=[XMIN, XMAX], color=SECONDARY, stroke_width=5)
        eq = MathTex(r"y=\frac{1}{2}x^2-1", font_size=32, color=SECONDARY)
        eq.next_to(curve.get_end(), RIGHT, buff=0.2)

        self.remove(band)
        self.play(FadeOut(self.rect), FadeOut(self.lab), run_time=0.8)
        self.play(Create(axes), Create(curve), Write(eq), run_time=1.6)
        self.wait(0.8)

        final = Text(
            "无序 → 有序：图像就是「按 x 排序、且每个 x 唯一」的点列极限",
            font=FONT_NAME, font_size=20, color=ACCENT,
        ).to_edge(DOWN, buff=0.25)
        self.play(ReplacementTransform(cap4, final), run_time=1.0)
        self.wait(3.5)

    def _band(self, xs, jitter, t):
        """厚度参数 $t$：$1$ 为粗带，$0$ 收敛为曲线"""
        h = 0.95 * t
        r = 0.035 + 0.05 * t
        col = "#58C4DD" if t > 0.25 else SECONDARY
        return VGroup(*[
            Dot(np.array([x, f(x) + j * h, 0.0]), radius=r, color=col,
                 fill_opacity=0.8)
            for x, j in zip(xs, jitter)
        ])
