# 数学拓展阅读

用 ElegantPaper 模板写的课后延伸阅读，供学有余力的学生自学。

与另外三个文档的区别：

| 文档 | 模板 | 读者 |
| --- | --- | --- |
| 教案 | ElegantBook | 教师 |
| 题库 | ElegantBook | 师生 |
| 导学案 | ElegantNote | 学生（课前/课中） |
| 拓展阅读 | ElegantPaper | 学生（课后自学） |

## 选题方向

- 课内知识点的深入：如「为什么 $a^0=1$」「零点定理的严格证明」
- 知识点的延伸：如「集合论与无穷」「从勾股定理到费马大定理」
- 数学史与思想：如「虚数的诞生」「微积分优先权之争」
- 大学先修：如「什么是群」「极限的 $\varepsilon$-$\delta$ 语言」

## 编译

```bash
cd extension
latexmk -xelatex main
```

首次编译会自动调用 biber 处理 `references.bib`。

## 结构

- `main.tex` — 入口，`\title`/`\author`/`\keywords` 与 `\tableofcontents`
- `references.bib` — 参考文献数据库
- `chapters/` — 每篇一个文件，文件名以序号开头（`01.tex`、`02.tex`）

新增一篇：在 `chapters/` 加文件，在 `main.tex` 里加一行 `\input{chapters/02}`。

## 写法约定

- 每篇都写 `\begin{abstract}...\end{abstract}` 与 `\keywords{}`；
- 定理类内容用 `theorem`/`lemma`/`proof`/`example` 环境（模板自带）；
- 引文用 `\cite{key}`，参考文献列表由 `\printbibliography` 自动生成；
- 不要重复设置字体与宏包，统一在 `../common/preamble.tex` 里改。
