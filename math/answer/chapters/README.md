# 答案与解析章节写法

## 文件命名

`01.tex`、`02.tex`……与 `../handout/chapters/` 的课次号一致。
配套试卷的解析写在 `exam-answers.tex`，配套作业写在 `hw-answers.tex`。

## 骨架

```latex
\section{章名（对应 ../handout/chapters/NN）}

\begin{ansblock}{练习 1.1}
\begin{enumerate}
  \item 答案
\end{enumerate}
\end{ansblock}

\begin{ansblock}{练习 1.2（含解析）}
...
\end{ansblock}

\begin{ansblock}{补充：三种解法的比较}
...
\end{ansblock}
```

## 什么时候写解析

- 学生**能自己核对**的题：只写答案；
- 学生**看不懂答案**的题：写解析，且解析要回答「怎么想到」；
- 有多种解法的题：单列一个「解法比较」块。

## 与讲义的同步

讲义里新增或改动练习后，**同步更新本册对应小节**。
建议在 `../handout/chapters/README.md` 的改动记录里注明「答案已同步到 ../answer/」。
