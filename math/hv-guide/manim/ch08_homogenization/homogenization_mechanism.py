# -*- coding: utf-8 -*-
"""齐次化机制可视化：把「次数配平」演出来，而不是背步骤。

叙事轴（一条线）：混次诊断 -> 配平成齐次 -> 同除主元降为一元 t -> 与考纲通法对读。
同源教材内容：
  - hv-guide/chapters/08_homogenization.tex（第 8 章：第一性原理、方法归纳、单位圆母题）
  - hv-guide/chapters/drill_master_ch04.tex 母题二（P(2,0)，k_PA·k_PB=-1 的齐次化构造）
四场：
  DegreeScan        原式结构与次数扫描（混次 vs 齐次）
  Homogenize        把直线「归一」成 1，乘进一次项（P(2,0) 模型）
  DivideAndRoots    同除 x'^2 令 t，两根之积出定点；单位圆同源机制
  CompareTable      考纲通法 vs 平移齐次化 对读表（drill 表格口径）
"""
from manim import *

# ---------------------------------------------------------------------
# 字体（跨平台替换）：
#   Windows 自带 SimHei；
#   macOS 请改为 "Heiti TC" 或 "STHeiti"；
#   Linux 若未安装 SimHei，改为系统已装的中文字体，例如
#   "Noto Sans CJK SC" / "WenQuanYi Zen Hei"。
#   （本机实测：缺 SimHei 时 Pango 会按字形回退到已装 CJK 字体，中文仍正常。）
# ---------------------------------------------------------------------
FONT_NAME = "SimHei"

BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"
GREY = "#9AA0A6"


def CN(s, size=22, color=WHITE, bold=False):
    """全片统一的中文文案入口。"""
    kw = dict(font=FONT_NAME, font_size=size, color=color)
    if bold:
        kw["weight"] = BOLD
    return Text(s, **kw)


def chip(text, color, size=19):
    """次数标签小药丸（衬底色块 + 文字）。"""
    t = CN(text, size=size, color=color, bold=True)
    bg = BackgroundRectangle(t, color=BG, fill_opacity=0.92, buff=0.07)
    return VGroup(bg, t)


def chip_under(part, text, color, drop=0.28):
    """把次数标签钉在公式某一项的正下方。"""
    c = chip(text, color)
    c.move_to([part.get_center()[0], part.get_bottom()[1] - drop, 0])
    return c


