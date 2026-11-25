# 笔记章节写法

## 文件命名

`01.tex`、`02.tex`……与 `../lesson/chapters/` 的课次号对应。
新增后在 `../main.tex` 里加 `\input{chapters/03}`。

## 骨架

```latex
\section{课题}

\begin{notezone}{课前：我已知什么}
\begin{itemize}
  \item 提示语 + \underline{\hspace{4em}}；
\end{itemize}
\noteblank[10ex]
\end{notezone}

\begin{notezone}{课中：概念怎么说的}
...
\noteblank[14ex]
\end{notezone}

\begin{notezone}{课中：一道我没听懂的例题}
...
\noteblank[16ex]
\end{notezone}

\begin{notezone}{课后：我能复述什么}
...
\noteblank[18ex]
\end{notezone}
```

## 三条原则

- **提示语不写答案**。写「概念怎么说的」，不写「元素三性：确定性、互异性、无序性」。
- **留白长度按难度给**。抄写 6～8ex，复述 14～18ex。
- **每章至少一个「我卡在哪」的区块**，这是笔记本最有价值的部分。

## 环境来自哪里

`notezone`、`noteblank` 在 `../common/envs.tex`（黄色盒子 + `\noteblank` 留白）。
