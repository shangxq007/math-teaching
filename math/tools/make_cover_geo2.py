#!/usr/bin/env python3
"""封面候选：低多边形渐变网格 / 简化圆锥曲线族。"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.tri import Triangulation

THEME = (60/255, 113/255, 183/255)
W, H = 24.0, 8.0
DPI = 110


def cand_mesh(path, color):
    """低多边形渐变网格。"""
    rng = np.random.default_rng(42)
    nx, ny = 26, 9
    gx = np.linspace(-12, 12, nx)
    gy = np.linspace(-4, 4, ny)
    pts = []
    for y in gy:
        for x in gx:
            jx = x + (rng.random()-0.5)*(24/(nx-1))*0.92
            jy = y + (rng.random()-0.5)*(8/(ny-1))*0.92
            pts.append((jx, jy))
    pts = np.array(pts)
    tri = Triangulation(pts[:, 0], pts[:, 1])

    # 节点颜色：左白右主题色，叠加纵向轻微变化
    node_c = []
    for (x, y) in pts:
        t = (x + 12)/24
        t = 0.5 - 0.5*np.cos(np.pi*t)          # 平滑两端
        c = (1-t)*np.array([1, 1, 1]) + t*np.array(color)
        c = c*(0.94 + 0.10*(y+4)/8)            # 纵向微差
        node_c.append(np.clip(c, 0, 1))
    node_c = np.array(node_c)

    fig = plt.figure(figsize=(W, H), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-12, 12); ax.set_ylim(-4, 4)
    ax.set_axis_off()
    for s in tri.triangles:
        c = node_c[s].mean(axis=0)
        ax.add_patch(Polygon(pts[s], facecolor=c, edgecolor='white', lw=0.35))
    fig.savefig(path, facecolor='white')
    plt.close(fig)


def cand_conics2(path, color):
    """简化圆锥曲线族。"""
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-12, 12); ax.set_ylim(-4, 4)
    ax.set_axis_off()
    ax.set_facecolor('white')

    def shade(f):
        return tuple(f*np.array(color) + (1-f)*np.array([1, 1, 1]))

    # 椭圆族（左）
    t = np.linspace(0, 2*np.pi, 600)
    for i, a in enumerate(np.linspace(0.5, 2.4, 5)):
        b = a*0.62
        ax.plot(a*np.cos(t) - 8.2, b*np.sin(t) + 0.5,
                color=shade(0.75 - i*0.11), lw=1.4, alpha=0.9)
    # 抛物线族（中）
    x = np.linspace(-12, 12, 900)
    for i, k in enumerate(np.linspace(-2.6, 2.6, 7)):
        y = 0.30*(x - k)**2 - 3.6
        ax.plot(x, y, color=shade(0.62 - abs(i-3)*0.06), lw=1.4, alpha=0.85)
    # 双曲线族（右）
    for i, k in enumerate(np.linspace(-2.2, 2.2, 6)):
        xx = np.linspace(1.6, 11, 600)
        yy = k + 1.5*np.sqrt(np.maximum(xx-1.6, 0))/1.5
        ax.plot(xx, yy, color=shade(0.55), lw=1.4, alpha=0.8)
        ax.plot(xx, 2*k - yy, color=shade(0.55), lw=1.4, alpha=0.8)
    fig.savefig(path, facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    import sys
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    cand_mesh(f'{d}/geo_mesh.png', THEME)
    cand_conics2(f'{d}/geo_conics2.png', THEME)
    print('done')
