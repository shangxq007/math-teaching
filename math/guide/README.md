# 导学案

面向学生的课前预习 + 课堂探究 + 当堂检测 + 课后作业一体化讲义，
使用 ElegantNote 模板（`math=newtx`、`color=cyan`）。

## 编译

```bash
cd guide
latexmk -xelatex main
```

## 结构

- `main.tex` — 自定义标题页（含封面横幅）与目录
- `chapters/` — 每课一个文件

## 每课的固定环节

```latex
\begin{learnobjective} ... \end{learnobjective}   % 学习目标
\begin{preview}        ... \end{preview}          % 预习导学
\begin{explore}        ... \end{explore}          % 课堂探究
\begin{inclasstest}    ... \end{inclasstest}      % 当堂检测
\begin{afterclass}     ... \end{afterclass}       % 课后作业
```

填空用 `\blank`，重点标注用 `\key{...}`。

## 与教案的对应关系

导学案的章节号与 `../lesson/` 一一对应，方便学生课前对照教师教案使用。
