# 高观点系列导学案（第 0 章 — 第 9 章）

> 架构与规范的**唯一权威**见 `ARCHITECTURE.md`；本 README 只讲日常用法。

独立成册，编号 0–9，不与 `../guide/`（湘教版章节）混排。文档类 `elegantnote`，XeLaTeX 编译。

## 结构

```
versions.tex                % 四合一多版本引擎（开关、\tk、\vchoice、盒子、计数器）
main.tex                    % 薄包装：\input{versions} + 版本面板 + \input{main_body}
main_body.tex               % 封面 + 目录 + chapters/*.tex + 附录
chapters/00.tex             % 第 0 章 集合、逻辑演算与证明武器库（总纲）
chapters/01.tex             % 第 1 章 函数的概念与基本初等函数（高观点结构版）
chapters/02.tex             % 第 2 章 三角函数、解三角形与复平面旋转（高观点统一版）
chapters/03.tex  …          % 第 3–7 章
chapters/08_homogenization.tex % 第 8 章 齐次化：把二元问题压成一元比例（小节已编号进目录）
chapters/09_fixed_point.tex  % 第 9 章 不动点：迭代、方程与几何变换的交汇
chapters/appA_legalization.tex / appB_honors_bridge.tex % 附录 A/B
```

`main_body.tex` 里 `\setcounter{section}{-1}`，使第一个 `\section` 编号为 0（第 0 章是总纲）。
加新章：在 `chapters/` 建 `NN*.tex`，再在 `main_body.tex` 末尾加一行 `\input{chapters/NN}`。

## 每章写法

沿用 `common/` 里的环境，不要自造盒子：

- 结构：`learnobjective` / `preview`（知识回顾 + 教材速读）/ `explore`（`\key{探究N：…}`）
  / `inclasstest` / `afterclass`
- 题目：`example` / `problem` / `solution`
- 行内：`\key{…}`、`\blank`、`\level{易|中|难}`
- 盒子：`derivation` / `summary` / `commonerror{名称}` / `method` / `conccard{结论}{适用条件}{易错点}`；多版本引擎另给 `corebox` / `methodbox{标题}` / `trapbox` / `warmupbox{标题}`
- 图：`figure` + `tikzpicture`（TikZ 原生绘制，禁止外部图片）
- 答案：`\tk{…}` 内部按数学模式书写（写 $\frac12$ 之类要套 `$…$`），教师版红色下划线、学生版留白
- 母题：`\begin{masterq}{标题}` + `enumerate[label=(\arabic*)]` 写七问，每问末 `\logotag{类别}`；
  七问固定顺序与功能见 `ARCHITECTURE.md` 第 7 节

## 编译

```bash
latexmk -xelatex main          # 默认母版：完整教师版
python3 build_all.py           # 一键导出四种版本到 dist/
python3 build_all.py --demo    # 额外导出一份挂载示范章节的版本
```

## 四合一多版本（同源四版本切换）

`versions.tex` 提供两个正交布尔开关，改 `main.tex` 顶部「版本切换面板」的两行即可：

| 开关组合 | 成品 |
|---|---|
| `\teachertrue` + `\basicfalse` | ① 完整教师版（全套推导、接口、双解与解析）★默认母版 |
| `\teacherfalse` + `\basicfalse` | ② 完整学生版（隐藏解析与填空答案） |
| `\teachertrue` + `\basictrue` | ③ 薄弱生教师版（大白话口诀 + 脚手架 + 完整答案） |
| `\teacherfalse` + `\basictrue` | ④ 薄弱生学生版（保留 `\tk{}` 留白横线） |

配套宏与环境（用法见 `chapters/demo_multiversion.tex`）：

- `advancedonly`：仅完整版渲染；薄弱生版彻底忽略不占位（莫比乌斯矩阵、射影同构、压轴第 3–4 阶梯）。
- `basiconly`：仅薄弱生版渲染（课前计算过关、大白话口诀、半成品步步填空）。
- `\tk{答案}`：教师版红色下划线答案；学生版等宽下划线留白。
- `\vchoice{完整版文本}{薄弱生大白话文本}`：同一句子里的措辞切换。
- `solution`：教师版渲染带边框【剖析与标准解答】；学生版隐藏只留书写空白。
- 盒子：`corebox` / `methodbox` / `trapbox` / `warmupbox`；例题、练习按节自动编号。


## 约定

- 全程中文，面向高中生但保持学术严谨；多用启发式追问。
- 每章至少 2 个 `conccard`、1 个 `commonerror`、1 个 `method`，含当堂检测 4 题与分层作业（教师版答案）。
- 素材取自 `../sources/raw/`，落笔前读原文，不要凭记忆复述。
