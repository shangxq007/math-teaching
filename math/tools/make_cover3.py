#!/usr/bin/env python3
"""封面候选方案 G（极坐标网格）/ H（Apollonian 垫片）。"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mp

THEME = (60/255, 113/255, 183/255)
W, H = 24.5, 7.0


def cand_g(path):
    """极坐标网格：以画面外左侧为极点的同心圆弧 + 径向线。"""
    fig = plt.figure(figsize=(W, H), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor('white')
    ax.set_aspect('equal')

    cx, cy = -26.0, 0.0
    for r in np.arange(16.0, 42.0, 1.6):
        th = np.linspace(-0.28, 0.28, 600)
        ax.plot(cx + r*np.cos(th), cy + r*np.sin(th),
                color=THEME, lw=1.0, alpha=0.45)
    for a in np.linspace(-0.28, 0.28, 31):
        ax.plot([cx, cx+42*np.cos(a)], [cy, cy+42*np.sin(a)],
                color=THEME, lw=1.0, alpha=0.45)

    ax.set_xlim(-8, 15)
    ax.set_ylim(-3.5, 3.5)
    ax.set_axis_off()
    fig.savefig(path, facecolor='white')
    plt.close(fig)


def cand_h(path):
    """Apollonian 垫片。"""
    fig = plt.figure(figsize=(W, H), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor('white')
    ax.set_aspect('equal')

    circles = []

    def apollon(c1, c2, c3, depth):
        if depth <= 0:
            return
        k1, k2, k3 = c1[0], c2[0], c3[0]
        z1, z2, z3 = c1[1], c2[1], c3[1]
        k4 = k1 + k2 + k3 + 2*np.sqrt(k1*k2 + k2*k3 + k3*k1)
        z4 = (k1*z1 + k2*z2 + k3*z3 +
              2*np.sqrt(k1*k2*z1*z2 + k2*k3*z2*z3 + k3*k1*z3*z1)) / k4
        c4 = (k4, z4)
        circles.append(c4)
        apollon(c4, c2, c3, depth-1)
        apollon(c1, c4, c3, depth-1)
        apollon(c1, c2, c4, depth-1)

    # 外圆（曲率为负）+ 两个内切圆
    outer = (-1.0, 0+0j)
    c_left = (2.0, -0.5+0j)
    c_right = (2.0, 0.5+0j)
    circles += [outer, c_left, c_right]
    apollon(c_left, c_right, outer, 6)

    for k, z in circles:
        rr = abs(1.0/k)
        ax.add_patch(mp.Circle((z.real, z.imag), rr, fill=False,
                               edgecolor=THEME, lw=0.8, alpha=0.7))

    # 缩放到横幅：圆族本身高约 2、宽约 2，横向重复 5 次
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_axis_off()
    fig.savefig(path, facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    import sys
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    cand_g(f'{d}/cand_g.png')
    cand_h(f'{d}/cand_h.png')
    print('done')
