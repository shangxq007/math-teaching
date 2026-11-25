"""基本初等函数特化示例：指数与对数的集合逆关系 · Manim CE

要点：指数函数 y=2^x 的有序数对 (x,y) 全部调换为 (y,x)，
      点集关于 y=x 对称，连成对数函数 y=log_2 x。
      「反函数 = 逆关系点集」。

渲染：
    sh scripts/manim-run.sh -ql scene2_explog.py ExpLogSetSymmetry
    sh scripts/manim-run.sh -qh scene2_explog.py ExpLogSetSymmetry
"""

from manim import *

FONT_NAME = "Noto Sans Mono CJK SC"

BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"


class ExpLogSetSymmetry(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text(
            "指数与对数：有序数对 (x,y) 与 (y,x) 的互换",
            font=FONT_NAME, font_size=28, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.2)
        self.wait(0.5)

        axes = Axes(
            x_range=[-1.2, 4.6, 1],
            y_range=[-1.2, 4.6, 1],
            x_length=6.6,
            y_length=6.6,
            axis_config={"include_tip": True, "color": WHITE},
        ).shift(DOWN * 0.2)
        labels = axes.get_axis_labels(x_label="x", y_label="y").set_color(WHITE)

        exp_curve = axes.plot(
            lambda x: 2 ** x, x_range=[-1.0, 2.0], color=PRIMARY, stroke_width=4,
        )
        exp_label = MathTex(
            r"y=2^x", font_size=32, color=PRIMARY,
        ).next_to(axes.c2p(2.1, 3.4), RIGHT, buff=0.1)

        self.play(Create(axes), Write(labels), run_time=1.2)
        self.play(Create(exp_curve), Write(exp_label), run_time=1.6)
        self.wait(0.8)

        # 关键点及其有序数对标注
        points = [(-1, 0.5), (0, 1), (1, 2), (2, 4)]
        tag_dirs = [LEFT, DOWN + LEFT, UP + RIGHT, RIGHT]
        dots, tags = VGroup(), VGroup()
        for (x, y), direction in zip(points, tag_dirs):
            p = axes.c2p(x, y)
            dots.add(Dot(p, radius=0.09, color=ACCENT))
            tags.add(MathTex(
                r"(%d,%s)" % (x, str(y)), font_size=24, color=ACCENT,
            ).next_to(p, direction, buff=0.22))

        self.play(FadeIn(dots), Write(tags), run_time=1.4)
        self.wait(1.0)

        # 对称轴 y = x
        axis_line = axes.plot(
            lambda x: x, x_range=[-1.0, 4.4], color=GRAY,
            stroke_width=2,
        )
        axis_line = DashedVMobject(axis_line, num_dashes=40)
        axis_tag = MathTex(r"y=x", font_size=28, color=GRAY).next_to(
            axes.c2p(3.4, 3.4), UP, buff=0.1,
        )

        self.play(Create(axis_line), Write(axis_tag), run_time=1.2)
        self.wait(0.8)

        # 每个点沿弧线翻转到关于 y=x 的对称位置
        flipped_dots = VGroup()
        for (x, y), dot in zip(points, dots):
            target = axes.c2p(y, x)
            new_dot = Dot(target, radius=0.09, color=SECONDARY)
            flipped_dots.add(new_dot)
            self.play(
                dot.animate.move_to(target).set_color(SECONDARY),
                path_arc=PI / 3, run_time=1.0,
            )

        # 标注调换后的数对
        new_dirs = [UP + RIGHT, RIGHT, DOWN + RIGHT, DOWN + RIGHT]
        new_tags = VGroup()
        for (x, y), direction in zip(points, new_dirs):
            new_tags.add(MathTex(
                r"(%s,%d)" % (str(y), x), font_size=24, color=SECONDARY,
            ).next_to(axes.c2p(y, x), direction, buff=0.22))
        self.play(Write(new_tags), run_time=1.2)
        self.wait(0.8)

        # 连成对数曲线
        log_curve = axes.plot(
            lambda x: np.log2(x), x_range=[0.35, 4.4], color=SECONDARY, stroke_width=4,
        )
        log_label = MathTex(
            r"y=\log_2 x", font_size=32, color=SECONDARY,
        ).next_to(axes.c2p(4.3, 2.14), UP, buff=0.2)

        self.play(Create(log_curve), Write(log_label), run_time=1.6)
        self.wait(1.0)

        conclusion = Text(
            "对数函数 = 指数函数点集关于 y=x 的逆关系",
            font=FONT_NAME, font_size=24, color=ACCENT,
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(conclusion), run_time=1.2)
        self.wait(2.5)
