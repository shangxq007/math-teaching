# -*- coding: utf-8 -*-
"""终极对偶律：主动变换（动图形） vs 被动变换（动坐标系）同屏对比。

左屏：坐标系静止，抛物线 y=x^2 向右移 2 单位 -> y=(x-2)^2。
右屏：抛物线屏幕空间静止，坐标轴向左移 2 单位 -> 新坐标读数 x'=x+2，方程 y'=(x'-2)^2。
对应 hv-guide 第 1 章「主被动对偶」与「左加右减」的逆操作替换。
"""
from manim import *

FONT_NAME = "Noto Sans Mono CJK SC"


class ActiveVsPassiveDuality(Scene):
    def construct(self):
        title = Text(
            "终极对偶律：主动移动曲线 vs 被动移动坐标系",
            font=FONT_NAME,
            font_size=24,
        ).to_edge(UP, buff=0.2)
        divider = DashedLine(UP * 3.1, DOWN * 3.5, color=GRAY)
        self.play(Write(title), Create(divider))

        # ===== 左屏：主动变换（坐标系静止，曲线动） =====
        left_title = Text(
            "左屏：主动变换（坐标系不动）",
            font=FONT_NAME,
            font_size=20,
            color=BLUE,
        ).move_to(LEFT * 3.5 + UP * 2.7)
        left_axes = Axes(
            x_range=[-3.5, 4.5, 1],
            y_range=[-1, 4.5, 1],
            x_length=5.6,
            y_length=4.0,
            axis_config={"include_tip": True, "font_size": 16},
        ).move_to(LEFT * 3.5 + UP * 0.3)

        left_curve = left_axes.plot(
            lambda x: x ** 2, x_range=[-2.0, 2.0], color=BLUE, stroke_width=4
        )
        left_vertex = Dot(left_axes.c2p(0, 0), radius=0.08, color=YELLOW)
        left_eq = MathTex(r"y = x^2", font_size=26, color=BLUE).move_to(
            LEFT * 3.5 + DOWN * 2.1
        )
        left_desc = Text(
            "初始状态：顶点在原点 (0,0)",
            font=FONT_NAME,
            font_size=18,
            color=GRAY,
        ).next_to(left_eq, DOWN, buff=0.15)

        # ===== 右屏：被动变换（曲线静止，坐标系动） =====
        right_title = Text(
            "右屏：被动变换（曲线不动）",
            font=FONT_NAME,
            font_size=20,
            color=GREEN,
        ).move_to(RIGHT * 3.5 + UP * 2.7)
        right_axes = Axes(
            x_range=[-3.5, 4.5, 1],
            y_range=[-1, 4.5, 1],
            x_length=5.6,
            y_length=4.0,
            axis_config={"include_tip": True, "font_size": 16},
        ).move_to(RIGHT * 3.5 + UP * 0.3)

        right_curve = right_axes.plot(
            lambda x: x ** 2, x_range=[-2.0, 2.0], color=GREEN, stroke_width=4
        )
        right_vertex = Dot(right_axes.c2p(0, 0), radius=0.08, color=YELLOW)
        right_eq = MathTex(r"y = x^2", font_size=26, color=GREEN).move_to(
            RIGHT * 3.5 + DOWN * 2.1
        )
        right_desc = Text(
            "初始状态：顶点在原点 (0,0)",
            font=FONT_NAME,
            font_size=18,
            color=GRAY,
        ).next_to(right_eq, DOWN, buff=0.15)

        self.play(
            Write(left_title),
            Create(left_axes),
            Create(left_curve),
            FadeIn(left_vertex),
            Write(left_eq),
            Write(left_desc),
            Write(right_title),
            Create(right_axes),
            Create(right_curve),
            FadeIn(right_vertex),
            Write(right_eq),
            Write(right_desc),
        )
        self.wait(1.0)

        # ===== 核心同步演化 =====
        unit_dx = left_axes.c2p(1, 0) - left_axes.c2p(0, 0)

        left_eq_after = MathTex(r"y = (x - 2)^2", font_size=26, color=YELLOW).move_to(
            LEFT * 3.5 + DOWN * 2.1
        )
        left_desc_after = Text(
            "曲线主动向右移 2 单位，顶点变为 (2,0)",
            font=FONT_NAME,
            font_size=18,
            color=YELLOW,
        ).next_to(left_eq_after, DOWN, buff=0.15)

        right_eq_after = MathTex(
            r"y' = (x' - 2)^2 \ (x' = x + 2)", font_size=26, color=YELLOW
        ).move_to(RIGHT * 3.5 + DOWN * 2.1)
        right_desc_after = Text(
            "坐标轴被动向左移 2 单位，顶点读数仍为 (2,0)",
            font=FONT_NAME,
            font_size=18,
            color=YELLOW,
        ).next_to(right_eq_after, DOWN, buff=0.15)

        self.play(
            VGroup(left_curve, left_vertex).animate.shift(RIGHT * 2 * unit_dx),
            right_axes.animate.shift(LEFT * 2 * unit_dx),
            run_time=2.2,
        )
        self.play(FadeOut(left_eq), FadeOut(left_desc), FadeOut(right_eq), FadeOut(right_desc))
        self.play(
            Write(left_eq_after),
            Write(left_desc_after),
            Write(right_eq_after),
            Write(right_desc_after),
        )
        self.wait(1.0)

        concl = VGroup(
            Text(
                "结论：图形右移 2 单位，等价于坐标系左移 2 单位",
                font=FONT_NAME,
                font_size=21,
                color=ORANGE,
            ),
            MathTex(
                r"x' = x + 2 \ \Longrightarrow\ y' = (x' - 2)^2",
                font_size=24,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.18)
        concl.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(concl))
        self.wait(2.6)
