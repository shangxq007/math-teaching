#!/usr/bin/env python3
"""几何风景封面：低多边形山峦（多边形山脊 + 渐变天空 + 太阳）。"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle

THEME = (60/255, 113/255, 183/255)
W, H = 24.0, 8.0
DPI = 110


def shade(color, f):
    return tuple(f*c + (1-f) for c in color)


def sky(ax, color):
    n = 400
    ys = np.linspace(0, 1, n)
    c_top = shade(color, 0.45)
    c_bot = (1, 1, 1)
    grad = np.zeros((n, 1, 3))
    for i, t in enumerate(ys):
        grad[i, 0, :] = tuple(c_top[k]*(1-t) + c_bot[k]*t for k in range(3))
    ax.imshow(grad, extent=[-12, 12, -4, 4], origin='lower', aspect='auto', zorder=0)


def ridge_points(rng, n, base, height):
    """生成低多边形山脊：n 个随机峰谷点。"""
    xs = np.linspace(-12, 12, n)
    hs = rng.uniform(0.25, 1.0, n)
    hs[0] = hs[-1] = 0.15
    return xs, base + height*hs


def mountain(path, color):
    rng = np.random.default_rng(20261106)
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-12, 12); ax.set_ylim(-4, 4)
    ax.set_axis_off()

    sky(ax, color)

    # 太阳（在山后）
    ax.add_patch(Circle((5.6, 1.55), 0.95, facecolor=shade(color, 1.0),
                        alpha=0.95, zorder=1, edgecolor='none'))

    layers = [
        (11,  0.90, 1.55, 0.20, 3),
        (13,  0.45, 1.85, 0.38, 4),
        (15, -0.05, 2.05, 0.58, 5),
        (17, -0.60, 2.25, 0.82, 6),
    ]
    for i, (n, base, height, f, seed) in enumerate(layers):
        r = np.random.default_rng(seed)
        xs, ys = ridge_points(r, n, base, height)
        # 加密插值，保持折线感
        verts = list(zip(xs, ys)) + [(12.0, -4.0), (-12.0, -4.0)]
        ax.add_patch(Polygon(verts, closed=True, facecolor=shade(color, f),
                             edgecolor='none', zorder=2+i))

    fig.savefig(path, facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    import sys
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    mountain(f'{d}/geo_mountain2.png', THEME)
    print('done')
