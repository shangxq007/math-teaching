# 讲义章节写法

## 文件命名

`01.tex`、`02.tex`……两位序号，与 `../lesson/chapters/` 的课次号对应。
新增章节后，在 `../main.tex` 里加一行 `\input{chapters/03}`。

## 章节骨架

```latex
\chapter{章名}

（一段引入，说明本章在整册里的位置）

\section{节名}

\begin{definition} ... \end{definition}

\begin{derivation} ... \end{derivation}

\begin{example} ... \end{example}
\begin{solution} ... \end{solution}

\begin{commonerror}{错法主题} ... \end{commonerror}

\begin{summary} ... \end{summary}

\begin{method} ... \end{method}

\begin{exercise} ... \end{exercise}

\reading{01}{篇名}
```

## 环境来自哪里

`definition` / `theorem` / `example` / `proof` / `exercise` 是 ElegantBook 自带；
`derivation` / `summary` / `commonerror` / `method` 在 `../common/envs.tex`。

## 常见问题

- **公式里的数集**统一用 `\mathbf{R}`、`\mathbf{Z}`，不要用 `mathbb`（未加载 amssymb 的宏包时
  会缺字）。
- **`\complement` 未定义**：导言区已加 `\providecommand{\complement}{\mathop{∁}}`，直接用即可。
- **编译报错先看字体**：`fontspec Error: The font ... cannot be found` 说明缺字体，
  不要往宏包方向查。
