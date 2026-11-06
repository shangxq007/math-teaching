# 题库

按章节组织的习题集，题目用 `problem` 环境，解答用 `solution` 环境。

## 编译

```bash
cd bank
latexmk -xelatex main
```

默认输出含答案版；去掉 `main.tex` 里的 `answer` 类选项即得到无答案版。

## 结构

- `main.tex` — 封面与目录
- `chapters/` — 每章一个文件

## 写法

```latex
\section{集合与常用逻辑用语}

\begin{problem}[易]
  设 $A=\{1,2,3\}$，则 $A$ 的子集个数为______。
\end{problem}
\begin{solution}
  含有 $n$ 个元素的集合有 $2^n$ 个子集，故为 $2^3=8$。
\end{solution}
```

难度用 `\level{易}`、`\level{中}`、`\level{难}` 标注。