# =====================================================================
# 第一场：原式结构与次数扫描
# =====================================================================
class DegreeScan(Scene):
    """原式结构：先扫次数——齐次式才只认射线 t=y/x。"""

    def construct(self):
        self.camera.background_color = BG

        title = CN("原式结构：先做「次数扫描」", 36, PRIMARY, bold=True)
        title.to_edge(UP, buff=0.25)
        sub = CN("齐次化不是背步骤，而是问一句：各项次数一样吗？", 21, GREY)
        sub.next_to(title, DOWN, buff=0.10)
        self.play(FadeIn(title), FadeIn(sub), run_time=1.0)
        self.wait(0.6)

        # ---------- 左：P(2,0) 垂弦模型 ----------
        lx = -3.55
        card_l = CN("模型 · 椭圆垂弦（第 4 章 drill · 母题二）", 20, ACCENT)
        card_l.move_to([lx, 2.6, 0])

        r1 = VGroup(CN("椭圆 ", 20),
                    MathTex(r"\frac{x^2}{4}+\frac{y^2}{3}=1", font_size=28),
                    CN(" 上一点 ", 20),
                    MathTex(r"P(2,0)", font_size=28)).arrange(RIGHT, buff=0.06)
        r1.move_to([lx, 2.22, 0])
        r2 = VGroup(CN("弦 AB 满足 ", 20),
                    MathTex(r"PA\perp PB", font_size=28)).arrange(RIGHT, buff=0.06)
        r2.move_to([lx, 1.82, 0])
        r3 = VGroup(CN("即 ", 20),
                    MathTex(r"k_{PA}\cdot k_{PB}=-1", font_size=28)).arrange(
                        RIGHT, buff=0.06)
        r3.move_to([lx, 1.42, 0])
        r4 = VGroup(CN("平移原点至 P：", 20),
                    MathTex(r"x'=x-2,\ y'=y", font_size=26)).arrange(RIGHT,
                                                                    buff=0.06)
        r4.move_to([lx, 1.02, 0])

        self.play(FadeIn(card_l), FadeIn(r1), FadeIn(r2), FadeIn(r3),
                  run_time=1.0)
        self.wait(0.4)
        self.play(FadeIn(r4), run_time=0.8)
        self.wait(0.3)

        eq0 = MathTex(r"3x'^2", r"+", r"4y'^2", r"+", r"12x'", r"=", r"0",
                      font_size=44)
        eq0[0].set_color(PRIMARY)
        eq0[2].set_color(PRIMARY)
        eq0[4].set_color(ACCENT)
        eq0.move_to([lx, 0.28, 0])
        self.play(Write(eq0), run_time=1.2)
        self.wait(0.3)

        c0 = chip_under(eq0[0], "2 次", PRIMARY)
        c2 = chip_under(eq0[2], "2 次", PRIMARY)
        c4 = chip_under(eq0[4], "1 次", ACCENT)
        self.play(FadeIn(c0), FadeIn(c2), FadeIn(c4), run_time=0.8)
        self.wait(0.3)

        # 混次诊断：脉冲那个「落单」的一次项
        self.play(Indicate(eq0[4], color=ACCENT, scale_factor=1.25),
                  run_time=1.0)
        cap_l = CN("常数项被平移吃掉，一次项仍在 → 混次", 22, ACCENT, bold=True)
        cap_l.move_to([lx, -0.95, 0])
        self.play(FadeIn(cap_l), run_time=0.8)
        self.wait(0.6)

        # ---------- 右：齐次式对照 ----------
        rx = 3.55
        card_r = CN("对照 · 齐次式（第 8 章 · 单位圆）", 20, SECONDARY)
        card_r.move_to([rx, 2.6, 0])
        eqr = MathTex(r"\frac{1}{x^2}", r"+", r"\frac{1}{y^2}", font_size=40)
        eqr[0].set_color(SECONDARY)
        eqr[2].set_color(SECONDARY)
        eqr.move_to([rx, 2.05, 0])
        d0 = chip_under(eqr[0], "−2 次", SECONDARY)
        d2 = chip_under(eqr[2], "−2 次", SECONDARY)

        cap_r1 = VGroup(CN("每一项同次 ⇒ 值只依赖射线比例 ", 20),
                        MathTex(r"t=\frac{y}{x}", font_size=26)).arrange(
                            RIGHT, buff=0.06)
        cap_r1.move_to([rx, 1.15, 0])
        cap_r2 = CN("约束 x²+y²=1 是「1 的代换」的来源", 20)
        cap_r2.move_to([rx, 0.65, 0])

        self.play(FadeIn(card_r), Write(eqr), run_time=1.0)
        self.play(FadeIn(d0), FadeIn(d2), run_time=0.6)
        self.play(FadeIn(cap_r1), FadeIn(cap_r2), run_time=0.8)
        self.wait(0.6)

        # ---------- 总结论 ----------
        verd1 = CN("判定：齐次 ⇔ 所有项同次；", 24, WHITE, bold=True)
        verd2 = CN("混次式先配平次数，再谈同除。", 24, ACCENT, bold=True)
        verd = VGroup(verd1, verd2).arrange(RIGHT, buff=0.15)
        verd.move_to([0, -2.7, 0])
        self.play(FadeIn(verd), run_time=1.0)
        self.wait(1.2)


