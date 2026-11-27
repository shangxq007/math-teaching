# hv-guide 架构与规范（唯一权威）

> 本文件是《高观点》导学案分册 `hv-guide/` 的权威架构说明。
> 任何历史提示词、口头约定与本文件冲突时，**以本文件为准**；
> 需要改动结构或规范时，先改本文件，再改代码。
> 生效日期：2026-11-24。

## 1. 定位

- 册名：高观点系列导学案（第 0 章 — 第 9 章 + 附录 A/B），编号自成体系，
  不与 `../guide/`（章节）混排。
- 文档类：`elegantnote`（选项 `cn,11pt,color=cyan,math=newtx,normal`），XeLaTeX。
- 输出形态：同源四版本（教师/学生 × 完整/薄弱生），单源维护，无副本漂移。

## 2. 现行拓扑

| 路径 | 职责 | 备注 |
|---|---|---|
| `main.tex` | 薄壳：文档类 + `\input{../common/{preamble,macros,envs}}` + `\input{versions}` + 版本面板两行开关 + `\input{main_body}` | 只改「版本面板」两行即可切换导出 |
| `main_body.tex` | 封面 + 目录 + `\input{chapters/*}` + 附录装配 | `\setcounter{section}{-1}` 使首章编号为 0 |
| `chapters/*.tex` | 各章源文件（00–09、appA/appB、demo_multiversion） | 加新章 = 建文件 + 在 main_body 加一行 |
| `chapters/drill_master_chNN.tex` | 各章 drill：结构雷达闪电战（6 题）＋两道五问连环母题＋notezone 归档 | 挂载在对应 `chapters/NN` 之后；编写规范见 skill `hv-guide-drill-authoring`；「五问」与正文七问 masterq 的分工见 §7 |
| `../extension/` | 拓展阅读实体分册（`\reading{}{}` 指向处） | 各章末尾用 `\reading{拓展阅读 NN}{标题}` 挂指引行；全局编号注册表见 `../extension/README.md` |
| `versions.tex` | 四版本引擎：布尔开关、`\tk{}`、`\vchoice{}{}`、`advancedonly`/`basiconly`、盒子、计数器、`solution` 重定义、`masterq` 母题环境 | 所有「版本感知」环境唯一定义处 |
| `../common/preamble.tex`、`macros.tex`、`envs.tex` | 数学组共享宏包与宏 | **不属于本分册**，不得复制进分册 |

依赖方向：`common/ → versions.tex → chapters/*.tex → main_body.tex → main.tex`。
禁止反向依赖（如 common 里引用 versions 的宏）。

## 3. 编译

```bash
latexmk -xelatex main.tex        # 默认母版（完整教师版），产物 main.pdf
python3 build_all.py             # 四版本全部重编，产物在 dist/
python3 build_all.py --demo      # 额外出一份挂载示范章节的版本
python3 build_all.py --only student_basic   # 只编指定版本
```

- 编译器：TeX Live 2026 的 `xelatex`；中文字体走 FandolSong，数学走 newtx。
- `build_all.py` 为每个版本生成极薄包装 `_variant_<tag>.tex`（仅导言区 + 两行开关 +
  `\input{main_body}`），再以 `-jobname=hvguide_<tag>` 编译并拷入 `dist/`。
- `_variant_*.tex`、`hvguide_*` 均为生成物，已在 `../../.gitignore` 中忽略。

## 4. 版本开关语义

| 开关组合 | 成品 | `\tk{}` | `solution` | `advancedonly` | `basiconly` |
|---|---|---|---|---|---|
| `\teachertrue \basicfalse` | ① 完整教师版（默认母版） | 红色答案 | 带边框剖析 | 渲染 | 忽略 |
| `\teacherfalse \basicfalse` | ② 完整学生版 | 留白横线 | 隐藏 | 渲染 | 忽略 |
| `\teachertrue \basictrue` | ③ 薄弱生教师版 | 红色答案 | 带边框剖析 | 忽略 | 渲染 |
| `\teacherfalse \basictrue` | ④ 薄弱生学生版 | 留白横线 | 隐藏 | 忽略 | 渲染 |

