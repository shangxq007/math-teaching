"""第 9 章 §5 · 莫比乌斯变换的双不动点：源、汇与共轭流场

唯一算例（用户指定，不得改数）：

    f(z) = (3z + 4) / (z + 3)

对应矩阵 M = [[3, 4], [1, 3]]：
  * 特征值 λ1 = 5、λ2 = 1，特征向量 (2, 1)、(-2, 1)
    ⇒ 射影直线上的两个不动点 z = ±2；
  * Δ = (a-d)^2 + 4bc = 16 > 0 → 双曲型（一源一汇）；
  * 乘子 |λ| = λ1/λ2 = 5：z1 = 2 处 |f'(2)| = 1/|λ| = 1/5 < 1，是【汇】；
    z2 = -2 处 |f'(-2)| = |λ| = 5 > 1，是【源】。

流场的严格构造（不是示意圆）：
  共轭坐标 w=(z-2)/(z+2) 下，迭代是纯伸缩 w → w/|λ| = w/5。
  故 |w|=k 给出【等距比圆】（阿波罗尼奥斯圆）：
      |z-2| = k|z+2|  ⇔  |z - c_k| = r_k,
      c_k = 2(1+k^2)/(1-k^2),  r_k = 4k/|1-k^2|   (k≠1)；
      k=1 退化为直线 x=0（两不动点的中垂线，即「分隔线」）。
  这些圆【不经过】±2（比值在 2 处为 0、在 -2 处为 ∞），而是把源、汇
  分别围在两侧：k<1 时围住汇 2，k>1 时围住源 -2。k=1 是两者的分界。
  每一步 |w| → |w|/5，轨道沿圆弧从大 k 走向小 k，最终没入汇 2。

  脚本只画 k∈{0.35, 0.5, 0.7}（右侧，围住汇）与 k=1（虚线分隔线）；
  幕二的共轭同心圆半径恰取同一组数 {0.35,0.5,0.7,1}，一一对应。
  数值自验：每个所画圆上的采样点到源 -2、极点 -3 的距离均 > 0.2。

    数值断言（脚本内自验，非装饰）：
        f(±2)=±2；f'(2)=1/5、f'(-2)=5；Δ=16；M(2,1)=5(2,1)、M(-2,1)=(-2,1)；
        极点 pole=-3；conj 把 2↦0、-2↦∞；f(z) 后再取 w 恰为 w/5；
        所有网格顶点与采样流线上的点到极点的距离均 > R_GUARD=0.40（硬性约束）。

叙事弧（一条轴：换坐标系把不动点搬到 0 与 ∞）：
  幕一  复平面网格在 f 下的像：正交直线网被弯成过 ±2 的圆网，
        ±2 两点钉住不动，极点 -3 用挖掉的洞标出；再叠上真正的流线（源→汇）。
  幕二  共轭 w=(z-2)/(z+2)：汇 2→0、源 -2→∞。两族流线同时显形：
        等距比圆 |w|=k（围住汇）→ 以 0 为心的同心圆；
        过 ±2 的圆 → 过 0 的直线（射线，即 §5 右图）。迭代退化为 w_{n+1}=(1/5)w_n，
        沿圆弧或射线向心收缩。
  幕三  乘子的两种读法：甲）对汇的距离 d_{n+1}≈(1/5)d_n（局部线性化）；
        乙）共轭模 r_{n+1}=(1/5)r_n（精确等比）。最后放大源侧近域，
        同一 f 把点以 5 倍推离。收尾：|f'| 与 |λ| 互为倒数。

字体：中文统一 Text(..., font=FONT_NAME)；数学一律 MathTex（原始字符串）。
渲染（必须走 skill 的 wrapper + TL 自带 dvisvgm）：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql mobius_flow_field.py MobiusFlowField
"""

from manim import *
import numpy as np

# ---------------------------------------------------------------- 字体 / 配色
# FONT_NAME —— 跨平台替换说明：
#   Windows ：原生黑体，"SimHei" 可直接用（本机无此字体时的默认值）。
#   macOS   ：改为 "PingFang SC" 或 "Heiti SC"。
#   Linux   ：本机 fc-list 无 SimHei，改用 "Noto Sans Mono CJK SC"
#             （唯一可用的等宽中文字体，Pango 比例字体会崩字距）；
#             也可用 "WenQuanYi Zen Hei"（非等宽）。
FONT_NAME = "SimHei"

