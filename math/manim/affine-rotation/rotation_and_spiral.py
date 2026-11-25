"""高观点系列 · 第 4 章配套动画
旋转消交叉项：xy=1 逆时针转 45° 还原为标准等轴双曲线；
随后复平面上展示复特征值 λ=r·e^{iθ} 的螺旋不动点迭代。
"""
from manim import *

FONT_NAME = "Noto Sans Mono CJK SC"

C_AXIS = GREY_BROWN
C_CURVE = "#7BD389"
C_NEWAX = "#F5A623"


class RotationEliminatesCrossTerm(Scene):
    def construct(self):
        # ---------------- 幕一：旋转坐标轴消灭交叉项 ----------------
        t1 = Text("1. 旋转坐标轴 45°：交叉项 xy 消失，还原标准双曲线",
                  font=FONT_NAME, font_size=24)
        t1.to_edge(UP, buff=0.25)

        plane = NumberPlane(
            x_range=[-4.5, 4.5, 1],
            y_range=[-4.5, 4.5, 1],
            x_length=6.0,
            y_length=6.0,
            background_line_style={"stroke_color": BLUE_D, "stroke_width": 1,
                                   "stroke_opacity": 0.35},
        )

        b1 = plane.plot(lambda x: 1 / x, x_range=[0.32, 3.4], color=C_CURVE, stroke_width=4)
        b2 = plane.plot(lambda x: 1 / x, x_range=[-3.4, -0.32], color=C_CURVE, stroke_width=4)
        v1 = Dot(plane.c2p(1, 1), radius=0.09, color=YELLOW)
        v2 = Dot(plane.c2p(-1, -1), radius=0.09, color=YELLOW)
        lab1 = MathTex(r"(1,1)", font_size=22, color=YELLOW).next_to(v1, UR, buff=0.08)
        lab2 = MathTex(r"(-1,-1)", font_size=22, color=YELLOW).next_to(v2, DL, buff=0.08)

        eq_a = MathTex(r"xy = 1", font_size=30, color=C_CURVE).to_corner(UL, buff=0.9)
        note_a = Text("含交叉项 xy，对称轴被转了 45°",
                      font=FONT_NAME, font_size=18, color=WHITE).next_to(eq_a, DOWN, buff=0.18)
        note_a.align_to(eq_a, LEFT)

        self.play(FadeIn(t1))
        self.play(Create(plane), Create(b1), Create(b2),
                  FadeIn(v1), FadeIn(v2), Write(lab1), Write(lab2))
        self.play(Write(eq_a), FadeIn(note_a))
        self.wait(1.2)

        # 连同网格与曲线一起旋转
        world = VGroup(plane, b1, b2, v1, v2, lab1, lab2)
        eq_b = MathTex(r"\frac{x'^2}{2}-\frac{y'^2}{2}=1",
                       font_size=30, color=YELLOW).to_corner(UL, buff=0.9)
        note_b = Text("交叉项消失：等轴双曲线 a=b=√2",
                      font=FONT_NAME, font_size=18, color=WHITE).next_to(eq_b, DOWN, buff=0.18)
        note_b.align_to(eq_b, LEFT)

        self.play(Rotate(world, angle=PI / 4, about_point=plane.get_center()),
                  ReplacementTransform(eq_a, eq_b), ReplacementTransform(note_a, note_b),
                  run_time=2.4)
        self.wait(1.6)

        self.play(*[FadeOut(m) for m in [world, eq_b, note_b]])

        # ---------------- 幕二：复特征值的螺旋不动点 ----------------
        t2 = Text("2. 复特征值：每步缩放 r 倍并旋转 θ 角（对数螺线收敛）",
                  font=FONT_NAME, font_size=24)
        t2.to_edge(UP, buff=0.25)
        self.play(ReplacementTransform(t1, t2))

        cp = ComplexPlane(
            x_range=[-3.6, 3.6, 1],
            y_range=[-3.6, 3.6, 1],
            x_length=6.2,
            y_length=6.2,
            background_line_style={"stroke_opacity": 0.35},
        ).shift(DOWN * 0.35)
        self.play(Create(cp))

        fp = Dot(cp.n2p(0), radius=0.1, color=YELLOW)
        fplab = MathTex(r"z^*=0", font_size=24, color=YELLOW).next_to(fp, DR, buff=0.1)
        lam = MathTex(r"\lambda = 0.88\,e^{\,i\pi/4}",
                      font_size=28, color="#7BD389").to_corner(UL, buff=0.9)
        sub = Text("不动点 z* = 0；每乘一次 λ：模 ×0.88，辐角 +45°",
                   font=FONT_NAME, font_size=18, color=WHITE).next_to(lam, DOWN, buff=0.18)
        sub.align_to(lam, LEFT)

        self.play(FadeIn(fp), Write(fplab), Write(lam), FadeIn(sub))

        factor = 0.88 * np.exp(1j * PI / 4)
        z = complex(3.0, 0.0)
        vec = Arrow(cp.n2p(0), cp.n2p(z), buff=0, color=C_CURVE, stroke_width=4)
        tip = Dot(cp.n2p(z), radius=0.06, color=C_NEWAX)
        trail = VGroup()

        self.play(GrowArrow(vec), FadeIn(tip))

        for _ in range(14):
            nz = z * factor
            seg = Line(cp.n2p(z), cp.n2p(nz), color=C_NEWAX, stroke_width=2.5)
            nv = Arrow(cp.n2p(0), cp.n2p(nz), buff=0, color=C_CURVE, stroke_width=4)
            self.play(Create(seg), Transform(vec, nv),
                      tip.animate.move_to(cp.n2p(nz)), run_time=0.22)
            trail.add(seg)
            z = nz

        concl = Text("实特征根沿直线逼近；复特征根绕原点旋进（投影即周期震荡）",
                     font=FONT_NAME, font_size=20, color=YELLOW)
        concl.to_edge(DOWN, buff=0.28)
        self.play(Write(concl))
        self.wait(2.2)