另有 `\ifdemomode`：置真时 `main_body.tex` 挂载 `chapters/demo_multiversion.tex`。

## 5. 环境归属规则（防漂移）

- 凡「版本感知」环境一律定义在 `versions.tex`：
  `\tk{}`、`\vchoice{}{}`、`advancedonly`、`basiconly`、
  `corebox` / `methodbox` / `trapbox` / `warmupbox`、
  `hvexample` / `hvexercise` / `hvmasterq`、`\logotag`、`solution` 重定义。
- 只属于静态排版的通用环境放 `common/envs.tex`，全组共享。
- **禁止在任何 `chapters/*.tex` 内 `\newcommand` / `\newenvironment` 重定义上述名称**；
  新增版本相关环境必须先进 `versions.tex`。
- 2026-11-24 核对：无重复定义，无跨层反向依赖。

## 6. 与旧规格提示词的差异裁决

以下条目自本文件生效起不再是验收依据，历史对话中的旧描述一律作废：

| 旧条目 | 实际实现 | 裁决 |
|---|---|---|
| 每册自建 `preamble.sty` 供 include | 共享 `../common/preamble.tex` + 分册 `versions.tex` 两层 | 旧条目作废；分册不得自建 preamble，避免宏包重复加载 |
| `ctexbook` + `fontspec` 手工配中文字体 | `elegantnote[cn]`，字体由文档类统一提供 | 旧条目作废；中文/数学字体一律走文档类选项 |
| 多文件各自维护、靠复制同步版本 | `main_body.tex` + `chapters/` 单源 + `build_all.py` 生成包装 | 维持单源；包装文件只由脚本生成，不手改 |
| 「一套环境全册通用、各册另造盒子」 | 版本环境集中在 `versions.tex`，静态环境集中在 `common/` | 以本文件第 5 节为准 |

## 7. 内容写作规范：七问连环母题（Scaffolded Master Problem）

一道母题挂载 7 个递进小问；学生在留白处写下的推理过程，本身就是这一章的笔记。

工程接口（定义于 `versions.tex`）：

```latex
\refstepcounter{hvmasterq}   % 每道母题前手动步进（勿写进 masterq 定义内）
\begin{masterq}{母题标题}
\begin{enumerate}[label=(\arabic*)]
\item ... \logotag{存档类别}
...
\end{enumerate}
\end{masterq}
```

七问固定顺序与功能（顺序即写作顺序，不得调换）：

| 问 | 名称 | 训练功能 | 典型归档标签 |
|---|---|---|---|
| (1) | 画图与数值感知 | 概念引入，先算具体值再描点 | 核心公理 |
| (2) | 多视角结构翻译 | 集合语言 / 几何图形 / 代数恒等式互译 | 结构翻译 |
| (3) | 考纲规范通法 | 考场可写的标准推导（`\tk{}` 搭骨架） | 考纲通法 |
| (4) | 高观点降维秒杀 | 大招公式、齐次化、射影等二级结论 | 大招公式 |
| (5) | 公式变形家族生成 | 推广成族，一张表覆盖一类题 | 公式族 |
| (6) | 参数变式与逆向追问 | 反求参数、充要边界 | 充要边界 |
| (7) | 边界陷阱与错题排雷 | 错题本与避坑铁律 | 避坑铁律 |

落地情况：`chapters/08_homogenization.tex` 第 5 节已有两道母题
（线性约束 `x+y=1`；二次约束 `x^2+y^2=1`）。后续新增章节按此模板补母题，
并在本章末 `notezone` 给出「七问 ↔ 笔记功能」对应表。

**专题章骨架豁免（第 8、9 章）**：这两章是「二级结论／方法链」专题，
采用编号小节（`subsection{第 N 节 …}`）＋ `methodbox`/`corebox`/`warmupbox`
＋ 章内七问母题的体例，**不要求** `learnobjective/preview/explore/inclasstest/
afterclass` 全套骨架；其课后练习功能由独立 drill 模块
`chapters/drill_master_ch08.tex`、`chapters/drill_master_ch09.tex` 承载
（结构雷达闪电战 6 题＋两道五问连环母题＋notezone）。第 0–7 章仍按标准骨架执行。
新增专题章若沿用此豁免，必须在本段登记并同步挂载对应 drill。