BG = "#1C1C1C"
PRIMARY = "#58C4DD"      # 主色：复平面 / 共轭同心圆
SECONDARY = "#83C167"    # 次色：迭代轨道、结论
ACCENT = "#FFFF00"       # 强调：公式、结论框
RED_H = "#FF5252"        # 源（排斥、推离）
ORANGE = "#F5A623"       # 流向箭头、探针链
GRAY = "#9E9E9E"         # 结构性元素（坐标轴、注释）
POLE_COL = "#B06AB3"     # 极点 z=-3

# ---------------------------------------------------------------- 唯一算例常数
A, B, C, D = 3.0, 4.0, 1.0, 3.0      # f(z)=(A z+B)/(C z+D)
LAM1, LAM2 = 5.0, 1.0                # 矩阵 M=[[3,4],[1,3]] 的两个特征值
LAM = LAM1 / LAM2                    # |λ|：源侧乘子（共轭坐标中表现为 ÷|λ|）
FP_SINK, FP_SOURCE = 2.0, -2.0       # 汇 / 源
POLE = -D / C                        # 极点 z = -3
R_GUARD = 0.40                       # 网格与流线对极点的最小间距（>0.35，硬性约束）


def f_num(z):
    """f(z)=(3z+4)/(z+3)，numpy 复数安全。"""
    z = complex(z)
    den = C * z + D
    if abs(den) < 1e-15:
        return complex(np.inf, 0.0)
    return (A * z + B) / den


def conj_num(z):
    """共轭坐标 w=(z-2)/(z+2)：汇→0，源→∞。"""
    if abs(z - FP_SOURCE) < 1e-15:
        return complex(np.inf, 0.0)
    return (z - FP_SINK) / (z - FP_SOURCE)


def apollonius(k):
    """等距比线 |w|=k（w=(z-2)/(z+2)）的圆：返回 (圆心, 半径)；k==1 为中垂线。"""
    cen = FP_SINK * (1.0 + k * k) / (1.0 - k * k)
    rad = (FP_SINK - FP_SOURCE) * k / abs(1.0 - k * k)
    return cen, rad


# 幕一与幕二共用同一组 k：保证「共轭后同心圆」与 z 平面流线一一对应
STREAM_KS = [0.35, 0.5, 0.7]
SEP_K = 1.0


