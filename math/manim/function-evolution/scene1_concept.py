"""第 1 章 · 函数的概念引入（一）：从一般关系到函数 —— 概念线

只讲一件事：概念的收窄。
    幕 1  最一般的二元关系：A×B 中任意取点，一对多、有空缺都合法
    幕 2  加上唯一性限制：每个 x 只能对应唯一确定的 y —— 筛出映射（函数）
    幕 3  同一对象的三种等价表示：数对集合 / 箭头图 / 坐标点

配套图像线见 scene2_order.py（无序 → 有序）。

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene1_concept.py FunctionConceptEvolution

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


class FunctionConceptEvolution(Scene):
    def construct(self):
        self.camera.background_color = BG
        self._act_one()
        self._act_two()
        self._act_three()

    # ================= 幕 1：最一般的关系 =================
    def _act_one(self):
        title = Text(
            "1. 最一般的关系：A×B 里想取哪些点都可以",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.2)

        box_a = RoundedRectangle(width=1.3, height=3.0, corner_radius=0.2,
                                 color=PRIMARY, stroke_width=3)
        box_a.shift(LEFT * 5.3)
        box_b = RoundedRectangle(width=1.3, height=3.0, corner_radius=0.2,
                                 color=SECONDARY, stroke_width=3)
        box_b.shift(LEFT * 3.1)
        lab_a = MathTex("A", font_size=34, color=PRIMARY).next_to(box_a, UP, buff=0.15)
        lab_b = MathTex("B", font_size=34, color=SECONDARY).next_to(box_b, UP, buff=0.15)

        elems_a = VGroup(*[MathTex(str(i), font_size=30, color=WHITE) for i in (1, 2, 3)])
        elems_a.arrange(DOWN, buff=0.65).move_to(box_a)
        elems_b = VGroup(*[MathTex(str(j), font_size=30, color=WHITE) for j in (2, 4, 6)])
        elems_b.arrange(DOWN, buff=0.65).move_to(box_b)

        # 右侧：A×B 的全部 9 个候选点
        axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 7, 2],
            x_length=5.0, y_length=4.4,
            axis_config={"include_tip": True, "color": WHITE, "stroke_width": 2},
        ).shift(RIGHT * 2.55 + DOWN * 0.15)
        ax_lab = axes.get_axis_labels(x_label="x", y_label="y").set_color(WHITE)
        cart_lab = MathTex(r"A\times B", font_size=26, color=GRAY)
        cart_lab.next_to(axes, DOWN, buff=0.25)

        grid_dots, dot_map = VGroup(), {}
        for i, xv in enumerate((1, 2, 3)):
            for j, yv in enumerate((2, 4, 6)):
                d = Dot(axes.c2p(xv, yv), radius=0.06, color=GRAY)
                grid_dots.add(d)
                dot_map[(i, j)] = d

        self.play(Create(box_a), Create(box_b), Write(lab_a), Write(lab_b),
                  Write(elems_a), Write(elems_b), run_time=1.4)
        self.play(Create(axes), Write(ax_lab), FadeIn(grid_dots), Write(cart_lab),
                  run_time=1.4)
        self.wait(0.8)

        # 一对多 + 空缺：任意对应都合法
        free_arrows = VGroup(
            Arrow(elems_a[0].get_right(), elems_b[0].get_left(), buff=0.12,
                  color=RED_H, stroke_width=3),
            Arrow(elems_a[0].get_right(), elems_b[1].get_left(), buff=0.12,
                  color=RED_H, stroke_width=3),
            Arrow(elems_a[1].get_right(), elems_b[2].get_left(), buff=0.12,
                  color=RED_H, stroke_width=3),
        )
        note1 = VGroup(
            Text("想怎么连就怎么连", font=FONT_NAME, font_size=21, color=RED_H),
            Text("可以一对多，也可以谁都不对应", font=FONT_NAME,
                 font_size=19, color=GRAY),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)

        self.play(Create(free_arrows), run_time=1.2)
        for k in ((0, 0), (0, 1), (1, 2)):
            self.play(dot_map[k].animate.set_color(RED_H).scale(1.4), run_time=0.3)
        self.play(Write(note1), run_time=1.2)
        self.wait(1.2)

        self.title1 = title
        self.left_all = VGroup(box_a, box_b, lab_a, lab_b, elems_a, elems_b)
        self.free_arrows = free_arrows
        self.note1 = note1
        self.axes, self.ax_lab, self.grid_dots, self.cart_lab = \
            axes, ax_lab, grid_dots, cart_lab
        self.dot_map = dot_map

    # ================= 幕 2：唯一性筛选 =================
    def _act_two(self):
        title2 = Text(
            "2. 加一条规矩：每个 x 只能对应唯一确定的 y",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(self.title1, title2), run_time=0.8)

        # 删掉一对多与空缺，补全唯一对应
        keep = VGroup(
            Arrow(self.left_all[4][0].get_right(), self.left_all[5][0].get_left(),
                  buff=0.12, color=SECONDARY, stroke_width=4),
            Arrow(self.left_all[4][1].get_right(), self.left_all[5][1].get_left(),
                  buff=0.12, color=SECONDARY, stroke_width=4),
            Arrow(self.left_all[4][2].get_right(), self.left_all[5][2].get_left(),
                  buff=0.12, color=SECONDARY, stroke_width=4),
        )
        note2 = VGroup(
            MathTex(r"R_2=\{(1,2),(2,4),(3,6)\}", font_size=24, color=SECONDARY),
            Text("每个 x 唯一确定一个 y —— 这就是函数", font=FONT_NAME,
                 font_size=19, color=GRAY),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)

        self.play(FadeOut(self.free_arrows), FadeOut(self.note1), run_time=0.8)
        self.play(Create(keep), run_time=1.2)
        for k in ((0, 0), (1, 1), (2, 2)):
            self.play(self.dot_map[k].animate.set_color(SECONDARY).scale(1.5),
                      run_time=0.35)
        self.play(
            *[self.dot_map[k].animate.set_opacity(0.12)
              for k in self.dot_map if k not in ((0, 0), (1, 1), (2, 2))],
            run_time=1.0,
        )
        self.play(Write(note2), run_time=1.2)
        self.wait(1.2)

        self.title2 = title2
        self.keep = keep
        self.note2 = note2

    # ================= 幕 3：三种等价表示 =================
    def _act_three(self):
        title3 = Text(
            "3. 同一个函数，三种等价长相",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(self.title2, title3), run_time=0.8)

        # ① 数对集合：把 $R_2$ 移到左上角并加注序号
        tag_pair = Text("① 数对集合", font=FONT_NAME, font_size=19, color=GRAY)
        tag_pair.next_to(self.note2, LEFT, buff=0.3, aligned_edge=UP)
        self.play(
            self.note2.animate.to_corner(UL, buff=0.4).scale(0.9),
            Write(tag_pair), run_time=1.0,
        )

        # ② 箭头图：标注左侧的集合框与箭头
        tag_arrow = Text("② 箭头图", font=FONT_NAME, font_size=19, color=GRAY)
        tag_arrow.next_to(self.left_all, DOWN, buff=0.25)
        self.play(Write(tag_arrow), run_time=0.9)

        # ③ 坐标点列：标注右侧坐标系
        tag_graph = Text("③ 坐标点列", font=FONT_NAME, font_size=19, color=GRAY)
        tag_graph.next_to(self.cart_lab, DOWN, buff=0.18)
        self.play(ReplacementTransform(self.cart_lab, tag_graph), run_time=0.9)
        self.wait(0.8)

        # 收束：函数的符号化
        formula = VGroup(
            MathTex(r"f:A\to B,\qquad y=f(x)=2x", font_size=32, color=ACCENT),
            Text("外衣有三种，本质只有一条", font=FONT_NAME,
                 font_size=20, color=WHITE),
            Text("每个 x 唯一确定一个 y", font=FONT_NAME,
                 font_size=22, color=SECONDARY),
        ).arrange(DOWN, buff=0.28)
        formula.move_to(np.array([3.9, -1.9, 0.0]))

        final = Text(
            "所以判断是不是函数，只看对应关系，不看它长什么样",
            font=FONT_NAME, font_size=19, color=GRAY,
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(formula), run_time=1.4)
        self.play(Write(final), run_time=1.0)
        self.wait(3.5)
