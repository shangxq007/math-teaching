# 题库章节目录

每个文件对应**一章**，文件名以两位序号开头，按顺序在 `../main.tex` 中 `\input`。

- `01.tex` — 集合与常用逻辑用语（第 1 章）
- `02.tex` — 一元二次函数、方程和不等式（第 2 章）
- `03.tex` — 函数、幂函数、指数函数、对数函数（第 3、4 章）
- `04.tex` — 三角函数（第 5 章）

## 题目写法

```latex
\begin{problem}\level{易}
题目内容
\end{problem}
\begin{solution}
解答内容
\end{solution}
```

`\level{易|中|难}` 用于标注难度。将 `main.tex` 文档类选项中的 `answer` 改为
`noanswer` 即可隐藏全部 `solution`，用于印发试卷。