def _assert_setup():
    """数值自验：不动点、乘子、特征方向、共轭映射、复合关系、极点间距。"""
    eps = 1e-9
    M = np.array([[A, B], [C, D]], dtype=float)
    ev = np.linalg.eigvals(M)

    # 1) 不动点精确为 ±2
    assert abs(f_num(FP_SINK) - FP_SINK) < eps, "f(2) != 2"
    assert abs(f_num(FP_SOURCE) - FP_SOURCE) < eps, "f(-2) != -2"
    # 2) 判别式 Δ=(a-d)^2+4bc = 16 > 0（双曲型）
    assert abs(((A - D) ** 2 + 4 * B * C) - 16.0) < eps
    # 3) 特征值恰为 5 与 1
    srt = sorted(np.abs(ev).tolist())
    assert abs(srt[0] - 1.0) < eps and abs(srt[1] - 5.0) < eps
    # 4) 特征向量方向正是 (2,1) 与 (-2,1) —— 即不动点 ±2
    for vec, pt in ((np.array([2.0, 1.0]), FP_SINK),
                    (np.array([-2.0, 1.0]), FP_SOURCE)):
        img = M @ vec
        assert abs(img[0] - pt * img[1]) < eps, "特征方向≠不动点"
    # 5) 乘子：z=2 处 1/5（汇），z=-2 处 5（源）
    det = A * D - B * C
    assert abs(det / (C * FP_SINK + D) ** 2 - 0.2) < eps
    assert abs(det / (C * FP_SOURCE + D) ** 2 - 5.0) < eps
    # 6) 极点恰为 -3，且 f 把它送到 ∞
    assert abs(POLE - (-3.0)) < eps
    assert abs(f_num(POLE + 1e-12)) > 1e10
    # 7) 共轭映射：2→0，-2→∞
    assert abs(conj_num(FP_SINK)) < eps
    assert abs(conj_num(FP_SOURCE)) > 1e9
    # 8) 复合恒等式：w=(z-2)/(z+2) 下 f 的作用恰为 w → w/5
    for z in (0.5, 1.3, 3.7, -1.2, -0.5 + 1.5j, 4.0 - 2.0j):
        w = conj_num(z)
        assert abs(conj_num(f_num(z)) - w / LAM) <= 1e-9 * max(1.0, abs(w))
    # 8b) 源侧的共轭坐标 v=(z+2)/(z-2) 满足 v→5v（与 w→w/5 互为倒数）
    for x in (-1.2, -1.5, 0.8, 3.7):
        v = (x + 2.0) / (x - 2.0)
        vf = (f_num(x) + 2.0) / (f_num(x) - 2.0)
        assert abs(vf - LAM * v) < eps, "源侧共轭坐标未 ×5"
    # 8c) 局部线性化口径：d_{n+1}/d_n → 1/5（n 越大越接近）
    z, ratios = 0.5, []
    prev = None
    for _ in range(12):
        d = abs(z - FP_SINK)
        if prev is not None:
            ratios.append(d / prev)
        prev, z = d, f_num(z)
    assert abs(ratios[-1] - 0.2) < 1e-6 and ratios[0] > ratios[-1]
    # 9) 硬约束：幕一网格的全部【顶点】到极点的距离 > R_GUARD
    #    （顶点 = 直线段的端点；线段内部按 0.2 步长加密采样复核）
    xs = [-4, -3.5, -2, -1, 0, 1, 2, 3, 4]
    ys = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
    pts = [complex(xv, y) for xv in xs for y in ys]
    dmin = min(abs(p - POLE) for p in pts)
    assert dmin > R_GUARD, "网格顶点撞到极点邻域: %.3f" % dmin
    dense = [complex(xv, y) for xv in xs for y in np.linspace(-4, 4, 14)]
    dense += [complex(x, yv) for yv in ys for x in np.linspace(-4.4, 4.4, 14)]
    dmin2 = min(abs(p - POLE) for p in dense)
    assert dmin2 > 1e-6, "网格线段穿过极点: %.3f" % dmin2
    # 10) 每条所画流线（|w|=k）上的采样点到源 -2、极点 -3 均保持安全距离
    for k in STREAM_KS:
        cen, rad = apollonius(k)
        samp = [cen + rad * np.exp(1j * t)
                for t in np.linspace(0, TAU, 720, endpoint=False)]
        assert min(abs(p - FP_SOURCE) for p in samp) > 0.2, "流线贴到源"
        assert min(abs(p - POLE) for p in samp) > 0.2, "流线贴到极点"
    print("[mobius_flow_field] 数值自验通过：不动点 ±2；f'(2)=1/5、f'(-2)=5；"
          "Δ=16>0；w_{n+1}=w_n/5；网格距极点 %.3f > %.2f；流线 k=%s"
          % (dmin, R_GUARD, STREAM_KS))


_assert_setup()


# ============================================================ 小工具
def _line_by_points(plane, pts, color, width, opacity=1.0):
    """由复数点列生成折线段（逐点构造，避免 Polyline 兼容问题）。"""
    return VGroup(*[
        Line(plane.n2p(zs), plane.n2p(ze), color=color,
             stroke_width=width, stroke_opacity=opacity)
        for zs, ze in zip(pts[:-1], pts[1:])
    ])


def _arrow_at(plane, z0, z1, color, width=3.0, tip=0.14):
    return Arrow(plane.n2p(z0), plane.n2p(z1), buff=0.0, color=color,
                 stroke_width=width, tip_length=tip)


