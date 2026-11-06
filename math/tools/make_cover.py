#!/usr/bin/env python3
"""生成数学文档封面横幅：低多边形山峦（几何风格风景）。

用法：python3 make_cover.py [输出目录]

默认输出三张 3:1 横幅，配色对应三个文档主题：
    cover_blue.png   教案   ElegantBook blue  structurecolor #3C71B7
    cover_green.png  题库   ElegantBook green structurecolor #007802
    cover_cyan.png   导学案 ElegantNote  cyan  ecolor          #1FBABE

图案：渐变天空 + 半隐太阳 + 四层低多边形山脊（空气透视，远浅近深）。
"""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle

W, H = 24.0, 8.0          # 3:1 横幅
DPI = 110

THEMES = {
    'blue':  (60/255, 113/255, 183/255),
    'green': (0/255, 120/255, 2/255),
    'cyan':  (31/255, 186/255, 190/255),
}

# (山脊点数, 基准高度, 起伏幅度, 颜色深度, 随机种子)
# 颜色深度 0 = 纯白，1 = 纯主题色；远景浅、近景深
LAYERS = [
    (11,  0.90, 1.55, 0.18, 3),
    (13,  0.45, 1.85, 0.36, 4),
    (15, -0.05, 2.05, 0.58, 5),
    (18, -0.60, 2.25, 0.82, 6),
]


def shade(color, f):
    """往白色混合：f=1 原色，f=0 纯白。"""
    return tuple(f*c + (1-f) for c in color)


def sky(ax, color):
    """垂直渐变天空：顶部主题色淡彩 -> 地平线纯白。"""
    n = 400
    ys = np.linspace(0, 1, n)          # imshow origin='lower'：i=0 在底部
    c_top = shade(color, 0.42)
    grad = np.zeros((n, 1, 3))
    for i, t in enumerate(ys):
        grad[i, 0, :] = tuple(c_top[k]*t + (1-t) for k in range(3))
    ax.imshow(grad, extent=[-12, 12, -4, 4], origin='lower', aspect='auto', zorder=0)


def ridge_points(rng, n, base, height):
    """低多边形山脊：n 个随机峰谷点。"""
    xs = np.linspace(-12, 12, n)
    hs = rng.uniform(0.25, 1.0, n)
    hs[0] = hs[-1] = 0.15          # 两端收低，避免贴边
    return xs, base + height*hs


def cover(path, color):
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-12, 12)
    ax.set_ylim(-4, 4)
    ax.set_axis_off()

    sky(ax, color)

    # 太阳（半隐于远山之后）
    ax.add_patch(Circle((5.6, 1.55), 0.95, facecolor=shade(color, 1.0),
                        alpha=0.95, zorder=1, edgecolor='none'))

    # 山峦：从远到近
    for i, (n, base, height, f, seed) in enumerate(LAYERS):
        r = np.random.default_rng(seed)
        xs, ys = ridge_points(r, n, base, height)
        verts = list(zip(xs, ys)) + [(12.0, -4.0), (-12.0, -4.0)]
        ax.add_patch(Polygon(verts, closed=True, facecolor=shade(color, f),
                             edgecolor='none', zorder=2+i))

    fig.savefig(path, facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    for name, rgb in THEMES.items():
        cover(f'{out}/cover_{name}.png', rgb)
        print(f'wrote {out}/cover_{name}.png')
