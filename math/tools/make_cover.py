#!/usr/bin/env python3
"""生成数学文档封面横幅。

用法：python3 make_cover.py [输出目录]

输出三张 3:1 横幅，分别对应 ElegantBook/ElegantNote 的三个主题色：
    cover_blue.png   教案   (#3C71B7)
    cover_green.png  题库   (#007802)
    cover_cyan.png   导学案 (#1FBABE)

图案：同心波纹等高线（单源扩散波），白底，铺满整个横幅。
"""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

W, H = 24.0, 8.0          # 3:1
DPI = 110

THEMES = {
    'blue':  (60/255, 113/255, 183/255),   # ElegantBook blue structurecolor
    'green': (0/255, 120/255, 2/255),      # ElegantBook green structurecolor
    'cyan':  (31/255, 186/255, 190/255),   # ElegantNote  cyan ecolor
}


def make_cmap(color):
    """白 -> 主题色 的柔和渐变。"""
    light = tuple(0.86*np.array(color) + 0.14)
    mid = tuple(0.62*np.array(color) + 0.38)
    dark = tuple(0.30*np.array(color))
    return LinearSegmentedColormap.from_list('cover', [(1, 1, 1), light, mid, color, dark])


def cover(path, color):
    x = np.linspace(-12, 12, 620)
    y = np.linspace(-4, 4, 240)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt((X/2.7)**2 + Y**2)
    Z = np.sin(2.3*R) * np.exp(-0.11*R)

    fig = plt.figure(figsize=(W, H), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor('white')

    levels = np.linspace(-1, 1, 48)
    ax.imshow(Z, extent=[-12, 12, -4, 4], origin='lower',
              cmap=make_cmap(color), aspect='auto', interpolation='bilinear')
    ax.contour(X, Y, Z, levels=levels, colors='white', linewidths=0.5, alpha=0.35)

    ax.set_axis_off()
    ax.set_xlim(-12, 12)
    ax.set_ylim(-4, 4)
    fig.savefig(path, facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    for name, rgb in THEMES.items():
        cover(f'{out}/cover_{name}.png', rgb)
        print(f'wrote {out}/cover_{name}.png')