class MobiusFlowField(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ======================================================
        # 幕一：复平面网格在 f 下的像 —— 直线网弯成圆网，±2 钉住
        # ======================================================
        title1 = Text("1. 双曲型莫比乌斯变换：网格被弯成圆网",
                      font=FONT_NAME, font_size=25, color=PRIMARY)
        title1.to_edge(UP, buff=0.28)
        self.play(Write(title1), run_time=1.1)
        self.wait(0.4)

        # 左侧文字区固定在画幅左缘，网格本体下移到画面中下部
        plane = ComplexPlane(
            x_range=[-4.4, 4.4, 1],
            y_range=[-3.0, 3.0, 1],
            x_length=8.8, y_length=6.0,
            background_line_style={"stroke_color": GRAY, "stroke_width": 1,
                                   "stroke_opacity": 0.40},
            faded_line_style={"stroke_color": GRAY, "stroke_width": 1,
                               "stroke_opacity": 0.20},
            faded_line_ratio=1,
        ).move_to(RIGHT * 1.9 + DOWN * 0.95)
        self.play(Create(plane), run_time=1.3)
        self.wait(0.4)

        eq_f = MathTex(r"f(z)=\frac{3z+4}{z+3}", font_size=32, color=ACCENT)
        eq_d = MathTex(r"\Delta=(a-d)^{2}+4bc=16>0", font_size=21,
                       color=WHITE)
        note_d = Text("Δ>0 ⇒ 双曲型：恰好一源一汇",
                      font=FONT_NAME, font_size=20, color=WHITE)
        panel = VGroup(eq_f, eq_d, note_d).arrange(
            DOWN, buff=0.26, aligned_edge=LEFT)
        panel.move_to(LEFT * 4.25 + UP * 2.35)
        self.play(Write(panel), run_time=1.4)
        self.wait(0.6)

        # 网格在 f 下的像（顶点全部远离极点，见 _assert_setup 第 9 条）
        xs = [-4, -3.5, -2, -1, 0, 1, 2, 3, 4]
        ys = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        net = VGroup()
        for xv in xs:
            net.add(_line_by_points(
                plane, [complex(xv, y) for y in np.linspace(-4, 4, 18)],
                PRIMARY, 1.6, 0.75))
        for yv in ys:
            net.add(_line_by_points(
                plane, [complex(x, yv) for x in np.linspace(-4.4, 4.4, 18)],
                PRIMARY, 1.6, 0.75))
        self.play(ApplyComplexFunction(f_num, net), run_time=2.8)
        self.wait(0.6)

        note_net = Text("直线网 → 正交圆网；极点 z=-3 处撕开一个洞",
                        font=FONT_NAME, font_size=19, color=WHITE)
        note_net.move_to(LEFT * 4.15 + UP * 1.15)
        self.play(Write(note_net), run_time=1.1)

        hole = Circle(radius=R_GUARD, color=POLE_COL, stroke_width=3,
                      fill_color=BG, fill_opacity=1.0)
        hole.move_to(plane.n2p(POLE))
        hole_lbl = Text("极点 z=-3", font=FONT_NAME, font_size=18,
                        color=POLE_COL)
        hole_lbl.next_to(hole, DL, buff=0.14)
        self.play(FadeIn(hole), Write(hole_lbl), run_time=1.0)
        self.wait(0.6)

        sink_dot = Dot(plane.n2p(FP_SINK), radius=0.11, color=PRIMARY)
        sink_lbl = VGroup(Text("汇 ", font=FONT_NAME, font_size=19,
                               color=PRIMARY),
                          MathTex(r"z_1=2,\ |f'|=1/5<1", font_size=20,
                                  color=PRIMARY)).arrange(RIGHT, buff=0.16)
        sink_lbl.next_to(sink_dot, UR, buff=0.16)
        src_dot = Dot(plane.n2p(FP_SOURCE), radius=0.11, color=RED_H)
        src_lbl = VGroup(Text("源 ", font=FONT_NAME, font_size=19,
                              color=RED_H),
                         MathTex(r"z_2=-2,\ |f'|=5>1", font_size=20,
                                 color=RED_H)).arrange(RIGHT, buff=0.16)
        src_lbl.next_to(src_dot, UP, buff=0.18)
        self.play(FadeIn(sink_dot), FadeIn(src_dot),
                  Write(sink_lbl), Write(src_lbl), run_time=1.2)
        self.wait(0.8)

        # 真正的流线：|w|=k 给出的一族等距比圆（阿波罗尼奥斯圆），源侧 → 汇侧
        flow = VGroup()
        for k in STREAM_KS:
            cen, rad = apollonius(k)
            flow.add(Circle(radius=rad, color=SECONDARY, stroke_width=2,
                            stroke_opacity=0.8).move_to(plane.n2p(cen)))
        # k=1 的分隔线就是虚轴 x=0，与坐标轴重合，不另画
        self.play(Create(flow), run_time=2.0)
        self.wait(0.5)
        # 沿弧的流向箭头：在前两条圆的 60° 处，水平指向汇一侧（大圆超出画幅，不画）
        arrows = VGroup()
        for k in STREAM_KS[:2]:
            cen, rad = apollonius(k)
            th = np.deg2rad(60)
            p0 = cen + rad * np.exp(1j * th)
            sgn = 1.0 if FP_SINK > cen else -1.0
            arrows.add(_arrow_at(plane, p0, p0 + sgn * 0.30, ORANGE,
                                 width=3.2, tip=0.14))
        self.play(Create(arrows), run_time=1.2)
        self.wait(0.6)

        cap1 = Text("流线：到 ±2 距离之比为定值的一族圆\n"
                    "|w| 每步 ×1/5，沿圆弧没入汇 z₁=2",
                    font=FONT_NAME, font_size=19, color=SECONDARY)
        cap1.move_to(LEFT * 4.0 + DOWN * 0.05)
        self.play(Write(cap1), run_time=1.2)
        self.wait(2.2)

        # ======================================================
        # 幕二：共轭 w=(z-2)/(z+2) —— 弯圆拉成同心圆
        # ======================================================
        title2 = Text("2. 共轭拉直：w=(z-2)/(z+2)，汇→0、源→∞",
                      font=FONT_NAME, font_size=25, color=PRIMARY)
        title2.to_edge(UP, buff=0.28)
        self.play(ReplacementTransform(title1, title2), run_time=1.0)
        self.play(FadeOut(panel), FadeOut(note_net), FadeOut(hole),
                  FadeOut(hole_lbl), FadeOut(flow), FadeOut(cap1),
                  FadeOut(arrows), FadeOut(sink_dot), FadeOut(sink_lbl),
                  FadeOut(src_dot), FadeOut(src_lbl), FadeOut(net),
                  run_time=0.8)

        wplane = ComplexPlane(
            x_range=[-3.0, 3.0, 1],
            y_range=[-2.2, 2.2, 1],
            x_length=7.2, y_length=6.0,
            background_line_style={"stroke_color": GRAY, "stroke_width": 1,
                                   "stroke_opacity": 0.35},
            faded_line_style={"stroke_color": GRAY, "stroke_width": 1,
                              "stroke_opacity": 0.2},
            faded_line_ratio=1,
        ).move_to(RIGHT * 1.6 + DOWN * 0.5)
        self.play(Create(wplane), run_time=1.3)
        self.wait(0.4)

        eq_c = MathTex(r"w=\frac{z-z_1}{z-z_2}=\frac{z-2}{z+2}",
                       font_size=28, color=ACCENT)
        eq_c.move_to(LEFT * 4.35 + UP * 2.45)
        self.play(Write(eq_c), run_time=1.3)
        self.wait(0.5)

        origin_dot = Dot(wplane.n2p(0), radius=0.11, color=PRIMARY)
        origin_lbl = VGroup(Text("原汇 ", font=FONT_NAME, font_size=19,
                                 color=PRIMARY),
                            MathTex(r"w=0", font_size=20,
                                    color=PRIMARY)).arrange(RIGHT, buff=0.16)
        origin_lbl.next_to(origin_dot, DR, buff=0.2)
        inf_note = Text("原源 → ∞：|w| 越滚越大", font=FONT_NAME,
                        font_size=19, color=RED_H)
        inf_note.move_to(LEFT * 4.35 + UP * 1.35)
        self.play(FadeIn(origin_dot), Write(origin_lbl),
                  Write(inf_note), run_time=1.2)
        self.wait(0.6)

        # 共轭把「|z-2|/|z+2| = k」这族圆拉成以 0 为心的同心圆，半径恰为同一组 k
        rings = VGroup()
        for rr in STREAM_KS:
            rings.add(Circle(radius=rr, color=PRIMARY, stroke_width=2,
                             stroke_opacity=0.8).move_to(wplane.n2p(0)))
        rings.add(Circle(radius=SEP_K, color=GRAY, stroke_width=1.6,
                         stroke_opacity=0.7).move_to(wplane.n2p(0)))
        # 另一族：过两不动点 ±2 的圆，共轭后变成过 0 的直线（射线）——即第 9 章 §5 图
        rays = VGroup()
        for deg in (25, 65, 115, 155, 205, 335):
            th = np.deg2rad(deg)
            rays.add(Arrow(wplane.n2p(2.3 * np.exp(1j * th)),
                           wplane.n2p(0.28 * np.exp(1j * th)),
                           buff=0.0, color=ORANGE, stroke_width=2,
                           stroke_opacity=0.85, tip_length=0.12))
        self.play(Create(rings), run_time=1.8)
        self.play(Create(rays), run_time=1.4)
        self.wait(0.5)

        cap2 = Text("等距比圆 |w|=k → 以 0 为心的同心圆\n"
                    "过 ±2 的圆 → 过 0 的射线",
                    font=FONT_NAME, font_size=19, color=SECONDARY)
        cap2.move_to(LEFT * 3.9 + DOWN * 0.15)
        self.play(Write(cap2), run_time=1.4)
        self.wait(0.7)

        # 两条轨道：固定辐角，模长每步 ×1/5
        for k, (r0, deg, col) in enumerate(
                [(1.9, 55, SECONDARY), (1.5, 125, ACCENT)]):
            th = np.deg2rad(deg)
            rs = [r0 * (0.2 ** n) for n in range(6)]
            pts = [r * np.exp(1j * th) for r in rs]
            segs = _line_by_points(wplane, pts, col, 2.6)
            dots = VGroup(*[Dot(wplane.n2p(p), radius=0.055, color=col)
                            for p in pts])
            lbl = Text("w_%d" % k, font=FONT_NAME, font_size=17, color=col)
            lbl.next_to(dots[-1], RIGHT, buff=0.14)
            self.play(Create(segs), FadeIn(dots), Write(lbl),
                      run_time=1.3)
            self.wait(0.5)
            if k == 0:
                self.play(FadeOut(lbl), run_time=0.4)

        concl2 = Text("同一射线上每步模长 ×1/5 ⇒ 沿圆弧或射线收拢到原点",
                      font=FONT_NAME, font_size=19, color=ACCENT)
        concl2.move_to(LEFT * 4.05 + DOWN * 1.15)
        self.play(Write(concl2), run_time=1.2)
        self.wait(2.4)

        # ======================================================
        # 幕三：乘子的两种读法 + 源侧放大
        # ======================================================
        title3 = Text("3. 乘子的意义：1/5 对谁？—— 汇收缩、源放大",
                      font=FONT_NAME, font_size=25, color=PRIMARY)
        title3.to_edge(UP, buff=0.28)
        self.play(ReplacementTransform(title2, title3), run_time=1.0)
        self.play(FadeOut(wplane), FadeOut(rings), FadeOut(origin_dot),
                  FadeOut(origin_lbl), FadeOut(inf_note), FadeOut(cap2),
                  FadeOut(concl2), FadeOut(eq_c), run_time=0.8)
        # 清掉幕二直接加到场景上的轨道点/线/标签（不在任何容器内）
        for m in list(self.mobjects):
            if m is not title3:
                self.remove(m)

        # --- 上排：两张对照表 ---
        zs = [0.5]
        for _ in range(3):
            zs.append(float(np.real(f_num(zs[-1]))))
        ds = [abs(z - FP_SINK) for z in zs]
        ws = [abs(conj_num(z)) for z in zs]

        head_a = Text("甲：对【汇】的距离 d=|z-2|", font=FONT_NAME,
                      font_size=20, color=SECONDARY)
        head_a.move_to(LEFT * 4.5 + UP * 2.45)
        eq_a = MathTex(r"d_{n+1}\approx\tfrac15\,d_n\quad(\text{local})",
                       font_size=20, color=WHITE)
        eq_a.next_to(head_a, DOWN, buff=0.24, aligned_edge=LEFT)
        rows_a = VGroup(*[
            VGroup(MathTex("z_%d=%.3f" % (i, z), font_size=17, color=GRAY),
                   MathTex("d_%d=%.4f" % (i, d), font_size=17,
                           color=WHITE)).arrange(RIGHT, buff=0.4)
            for i, (z, d) in enumerate(zip(zs, ds))])
        rows_a.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        rows_a.next_to(eq_a, DOWN, buff=0.22, aligned_edge=LEFT)

        head_b = Text("乙：共轭坐标的模 r=|w|（精确）", font=FONT_NAME,
                      font_size=20, color=ACCENT)
        head_b.move_to(UP * 2.45 + RIGHT * 0.9)
        eq_b = MathTex(r"r_{n+1}=\tfrac15\,r_n\quad(\text{exact})",
                       font_size=20, color=WHITE)
        eq_b.next_to(head_b, DOWN, buff=0.24, aligned_edge=LEFT)
        rows_b = VGroup(*[
            VGroup(MathTex("z_%d=%.3f" % (i, z), font_size=17, color=GRAY),
                   MathTex("r_%d=%.4f" % (i, r_), font_size=17,
                           color=WHITE)).arrange(RIGHT, buff=0.4)
            for i, (z, r_) in enumerate(zip(zs, ws))])
        rows_b.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        rows_b.next_to(eq_b, DOWN, buff=0.22, aligned_edge=LEFT)

        self.play(Write(head_a), Write(eq_a), run_time=1.1)
        self.play(Write(rows_a), run_time=1.4)
        self.wait(0.4)
        self.play(Write(head_b), Write(eq_b), run_time=1.1)
        self.play(Write(rows_b), run_time=1.4)
        self.wait(0.8)

        box_l = VGroup(
            MathTex(r"|f'(2)|=\tfrac15<1", font_size=21, color=SECONDARY),
            Text("⇔ 汇侧：被吸入（1/λ）", font=FONT_NAME, font_size=18,
                 color=SECONDARY),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        box_r = VGroup(
            MathTex(r"|f'(-2)|=5>1", font_size=21, color=RED_H),
            Text("⇔ 源侧：被推离（|λ|）", font=FONT_NAME, font_size=18,
                 color=RED_H),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        boxes = VGroup(box_l, box_r).arrange(RIGHT, buff=1.4)
        boxes.move_to(UP * 0.95)
        frame = SurroundingRectangle(boxes, color=ACCENT, buff=0.3,
                                     stroke_width=3)
        self.play(Write(box_l), Write(box_r), run_time=1.2)
        self.play(Create(frame), run_time=0.9)
        self.wait(1.0)

        # --- 下排：源侧近域放大 + 结语 ---
        self.play(FadeOut(rows_a), FadeOut(rows_b), FadeOut(head_a),
                  FadeOut(eq_a), FadeOut(head_b), FadeOut(eq_b),
                  FadeOut(boxes), FadeOut(frame), run_time=0.7)

        # 窗口必须装得下整条探针链（-1.9 → … → 1.05），否则线会穿过右侧文字
        chain = [-1.9]
        for _ in range(3):
            chain.append(float(np.real(f_num(chain[-1]))))
        assert min(chain) > -2.6 and max(chain) < 1.1, "探针链飞出放大窗口"

        zoom_plane = ComplexPlane(
            x_range=[-2.6, 1.1, 0.5],
            y_range=[-0.55, 0.55, 0.25],
            x_length=6.4, y_length=2.2,
            background_line_style={"stroke_color": GRAY, "stroke_width": 1,
                                   "stroke_opacity": 0.30},
            faded_line_style={"stroke_color": GRAY, "stroke_width": 1,
                              "stroke_opacity": 0.18},
            faded_line_ratio=1,
        ).move_to(LEFT * 2.0 + DOWN * 1.95)
        src_z = Dot(zoom_plane.n2p(FP_SOURCE), radius=0.09, color=RED_H)
        src_z_lbl = Text("源 -2", font=FONT_NAME, font_size=16,
                         color=RED_H).next_to(src_z, DL, buff=0.14)

        ch_dots = VGroup(*[Dot(zoom_plane.n2p(z), radius=0.055,
                               color=ORANGE) for z in chain])
        ch_lines = VGroup(*[
            Line(zoom_plane.n2p(a), zoom_plane.n2p(b), color=ORANGE,
                 stroke_width=2.2) for a, b in zip(chain[:-1], chain[1:])])
        push_lbl = Text("源侧近域：|f'(-2)|=5，每步推远 5 倍",
                        font=FONT_NAME, font_size=17, color=RED_H)
        push_lbl.next_to(zoom_plane, UP, buff=0.18)

        self.play(Create(zoom_plane), FadeIn(src_z), Write(src_z_lbl),
                  run_time=1.2)
        self.play(Create(ch_lines), FadeIn(ch_dots), run_time=1.3)
        self.play(Write(push_lbl), run_time=1.1)
        self.wait(1.2)

        final = Text("乘子 |λ|=5 与 |f'| 互为倒数：\n"
                     "|f'|<1 ⟺ 汇被吸入，|f'|>1 ⟺ 源被推开",
                     font=FONT_NAME, font_size=20, color=ACCENT)
        final.move_to(RIGHT * 4.1 + DOWN * 1.95)
        self.play(Write(final), run_time=1.6)
        self.wait(3.5)
