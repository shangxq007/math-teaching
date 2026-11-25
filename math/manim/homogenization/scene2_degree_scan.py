"""第 8 章 · 齐次化：把二元问题压成一元比例 —— 场景 2：次数扫描与配比

叙事：动手前先做「次数扫描」：给每一项标一个次数
      （常数 0 次、x 与 y 各 1 次、x²/xy/y² 为 2 次、1/x 为 -1 次、√x 为 1/2 次）
      判据：所有项次数相同 ⟺ 齐次式
      → 配比演示一「1 的代换」：(1/x+1/y)·1 = (1/x+1/y)(x+y)
        = 2 + y/x + x/y，每项抬 1 次，全部对齐到 0 次
      → 配比演示二「平方升次」：√x 是 1/2 次，平方后升为整次
      → 收束流程图：次数扫描 → 配平（乘 1 · 平方 · 平移 · 分解 · 旋转）
        → 同除主元最高次幂 → 一元函数 t=y/x

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene2_degree_scan.py DegreeScan
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


class DegreeScan(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ======================================================
        # 第一幕：次数扫描雷达
        # ======================================================
        title1 = Text(
            "1. 次数扫描雷达：先给每一项标次数",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=1.1)
        self.wait(0.4)

        terms = [
            ("常数项", "0", 0.55),
            ("一次项", "1", 1.05),
            ("二次项", "2", 1.55),
            ("分式项", "-1", 2.05),
            ("根式项", r"\tfrac12", 2.55),
        ]
        baseline = Line(LEFT * 6.1, RIGHT * 1.0, color=GRAY,
                        stroke_width=2).move_to(DOWN * 1.8)
        bars = VGroup()
        for i, (name, deg, h) in enumerate(terms):
            x = -5.55 + i * 1.5
            hh = h * 0.8
            bar = Rectangle(width=0.78, height=hh, fill_color=GRAY,
                            fill_opacity=0.35, stroke_color=WHITE,
                            stroke_width=2)
            bar.move_to(np.array([x, -1.8 + hh / 2.0, 0]))
            lab = Text(name, font=FONT_NAME, font_size=19,
                       color=WHITE).next_to(bar, UP, buff=0.1)
            dlab = MathTex(r"\deg=" + deg, font_size=19,
                           color=ACCENT).next_to(bar, DOWN, buff=0.16)
            bars.add(VGroup(bar, lab, dlab))
        self.play(Create(baseline), run_time=0.9)
        self.play(LaggedStart(*[Write(b) for b in bars], lag_ratio=0.28),
                  run_time=2.2)
        self.wait(0.6)
        sub = Text("（柱高仅为扫描顺序，次数见下方标签）", font=FONT_NAME,
                   font_size=17, color=GRAY).next_to(baseline, DOWN,
                                                    buff=0.55)
        self.play(FadeIn(sub), run_time=0.8)
        self.wait(1.6)

        crit = VGroup(
            Text("判据", font=FONT_NAME, font_size=21, color=ACCENT),
            Text("所有项次数相同 ⟺ 齐次式", font=FONT_NAME, font_size=22,
                 color=WHITE),
            VGroup(MathTex(r"x^2+2xy+y^2", font_size=21, color=SECONDARY),
                   Text("(2,2,2) 齐次", font=FONT_NAME, font_size=19,
                        color=SECONDARY)).arrange(RIGHT, buff=0.25),
            VGroup(MathTex(r"x^2+y+1", font_size=21, color=RED_H),
                   Text("(2,1,0) 非齐次", font=FONT_NAME, font_size=19,
                        color=RED_H)).arrange(RIGHT, buff=0.25),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        crit.move_to((4.0, 1.15, 0))
        self.play(Write(crit), run_time=1.6)
        self.wait(2.6)

        # ======================================================
        # 第二幕：配比手术刀之一——「1 的代换」
        # ======================================================
        title2 = Text(
            "2. 配比：「1 的代换」把每项抬到同一次数",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=1.0)
        self.play(FadeOut(bars), FadeOut(baseline), FadeOut(sub),
                  FadeOut(crit), run_time=0.7)

        E0 = MathTex(r"\left(\frac1x+\frac1y\right)\cdot 1",
                     font_size=34, color=WHITE).move_to(UP * 2.15)
        op_a = Text("约束 x+y=1 就是数字 1，把它乘进去",
                    font=FONT_NAME, font_size=20, color=GRAY).move_to(UP * 1.25)
        E1 = MathTex(r"\left(\frac1x+\frac1y\right)(x+y)",
                     font_size=34, color=WHITE).move_to(UP * 2.15)
        E2 = MathTex(r"2+\frac{y}{x}+\frac{x}{y}", font_size=36,
                     color=SECONDARY).move_to(UP * 2.15)

        self.play(Write(E0), run_time=1.1)
        self.wait(0.8)
        self.play(Write(op_a), run_time=0.9)
        self.play(ReplacementTransform(E0, E1), run_time=1.3)
        self.wait(1.2)
        self.play(FadeOut(op_a), ReplacementTransform(E1, E2), run_time=1.4)
        self.wait(1.6)

        # 次数标尺：-1 → 0
        ruler = NumberLine(x_range=[-1.5, 2.5], length=8.0,
                           include_numbers=True, font_size=15,
                           color=GRAY).move_to(DOWN * 1.15)
        r_lbl = Text("次数标尺", font=FONT_NAME, font_size=18,
                     color=GRAY).next_to(ruler, DOWN, buff=0.35)
        d_before = VGroup(*[Dot(ruler.n2p(-1), radius=0.07, color=RED_H)
                            for _ in range(2)])
        d_after = VGroup(*[Dot(ruler.n2p(0), radius=0.07, color=SECONDARY)
                           for _ in range(3)])
        txt_before = Text("原式各项：-1 次", font=FONT_NAME, font_size=19,
                          color=RED_H).next_to(d_before, UP, buff=0.25)
        txt_after = Text("乘完后各项：0 次，全部对齐", font=FONT_NAME,
                         font_size=19, color=SECONDARY).next_to(
                             d_after, UP, buff=0.25)
        self.play(Create(ruler), Write(r_lbl), run_time=1.0)
        self.play(FadeIn(d_before), Write(txt_before), run_time=0.9)
        self.wait(1.0)
        self.play(FadeOut(d_before), FadeOut(txt_before),
                  FadeIn(d_after), Write(txt_after), run_time=1.1)
        self.wait(0.6)
        lift = Text("每项恰好抬 1 次：缺几次，就补几次",
                    font=FONT_NAME, font_size=20, color=ACCENT).move_to(
                        DOWN * 2.35)
        self.play(Write(lift), run_time=1.0)
        self.wait(2.2)

        # ======================================================
        # 第三幕：配比手术刀之二 + 收束流程
        # ======================================================
        title3 = Text(
            "3. 平方升次 → 收束：扫描 · 配平 · 同除 · 一元",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title2, title3), run_time=1.0)
        self.play(FadeOut(E2), FadeOut(ruler), FadeOut(r_lbl),
                  FadeOut(d_after), FadeOut(txt_after), FadeOut(lift),
                  run_time=0.7)

        sq0 = MathTex(r"\sqrt{x}+\sqrt{y}=1", font_size=28,
                      color=WHITE).move_to(UP * 2.2)
        sq1 = MathTex(r"x+y+2\sqrt{xy}=1", font_size=28,
                      color=SECONDARY).move_to(UP * 2.2)
        sq_note = Text("根号是 1/2 次，平方一次升为整次 1 次",
                       font=FONT_NAME, font_size=19, color=GRAY).move_to(
                           UP * 1.35)
        self.play(Write(sq0), run_time=1.0)
        self.wait(0.8)
        self.play(ReplacementTransform(sq0, sq1), Write(sq_note),
                  run_time=1.3)
        self.wait(2.0)
        self.play(FadeOut(sq1), FadeOut(sq_note), run_time=0.6)

        boxes = [
            ("次数扫描", PRIMARY),
            ("配平手术刀\n乘 1 · 平方 · 平移 · 分解 · 旋转", SECONDARY),
            ("同除主元\n最高次幂", ACCENT),
            ("一元函数\nt = y/x", RED_H),
        ]
        flow = VGroup()
        for text, col in boxes:
            inner = Text(text, font=FONT_NAME, font_size=20, color=WHITE,
                         line_spacing=1.1)
            box = VGroup(inner, SurroundingRectangle(
                inner, color=col, buff=0.28, stroke_width=3,
                corner_radius=0.12))
            flow.add(box)
        flow.arrange(RIGHT, buff=0.55)
        flow.move_to(UP * 0.5)
        arrows = VGroup()
        for i in range(3):
            a = Arrow(flow[i].get_right(), flow[i + 1].get_left(),
                      buff=0.12, color=GRAY, stroke_width=3,
                      tip_length=0.16)
            arrows.add(a)
        self.play(LaggedStart(*[Write(b) for b in flow], lag_ratio=0.3),
                  run_time=2.0)
        self.play(LaggedStart(*[Create(a) for a in arrows],
                              lag_ratio=0.25), run_time=1.4)
        self.wait(0.8)

        motto = Text("口诀：次数不齐先配平，同除主元变一元；方向不正先旋转",
                     font=FONT_NAME, font_size=21, color=ACCENT).move_to(
                         DOWN * 2.4)
        self.play(Write(motto), run_time=1.3)
        self.wait(3.5)
