# 速查表章节写法

## 文件命名

`01.tex`、`02.tex`……按主题分页，不按课次。
新增页后在 `../main.tex` 加 `\input{chapters/03}`。

## 骨架

```latex
% 第 N 页：主题
\clearpage
\begin{multicols}{3}

\begin{fastcard}{专题名}
\begin{itemize}[leftmargin=1.2em, topsep=0.2ex, itemsep=0.1ex, parsep=0pt]
\item 结论一
\item 结论二
\end{itemize}
\end{fastcard}

...
\end{multicols}
```

## 三条原则

- **一条只写一个结论**，不要把推导过程塞进来（那是概要的事）。
- **同一专题的公式放在一起**，不要按章节顺序排。
- **密度优先**：能一页放下就不分两页；栏没填满说明这条页该合并。

## 调整密度

`extarticle` 的字号（8pt / 9pt / 10pt）和 `\begin{multicols}{N}` 的栏数一起调。
本机实测：8pt + 3 栏 ≈ 6～8 个专题/页。
