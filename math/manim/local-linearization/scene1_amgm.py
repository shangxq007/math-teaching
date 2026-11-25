"""第 6 章 · 导数与局部线性化引擎 —— 场景 1：基本不等式的半圆几何模型

叙事：水平直径 AB，左段 AC = a、右段 CB = b，以 AB 为直径作半圆。
      半径 R = (a+b)/2 恒定；从分界点 C 作垂线交半圆于 P，由射影定理 PC = sqrt(ab)。
      ValueTracker 让 C 沿直径滑动：R 不动、PC 变化；
      当 C 经过圆心（a = b）时 PC 与半径重合 —— 等号成立。

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene1_amgm.py AMGMGeometricProof

字体：中文统一 Noto Sans Mono CJK SC；数学一律 MathTex（原始字符串）。
"""

from manim import *
import numpy as np

FONT_NAME = "Noto Sans Mono CJK SC"

PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"
GRAY = "#9A9A9A"

DIAM = 6.0                 # 直径 AB 总长（固定）
XA = -DIAM / 2             # A 点横坐标
GEO = np.array([-1.7, -0.35, 0.0])   # 几何区整体平移（画幅左侧）


class AMGMGeometricProof(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        t = ValueTracker(1.6)          # C 点位置：AC = t
        self.t = t

        title = Text(
            "1. 基本不等式的几何本质：半圆射影定理",
            font=FONT_NAME, font_size=25, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.2)
        self.wait(0.5)

        def pt(x, y):
            return np.array([x, y, 0.0]) + GEO

        A, B, O = pt(XA, 0), pt(-XA, 0), pt(0, 0)
        R = DIAM / 2

        diam_line = Line(A, B, color=WHITE, stroke_width=4)
        semicircle = Arc(radius=R, start_angle=0, angle=PI, color=PRIMARY,
                         stroke_width=3, arc_center=O)
        dot_a = Dot(A, radius=0.07, color=PRIMARY)
        dot_b = Dot(B, radius=0.07, color=ACCENT)
        dot_o = Dot(O, radius=0.07, color=WHITE)
        lab_a = Text("A", font=FONT_NAME, font_size=20, color=PRIMARY)
        lab_a.next_to(dot_a, DOWN + LEFT, buff=0.1)
        lab_b = Text("B", font=FONT_NAME, font_size=20, color=ACCENT)
        lab_b.next_to(dot_b, DOWN + RIGHT, buff=0.1)
        lab_o = Text("O", font=FONT_NAME, font_size=20, color=WHITE)
        lab_o.next_to(dot_o, DOWN + LEFT, buff=0.12)

        # 动态元素
        seg_a = always_redraw(lambda: Line(A, self._c(), color=PRIMARY,
                                           stroke_width=9))
        seg_b = always_redraw(lambda: Line(self._c(), B, color=ACCENT,
                                           stroke_width=9))
        radius_od = always_redraw(lambda: Line(O, pt(0, R), color=ACCENT,
                                               stroke_width=6))
        chord_cp = always_redraw(lambda: Line(self._c(), self._p(),
                                              color=SECONDARY, stroke_width=6))
        dot_p = always_redraw(lambda: Dot(self._p(), radius=0.075,
                                          color=SECONDARY))
        dot_c = always_redraw(lambda: Dot(self._c(), radius=0.075, color=WHITE))

        # P 标在右侧、D 标在左侧，避免两点重合时压字
        lab_p = always_redraw(lambda: Text(
            "P", font=FONT_NAME, font_size=20, color=SECONDARY,
        ).next_to(self._p(), RIGHT, buff=0.26))
        lab_d = always_redraw(lambda: Text(
            "D", font=FONT_NAME, font_size=20, color=ACCENT,
        ).next_to(pt(0, R), UP + LEFT, buff=0.18))
        lab_c = always_redraw(lambda: Text(
            "C", font=FONT_NAME, font_size=20, color=WHITE,
        ).next_to(self._c(), DOWN + RIGHT, buff=0.14))

        rt = always_redraw(lambda: VGroup(
            Line(self._c() + 0.22 * RIGHT + 0.22 * UP,
                 self._c() + 0.22 * RIGHT, color=GRAY, stroke_width=2),
            Line(self._c() + 0.22 * RIGHT + 0.22 * UP,
                 self._c() + 0.22 * UP, color=GRAY, stroke_width=2),
        ))

        self.play(Create(diam_line), Create(semicircle), run_time=1.4)
        self.play(FadeIn(dot_a), FadeIn(dot_b), FadeIn(dot_o),
                  Write(lab_a), Write(lab_b), Write(lab_o), run_time=1.0)
        self.play(Create(seg_a), Create(seg_b), Create(radius_od),
                  Create(chord_cp), FadeIn(dot_p), FadeIn(dot_c),
                  Write(lab_p), Write(lab_d), Write(lab_c), Create(rt),
                  run_time=1.4)
        self.wait(0.8)

        # ---------------- 右侧静态对照面板 ----------------
        panel = VGroup(
            Text("长度对照", font=FONT_NAME, font_size=22, color=WHITE),
            MathTex(r"R=\frac{a+b}{2}", font_size=24, color=ACCENT),
            Text("算术平均 —— 不随 C 改变", font=FONT_NAME,
                 font_size=17, color=GRAY),
            MathTex(r"PC=\sqrt{ab}", font_size=24, color=SECONDARY),
            Text("几何平均 —— 随 C 改变", font=FONT_NAME,
                 font_size=17, color=GRAY),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        panel.move_to(np.array([4.5, 0.9, 0.0]))

        self.play(Write(panel), run_time=1.4)
        self.wait(0.5)

        cap1 = Text(
            "C 沿直径滑动：黄色半径不变，绿色垂线段始终够不到圆顶",
            font=FONT_NAME, font_size=19, color=GRAY,
        ).to_edge(DOWN, buff=0.35)
        self.play(Write(cap1), run_time=1.0)

        # ---------------- C 滑到圆心：等号成立 ----------------
        self.play(t.animate.set_value(3.0), run_time=3.0,
                  rate_func=there_and_back)
        self.wait(0.5)

        ring = always_redraw(lambda: Circle(
            radius=0.55, color=ACCENT, stroke_width=4,
        ).move_to(self._p()))
        eq = VGroup(
            MathTex(r"\frac{a+b}{2}\ge\sqrt{ab}", font_size=32, color=ACCENT),
            Text("当且仅当 a = b 时取等号", font=FONT_NAME,
                 font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.2)
        eq.move_to(np.array([4.5, 0.9, 0.0]))

        self.play(FadeOut(panel), FadeOut(cap1), run_time=0.6)
        self.play(t.animate.set_value(3.0), run_time=1.2,
                  rate_func=linear)
        self.add(ring)
        self.play(Write(eq), run_time=1.3)
        self.wait(0.8)
        self.play(t.animate.set_value(2.2), run_time=1.8,
                  rate_func=there_and_back)
        self.remove(ring)
        self.wait(0.8)

        final = Text(
            "几何意义：和一定时，两数越接近，乘积越大",
            font=FONT_NAME, font_size=21, color=ACCENT,
        ).to_edge(DOWN, buff=0.35)
        self.play(Write(final), run_time=1.2)
        self.wait(4.0)

    # ---------- 辅助 ----------
    def _c(self):
        return np.array([XA + self.t.get_value(), 0.0, 0.0]) + GEO

    def _p(self):
        tv = self.t.get_value()
        x = XA + tv
        y = float(np.sqrt(max(tv * (DIAM - tv), 1e-6)))
        return np.array([x, y, 0.0]) + GEO
