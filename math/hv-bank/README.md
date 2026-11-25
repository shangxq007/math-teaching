# 高观点系列题库（第 0 章 — 第 9 章）

独立成册，编号 0–9，不与 `../bank/`（湘教版章节）混排。文档类 `elegantbook`，`answer` 模式显示答案，XeLaTeX 编译。

## 结构

```
main.tex                    % 导言区 + 封面 + 目录
chapters/00.tex             % 第 0 章 集合、逻辑演算与证明武器库（8 题）
chapters/01.tex             % 第 1 章 函数的概念与基本初等函数（12 题）
chapters/02.tex             % 第 2 章 三角函数、解三角形与复平面旋转（10 题）
chapters/03.tex             % 第 3 章 平面向量与空间向量（10 题）
chapters/04.tex             % 第 4 章 立体几何与圆锥曲线大一统（10 题）
chapters/05.tex             % 第 5 章 数列与离散动态系统（10 题）
chapters/06.tex             % 第 6 章 导数与局部线性化引擎（10 题）
chapters/07.tex             % 第 7 章 计数原理、概率空间与统计回归（10 题）
chapters/08.tex             % 第 8 章 齐次化：把二元问题压成一元比例（8 题）
chapters/09.tex             % 第 9 章 不动点：迭代、方程与几何变换的交汇（8 题）
```

`main.tex` 里两处关键设置：

```latex
\renewcommand{\xchaptertitle}{第 \arabic{chapter} 章}   % 编号用阿拉伯数字（默认 \zhnumber 会把 0 写成「零」）
\setcounter{chapter}{-1}                                % 第一个 \chapter 编号为 0
```

加新章：在 `chapters/` 建 `NN.tex`（序号与章号一致），再在 `main.tex` 末尾加一行 `\input{chapters/NN}`。

## 每题写法

```latex
\begin{problem}\level{易|中|难}
题干
\end{problem}
\begin{solution}
解析（含三个 \paragraph 板块）
\end{solution}
```

解析固定三个加粗小板块：

1. `\paragraph{集合与结构剖析}`（复平面类可用「复平面结构剖析」）
2. `\paragraph{标准解题步骤}`
3. `\paragraph{学生典型易错点诊断}`

解析 6–12 行，公式用 LaTeX，不要把答案藏在题干里。

## 编译

```bash
latexmk -xelatex main
```

## 约定

- 难度按 `\level` 标注；每章四层（基础/进阶/深化/拓展）各 2–3 题。
- 素材取自 `../sources/raw/`。
