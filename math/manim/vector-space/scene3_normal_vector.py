"""第 3 章 · 平面向量与空间向量 —— 场景 3：法向量与二面角

叙事：沿棱 l 的投影图（head-on 视图）画出两个半平面 α、β 与二面角 θ
      → 在各平面内取法向量 n1（青）⊥ α、n2（橙）⊥ β，标出法向量夹角 φ
         （两法向量同侧时 φ = 180° − θ，异侧时 φ = θ）
      → 动态把 θ 从 120°（钝）→ 90°（直）→ 60°（锐），φ 同步翻转，
         强调「相等或互补」要按图判定锐钝
      → 定格：用法向量统一处理平行 / 垂直 / 夹角

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql scene3_normal_vector.py NormalVectorDihedral
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

# 沿棱投影图的几何参数
O_POS = np.array([-3.05, 0.10, 0.0])
R_SECTOR = 2.30             # 半平面扇形的半径
SECTOR_HALF = 20 * DEGREES  # 扇形半张角
N_LEN = 1.70                # 法向量长度


def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0.0])


class NormalVectorDihedral(Scene):
    def construct(self):
        self.camera.background_color = BG

        theta = ValueTracker(120 * DEGREES)

        def ray_a():
            """半平面 α 的迹线方向（左上）"""
            return PI / 2 + theta.get_value() / 2

        def ray_b():
            """半平面 β 的迹线方向（右上）"""
            return PI / 2 - theta.get_value() / 2

        # ======================================================
        # 第一幕：投影图上的棱与二面角
        # ======================================================
        title1 = Text(
            "1. 二面角：两个半平面沿棱张开",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title1), run_time=1.0)
        self.wait(0.4)

        # 棱：垂直于投影面的直线用「圆圈 + 圆心点」表示
        edge_ring = Circle(radius=0.17, color=WHITE, stroke_width=2.5).move_to(O_POS)
        edge_dot = Dot(O_POS, radius=0.07, color=WHITE)
        edge_lab = MathTex(r"l", font_size=26, color=WHITE)
        edge_tag = Text("棱", font=FONT_NAME, font_size=20, color=GRAY)
        edge_group = VGroup(edge_tag, edge_lab).arrange(RIGHT, buff=0.08)
        edge_group.next_to(edge_ring, LEFT, buff=0.16)

        self.play(FadeIn(edge_ring), FadeIn(edge_dot), run_time=0.7)
        self.play(Write(edge_group), run_time=0.6)
        self.wait(0.8)

        # 两个半平面（扇形）+ 迹线
        sec_a = always_redraw(lambda: Sector(
            radius=R_SECTOR, start_angle=ray_a() - SECTOR_HALF,
            angle=2 * SECTOR_HALF, arc_center=O_POS,
            color=PRIMARY, fill_opacity=0.13, stroke_width=2.5,
        ))
        sec_b = always_redraw(lambda: Sector(
            radius=R_SECTOR, start_angle=ray_b() - SECTOR_HALF,
            angle=2 * SECTOR_HALF, arc_center=O_POS,
            color=ORANGE, fill_opacity=0.13, stroke_width=2.5,
        ))
        trace_a = always_redraw(lambda: Line(
            O_POS, O_POS + R_SECTOR * unit(ray_a()), color=WHITE, stroke_width=2.5,
        ))
        trace_b = always_redraw(lambda: Line(
            O_POS, O_POS + R_SECTOR * unit(ray_b()), color=WHITE, stroke_width=2.5,
        ))

        self.play(FadeIn(sec_a), FadeIn(sec_b), run_time=1.1)
        self.play(Create(trace_a), Create(trace_b), run_time=0.8)
        self.wait(1.0)

        alpha_lab = always_redraw(lambda: MathTex(
            r"\alpha", font_size=26, color=PRIMARY,
        ).move_to(O_POS + (R_SECTOR + 0.42) * unit(ray_a())))
        beta_lab = always_redraw(lambda: MathTex(
            r"\beta", font_size=26, color=ORANGE,
        ).move_to(O_POS + (R_SECTOR + 0.42) * unit(ray_b())))
        self.play(Write(alpha_lab), Write(beta_lab), run_time=0.8)

        # 二面角弧与标注
        dihedral_arc = always_redraw(lambda: Arc(
            radius=1.25, start_angle=ray_b(), angle=ray_a() - ray_b(),
            arc_center=O_POS, color=ACCENT, stroke_width=4,
        ))
        theta_lab = MathTex(r"\theta", font_size=28, color=ACCENT)
        theta_lab.move_to(O_POS + 1.58 * UP)
        self.play(Create(dihedral_arc), Write(theta_lab), run_time=1.0)
        self.wait(1.0)

        panel1 = VGroup(
            Text("二面角：棱 l 处两半平面的夹角", font=FONT_NAME, font_size=22, color=WHITE),
            Text("沿棱投影，把立体问题压成平面角", font=FONT_NAME, font_size=21, color=SECONDARY),
        ).arrange(DOWN, buff=0.30)
        panel1.move_to((3.55, 1.55, 0))
        self.play(Write(panel1), run_time=1.1)
        self.wait(1.5)

        # ======================================================
        # 第二幕：两个法向量与法向量夹角
        # ======================================================
        title2 = Text(
            "2. 各平面的法向量：垂直于两个半平面",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title1, title2), run_time=0.9)

        # 法向量指向外侧：n1 在 α 一侧、n2 在 β 一侧，颜色与所在半平面一致
        def n1_dir():
            return ray_a() + PI / 2

        def n2_dir():
            return ray_b() - PI / 2

        n1 = always_redraw(lambda: Arrow(
            O_POS, O_POS + N_LEN * unit(n1_dir()), buff=0,
            color=PRIMARY, stroke_width=6,
        ))
        n2 = always_redraw(lambda: Arrow(
            O_POS, O_POS + N_LEN * unit(n2_dir()), buff=0,
            color=ORANGE, stroke_width=6,
        ))
        n1_lab = always_redraw(lambda: MathTex(
            r"\vec n_1", font_size=25, color=PRIMARY,
        ).move_to(O_POS + (N_LEN + 0.40) * unit(n1_dir())))
        n2_lab = always_redraw(lambda: MathTex(
            r"\vec n_2", font_size=25, color=ORANGE,
        ).move_to(O_POS + (N_LEN + 0.40) * unit(n2_dir())))

        # 法向量与迹线垂直的直角标记
        def right_mark(d1, d2):
            s = 0.24
            pts = [O_POS, O_POS + s * unit(d1),
                   O_POS + s * unit(d1) + s * unit(d2), O_POS + s * unit(d2)]
            return Polygon(*pts, color=WHITE, stroke_width=2, fill_opacity=0)

        ra1 = always_redraw(lambda: right_mark(n1_dir(), ray_a()))
        ra2 = always_redraw(lambda: right_mark(n2_dir(), ray_b()))

        phi_arc = always_redraw(lambda: Arc(
            radius=0.80, start_angle=n1_dir(),
            angle=(n2_dir() - n1_dir()) % TAU,
            arc_center=O_POS, color=RED_H, stroke_width=4,
        ))
        phi_lab = MathTex(r"\varphi", font_size=26, color=RED_H)
        phi_lab.move_to(O_POS + 0.50 * DOWN)

        self.play(Create(n1), Create(n2), run_time=1.1)
        self.play(Write(n1_lab), Write(n2_lab), run_time=0.7)
        self.play(Create(ra1), Create(ra2), run_time=0.6)
        self.play(Create(phi_arc), Write(phi_lab), run_time=0.9)
        self.wait(0.8)

        panel2 = VGroup(
            MathTex(r"\vec n_1\perp\alpha,\ \vec n_2\perp\beta", font_size=25, color=WHITE),
            MathTex(r"\varphi=180^\circ-\theta", font_size=26, color=ACCENT),
            Text("同侧法向量：夹角与二面角互补；异侧：相等",
                 font=FONT_NAME, font_size=21, color=SECONDARY),
        ).arrange(DOWN, buff=0.26)
        panel2.move_to((3.55, 1.70, 0))

        self.play(FadeOut(panel1), run_time=0.5)
        self.play(Write(panel2), run_time=1.3)
        self.wait(1.8)

        # ======================================================
        # 第三幕：θ 动态变化，φ 同步翻转
        # ======================================================
        title3 = Text(
            "3. 动态：θ 钝 → 直 → 锐，φ 同步翻转",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title2, title3), run_time=0.9)

        panel3 = VGroup(
            MathTex(r"\varphi=180^\circ-\theta", font_size=26, color=ACCENT),
            Text("θ 与 φ 总是一个锐一个钝（或同为直角）",
                 font=FONT_NAME, font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.30)
        panel3.move_to((3.55, 2.20, 0))
        self.play(FadeOut(panel2), Write(panel3), run_time=1.0)

        self.play(theta.animate.set_value(90 * DEGREES), run_time=2.4)
        self.wait(0.4)

        read1 = VGroup(
            MathTex(r"\theta=90^\circ", font_size=25, color=ACCENT),
            Text("直角", font=FONT_NAME, font_size=20, color=WHITE),
            MathTex(r"\Rightarrow\ \varphi=90^\circ", font_size=25, color=RED_H),
        ).arrange(RIGHT, buff=0.22)
        read1.move_to((3.55, 0.90, 0))
        self.play(Write(read1), run_time=0.9)
        self.wait(1.4)

        self.play(theta.animate.set_value(60 * DEGREES), run_time=2.4)
        self.wait(0.4)

        read2 = VGroup(
            MathTex(r"\theta=60^\circ", font_size=25, color=ACCENT),
            Text("锐", font=FONT_NAME, font_size=20, color=SECONDARY),
            MathTex(r"\Rightarrow\ \varphi=120^\circ", font_size=25, color=RED_H),
            Text("钝", font=FONT_NAME, font_size=20, color=RED_H),
        ).arrange(RIGHT, buff=0.22)
        read2.move_to((3.55, -0.05, 0))
        self.play(Write(read2), run_time=0.9)
        self.wait(1.0)

        judge = Text(
            "相等还是互补：看图判定二面角是锐角还是钝角",
            font=FONT_NAME, font_size=21, color=ACCENT,
        ).move_to((3.55, -1.05, 0))
        self.play(Write(judge), run_time=1.1)
        self.wait(1.6)

        # ======================================================
        # 定格：法向量统一处理平行 / 垂直 / 夹角
        # ======================================================
        title4 = Text(
            "4. 定格：用法向量统一处理平行 / 垂直 / 夹角",
            font=FONT_NAME, font_size=26, color=PRIMARY,
        ).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title3, title4), run_time=0.9)

        self.play(
            FadeOut(panel3), FadeOut(read1), FadeOut(read2), FadeOut(judge),
            run_time=0.5,
        )

        row_par = VGroup(
            Text("平行", font=FONT_NAME, font_size=21, color=SECONDARY),
            MathTex(r"\alpha\parallel\beta\ \Leftrightarrow\ \vec n_1\parallel\vec n_2",
                     font_size=25, color=WHITE),
        ).arrange(RIGHT, buff=0.30)
        row_per = VGroup(
            Text("垂直", font=FONT_NAME, font_size=21, color=RED_H),
            MathTex(r"\alpha\perp\beta\ \Leftrightarrow\ \vec n_1\cdot\vec n_2=0",
                     font_size=25, color=WHITE),
        ).arrange(RIGHT, buff=0.30)
        row_ang = VGroup(
            Text("夹角", font=FONT_NAME, font_size=21, color=ACCENT),
            MathTex(r"\cos\theta=\dfrac{|\vec n_1\cdot\vec n_2|}{|\vec n_1|\,|\vec n_2|}",
                     font_size=25, color=WHITE),
        ).arrange(RIGHT, buff=0.30)

        panel4 = VGroup(row_par, row_per, row_ang).arrange(
            DOWN, buff=0.38, aligned_edge=LEFT,
        )
        panel4.move_to((3.30, 1.30, 0))
        self.play(Write(row_par), run_time=0.9)
        self.play(Write(row_per), run_time=0.9)
        self.play(Write(row_ang), run_time=1.1)
        self.wait(0.8)

        caption = Text(
            "用法向量统一处理平行 / 垂直 / 夹角",
            font=FONT_NAME, font_size=24, color=ACCENT,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(caption), run_time=1.1)
        self.wait(3.0)
