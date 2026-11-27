# 数学拓展阅读

用 ElegantPaper 模板写的课后延伸阅读，供学有余力的学生自学。

与另外三个文档的区别：

| 文档 | 模板 | 读者 |
| --- | --- | --- |
| 教案 | ElegantBook | 教师 |
| 题库 | ElegantBook | 师生 |
| 导学案 | ElegantNote | 学生（课前/课中） |
| 拓展阅读 | ElegantPaper | 学生（课后自学） |

## 编号注册表

拓展阅读的编号是**全局连续编号**，与课次解耦：
01–06 段恰好与 `../lesson/chapters/` 的课次号一致；00 为全书总序篇；
07 段及以后分配给高观点系列（`hv-guide/`）各章。新增篇目一律顺延取号，不得复用。

| 编号 | 篇名 | 引用出处 | 状态 |
| --- | --- | --- | --- |
| 00 | 逻辑与证明的武器库 | hv-guide 第 0 章 | 待补 |
| 01 | 集合之美 | guide/lesson/handout 第 1 课（章） | **已成篇**（`chapters/01.tex`） |
| 02–04 | （预留，暂未指派） | — | 待补 |
| 05 | 函数与模型 | guide 第 3 章 | 待补 |
| 06 | 三角与周期 | guide 第 4 章 | 待补 |
| 07 | 函数的结构特化 | hv-guide 第 1 章 | 待补 |
| 08 | 复数与三角的大一统 | hv-guide 第 2 章 | 待补 |
| 09 | 向量：几何空间的通用线性语言 | hv-guide 第 3 章 | 待补 |
| 10 | 圆锥曲线：同一个三维对象的三种截面 | hv-guide 第 4 章 | 待补 |
| 11 | 数列：离散动力系统的轨迹 | hv-guide 第 5 章 | 待补 |
| 12 | 导数：以直代曲的局部线性化 | hv-guide 第 6 章 | 待补 |
| 13 | 概率：从计数测度到样本空间 | hv-guide 第 7 章 | 待补 |
| 14 | 齐次化：比例结构与射影桥梁 | hv-guide 第 8 章 | 待补 |
| 15 | 不动点：从迭代到流场 | hv-guide 第 9 章 | 待补 |

新增一篇时：文件名沿用编号，在篇首写一行
`\corresponding{来源章/课《标题》}`，并更新上表与状态。

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
