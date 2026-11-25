"""第 6 章 · 导数与局部线性化引擎 —— 场景 2：切线放缩（凸函数的局部线性化）

叙事：坐标系中画 y = e^x（绿），在 (0,1) 处贴合切线 y = x+1（橙）；
      用半透明面积带显示曲线恒在切线上方，仅在 x = 0 接触 → e^x >= x+1。
      再以 y = x 为镜像对称翻转到 y = ln x（蓝）与切线 y = x-1（红），
      凹函数恒在切线下方 → ln x <= x-1。

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene2_tangent.py TangentInequalityVisualization

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


class TangentInequalityVisualization(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        title = Text(
            "2. 切线放缩：凸函数压在切线上方",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.2)
        self.wait(0.4)

        axes = Axes(
            x_range=[-3.2, 2.2, 1],
            y_range=[-2.0, 4.0, 1],
            x_length=6.6,
            y_length=5.4,
            axis_config={"include_tip": True, "color": WHITE, "stroke_width": 2},
        ).shift(LEFT * 1.7 + DOWN * 0.35)

        exp_graph = axes.plot(np.exp, x_range=[-3.2, 1.0],
                              color=SECONDARY, stroke_width=4)
        tangent = axes.plot(lambda x: x + 1, x_range=[-3.2, 2.2],
                            color=ACCENT, stroke_width=4)
        area = axes.get_area(exp_graph, x_range=[-3.2, 1.0],
                             color=SECONDARY, opacity=0.28)
        # 只保留曲线与切线之间的区域：叠一层背景色盖住切线下方
        cover = axes.plot(lambda x: x + 1, x_range=[-3.2, 2.2],
                          color="#1C1C1C", stroke_width=14,
                          z_index=area.z_index - 1)

        p0 = axes.c2p(0, 1)
        touch = Dot(p0, radius=0.08, color=WHITE)

        exp_lab = MathTex(r"y=e^x", font_size=25, color=SECONDARY)
        exp_lab.next_to(exp_graph, UP, buff=0.2)
        tan_lab = MathTex(r"y=x+1", font_size=25, color=ACCENT)
        tan_lab.next_to(tangent.get_end(), RIGHT, buff=0.15)
        touch_lab = Text("唯一接触点 (0,1)", font=FONT_NAME,
                         font_size=19, color=WHITE)
        touch_lab.next_to(touch, DOWN + LEFT, buff=0.18)

        self.play(Create(axes), run_time=1.3)
        self.play(Create(exp_graph), Write(exp_lab), run_time=1.4)
        self.wait(0.5)
        self.play(FadeIn(area), Create(cover), run_time=1.2)
        self.play(Create(tangent), Write(tan_lab), run_time=1.2)
        self.play(FadeIn(touch), Write(touch_lab), run_time=1.0)
        self.wait(0.8)

        concl1 = VGroup(
            MathTex(r"e^x \ge x+1", font_size=30, color=ACCENT),
            Text("当且仅当 x = 0 取等", font=FONT_NAME,
                 font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.25)
        concl1.to_edge(RIGHT, buff=0.7).shift(UP * 0.6)
        self.play(Write(concl1), run_time=1.4)
        self.wait(1.0)

        # ---------------- 关于 y = x 对称翻转 ----------------
        title2 = Text(
            "3. 沿 y = x 翻转：凹函数压在切线下方",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        mirror_dash = DashedLine(axes.c2p(-2, -2), axes.c2p(2.2, 2.2),
                                 color=GRAY, stroke_width=2)
        mir_lab = MathTex(r"y=x", font_size=22, color=GRAY)
        mir_lab.next_to(mirror_dash.get_end(), RIGHT, buff=0.15)

        self.play(
            ReplacementTransform(title, title2),
            FadeOut(concl1), FadeOut(touch_lab),
            Create(mirror_dash), Write(mir_lab),
            run_time=1.3,
        )
        self.wait(0.6)

        log_curve = axes.plot(lambda x: np.log(x), x_range=[0.05, 3.0],
                              color=PRIMARY, stroke_width=4)
        log_tangent = axes.plot(lambda x: x - 1, x_range=[-2.0, 2.2],
                                color=RED_H, stroke_width=4)
        log_lab = MathTex(r"y=\\ln x", font_size=25, color=PRIMARY)
        log_lab.next_to(log_curve, UP, buff=0.25)
        logtan_lab = MathTex(r"y=x-1", font_size=25, color=RED_H)
        logtan_lab.next_to(log_tangent.get_end(), RIGHT, buff=0.15)

        self.play(
            FadeOut(exp_graph), FadeOut(tangent), FadeOut(area),
            FadeOut(cover), FadeOut(touch), FadeOut(exp_lab),
            run_time=1.0,
        )
        self.play(Create(log_curve), Write(log_lab), run_time=1.4)
        self.play(Create(log_tangent), Write(logtan_lab), run_time=1.2)
        self.wait(0.6)

        concl2 = VGroup(
            MathTex(r"\ln x \le x-1", font_size=30, color=RED_H),
            Text("当且仅当 x = 1 取等", font=FONT_NAME,
                 font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.25)
        concl2.to_edge(RIGHT, buff=0.7).shift(DOWN * 0.4)
        self.play(Write(concl2), run_time=1.4)
        self.wait(0.8)

        caption = Text(
            "同一个机制：曲线总是贴在切线的一侧（凸在上、凹在下）",
            font=FONT_NAME, font_size=20, color=ACCENT,
        ).to_edge(DOWN, buff=0.35)
        self.play(Write(caption), run_time=1.4)
        self.wait(4.0)
