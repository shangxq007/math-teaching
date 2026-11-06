# 教案

面向教师的教学方案，每章一课时。

## 编译

```bash
cd lesson
latexmk -xelatex main
```

## 结构

- `main.tex` — 封面与目录，`\input` 各章
- `chapters/` — 每章一个文件，文件名以序号开头（`01.tex`、`02.tex`）

## 每章的固定环节

```latex
\begin{objective} ... \end{objective}   % 教学目标
\begin{keypoint}  ... \end{keypoint}    % 教学重难点
\begin{procedure} ... \end{procedure}   % 教学过程（含例题、练习）
\begin{board}     ... \end{board}       % 板书设计
\begin{homework}  ... \end{homework}    % 作业布置
```

这些环境定义在 `../common/macros.tex`，配色跟随主题色。

## 新增课时

在 `chapters/` 新增 `02.tex`，在 `main.tex` 加一行 `\input{chapters/02}`。
