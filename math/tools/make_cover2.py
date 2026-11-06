#!/usr/bin/env python3
"""封面候选方案 D/E/F。"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

THEME = (60/255, 113/255, 183/255)
W, H = 24.5, 7.0


def cmap_from(color, name='c'):
    return LinearSegmentedColormap.from_list(
        name, [(1, 1, 1), tuple(0.82*np.array(color)+0.18), color,
               tuple(0.45*np.array(color))])


def cand_d(path):
    """双源干涉波纹。"""
    x = np.linspace(-12, 12, 520)
    y = np.linspace(-3.5, 3.5, 180)
    X, Y = np.meshgrid(x, y)
    r1 = np.sqrt((X+4.0)**2 + Y**2)
    r2 = np.sqrt((X-4.0)**2 + Y**2)
    Z = (np.sin(2.2*r1) + np.sin(2.2*r2)) / 2

    fig = plt.figure(figsize=(W, H), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor('white')
    levels = np.linspace(-1, 1, 46)
    ax.contourf(X, Y, Z, levels=levels, cmap=cmap_from(THEME), alpha=0.92)
    ax.contour(X, Y, Z, levels=levels[::3], colors='white', linewidths=0.6, alpha=0.55)
    ax.set_axis_off()
    ax.set_xlim(-12, 12); ax.set_ylim(-3.5, 3.5)
    fig.savefig(path, facecolor='white')
    plt.close(fig)


def cand_e(path):
    """单源同心波纹，铺满宽度。"""
    x = np.linspace(-12, 12, 520)
    y = np.linspace(-3.5, 3.5, 180)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt((X/2.6)**2 + Y**2)
    Z = np.sin(2.4*R) * np.exp(-0.10*R)

    fig = plt.figure(figsize=(W, H), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor('white')
    levels = np.linspace(-1, 1, 46)
    ax.contourf(X, Y, Z, levels=levels, cmap=cmap_from(THEME), alpha=0.92)
    ax.contour(X, Y, Z, levels=levels[::3], colors='white', linewidths=0.6, alpha=0.55)
    ax.set_axis_off()
    ax.set_xlim(-12, 12); ax.set_ylim(-3.5, 3.5)
    fig.savefig(path, facecolor='white')
    plt.close(fig)


def cand_f(path):
    """3D 马鞍面铺满横幅。"""
    x = np.linspace(-7.5, 7.5, 300)
    y = np.linspace(-2.6, 2.6, 150)
    X, Y = np.meshgrid(x, y)
    Z = 0.55*(X**2/9 - Y**2/4) + 0.35*np.sin(1.4*X)*np.cos(1.1*Y)
    Z = (Z - Z.min())/(Z.max()-Z.min())*2 - 1

    fig = plt.figure(figsize=(W, H), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.plot_surface(X, Y, Z, cmap=cmap_from(THEME), linewidth=0,
                    antialiased=True, shade=True, rcount=150, ccount=300)
    ax.set_axis_off()
    ax.view_init(elev=28, azim=-52)
    ax.set_xlim(-7.5, 7.5); ax.set_ylim(-2.6, 2.6); ax.set_zlim(-1, 1)
    ax.set_box_aspect((15, 5.2, 2.6))
    fig.savefig(path, facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    import sys
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    cand_d(f'{d}/cand_d.png')
    cand_e(f'{d}/cand_e.png')
    cand_f(f'{d}/cand_f.png')
    print('done')
