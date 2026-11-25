"""第 1 章前置 · 舞台的诞生：从散装集合到实数连续统 R

对应「双支柱」中的舞台一侧：集合自身的四级进化
    Lv.1  原始集合：一袋散装弹珠（无序、不可比、不能算账）
    Lv.2  有序 + 代数集合：排成带刻度的数轴（Q）—— 解锁单调、奇偶、周期
    Lv.3  稠密但有孔：显微镜下暴露 sqrt(2) 等无理数孔洞，曲线漏过去，零点丢失
    Lv.4  完备连续：无理数填满孔洞，R 成为无缝金线 —— 零点被锁定；随后张成 R^2

配套「规则」一侧见 ../function-evolution/scene1_concept.py（一般关系 -> 函数）。

镜头语言说明：manim 0.22 已无 ``add_fixed_in_frame_mobjects``。这里把所有几何
内容装进一个 ``world`` 组，用 ``world.animate.scale(S, about_point=P)`` 模拟
显微镜推近／拉远；文字标题与字幕不进 world，因此天然钉在屏幕上。

渲染：
    export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
    export MANIM_BIN=~/Downloads/manim-env/bin/manim
    sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh \
        -ql stage_evolution.py RealLineCompletenessGenesis

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
GOLD = "#F5C242"

SQRT2 = float(np.sqrt(2.0))

# 数轴：横纵单位长度必须一致，否则圆变椭圆、抛物线失真
X_RANGE = [-3.2, 2.8, 0.5]
Y_RANGE = [-2.0, 2.0, 1.0]
UNIT = 1.733
X_LEN = 6.0 * UNIT          # 10.4
Y_LEN = 4.0 * UNIT          # 6.93

S = 4.0                     # 显微镜放大倍数


class RealLineCompletenessGenesis(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG
        self.world = VGroup()
        self.zoom_pt = ORIGIN
        self._title = None
        self._act_one()
        self._act_two()
        self._act_three()
        self._act_four()

    # ---------------- 工具 ----------------
    def put(self, *mobs):
        """把几何内容装进 world（随镜头一起缩放）。

        注意：``VGroup.add`` 会把传入的组展开成子对象存放，因此存入后
        对「组」本身做 FadeOut 不会影响画面里的成员 —— 一律走 self.fade()。
        """
        self.world.add(*mobs)
        return mobs[0] if len(mobs) == 1 else mobs

    @staticmethod
    def fade(mob):
        """返回逐成员的 FadeOut 列表（组会被 world.add 展开，必须逐个淡出）"""
        members = getattr(mob, "submobjects", None)
        return [FadeOut(m) for m in members] if members else [FadeOut(mob)]

    def _new_title(self, text):
        old = self._title
        if old is not None:
            self.remove(old)
        t = Text(text, font=FONT_NAME, font_size=24, color=PRIMARY)
        t.to_edge(UP, buff=0.25)
        self.add(t)
        self._title = t
        return t

    def _make_axes(self):
        ax = Axes(
            x_range=X_RANGE, y_range=Y_RANGE,
            x_length=X_LEN, y_length=Y_LEN,
            axis_config={"include_tip": False, "color": WHITE,
                         "stroke_width": 2, "numbers_to_include": None},
        )
        ax.y_axis.set_opacity(0)
        return ax

    # ================= 幕 1：Lv.1 散装 -> Lv.2 数轴 =================
    def _act_one(self):
        self._new_title("Lv.1  原始集合：一袋散装弹珠")

        values = [-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
        rng = np.random.default_rng(5)

        chips = VGroup()
        for v in values:
            pos = np.array([rng.uniform(-3.6, 3.6), rng.uniform(-1.2, 1.8), 0.0])
            chip = VGroup(
                Dot(pos, radius=0.10, color=ACCENT),
                MathTex(f"{v:g}", font_size=24, color=WHITE),
            )
            chip[1].next_to(chip[0], RIGHT, buff=0.12)
            chips.add(chip)

        bag = Ellipse(width=8.6, height=3.6, color=GRAY, stroke_width=2.5)
        bag.move_to(np.array([-0.4, 0.35, 0.0]))
        self.bag = bag
        note = VGroup(
            Text("只有「属于」和「元素个数」", font=FONT_NAME,
                 font_size=20, color=GRAY),
            Text("不能比大小，也不能加减", font=FONT_NAME,
                 font_size=20, color=RED_H),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.5)

        self.play(Create(self.put(bag)),
                  LaggedStart(*[FadeIn(c) for c in self.put(chips)],
                              lag_ratio=0.12), run_time=2.2)
        self.play(Write(note), run_time=1.0)
        self.wait(0.8)

        self._new_title("Lv.2  注入全序与代数运算：排成数轴")
        rule = VGroup(
            MathTex(r"(<)\quad +,-,\times,\div", font_size=30, color=ACCENT),
            Text("给集合装上「比大小」和「算账」两件套",
                 font=FONT_NAME, font_size=20, color=GRAY),
        ).arrange(DOWN, buff=0.2).move_to(np.array([0.0, -2.6, 0.0]))

        ax = self._make_axes()
        x_lab = MathTex("x", font_size=28, color=WHITE)
        x_lab.next_to(ax.x_axis.get_right(), RIGHT, buff=0.15)
        tick_labs = VGroup(*[
            MathTex(f"{v:g}", font_size=20, color=GRAY)
            .next_to(ax.c2p(float(v), 0), DOWN, buff=0.18)
            for v in (-2, -1, 0, 1, 2)
        ])
        self.put(ax, x_lab, tick_labs)

        self.play(Write(rule), run_time=1.0)
        self.play(
            LaggedStart(*[
                chip.animate.move_to(ax.c2p(v, 0) + UP * 0.42)
                for chip, v in zip(chips, values)
            ], lag_ratio=0.08, run_time=2.4),
            FadeOut(bag), *self.fade(note), run_time=2.0,
        )
        self.play(Create(ax.x_axis), Write(x_lab), FadeIn(tick_labs),
                  run_time=1.4)
        self.play(*self.fade(rule), run_time=0.8)

        cap = Text("看着是一条连续的线，其实是有理数集 Q —— 满布针眼",
                   font=FONT_NAME, font_size=20, color=GRAY)
        cap.to_edge(DOWN, buff=0.45)
        self.play(Write(cap), run_time=1.2)
        self.wait(1.2)

        self.axes = ax
        self.chips = chips
        self.tick_labs = tick_labs
        self.x_lab = x_lab
        self.cap1 = cap

    # ================= 幕 2：显微镜下的孔洞 =================
    def _act_two(self):
        self._new_title("Lv.3  显微镜推近：筛子上的针眼漏洞")
        self.play(FadeOut(self.cap1), run_time=0.6)

        ax = self.axes
        curve = ax.plot(lambda x: x ** 2 - 2.0, x_range=[-1.3, 1.95],
                        color=SECONDARY, stroke_width=2.5)
        f_lab = MathTex(r"y=x^2-2", font_size=28, color=SECONDARY)
        f_lab.next_to(curve.get_end(), RIGHT, buff=0.2)
        self.put(curve, f_lab)

        self.play(Create(curve), Write(f_lab), run_time=1.6)
        self.wait(0.6)

        # ---- 孔洞：此刻还太小看不见，推近后才显形 ----
        rng = np.random.default_rng(9)
        hole_xs = np.sort(np.append(np.linspace(1.12, 1.75, 9), SQRT2))
        holes = VGroup()
        meta = []
        for hx in hole_xs:
            is_root = abs(hx - SQRT2) < 1e-6
            r = 0.052 if is_root else float(rng.uniform(0.022, 0.034))
            c = Circle(radius=r, color=WHITE, stroke_width=1.2,
                       fill_color=BG, fill_opacity=1.0)
            c.move_to(ax.c2p(float(hx), 0.0))
            holes.add(c)
            meta.append((c, r, is_root))

        fine = VGroup(*[
            Circle(radius=0.009, color=GRAY, stroke_width=0.8,
                   fill_color=BG, fill_opacity=1.0)
            .move_to(ax.c2p(float(x), 0.0))
            for x in np.linspace(1.00, 1.88, 26)
        ])
        self.put(holes, fine)

        root_circ = next(c for c, r, k in meta if k)
        root_lab = MathTex(r"\sqrt{2}", font_size=30, color=RED_H)
        root_lab.set_opacity(0)          # 推近后才就位、显现

        # 遮片：让抛物线看起来在 sqrt(2) 处断开
        veil = Circle(radius=0.07, color=BG, fill_color=BG, fill_opacity=1.0,
                      stroke_width=0)
        veil.move_to(ax.c2p(SQRT2, 0.0))
        cc = veil.get_center()
        cross = VGroup(
            Line(cc + UL * 0.075, cc + DR * 0.075, color=RED_H, stroke_width=2.5),
            Line(cc + UR * 0.075, cc + DL * 0.075, color=RED_H, stroke_width=2.5),
        )
        cross.set_opacity(0)
        self.put(veil, cross)

        warn = Text("曲线从孔洞中漏过 —— 零点不存在",
                    font=FONT_NAME, font_size=20, color=RED_H)
        warn.to_edge(DOWN, buff=0.35)
        self.add(root_lab)

        self.zoom_pt = ax.c2p(1.42, 0.0)
        self.play(
            FadeOut(f_lab),
            *self.fade(self.chips), *self.fade(self.tick_labs),
            FadeOut(self.x_lab),
            self.world.animate.scale(S, about_point=self.zoom_pt),
            run_time=2.8, rate_func=smooth,
        )
        self.play(
            root_lab.animate.set_opacity(1.0),
            cross.animate.set_opacity(1.0),
            Write(warn), run_time=1.6,
        )
        # 文字标签不进 world，需按放大后的坐标手动就位
        disp = self.zoom_pt + (ax.c2p(SQRT2, 0.0) - self.zoom_pt) * S
        root_lab.move_to(disp + UP * 0.34)
        self.wait(0.8)
        self.play(cross.animate.set_opacity(0.15), run_time=0.35)
        self.play(cross.animate.set_opacity(1.0), run_time=0.35)
        self.wait(1.8)

        self.meta = meta
        self.holes = holes
        self.fine = fine
        self.root_lab = root_lab
        self.cross = cross
        self.veil = veil
        self.warn = warn

    # ================= 幕 3：无理数填洞 =================
    def _act_three(self):
        self._new_title("Lv.4  无理数倾泻而下：填满所有孔洞")
        self.play(FadeOut(self.warn), FadeOut(self.root_lab), run_time=0.8)

        ax = self.axes
        meta = self.meta

        golds = VGroup(*[
            Dot(c.get_center() + UP * 0.55,
                radius=(0.030 if k else r * 1.5), color=GOLD, fill_opacity=1.0)
            for c, r, k in meta
        ])
        rng_sand = np.random.default_rng(21)
        sand = VGroup(*[
            Dot(ax.c2p(1.42, 0.0) + UP * float(h) + LEFT * float(dx),
                radius=0.014, color=GOLD, fill_opacity=0.9)
            for h in np.linspace(0.45, 1.6, 12)
            for dx in rng_sand.uniform(-1.2, 1.2, 7)
        ])
        self.golds, self.sand = golds, sand
        self.put(golds, sand)

        self.play(LaggedStart(*[
            g.animate.move_to(c.get_center())
            for g, (c, r, k) in zip(golds, meta)
        ], lag_ratio=0.16, run_time=2.2))
        self.play(
            *self.fade(self.holes), *self.fade(self.fine),
            LaggedStart(*[FadeIn(d) for d in sand], lag_ratio=0.015,
                        run_time=2.0),
        )

        gold_line = Line(ax.c2p(X_RANGE[0], 0), ax.c2p(X_RANGE[1], 0),
                         color=GOLD, stroke_width=3)
        glow = VGroup(*[
            Line(ax.c2p(X_RANGE[0], 0), ax.c2p(X_RANGE[1], 0), color=GOLD,
                 stroke_width=3 + 5 * k, stroke_opacity=0.15)
            for k in range(1, 4)
        ])
        self.put(gold_line, glow)
        self.play(FadeOut(self.veil), *self.fade(self.cross),
                  FadeIn(glow, gold_line), run_time=1.4)

        hit = Dot(ax.c2p(SQRT2, 0.0), radius=0.045, color=SECONDARY,
                  fill_opacity=1.0)
        hit_lab = MathTex(r"(\sqrt{2},\,0)", font_size=26, color=SECONDARY)
        hit_disp = self.zoom_pt + (ax.c2p(SQRT2, 0.0) - self.zoom_pt) * S
        hit_lab.move_to(hit_disp + UP * 0.40)
        self.add(hit_lab)
        self.put(hit)

        say = Text("无缝可钻：零点被迫现身", font=FONT_NAME,
                   font_size=21, color=SECONDARY)
        say.to_edge(DOWN, buff=0.35)

        self.play(FadeIn(hit), Write(hit_lab), Write(say), run_time=1.4)
        self.wait(2.4)

        self.gold_line, self.glow = gold_line, glow
        self.hit, self.hit_lab = hit, hit_lab
        self.say = say

    # ================= 幕 4：张成 R^2 =================
    def _act_four(self):
        self._new_title("舞台就绪：R × R 连续平面诞生")
        self.play(FadeOut(self.say), run_time=0.6)

        ax = self.axes
        # 镜头先拉远复位（视觉上回到全局视野）
        self.play(
            self.world.animate.scale(1.0 / S, about_point=self.zoom_pt),
            run_time=2.6, rate_func=smooth,
        )
        # 整个旧世界退场：连同金砂、红叉、放大镜痕迹一并清干净，
        # 幕 4 用全新的世界重建，避免任何跨幕残留。
        self.remove(self.world)
        # 幕 1-3 里挂在场景层（不入 world）的文字标签也要一起撤掉，
        # 否则幕 4 重建同名标签时会出现重影。
        for mob in (self.hit_lab, self.root_lab, getattr(self, "say", None),
                    getattr(self, "warn", None)):
            if mob is not None:
                self.remove(mob)
        self.world = VGroup()

        # --- 重建舞台（全部按原始尺度坐标） ---
        base_axis = Line(ax.c2p(X_RANGE[0], 0), ax.c2p(X_RANGE[1], 0),
                         color=WHITE, stroke_width=1.5, stroke_opacity=0.5)
        gold_line = Line(ax.c2p(X_RANGE[0], 0), ax.c2p(X_RANGE[1], 0),
                         color=GOLD, stroke_width=3)
        glow = VGroup(*[
            Line(ax.c2p(X_RANGE[0], 0), ax.c2p(X_RANGE[1], 0), color=GOLD,
                 stroke_width=3 + 5 * k, stroke_opacity=0.15)
            for k in range(1, 4)
        ])
        y_line = Line(ax.c2p(0, -2.0), ax.c2p(0, 2.0), color=GOLD, stroke_width=4)
        y_glow = VGroup(*[
            Line(ax.c2p(0, -2.0), ax.c2p(0, 2.0), color=GOLD,
                 stroke_width=4 + 6 * k, stroke_opacity=0.15)
            for k in range(1, 4)
        ])
        grid = VGroup(*[
            Line(ax.c2p(x, -2.0), ax.c2p(x, 2.0), color=GRAY, stroke_width=1,
                 stroke_opacity=0.25)
            for x in np.arange(-3.0, 2.81, 0.4)
        ] + [
            Line(ax.c2p(X_RANGE[0], y), ax.c2p(X_RANGE[1], y), color=GRAY,
                 stroke_width=1, stroke_opacity=0.25)
            for y in np.arange(-2.0, 2.01, 0.5)
        ])
        curve = ax.plot(lambda x: x ** 2 - 2.0, x_range=[-1.3, 1.95],
                        color=SECONDARY, stroke_width=2.5)
        hit = Dot(ax.c2p(SQRT2, 0.0), radius=0.07, color=SECONDARY,
                  fill_opacity=1.0)
        hit_lab = MathTex(r"(\sqrt{2},\,0)", font_size=24, color=SECONDARY)
        hit_lab.next_to(hit.get_top(), UP + RIGHT, buff=0.14)
        xy_lab = MathTex(r"\mathbb{R}^2", font_size=34, color=ACCENT)
        xy_lab.next_to(ax.c2p(2.6, 1.85), RIGHT, buff=0.2)

        self.put(base_axis, gold_line, glow, y_line, y_glow, grid,
                 curve, hit, hit_lab, xy_lab)

        final = Text("接下来，在这块舞台上筛选出「单值」的那条曲线",
                     font=FONT_NAME, font_size=22, color=PRIMARY)
        final.to_edge(DOWN, buff=0.4)

        self.play(Create(gold_line), Create(y_line), FadeIn(glow, y_glow),
                  run_time=1.6)
        self.play(FadeIn(grid), FadeIn(curve), FadeIn(hit),
                  Write(hit_lab), Write(xy_lab), run_time=1.8)
        self.play(Write(final), run_time=1.4)
        self.wait(3.5)
