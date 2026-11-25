"""第 9 章 · 不动点：迭代、方程与几何变换的交汇 —— 场景 2：共轭化（换坐标）

叙事：以 a_{n+1}=1/2 a_n+1, x*=2 为例。
      令 b_n=a_n-x*，把锚点搬到原点：
        a_{n+1}-2 = 1/2 a_n - 1 = 1/2(a_n-2)，即 b_{n+1}=1/2 b_n
      一阶线性递推 → 等比数列
      → 几何：两条数轴同步——a 轴上的点朝 x*=2 靠拢；
        平移后的 b 轴上，每条轨道到原点的距离每步 ×1/2
      → 通项：b_n=-2·(1/2)^n，a_n=2-2^{1-n}；
        公式族：a_{n+1}=pa_n+q ⇒ x*=q/(1-p)，a_n=x*+p^n(a_0-x*)
        与第 8 章同构：除以尺度（齐次化）与减去锚点（平移），
        都是把不动点搬到原点

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene2_conjugation.py ConjugationGeometric
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


class ConjugationGeometric(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ======================================================
        # 第一幕：代数变形——令 b_n = a_n - x*
        # ======================================================
        title1 = Text(
            "1. 换坐标：令 b_n = a_n - x*",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=1.1)
        self.wait(0.4)

        E0 = MathTex(r"a_{n+1}=\frac12 a_n+1,\qquad x^*=2",
                     font_size=30, color=WHITE).move_to(UP * 2.15)
        E1 = MathTex(r"a_{n+1}-2=\frac12 a_n-1=\frac12\,(a_n-2)",
                     font_size=30, color=WHITE).move_to(UP * 1.15)
        op1 = Text("两边减去不动点 x*=2", font=FONT_NAME, font_size=19,
                   color=GRAY).next_to(E1, RIGHT, buff=0.35)
        E2 = MathTex(r"b_n=a_n-2\ \Longrightarrow\ b_{n+1}=\frac12\,b_n",
                     font_size=32, color=ACCENT).move_to(DOWN * 0.15)
        concl = Text("一阶线性递推 → 等比数列（公比 1/2）",
                     font=FONT_NAME, font_size=21, color=SECONDARY).move_to(
                         DOWN * 1.05)

        self.play(Write(E0), run_time=1.2)
        self.wait(0.8)
        self.play(ReplacementTransform(E0, E1), Write(op1), run_time=1.4)
        self.wait(1.4)
        self.play(FadeOut(op1), ReplacementTransform(E1, E2), run_time=1.4)
        self.wait(0.6)
        self.play(FadeIn(concl), run_time=1.0)
        self.wait(2.4)

        # ======================================================
        # 第二幕：几何——平移数轴，距离每步减半
        # ======================================================
        title2 = Text(
            "2. 几何：平移数轴，轨道朝原点等比收缩",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=1.0)
        self.play(FadeOut(E2), FadeOut(concl), run_time=0.6)

        items = []
        top_nl = NumberLine(x_range=[-1, 4], length=8.6,
                            include_numbers=True, font_size=15,
                            color=GRAY).move_to(UP * 1.95)
        bot_nl = NumberLine(x_range=[-4, 2], length=8.6,
                            include_numbers=True, font_size=15,
                            color=GRAY).move_to(DOWN * 1.35)
        top_lbl = Text("a 轴", font=FONT_NAME, font_size=18,
                       color=PRIMARY).next_to(top_nl, LEFT, buff=0.25)
        bot_lbl = Text("b 轴（b = a - 2）", font=FONT_NAME, font_size=18,
                       color=SECONDARY).next_to(bot_nl, LEFT, buff=0.25)

        anchor_top = Dot(top_nl.n2p(2), radius=0.09, color=ACCENT)
        anchor_lbl = MathTex(r"x^*=2", font_size=19, color=ACCENT)
        anchor_lbl.next_to(anchor_top, UP, buff=0.16)
        origin_bot = Dot(bot_nl.n2p(0), radius=0.09, color=ACCENT)
        origin_lbl = MathTex(r"0", font_size=19, color=ACCENT)
        origin_lbl.next_to(origin_bot, DOWN + RIGHT, buff=0.16)

        shift_arrow = Arrow(top_nl.n2p(2) + DOWN * 0.12,
                            bot_nl.n2p(0) + UP * 0.12,
                            color=ACCENT, stroke_width=3,
                            tip_length=0.16)
        shift_lbl = Text("平移 -2", font=FONT_NAME, font_size=17,
                         color=ACCENT).next_to(shift_arrow, RIGHT,
                                                buff=0.15)

        items += [top_nl, bot_nl, top_lbl, bot_lbl, anchor_top, anchor_lbl,
                  origin_bot, origin_lbl, shift_arrow, shift_lbl]
        self.play(Create(top_nl), Create(bot_nl), run_time=1.2)
        self.play(Write(top_lbl), Write(bot_lbl), run_time=0.9)
        self.play(FadeIn(anchor_top), Write(anchor_lbl),
                  FadeIn(origin_bot), Write(origin_lbl), run_time=1.0)
        self.play(Create(shift_arrow), Write(shift_lbl), run_time=1.0)
        self.wait(1.8)

        a_vals = [0.0, 1.0, 1.5, 1.75, 1.875]
        segs = VGroup()
        for i, a in enumerate(a_vals):
            b = a - 2.0
            da = Dot(top_nl.n2p(a), radius=0.07, color=PRIMARY)
            db = Dot(bot_nl.n2p(b), radius=0.07, color=SECONDARY)
            la = MathTex("a_%d" % i, font_size=15, color=PRIMARY)
            la.next_to(da, UP + LEFT, buff=0.1)
            lb = MathTex("b_%d" % i, font_size=15, color=SECONDARY)
            lb.next_to(db, DOWN + LEFT, buff=0.1)
            link = DashedLine(top_nl.n2p(a) + DOWN * 0.08,
                              bot_nl.n2p(b) + UP * 0.08,
                              color=GRAY, stroke_width=1.5)
            items += [da, db, la, lb, link]
            self.play(FadeIn(da), FadeIn(db), FadeIn(link),
                      Write(la), Write(lb), run_time=0.8)
            if i > 0:
                seg = Line(bot_nl.n2p(0) + UP * (0.06 * i),
                           bot_nl.n2p(b) + UP * (0.06 * i),
                           color=ACCENT, stroke_width=2.5)
                segs.add(seg)
                items.append(seg)
                self.play(Create(seg), run_time=0.6)
            self.wait(0.4)

        ratio = Text("每走一步，到原点的距离 × 1/2",
                     font=FONT_NAME, font_size=20, color=ACCENT).move_to(
                         DOWN * 2.75)
        items.append(ratio)
        self.play(Write(ratio), run_time=1.1)
        self.wait(2.4)

        # ======================================================
        # 第三幕：通项与公式族
        # ======================================================
        title3 = Text(
            "3. 通项与公式族：a_n = x* + p^n (a_0 - x*)",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title2, title3), run_time=1.0)
        self.play(FadeOut(*items), run_time=0.7)

        panel = VGroup(
            VGroup(Text("本例 ", font=FONT_NAME, font_size=20,
                        color=WHITE),
                   MathTex(r"b_0=-2", font_size=22, color=ACCENT)),
            MathTex(r"b_n=-2\left(\frac12\right)^n",
                    font_size=25, color=WHITE),
            MathTex(r"a_n=2-2^{\,1-n}", font_size=28, color=ACCENT),
            VGroup(Text("检验 ", font=FONT_NAME, font_size=19,
                        color=GRAY),
                   MathTex(r"a_0=0,\ a_1=1", font_size=20,
                           color=GRAY)),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        panel.move_to(UP * 1.6 + LEFT * 2.9)
        self.play(Write(panel), run_time=1.6)
        self.wait(1.0)

        fam = VGroup(
            MathTex(r"a_{n+1}=pa_n+q\ \Rightarrow\ "
                    r"x^*=\frac{q}{1-p},\quad a_n=x^*+p^n(a_0-x^*)",
                    font_size=22, color=WHITE),
            VGroup(Text("p=1 退化为等差；|p|>1 且起点不在 x* 时发散",
                        font=FONT_NAME, font_size=19, color=SECONDARY)),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        fam.move_to(DOWN * 0.6 + LEFT * 1.4)
        box = SurroundingRectangle(fam, color=ACCENT, buff=0.24,
                                   stroke_width=3)
        self.play(Write(fam), run_time=1.5)
        self.play(Create(box), run_time=0.9)
        self.wait(0.8)

        caption = Text(
            "与第 8 章同构：除以尺度（齐次化）与减去锚点（平移），"
            "都把不动点搬到原点",
            font=FONT_NAME, font_size=20, color=ACCENT,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(caption), run_time=1.3)
        self.wait(4.0)