drill 的「五问」与正文七问 masterq 的分工（避免同册混淆）：drill 的两道连环母题为
考纲五问版——(1) 具象感知、(2) 考纲通法、(3) 高观点降维、(4) 结构推广、
(5) 易错排雷，不重列七问中的「多视角翻译」「公式族全表」，这两类由正文
masterq 承担；drill 标题写「五问连环母题」，正文标题写「七问连环母题」，不得混用。

第 8 章特有的版本互换：其第 3 节按版本二选一——完整/教师版为 advancedonly
「射影桥梁」，薄弱生版为 basiconly 同名「大白话版」。因此手动小节编号必须随版本
写对（薄弱生版末节为「第 6 节」，教师版为「第 5 节」），跨节指针一律用 `\vchoice`
给出两版措辞，禁止只写「见第 3 节」而假定内容相同。

## 8. 变更流程

1. 改内容 → `chapters/*.tex`；改装配 → `main_body.tex`；改版本行为 → `versions.tex`。
2. 改本规范 → 先改本文件，再动代码。
3. 完成前必须跑 `python3 build_all.py`，四个版本全部 0 error 才算通过。

## 9. 内容归属与去重规范

多次增补后同一内容可能在多章复述。以下为**唯一落点（home）**，
其它章节只能「引用 + 一句结论」，禁止整段重推：

| 主题 | 唯一落点 | 其它章节的合法用法 |
|---|---|---|
| 齐次化完整方法链（次数扫描、同除降维、四把手术刀、七问母题） | 第 8 章 | 第 6 章只作条件最值入口并注明「详见第 8 章」 |
| Möbius 矩阵／特征方向 $=$ 分式不动点 | 第 5 章探究三（含图 `fig:eigen-fixed`） | 第 8 章 §3 只引用动机，不重推 |
| 空间向量方向向量／法向量判据与三个高频失误 | 第 3 章 | 第 4 章只调用，另补点面距应用 |
| 平移消常数、旋转消交叉项的一般理论 | 第 5 章「跨章方法论大一统」 | 第 8 章「手术刀之二」标注出处 |
| 仿射变换、Dandelin 截面 | 第 4 章 | 他处只引用 |
| 「1 的代换」入口 | 第 6 章动作一 | 第 8 章为展开，双向互相注明 |
| 不动点统一理论（离散递推、连续 $f(x)=x$、几何变换、Möbius 射影） | 第 9 章 | 第 5 章只留数列应用与矩阵推导，其余章节引用 |
| 旋转消交叉项：一般公式 | 第 8 章「手术刀之五」 | 完整例子、图与数列复特征值应用在第 5 章 |

配套约束：

- 跨章复述必须写「见第 X 章」，否则视为重复讲授。
- 章内同一结论只保留一处主推导；例题可以同型，但题目骨架与答案
  不得逐字相同（当堂检测尤其要避免与母题/作业重复）。
- 审计留档（2026-11-25）：`AUDIT_跨章重复清单.md`、
  `_audit_structure_report.md`。新增内容前先对照上表与两份清单。
- 章内小节一律用 `\subsection`（带编号、进目录）；不得用
  `\subsection*`，否则该章在目录中只剩章标题（第 8 章曾犯，已修）。
- 全书元原则「四视角等价」：代数／几何／集合／映射是同一对象的四种表示，
  彼此以「保持结构的映射（同构）」相连；同一问题在不同框架下难度不同，
  解题即找同构把问题搬到顺手一侧。第 0 章新增「四视角等价地图」
  （`fig:four-view-map`）为总纲；各章章首统一附「多框架对读」卡
  （视角 × 看点 × 换框架说法 × 哪侧省力），已覆盖第 0–9 章；
  同处另配「全书知识脉络图」（`fig:book-map`）：三条主线
  （几何·结构／离散动力／连续分析）＋独立概率统计线，接口含
  差分↔导数、齐次化→射影、不动点汇合。