# =====================================================================
# 第二场：配平——归一成 1，乘进一次项
# =====================================================================
class Homogenize(Scene):
    """配平：直线归一为 1，乘进一次项，混次变齐次（P(2,0) 模型）。"""

    def construct(self):
        self.camera.background_color = BG

        title = CN("配平：把直线「归一」成 1，乘进一次项", 34, PRIMARY,
                   bold=True)
        title.to_edge(UP, buff=0.30)
        self.play(FadeIn(title), run_time=1.0)
        self.wait(0.4)

        step1 = CN("平移后的椭圆：二次项 + 一次项（混次，承上一场）", 20, GREY)
        step1.move_to([0, 2.82, 0])
        self.play(FadeIn(step1), run_time=0.7)

        eqA = MathTex(r"3x'^2", r"+", r"4y'^2", r"+", r"12x'", r"=", r"0",
                      font_size=40)
        eqA[0].set_color(PRIMARY)
        eqA[2].set_color(PRIMARY)
        eqA[4].set_color(ACCENT)
        eqA.move_to([0, 2.22, 0])
        hl = SurroundingRectangle(eqA[4], color=ACCENT, buff=0.06)
        self.play(Write(eqA), Create(hl), run_time=1.0)
        self.wait(0.4)

        op1 = VGroup(CN("设弦 ", 20),
                     MathTex(r"AB:\ m'x'+n'y'=1", font_size=28),
                     CN("（不过新原点，可归一）", 20)).arrange(RIGHT, buff=0.08)
        op1.move_to([0, 1.55, 0])
        arr1 = Arrow([0, 1.92, 0], [0, 1.78, 0], buff=0.08, color=GREY,
                     stroke_width=3)
        self.play(FadeIn(arr1), FadeIn(op1), run_time=0.9)
        self.wait(0.3)

        op1b = CN("把 1 = m'x'+n'y' 乘进一次项", 21, ACCENT, bold=True)
        op1b.move_to([0, 1.08, 0])
        arr2 = Arrow([0, 1.42, 0], [0, 1.24, 0], buff=0.08, color=GREY,
                     stroke_width=3)
        self.play(FadeIn(arr2), FadeIn(op1b), run_time=0.8)
        self.wait(0.2)

        eqB = MathTex(r"3x'^2", r"+", r"4y'^2", r"+",
                      r"12x'(m'x'+n'y')", r"=", r"0", font_size=38)
        eqB[0].set_color(PRIMARY)
        eqB[2].set_color(PRIMARY)
        eqB[4].set_color(ACCENT)
        eqB.move_to([0, 0.62, 0])
        self.play(FadeOut(hl), FadeOut(arr1), FadeOut(arr2), FadeOut(op1b),
                  ReplacementTransform(eqA, eqB), run_time=1.2)
        self.wait(0.3)

        op2 = CN("展开并合并同类项", 20, GREY)
        op2.move_to([0, 0.14, 0])
        arr3 = Arrow([0, 0.44, 0], [0, 0.30, 0], buff=0.08, color=GREY,
                     stroke_width=3)
        self.play(FadeOut(arr3), FadeIn(op2), run_time=0.7)
        arr4 = Arrow([0, -0.02, 0], [0, -0.20, 0], buff=0.08, color=GREY,
                     stroke_width=3)
        self.play(FadeIn(arr4), run_time=0.5)

        eqC = MathTex(r"(3+12m')x'^2", r"+", r"12n'x'y'", r"+",
                      r"4y'^2", r"=", r"0", font_size=36)
        for i in (0, 2, 4):
            eqC[i].set_color(SECONDARY)
        eqC.move_to([0, -0.62, 0])
        self.play(ReplacementTransform(eqB, eqC), run_time=1.2)
        self.wait(0.3)

        cc0 = chip_under(eqC[0], "2 次", SECONDARY)
        cc1 = chip_under(eqC[2], "2 次", SECONDARY)
        cc2 = chip_under(eqC[4], "2 次", SECONDARY)
        self.play(FadeIn(cc0), FadeIn(cc1), FadeIn(cc2), run_time=0.7)
        self.wait(0.4)

        key = VGroup(CN("关键：", 21, ACCENT, bold=True),
                     MathTex(r"m'x'+n'y'=1", font_size=28, color=ACCENT),
                     CN(" 是恒等代入；每一步都是同构变形，值不变。", 21))
        key.arrange(RIGHT, buff=0.10)
        key.move_to([0, -2.05, 0])
        self.play(FadeIn(key), run_time=0.9)
        self.wait(0.3)

        bottom = CN("配平结果：每一项都是二次 → 下一场同除 x'² 降为一元 t",
                    21, WHITE)
        bottom.move_to([0, -2.9, 0])
        self.play(FadeIn(bottom), run_time=0.9)
        self.wait(1.2)


