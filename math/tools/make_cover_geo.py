#!/usr/bin/env python3
"""封面候选：几何风格 / 几何风景。"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
from matplotlib.colors import LinearSegmentedColormap

THEME = (60/255, 113/255, 183/255)
W, H = 24.0, 8.0
DPI = 110


def shade(color, f):
    """往白色混合：f=1 原色，f<1 变浅。"""
    return tuple(f*c + (1-f) for c in color)


def sky(ax, color, top=1.0, bottom=1.0):
    """垂直渐变天空。"""
    n = 400
    ys = np.linspace(0, 1, n)
    c_top = shade(color, top)
    c_bot = shade(color, bottom)
    grad = np.zeros((n, 1, 3))
    for i, t in enumerate(ys):
        grad[i, 0, :] = tuple(c_top[k]*(1-t) + c_bot[k]*t for k in range(3))
    ax.imshow(grad, extent=[-12, 12, -4, 4], origin='lower', aspect='auto')


def ridge(x, rng, amp, freqs):
    y = np.zeros_like(x)
    for f in freqs:
        y += (amp/f**0.9) * np.sin(2*np.pi*f*x + rng.uniform(0, 2*np.pi))
    return y


def cand_mountain(path, color):
    """低多边形山峦（几何风景）。"""
    rng = np.random.default_rng(7)
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-12, 12); ax.set_ylim(-4, 4)
    ax.set_axis_off()

    sky(ax, color, top=0.55, bottom=1.0)

    # 太阳
    ax.add_patch(Circle((6.6, 1.55), 1.05, color=shade(color, 1.15), alpha=0.9, zorder=2))

    x = np.linspace(-12, 12, 700)
    layers = [
        (-0.6, 1.5, 0.30, 3),
        (-1.3, 2.2, 0.22, 4),
        (-2.1, 2.9, 0.16, 5),
        (-3.0, 3.6, 0.11, 6),
    ]
    for i, (base, amp, f, seed) in enumerate(layers):
        r = np.random.default_rng(seed)
        y = base + ridge(x, r, amp, [f, f*2.3, f*4.1, f*7.7])
        verts = np.concatenate([np.column_stack([x, y]),
                                np.array([[12, -4], [-12, -4]])])
        ax.add_patch(Polygon(verts, closed=True,
                             facecolor=shade(color, 0.30 + 0.22*i),
                             edgecolor='none', zorder=3+i))
    fig.savefig(path, facecolor='white')
    plt.close(fig)


def cand_circles(path, color):
    """重叠圆几何图案（生命之花风格）。"""
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-12, 12); ax.set_ylim(-4, 4)
    ax.set_aspect('equal')
    ax.set_axis_off()
    ax.set_facecolor('white')

    R = 1.0
    centers = [(0.0, 0.0)]
    for k in range(6):
        a = np.pi/6 + k*np.pi/3
        centers.append((R*np.cos(a), R*np.sin(a)))
    # 外圈再一圈
    for k in range(12):
        a = k*np.pi/6
        centers.append((2*R*np.cos(a), 2*R*np.sin(a)))

    for i, (cx, cy) in enumerate(centers):
        ax.add_patch(Circle((cx, cy), R, fill=False,
                            edgecolor=shade(color, 0.45 + 0.5*abs(np.sin(i))),
                            lw=1.6, alpha=0.85))
    fig.savefig(path, facecolor='white')
    plt.close(fig)


def cand_conics(path, color):
    """圆锥曲线族：椭圆 / 抛物线 / 双曲线。"""
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-12, 12); ax.set_ylim(-4, 4)
    ax.set_axis_off()
    ax.set_facecolor('white')

    x = np.linspace(-12, 12, 900)
    # 抛物线族
    for k in np.linspace(-3, 3, 9):
        y = 0.28*(x - k)**2 - 3.4
        ax.plot(x, y, color=shade(color, 0.85), lw=1.3, alpha=0.75)
    # 椭圆族
    t = np.linspace(0, 2*np.pi, 500)
    for a in np.linspace(0.6, 2.6, 6):
        b = a*0.62
        ax.plot(a*np.cos(t) - 6.0, b*np.sin(t) + 0.6,
                color=shade(color, 0.55), lw=1.3, alpha=0.8)
    # 双曲线族
    for k in np.linspace(-2.5, 2.5, 7):
        xx = np.linspace(2.0, 11, 500)
        yy = k + 1.6*np.sqrt(np.maximum(xx-2.0, 0))/1.4
        ax.plot(xx, yy, color=shade(color, 0.55), lw=1.3, alpha=0.8)
        ax.plot(xx, 2*k - yy, color=shade(color, 0.55), lw=1.3, alpha=0.8)
    fig.savefig(path, facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    import sys
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    cand_mountain(f'{d}/geo_mountain.png', THEME)
    cand_circles(f'{d}/geo_circles.png', THEME)
    cand_conics(f'{d}/geo_conics.png', THEME)
    print('done')
