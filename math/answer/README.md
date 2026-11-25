# 答案与解析

与讲义、试卷、作业配套的详解册。

## 定位与分工

| 文档 | 答案形态 |
| --- | --- |
| 题库 `../bank/` | 题目 + 答案（`answer` / `noanswer` 双模式） |
| **答案与解析（本目录）** | **题目 + 答案 + 解析（为什么这样做、易错点）** |
| 错题本 `../errorbook/` | 学生自己的错题 + 反思 |

题库给「对答案」，本册给「讲清楚」。**题目本体不在这里**，只写题号与出处。

## 结构

按配套文档分章，每章若干 `ansblock`：

```latex
\section{章名（对应 ../handout/chapters/NN）}

\begin{ansblock}{练习 1.1}
\begin{enumerate}
  \item 答案
  \item 答案 \quad\textit{易错点：...}
\end{enumerate}
\end{ansblock}
```

## 三条原则

- **只写答案不给解析的，不要收进本册**（那种放回题库）；
- **解析写「为什么这样想」**，不写「由此可得」；
- **每章末尾加一个「解法比较」块**，给学有余力的学生第二条路。

## 编译

```bash
cd answer
latexmk -xelatex -g main
```

## 文件

```
main.tex            导言区 + 封面
chapters/01.tex     第 1 章
chapters/README.md
```
