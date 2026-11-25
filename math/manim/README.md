# Manim 动画

教学用 Manim CE 动画工程。每个单元一个子目录，内含分场景脚本与渲染产物。

## 环境

本机有两个 venv，**都不在 PATH 上**，用绝对路径调用：

| venv | 版本 | 用途 |
| --- | --- | --- |
| `~/Downloads/manim-env` | Manim CE 0.22.1 | 默认，新脚本用这个 |
| `~/Downloads/manim-env-021` | Manim CE 0.21.0 | 第三方仓库（teach-math-with-manim 等）需要 0.21 API |

## 渲染：必须走 manim-run.sh + TeX Live 自带的 dvisvgm

**两条都不能少。**

`dvisvgm` 负责 DVI→SVG。Debian 自带的 3.4.4 对 TeX Live 2026 的字体算不出包围盒：
生成的 SVG 里 `width='0pt' height='0pt'`（`$\pm$`、`$\iff$`、单个字母都会中招），
manim 拿到零尺寸 SVG 后字符互相叠印。**症状是公式糊成一团，但 `.tex` 源码完全正确。**

装 TeX Live 自己的 dvisvgm（3.6）并让它优先：

```bash
sudo tlmgr install dvisvgm          # 装到 /usr/local/texlive/2026/bin/x86_64-linux/
```

系统的 `dvisvgm` 还链的是发行版 libkpathsea，看不见装在 `/usr/local/texlive/2026`
的树，所以 `MathTex` 直接渲染会失败。`manim-video` skill 的 `manim-run.sh` 用 mount
namespace 挂一个 `texmf.cnf` 解决，**不用 sudo**：

```bash
cd manim/<unit>
export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH   # 用 TL 的 dvisvgm
export MANIM_BIN=~/Downloads/manim-env/bin/manim
sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh -ql scene.py SceneName   # 草稿 480p15
sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh -qh scene.py SceneName   # 成品 1080p60
```

`manim-run.sh` 默认调 `~/Downloads/manim-env-021/bin/manim`，要用 0.22.1 必须设 `MANIM_BIN`。

**自检**：渲染后 `grep -l "width='0pt'\|height='0pt'" media/Tex/*.svg` 应为空。

## 编码约定

- 中文一律 `Text(..., font="Noto Sans Mono CJK SC")`。这是本机唯一可用的**等宽**中文字体；
  Manim 的 Pango 渲染在比例字体下字距会崩，所以不要用 `SimHei` / `Microsoft YaHei`（本机也没有）。
- 数学一律 `MathTex`，且用**原始字符串** `MathTex(r"\frac{1}{2}")`。
- 每幕结束 `self.wait()`；换幕用 `ReplacementTransform` 更新标题，及时 `FadeOut` 上一幕的临时对象。
- 坐标系尺寸别顶满画幅：16:9 画幅高 8 个单位，坐标轴超过 ~6.6 就会和顶部标题打架。

## 目录

```
real-line-genesis/    第 1 章前置「舞台的诞生」：散装集合→有序代数→有理筛子→实数连续统，显微镜下零点丢失与现身
function-evolution/   第 1 章 函数概念引入：概念线（一般关系→函数）+ 图像线（无序→有序），另含指对数互逆
logic-weapons/        第 0 章 逻辑演算与证明武器库（反证法集合图、数学归纳法多米诺）
euler-rotation/       第 2 章 三角与复平面旋转（两角和旋转投影、乘 i 诱导公式、i 与欧拉公式诞生）
vector-space/          第 3 章 平面向量与空间向量（基底分解、数量积投影、法向量与二面角）+ 换基底与相似互换律 A'=P⁻¹AP + 向量镜面反射 a'=2proj-a
affine-conics/         第 4 章 立体几何与圆锥曲线（圆仿射压缩为椭圆、Dandelin 圆锥截面）
affine-rotation/       跨章方法论：坐标轴旋转 45° 消灭交叉项 xy（xy=1→标准等轴双曲线）+ 复特征值螺旋不动点
function-transform/    第 1 章 抽象函数周期之源（连续两次镜像反射合成刚体平移 T=2|b-a|）+ 45° 镜面反射定律（y=±x+b 坐标互换、指对同构交点秒杀）+ 平方/倒数变换五铁律（负部翻折、零点撕裂、无穷变零、单调反转、极值互换）+ 主被动对偶（动曲线 vs 动坐标系同屏）
sequence-dynamics/     第 5 章 数列与离散动态系统（蛛网图与特征值、不动点稳定性、特征向量收敛）
local-linearization/   第 6 章 导数与局部线性化引擎（半圆射影定理证基本不等式、切线放缩）
probability-ls/        第 7 章 计数原理、概率测度与统计线性逼近（最小二乘残差平方和、条件概率缩放）
```

## 验证

不要只跑 `--version`。改完脚本先 `-ql` 渲一遍，再抽帧确认中文与公式没乱码、没溢出，
最后才 `-qh`。