# =====================================================================
# 第三场：同除降维——令 t = y'/x'
# =====================================================================
class DivideAndRoots(Scene):
    """同除 x'^2 令 t：两根之积出定点；单位圆同源机制并列。"""

    def construct(self):
        self.camera.background_color = BG

        title = CN("降维：同除 x'²，令 t = y'/x'", 34, PRIMARY, bold=True)
        title.to_edge(UP, buff=0.30)
        self.play(FadeIn(title), run_time=1.0)
        self.wait(0.3)

        # ---------- 左列：P(2,0) 垂弦题收束 ----------
        lx = -3.55
        l0 = CN("配平后的齐次式（承上一场）", 19, GREY)
        l0.move_to([lx, 2.82, 0])
        l1 = MathTex(r"(3+12m')x'^2+12n'x'y'+4y'^2=0", font_size=28)
        l1.move_to([lx, 2.42, 0])
        self.play(FadeIn(l0), FadeIn(l1), run_time=0.9)
        self.wait(0.3)

        arr = Arrow([lx, 2.10, 0], [lx, 1.82, 0], buff=0.08, color=GREY,
                    stroke_width=3)
        lab = VGroup(CN("同除 x'²，令 ", 19),
                     MathTex(r"t=\frac{y'}{x'}", font_size=26)).arrange(
                        RIGHT, buff=0.05)
        lab.move_to([lx, 1.58, 0])
        self.play(FadeIn(arr), FadeIn(lab), run_time=0.8)

        l2 = MathTex(r"4t^2+12n't+(3+12m')=0", font_size=30)
        l2.move_to([lx, 1.05, 0])
        self.play(FadeIn(l2), run_time=0.9)
        self.wait(0.3)

        l3 = VGroup(CN("两根之积 ", 20),
                    MathTex(r"k_1k_2=\frac{3+12m'}{4}", font_size=28)).arrange(
                        RIGHT, buff=0.08)
        l3.move_to([lx, 0.42, 0])
        self.play(FadeIn(l3), run_time=0.9)
        self.wait(0.3)

        l4 = MathTex(r"\frac{3+12m'}{4}=-1\ \Rightarrow\ "
                     r"m'=-\frac{7}{12}", font_size=28)
        l4.move_to([lx, -0.30, 0])
        box4 = SurroundingRectangle(l4, color=SECONDARY, buff=0.12)
        self.play(FadeIn(l4), Create(box4), run_time=1.0)
        self.wait(0.3)

        l5 = VGroup(MathTex(r"x'=\frac{1}{m'}=-\frac{12}{7}", font_size=24),
                    CN("，还原 ", 20),
                    MathTex(r"x=x'+2=\frac{2}{7}", font_size=24)).arrange(
                        RIGHT, buff=0.10)
        l5.move_to([lx, -1.02, 0])
        self.play(FadeIn(l5), run_time=0.9)
        self.wait(0.3)

        l6 = VGroup(CN("定点 ", 22, SECONDARY, bold=True),
                    MathTex(r"Q\left(\frac{2}{7},0\right)", font_size=30))
        l6 = l6.arrange(RIGHT, buff=0.10)
        l6.move_to([lx, -1.72, 0])
        box6 = SurroundingRectangle(l6, color=SECONDARY, buff=0.14)
        self.play(FadeIn(l6), Create(box6), run_time=1.0)
        self.wait(0.3)

        lc = CN("三行恒等变形，几乎不用韦达（drill · 法二口径）", 19, ACCENT)
        lc.move_to([lx, -2.35, 0])
        self.play(FadeIn(lc), run_time=0.7)
        self.wait(0.4)

        # ---------- 右列：单位圆同源机制 ----------
        rx = 3.55
        r0 = CN("同源机制 · 单位圆（第 8 章母题二）", 20, SECONDARY, bold=True)
        r0.move_to([rx, 2.82, 0])
        r1 = VGroup(CN("条件 ", 20),
                    MathTex(r"x^2+y^2=1", font_size=28),
                    CN(" 当「1」用", 20)).arrange(RIGHT, buff=0.06)
        r1.move_to([rx, 2.32, 0])
        self.play(FadeIn(r0), FadeIn(r1), run_time=0.9)
        self.wait(0.3)

        r2 = MathTex(r"\frac{1}{x^2}+\frac{1}{y^2}", font_size=30)
        r2.set_color(SECONDARY)
        r2.move_to([rx, 1.80, 0])
        self.play(FadeIn(r2), run_time=0.9)
        self.wait(0.2)

        r3 = VGroup(CN("乘「1」并同除 x²，令 t：", 19),
                    MathTex(r"\frac{(1+t^2)^2}{t^2}", font_size=26)).arrange(
                        RIGHT, buff=0.08)
        r3.move_to([rx, 1.28, 0])
        r4 = MathTex(r"=\left(t+\frac{1}{t}\right)^2\ge 4", font_size=26)
        r4.move_to([rx, 0.72, 0])
        self.play(FadeIn(r3), FadeIn(r4), run_time=0.9)
        self.wait(0.3)

        rc = CN("先配平次数，再同除主元——同一招", 19, ACCENT)
        rc.move_to([rx, 0.12, 0])
        self.play(FadeIn(rc), run_time=0.7)
        self.wait(0.5)

        bottom = CN("同除主元最高次幂：把二元压成一元比例 t；除法中次数差保持不变。",
                    21, WHITE)
        bottom.move_to([0, -3.35, 0])
        self.play(FadeIn(bottom), run_time=0.9)
        self.wait(1.2)


