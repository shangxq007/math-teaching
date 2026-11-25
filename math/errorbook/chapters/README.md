# 错题本章节写法

## 文件命名

`01.tex`、`02.tex`……按章节组织，与 `../lesson/chapters/` 对应。
期末另建 `99-review.tex` 汇总高频错因。

## 骨架

```latex
\section{章名}

\begin{mistake}[错因分类]
（原题）题目原文

\wrong{我当时写的错解}

\correct{正确解法，关键步骤加一句「为什么这样想」}

\variant{改编一道同类题，或注明来自 ../bank/ 的题号}

\reflect{错因一句话 + 下次识别信号}
\end{mistake}
```

## 错因分类

只用这六类，便于统计：

`概念不清` / `运算错误` / `审题不细` / `方法不当` / `时间不够` / `书写不规范`

## 期末统计

在 `chapters/99-review.tex` 里按分类计数：

```latex
\begin{table}[htbp]
\centering
\begin{tabular}{lc}
\toprule
错因 & 次数 \\
\midrule
概念不清 & 3 \\
运算错误 & 5 \\
\bottomrule
\end{tabular}
\end{table}
```

次数最多的两类，就是下学期开学第一周要重讲的内容。
