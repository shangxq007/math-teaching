# 拓展阅读 · 章节文件

每篇拓展阅读一个文件，文件名以序号开头（`01.tex`、`02.tex`），
在 `../main.tex` 中 `\input{chapters/02}` 引入。

## 单篇结构建议

```latex
\section{引子}      % 从一个问题或故事切入
\section{核心内容}  % 定理、证明、例子
\section{延伸}      % 更深的背景或更远的联系
\section{结语}
```

## 环境

- 定理类：`theorem`、`lemma`、`proposition`、`proof`（ElegantPaper 自带）
- 定义类：`definition`、`example`、`conjecture`、`remark`
- 问题类：`problem`、`solution`（由 `../common/macros.tex` 补齐）
- 引文：`\cite{key}`，条目写在 `../references.bib`

## 篇幅

单篇控制在 2--5 页，目标是学生能在 20 分钟内读完。