# =====================================================================
# 第四场：对读表
# =====================================================================
class CompareTable(Scene):
    """对读：考纲通法 vs 平移齐次化（drill 表格口径，P(2,0) 模型）。"""

    def construct(self):
        self.camera.background_color = BG

        title = CN("对读：考纲通法 vs 平移齐次化", 32, PRIMARY, bold=True)
        title.to_edge(UP, buff=0.25)
        sub = CN("同一道 P(2,0) 垂弦题 · 第 4 章 drill 母题二", 20, GREY)
        sub.next_to(title, DOWN, buff=0.10)
        self.play(FadeIn(title), FadeIn(sub), run_time=1.0)
        self.wait(0.4)

        x0, x1, x2, x3 = -6.7, -5.1, 0.7, 6.7
        col_c = [(x0 + x1) / 2, (x1 + x2) / 2, (x2 + x3) / 2]

        hdr_y = 2.42
        headers = [CN("视角", 20, GREY, bold=True),
                   CN("考纲通法", 22, WHITE, bold=True),
                   CN("平移齐次化", 22, PRIMARY, bold=True)]
        for htxt, cx in zip(headers, col_c):
            htxt.move_to([cx, hdr_y, 0])
        self.play(*[FadeIn(h) for h in headers], run_time=0.8)

        rows = [
            ("思路",
             "设线联立，韦达回代，\n解参数方程",
             "平移到 P，归一\n乘进一次项"),
            ("计算量",
             "代入 + 因式分解，\n步骤多但每步熟悉",
             "三行恒等变形，\n只用两根之积"),
            ("何时用",
             "解答题写满\n规范步骤",
             "选填预判\n定点秒算"),
            ("风险点",
             "忘 m≠−2k 增根、\n漏竖直弦检验",
             "查 x′≠0、\n过新原点无解"),
        ]
        row_ys = [1.62, 0.76, -0.10, -0.96]
        for (label, c1, c2), ry in zip(rows, row_ys):
            lm = CN(label, 20, GREY, bold=True)
            lm.move_to([col_c[0], ry, 0])
            t1 = CN(c1, 19, WHITE)
            t1.move_to([col_c[1], ry, 0])
            t2 = CN(c2, 19, "#D6F0F8")
            t2.move_to([col_c[2], ry, 0])
            self.play(FadeIn(lm), FadeIn(t1), FadeIn(t2), run_time=0.8)
            self.wait(0.2)

        # 网格线（置于行块之间的空档，避免穿过文字）
        seps_y = [2.02, 1.19, 0.33, -0.53, -1.40]
        h_lns = [Line([x0, yy, 0], [x3, yy, 0], color=GREY,
                      stroke_opacity=0.5, stroke_width=2) for yy in seps_y]
        v_lns = [Line([xv, seps_y[0], 0], [xv, seps_y[-1], 0], color=GREY,
                      stroke_opacity=0.3, stroke_width=1.5)
                 for xv in (x1, x2)]
        self.play(*[Create(ln) for ln in h_lns],
                  *[Create(ln) for ln in v_lns], run_time=1.0)
        self.wait(0.4)

        freg = MathTex(r"Q=\left(\frac{x_0(a^2-b^2)}{a^2+b^2},\ "
                       r"\frac{y_0(b^2-a^2)}{a^2+b^2}\right)", font_size=26)
        freg.move_to([0, -1.95, 0])
        note = CN("同一结论：Frégier 公式代入 P(2,0) 也是 Q(2/7, 0)", 20, GREY)
        note.move_to([0, -2.50, 0])
        self.play(FadeIn(freg), FadeIn(note), run_time=0.9)
        self.wait(0.3)

        bottom = CN("考场上：先用齐次化（或 Frégier 公式）预判答案，再用通法把步骤写满。",
                    21, ACCENT)
        bottom.move_to([0, -3.20, 0])
        self.play(FadeIn(bottom), run_time=0.9)
        self.wait(1.5)
