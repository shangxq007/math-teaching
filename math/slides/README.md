# 数学课件（Beamer / PPT）

使用 Beamer + Metropolis 主题，16:9 宽屏，XeLaTeX 编译。

## 编译

```bash
cd slides
latexmk -xelatex main
```

或用 VS Code 打开本目录，保存即自动编译。

## 结构

- `main.tex` — 演示文稿入口（主题、字体、颜色）
- `chapters/` — 按章节拆分的幻灯片，在 `main.tex` 中 `\input`

## 常用命令

```latex
\begin{frame}{标题}
  内容
\end{frame}
```

- `\pause` — 逐步显示
- `\alert{重点}` — 高亮
- `block` / `exampleblock` / `alertblock` — 定理类色块
- `columns` — 分栏

## 备注

- 主题色在 `main.tex` 的 `\definecolor{slidetheme}` 中修改。
- 需要演讲者备注时，用 `\usepackage{pgfpages}` 并设置 `\setbeameroption{show notes}`。
