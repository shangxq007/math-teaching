"""第 4 章 · 立体几何与圆锥曲线 —— 场景 2：圆锥截面与 Dandelin 球

叙事：取圆锥的轴截面（等腰三角形 + 虚线双叶延伸），画出与轴夹角为 φ 的截面
      → 动画改变 φ：φ > α（母线半顶角）得椭圆，φ = α 得抛物线，φ < α 得双曲线；
        交线用红色高亮，右栏同步给出 e = cosφ / cosα 与截面正视示意图
      → 回到椭圆情形，放入 Dandelin 球（与圆锥面、截面均相切），
        切点即焦点 F，切圆平面与截面的交线即准线
      → 定格：同一个焦点-准线定义，e 的大小决定曲线类型

说明：三维表现采用「轴截面」二维剖面（课件允许的降维方案），
      另配截面正视小图，保证焦点 / 准线的几何由来清晰。

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene2_dandelin.py DandelinSections
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

# ------------------------------------------------------------------
# 几何参数（轴截面内，顶点在原点右侧 X0 处）
# ------------------------------------------------------------------
X0 = -1.5                       # 圆锥轴心的 x 坐标
APEX = np.array([X0, 2.3, 0.0])
ALPHA = 31 * DEGREES            # 母线半顶角 α
TANA = float(np.tan(ALPHA))
P_CUT = np.array([X0, -0.9, 0.0])   # 截面与轴的交点
PHI_E = 70 * DEGREES            # 椭圆：φ > α
PHI_P = ALPHA                   # 抛物线：φ = α
PHI_H = 5 * DEGREES             # 双曲线：φ < α

SIN_A = float(np.sin(ALPHA))
COS_A = float(np.cos(ALPHA))


def gdir(side):
    """母线方向（side=+1 右侧，-1 左侧），t 每增加 1 下降 1 个单位"""
    return np.array([side * TANA, -1.0, 0.0])


def ddir(phi):
    """截面迹线方向：与竖直向下的轴夹角为 phi"""
    return np.array([np.sin(phi), -np.cos(phi), 0.0])


def intersect(side, phi):
    """截面迹线与指定侧母线所在直线的交点参数 (t, s)"""
    g = gdir(side)
    d = ddir(phi)
    mat = np.column_stack([g[:2], -d[:2]])
    t, s = np.linalg.solve(mat, (P_CUT - APEX)[:2])
    return t, s


def pt_on_gen(side, t):
    return APEX + t * gdir(side)


def unit_vec(angle):
    return np.array([np.cos(angle), np.sin(angle), 0.0])


def dandelin(phi):
    """返回 (球心 C, 半径 r, 焦点 F, 切圆高度 yT, 右切点 T_R)"""
    n = np.array([np.cos(phi), np.sin(phi), 0.0])
    sf = np.sin(phi)
    yc = (APEX[1] * SIN_A + P_CUT[1] * sf) / (sf + SIN_A)
    r = (APEX[1] - yc) * SIN_A
    C = np.array([0.0, yc, 0.0])
    F = C - r * n
    g = gdir(1)
    tT = float(np.dot(C - APEX, g) / np.dot(g, g))
    T_R = APEX + tT * g
    yT = float(T_R[1])
    return C, r, F, yT, T_R


class DandelinSections(Scene):
    def construct(self):
        self.camera.background_color = BG

        phi = ValueTracker(PHI_E)

        # ==========================================================
        # 第一幕：圆锥轴截面、母线角 α、截面倾角 φ
        # ==========================================================
        title1 = Text(
            "1. 圆锥轴截面：截面倾角与母线角",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=0.9)
        self.wait(0.5)

        # 圆锥：两条母线（实线，向下延伸）+ 上叶虚线延伸
        right_gen = Line(APEX, APEX + 5.9 * gdir(1),
                         color=PRIMARY, stroke_width=3.5)
        left_gen = Line(APEX, APEX + 5.9 * gdir(-1),
                        color=PRIMARY, stroke_width=3.5)
        up_right = DashedLine(APEX, APEX - 0.95 * gdir(1) / np.linalg.norm(gdir(1)),
                              color=GRAY, stroke_width=2)
        up_left = DashedLine(APEX, APEX - 0.95 * gdir(-1) / np.linalg.norm(gdir(-1)),
                             color=GRAY, stroke_width=2)
        axis = DashedLine(np.array([X0, 3.05, 0]), np.array([X0, -3.9, 0]),
                          color=GRAY, stroke_width=2)

        self.play(Create(right_gen), Create(left_gen), run_time=1.2)
        self.play(Create(axis), Create(up_right), Create(up_left), run_time=0.8)
        self.wait(0.5)

        # 底面示意椭圆（虚线，增强三维感）
        base_rim = Ellipse(width=7.0, height=0.8, color=GRAY,
                           stroke_width=2, fill_opacity=0).move_to(
                               np.array([X0, -3.55, 0]))
        self.play(Create(base_rim), run_time=0.7)
        self.wait(0.4)

        # α 角：轴与右母线的夹角
        alpha_arc = Arc(radius=0.75, start_angle=-PI / 2, angle=ALPHA,
                        arc_center=APEX, color=ACCENT, stroke_width=3)
        alpha_mid = -PI / 2 + ALPHA / 2
        alpha_lab = MathTex(r"\alpha", font_size=24, color=ACCENT)
        alpha_lab.move_to(APEX + 1.02 * unit_vec(alpha_mid))
        self.play(Create(alpha_arc), Write(alpha_lab), run_time=0.8)

        # 截面（半透明薄片）与迹线，随 φ 更新；用透明度 tracker 做淡入
        depth_v = np.array([0.50, 0.12, 0.0])
        sheet_op = ValueTracker(0.0)

        def sheet_now():
            d = ddir(phi.get_value())
            op = sheet_op.get_value()
            L = 2.8
            p = P_CUT
            pts = [p - L * d - depth_v, p + L * d - depth_v,
                   p + L * d + depth_v, p - L * d + depth_v]
            return Polygon(*pts, color=PRIMARY, fill_opacity=0.12 * op,
                           stroke_width=1.5, stroke_opacity=op)

        cut_line = always_redraw(lambda: Line(
            P_CUT - 2.8 * ddir(phi.get_value()),
            P_CUT + 2.8 * ddir(phi.get_value()),
            color=WHITE, stroke_width=3,
            stroke_opacity=sheet_op.get_value(),
        ))
        sheet = always_redraw(sheet_now)
        phi_arc = always_redraw(lambda: Arc(
            radius=0.62, start_angle=-PI / 2, angle=phi.get_value(),
            arc_center=P_CUT, color=ACCENT, stroke_width=3,
            stroke_opacity=sheet_op.get_value(),
        ))
        phi_lab = MathTex(r"\varphi", font_size=24, color=ACCENT)
        phi_lab.move_to(P_CUT + 0.92 * unit_vec(-PI / 2 + phi.get_value() / 2))
        phi_lab.add_updater(lambda m: m.move_to(
            P_CUT + 0.92 * unit_vec(-PI / 2 + phi.get_value() / 2)))
        self.add(sheet, cut_line, phi_arc, phi_lab)
        self.wait(0.3)
        self.play(sheet_op.animate.set_value(1.0), Write(phi_lab),
                  run_time=0.9)
        self.wait(0.6)

        panel1 = VGroup(
            Text("轴截面：等腰三角形 + 双叶虚线延伸",
                 font=FONT_NAME, font_size=20, color=WHITE),
            MathTex(r"\alpha=31^\circ", font_size=24, color=ACCENT),
            Text("截面与轴的夹角决定曲线类型",
                 font=FONT_NAME, font_size=21, color=SECONDARY),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        panel1.move_to((2.45, 1.55, 0), aligned_edge=LEFT)
        self.play(Write(panel1), run_time=1.1)
        self.wait(1.5)

        # 公共：截面正视小图外框
        inset_c = np.array([4.35, -1.9, 0])
        inset_frame = Rectangle(width=4.7, height=2.5, color=GRAY,
                                stroke_width=1.5, fill_opacity=0).move_to(inset_c)

        # ---------------- 各曲线的截面正视示意图 ----------------
        def sketch_ellipse():
            g = VGroup(
                Ellipse(width=2.3, height=1.8, color=RED_H, stroke_width=3),
                Text("椭圆", font=FONT_NAME, font_size=20, color=WHITE),
            )
            g[1].move_to(g[0].get_bottom() + UP * 0.28)
            return g

        def sketch_parabola():
            f = lambda t: np.array([1.15 * t, 0.42 * t * t - 0.72, 0.0])
            curve = ParametricFunction(f, t_range=[-1.55, 1.55],
                                       color=RED_H, stroke_width=3)
            lab = Text("抛物线", font=FONT_NAME, font_size=20, color=WHITE)
            lab.move_to(curve.get_bottom() + DOWN * 0.30)
            return VGroup(curve, lab)

        def sketch_hyperbola():
            def branch(sign):
                f = lambda s: np.array([sign * 0.62 * np.cosh(s),
                                        0.72 * np.sinh(s), 0.0])
                return ParametricFunction(f, t_range=[-1.15, 1.15],
                                          color=RED_H, stroke_width=3)
            lab = Text("双曲线", font=FONT_NAME, font_size=20, color=WHITE)
            g = VGroup(branch(1), branch(-1), lab)
            lab.move_to(g[:2].get_bottom() + DOWN * 0.30)
            return g

        sketches = {"E": sketch_ellipse(), "P": sketch_parabola(),
                    "H": sketch_hyperbola()}
        for g in sketches.values():
            g.move_to(inset_c)

        # ---------------- 交线高亮（静态，逐状态重建） ----------------
        def trace_ellipse():
            tr, _ = intersect(1, PHI_E)
            tl, _ = intersect(-1, PHI_E)
            qr, ql = pt_on_gen(1, tr), pt_on_gen(-1, tl)
            seg = Line(ql, qr, color=RED_H, stroke_width=7)
            dots = VGroup(Dot(ql, radius=0.06, color=RED_H),
                          Dot(qr, radius=0.06, color=RED_H))
            return VGroup(seg, dots)

        def trace_parabola():
            t, _ = intersect(-1, PHI_P)
            q = pt_on_gen(-1, t)
            ray = Arrow(q, q + 4.4 * ddir(PHI_P), buff=0, color=RED_H,
                        stroke_width=6, tip_length=0.22)
            return VGroup(ray, Dot(q, radius=0.06, color=RED_H))

        def trace_hyperbola():
            tr, _ = intersect(1, PHI_H)
            tl, _ = intersect(-1, PHI_H)
            q_up = pt_on_gen(1, tr)          # tr < 0：上叶
            q_low = pt_on_gen(-1, tl)        # tl > 0：下叶
            ray_up = Arrow(q_up, q_up - 0.30 * ddir(PHI_H), buff=0,
                           color=RED_H, stroke_width=6, tip_length=0.18)
            ray_low = Arrow(q_low, q_low + 3.2 * ddir(PHI_H), buff=0,
                            color=RED_H, stroke_width=6, tip_length=0.2)
            return VGroup(ray_up, ray_low,
                          Dot(q_up, radius=0.06, color=RED_H),
                          Dot(q_low, radius=0.06, color=RED_H))

        def regime_panel(name, cond, eval_, col):
            g = VGroup(
                Text(name, font=FONT_NAME, font_size=30, color=col),
                MathTex(cond, font_size=24, color=WHITE),
                MathTex(eval_, font_size=22, color=ACCENT),
            ).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
            g.move_to((2.45, 1.62, 0), aligned_edge=LEFT)
            return g

        # ==========================================================
        # 第二幕：φ 变化 → 椭圆 / 抛物线 / 双曲线
        # ==========================================================
        title2 = Text(
            "2. 改变 φ：椭圆 → 抛物线 → 双曲线",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=0.9)

        self.play(FadeOut(panel1), run_time=0.5)

        # ---- 椭圆 ----
        panelE = regime_panel(
            "椭圆", r"\varphi>\alpha",
            r"e=\cos70^\circ/\cos31^\circ\approx0.40<1", SECONDARY)
        self.play(FadeIn(inset_frame), run_time=0.5)
        self.add(sketches["E"])
        self.play(FadeIn(sketches["E"]), run_time=0.6)
        self.play(Write(panelE), run_time=0.8)
        tr_e = trace_ellipse()
        self.play(FadeIn(tr_e), run_time=0.7)
        self.wait(1.5)

        # ---- 抛物线 ----
        panelP = regime_panel(
            "抛物线", r"\varphi=\alpha",
            r"e=\cos31^\circ/\cos31^\circ=1", ACCENT)
        self.play(FadeOut(tr_e), run_time=0.5)
        self.play(phi.animate.set_value(PHI_P), run_time=1.8,
                  rate_func=smooth)
        self.wait(0.3)
        self.play(FadeOut(sketches["E"]), run_time=0.4)
        self.add(sketches["P"])
        tr_p = trace_parabola()
        self.play(FadeIn(sketches["P"]), FadeIn(tr_p),
                  Write(panelP), run_time=0.9)
        self.play(FadeOut(panelE), run_time=0.5)
        self.wait(1.5)

        # ---- 双曲线 ----
        panelH = regime_panel(
            "双曲线", r"\varphi<\alpha",
            r"e=\cos5^\circ/\cos31^\circ\approx1.16>1", RED_H)
        self.play(FadeOut(tr_p), run_time=0.5)
        self.play(phi.animate.set_value(PHI_H), run_time=1.8,
                  rate_func=smooth)
        self.wait(0.3)
        self.play(FadeOut(sketches["P"]), run_time=0.4)
        self.add(sketches["H"])
        tr_h = trace_hyperbola()
        self.play(FadeIn(sketches["H"]), FadeIn(tr_h),
                  Write(panelH), run_time=0.9)
        self.play(FadeOut(panelP), run_time=0.5)
        self.wait(1.6)

        # ==========================================================
        # 第三幕：Dandelin 球 —— 焦点与准线
        # ==========================================================
        title3 = Text(
            "3. Dandelin 球：焦点与准线的由来",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title2, title3), run_time=0.9)

        self.play(FadeOut(tr_h), FadeOut(panelH), FadeOut(sketches["H"]),
                  FadeOut(inset_frame), run_time=0.5)
        self.play(phi.animate.set_value(PHI_E), run_time=1.9,
                  rate_func=smooth)
        self.play(FadeIn(tr_e), run_time=0.6)
        self.wait(0.3)

        C, r_sph, F_pt, yT, T_R = dandelin(PHI_E)
        T_L = np.array([2 * X0 - T_R[0], T_R[1], 0.0])

        sph = Circle(radius=r_sph, color=SECONDARY, stroke_width=3.5,
                     fill_opacity=0.06).move_to(C)
        sph_lab = Text("Dandelin 球", font=FONT_NAME, font_size=20,
                       color=SECONDARY)
        sph_lab.move_to(np.array([-4.05, 0.55, 0]))
        sph_leader = DashedLine(np.array([-3.30, 0.55, 0]),
                                C + np.array([-r_sph - 0.02, 0.08, 0]),
                                color=SECONDARY, stroke_width=1.5)
        chord = DashedLine(T_L, T_R, color=SECONDARY, stroke_width=2)
        t_dots = VGroup(Dot(T_L, radius=0.055, color=SECONDARY),
                        Dot(T_R, radius=0.055, color=SECONDARY))

        focus_dot = Dot(F_pt, radius=0.085, color=RED_H)
        focus_lab = MathTex(r"F", font_size=26, color=RED_H)
        focus_lab.next_to(focus_dot, DOWN + LEFT, buff=0.10)
        focus_word = Text("焦点", font=FONT_NAME, font_size=20, color=RED_H)
        focus_word.next_to(focus_lab, LEFT, buff=0.12)

        # 准线与截面的交点 D（准线本身垂直于纸面）
        sD = (yT - P_CUT[1]) / ddir(PHI_E)[1]
        D_pt = P_CUT + sD * ddir(PHI_E)
        d_dot = Dot(D_pt, radius=0.06, color=GRAY)
        d_lab = MathTex(r"D", font_size=24, color=GRAY)
        d_lab.next_to(d_dot, UP, buff=0.10)
        chord_ext = DashedLine(T_L, D_pt, color=GRAY, stroke_width=1.5)

        self.play(FadeIn(sph), Write(sph_lab), Create(sph_leader),
                  run_time=1.0)
        self.play(Create(chord), FadeIn(t_dots), run_time=0.7)
        self.play(FadeIn(focus_dot), Write(focus_lab), Write(focus_word),
                  run_time=0.8)
        self.play(Create(chord_ext), FadeIn(d_dot), Write(d_lab),
                  run_time=0.7)
        self.wait(0.5)

        # 右侧面板：焦点-准线定义
        panel3 = VGroup(
            Text("切点 F 即焦点", font=FONT_NAME, font_size=21, color=RED_H),
            Text("切圆平面与截面交线 = 准线",
                 font=FONT_NAME, font_size=21, color=WHITE),
            MathTex(r"e=\frac{\cos\varphi}{\cos\alpha}",
                    font_size=27, color=ACCENT),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        panel3.move_to((2.45, 2.05, 0), aligned_edge=LEFT)

        # 截面正视图：椭圆 + 焦点 + 准线 + 动点 M
        ec = np.array([3.45, -1.8, 0.0])
        a_e, e_e = 1.15, 0.40
        b_e = a_e * np.sqrt(1 - e_e ** 2)
        ell = Ellipse(width=2 * a_e, height=2 * b_e, color=RED_H,
                      stroke_width=3).move_to(ec)
        f_dot = Dot(ec + np.array([a_e * e_e, 0, 0]), radius=0.07,
                    color=RED_H)
        dir_x = ec[0] + a_e / e_e
        directrix = DashedLine(np.array([dir_x, inset_c[1] - 1.05, 0]),
                               np.array([dir_x, inset_c[1] + 1.05, 0]),
                               color=WHITE, stroke_width=2.5)
        theta_m = 135 * DEGREES
        M_pt = ec + np.array([a_e * np.cos(theta_m), b_e * np.sin(theta_m), 0])
        m_dot = Dot(M_pt, radius=0.06, color=ACCENT)
        mf_line = DashedLine(M_pt, f_dot.get_center(), color=ACCENT,
                             stroke_width=2)
        md_line = DashedLine(M_pt, np.array([dir_x, M_pt[1], 0]),
                             color=GRAY, stroke_width=2)
        f_lab = Text("焦点 F", font=FONT_NAME, font_size=19, color=RED_H)
        f_lab.next_to(f_dot, DOWN + RIGHT, buff=0.10)
        d_lab2 = Text("准线 d", font=FONT_NAME, font_size=19, color=WHITE)
        d_lab2.move_to(np.array([dir_x - 0.45, inset_c[1] + 1.25, 0]))
        m_lab = MathTex(r"M", font_size=22, color=ACCENT)
        m_lab.next_to(m_dot, UP + LEFT, buff=0.08)
        ratio_lab = MathTex(r"e=\dfrac{MF}{MD}", font_size=22, color=ACCENT)
        ratio_lab.move_to(np.array([inset_c[0], inset_c[1] + 1.45, 0]))

        act3_inset = VGroup(ell, directrix, f_dot, m_dot, mf_line, md_line,
                            f_lab, d_lab2, m_lab, ratio_lab)
        self.play(Write(panel3), FadeIn(inset_frame), run_time=1.0)
        self.play(FadeIn(act3_inset), run_time=1.2)
        self.wait(2.2)

        # ==========================================================
        # 第四幕：定格 —— e 决定曲线类型
        # ==========================================================
        title4 = Text(
            "4. 定格：e 决定曲线类型",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title3, title4), run_time=0.9)

        self.play(FadeOut(panel3), FadeOut(act3_inset),
                  FadeOut(inset_frame), run_time=0.6)

        row_e = VGroup(MathTex(r"e<1", font_size=26, color=WHITE),
                       Text("椭圆", font=FONT_NAME, font_size=24,
                            color=SECONDARY)).arrange(RIGHT, buff=0.30)
        row_p = VGroup(MathTex(r"e=1", font_size=26, color=WHITE),
                       Text("抛物线", font=FONT_NAME, font_size=24,
                            color=ACCENT)).arrange(RIGHT, buff=0.30)
        row_h = VGroup(MathTex(r"e>1", font_size=26, color=WHITE),
                       Text("双曲线", font=FONT_NAME, font_size=24,
                            color=RED_H)).arrange(RIGHT, buff=0.30)
        table = VGroup(row_e, row_p, row_h).arrange(
            DOWN, buff=0.30, aligned_edge=LEFT)
        table.move_to((4.20, 1.70, 0), aligned_edge=LEFT)

        self.play(Write(table), run_time=1.3)
        self.wait(0.8)

        caption = Text(
            "同一个焦点-准线定义，e 的大小决定曲线类型",
            font=FONT_NAME, font_size=19, color=ACCENT,
        ).to_edge(DOWN, buff=0.2)
        self.play(Write(caption), run_time=1.1)
        self.wait(2.6)
