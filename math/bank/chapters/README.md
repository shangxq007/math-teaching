# 题库章节目录

每个文件对应一章，文件名以两位序号开头，按顺序在 `../main.tex` 中 `\input`。

- `01.tex` — 集合与常用逻辑用语

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
