# 数学教学文档

使用 ElegantLaTeX 系列模板（ElegantBook / ElegantNote / ElegantPaper）+ XeLaTeX。

## 一、文档体系

按「读者 × 完整度」分三层。**判断一份材料属于哪一类，看它回答什么问题。**

### 学生用（主线）

| 目录 | 类型 | 回答什么 | 篇幅 |
| --- | --- | --- | --- |
| `handout/` | 讲义 | **学什么**：概念、推导、例题、练习、小结，可脱离教师自学 | 每章 6～10 页 |
| `outline/` | 理论概要 | **有哪些**：只留定义、定理、公式的骨架，无例题 | 每章 1～2 页 |
| `notes/` | 笔记 | **我怎么记的**：课前中后四段留白，由学生自己写 | 每课 1～2 页 |
| `formula/` | 速查表 | **是什么**：只有结果，没有推导，考前 10 分钟用 | 每页 6～8 个专题 |
| `map/` | 知识图谱与结论卡片 | **什么关系、什么时候用**：结构图 + 一卡一结论 | 按主题 |
| `topic/` | 专题训练 | **怎么迁移**：跨课次，同一问题多角度反复处理 | 按专题 |
| `errorbook/` | 错题本 | **我错在哪**：错解 → 正解 → 变式 → 反思 | 按章节 |
| `guide/` | 导学案 | **做什么**：预习填空、课堂探究、当堂检测、课后作业 | 每课 2～4 页 |
| `extension/` | 拓展阅读 | **还有什么**：课后延伸，含摘要、关键词、参考文献 | 每篇 3～5 页 |
| `modeling/` | 建模活动单 | **怎么用数学解决真问题**：选模型 → 拟合 → 检验 → 预测 | 每个项目 |

### 测评

| 目录 | 类型 | 说明 |
| --- | --- | --- |
| `exam/` | 试卷 + 命题细目表 | `main.tex` 学生卷（A3 横版双栏）；`blueprint.tex` 细目表（教师用） |
| `bank/` | 题库 | 题源，题目用 `problem`，解答用 `solution`；`answer`/`noanswer` 双模式 |
| `answer/` | 答案与解析 | 与讲义、试卷、作业配套的详解册 |

### 教师用

| 目录 | 类型 | 说明 |
| --- | --- | --- |
| `lesson/` | 教案 | 教学目标、重难点、教学过程、板书、作业 |
| `reflection/` | 教学反思 | 达成情况 → 意外之处 → 下次调整，与课次号对应 |
| `slides/` | 课件 | Beamer + Metropolis，16:9 |

### 共享

| 目录 | 说明 |
| --- | --- |
| `common/preamble.tex` | 字体、数学宏包、版式、`\complement` 补丁 |
| `common/macros.tex` | 教案/导学案结构环境与常用命令 |
| `common/envs.tex` | 讲义/笔记/卡片/错题本/速查表/反思的盒子环境 |
| `figures/` | 封面与图片素材 |
| `manim/` | Manim CE 动画工程（按单元分目录），渲染走 `manim-video` skill 的 `manim-run.sh` |
| `sources/` | 外部提供的原始素材（`raw/` 逐字拷贝 + 章节索引），写正文时从这里取 |

## 二、子目录

| 目录 | 类型 | 模板 | 说明 |
| --- | --- | --- | --- |
| `handout/` | 讲义 | ElegantBook | 学生主材料，六段结构 |
| `outline/` | 理论概要 | ElegantNote | 骨架版，无例题 |
| `notes/` | 笔记 | ElegantNote | 四段留白 |
| `formula/` | 速查表 | extarticle + multicol | A4 横版三栏 |
| `map/` | 知识图谱与流程 | ElegantNote | 知识层次图、二级结论卡片、解题流程图 |
| `topic/` | 专题训练 | ElegantNote | 跨课次主题，螺旋式 |
| `errorbook/` | 错题本 | ElegantNote | 一题一条，四段订正 |
| `guide/` | 导学案（湘教版章节） | ElegantNote | 每课含预习、探究、检测、作业 |
| `hv-guide/` | 高观点系列导学案（第 0–9 章） | ElegantNote | 独立成册，编号 0–9 |
| `extension/` | 拓展阅读 | ElegantPaper | 课后延伸与深入 |
| `modeling/` | 建模活动单 | ElegantNote | 完整建模过程 |
| `exam/` | 试卷 | exam-zh | A3 横版双栏 + 密封线 |
| `bank/` | 题库（湘教版章节） | ElegantBook | 题目 + 答案双模式 |
| `hv-bank/` | 高观点系列题库（第 0–9 章） | ElegantBook | 独立成册，编号 0–9 |
| `answer/` | 答案与解析 | ElegantNote | 配套详解 |
| `lesson/` | 教案 | ElegantBook | 每章一课时 |
| `reflection/` | 教学反思 | ElegantNote | 与课次号对应 |
| `slides/` | 课件 | Beamer + Metropolis | 16:9 演示文稿 |

每个子目录都有自己的 `README.md`，说明该类型的写法与约定。

## 三、快速开始

```bash
cd handout       # 或 outline / notes / formula / errorbook / reflection / answer
latexmk -xelatex main

cd exam
latexmk -xelatex main        # 学生卷
latexmk -xelatex blueprint   # 细目表
```

## 四、约定

- 每个 `chapters/` 目录存放按课时/章节拆分的 `.tex`，文件名以序号开头（`01.tex`、`02.tex`）。
- 新课时：在 `chapters/` 新增文件，并在 `main.tex` 中 `\input` 一行。
- 图片统一放 `figures/`，在 `main.tex` 中用 `\graphicspath{{../figures/}}` 引入。
- 中文字体与数学字体已在 `common/preamble.tex` 中统一配置，不要在单个文件里重复设置。
- **新增文档类时，先看 `common/envs.tex` 里有没有现成的环境**，再自己造盒子。
- `extension/` 的编号与 `lesson/` 的课次号对应；教案与导学案的作业环节用 `\reading{编号}{篇名}` 指向对应篇目。
- 讲义改动练习后，同步更新 `answer/` 对应小节。

## 五、高观点章节系列

一套独立的「结构主义」升级系列，**单独成册**（`hv-guide/` 与 `hv-bank/`，不与 `guide/`、`bank/` 混排，
编号自成体系 0–9）。素材来自 `sources/`。已完成/进行中：

| 章 | 主题 | 导学案 | 题库 | 动画 |
| --- | --- | --- | --- | --- |
| 第 0 章 | 集合、逻辑演算与证明武器库（总纲） | `hv-guide/chapters/00.tex` ✅ | `hv-bank/chapters/00.tex` ✅ | `manim/logic-weapons/` ✅ |
| 第 1 章 | 函数的概念与基本初等函数 | `hv-guide/chapters/01.tex` ✅（含前置引入「舞台的诞生」+ 收官专题「函数与图形变换完全图谱」） | `hv-bank/chapters/01.tex` ✅ | `manim/real-line-genesis/` ✅ + `manim/function-evolution/` ✅ + `manim/function-transform/` ✅ + `slides/outline-function.md` |
| 第 2 章 | 三角函数、解三角形与复平面旋转 | `hv-guide/chapters/02.tex` ✅ | `hv-bank/chapters/02.tex` ✅ | `manim/euler-rotation/` ✅ |
| 第 3 章 | 平面向量与空间向量 | `hv-guide/chapters/03.tex` ✅ | `hv-bank/chapters/03.tex` ✅ | `manim/vector-space/` ✅ |
| 第 4 章 | 立体几何与圆锥曲线大一统 | `hv-guide/chapters/04.tex` ✅ | `hv-bank/chapters/04.tex` ✅ | `manim/affine-conics/` ✅ + `manim/affine-rotation/` ✅ |
| 第 5 章 | 数列与离散动态系统 | `hv-guide/chapters/05.tex` ✅ | `hv-bank/chapters/05.tex` ✅ | `manim/sequence-dynamics/` ✅ |
| 第 6 章 | 导数与局部线性化引擎 | `hv-guide/chapters/06.tex` ✅ | `hv-bank/chapters/06.tex` ✅ | `manim/local-linearization/` ✅ |
| 第 7 章 | 计数原理、概率空间与统计回归 | `hv-guide/chapters/07.tex` ✅ | `hv-bank/chapters/07.tex` ✅ | `manim/probability-ls/` ✅ |
| 第 8 章 | 齐次化：把二元问题压成一元比例 | `hv-guide/chapters/08_homogenization.tex` ✅ | `hv-bank/chapters/08.tex` ✅（8 题） | `manim/homogenization/` ✅ + `slides/outline-homogenization.md` |
| 第 9 章 | 不动点：迭代、方程与几何变换的交汇 | `hv-guide/chapters/09_fixed_point.tex` ✅ | `hv-bank/chapters/09.tex` ✅（8 题） | `manim/fixed-point/` ✅ + `slides/outline-fixed-point.md` |

全部完成：`hv-guide` 117 页（教师版；学生版 95）、含跨章联动、附录 A 考纲合法化转译手册、附录 B 强基衔接桥、第 0 章四视角等价地图与全书知识脉络图、各章「多框架对读」卡；`hv-bank` 54 页，均 0 error。

每章三件套：**导学案**（guide，含学生版留白与教师版解析）、**分层题库**（bank，每题三板块解析）、
**Manim 动画**（manim/<单元>/）。第 1 章额外有一份 45 分钟 PPT 逐页大纲（`slides/outline-*.md`）。

## 六、依赖

- TeX Live 2026（本机 `/usr/local/texlive/2026`），XeLaTeX；
- `exam-zh` 与 `asana-math`（`sudo tlmgr install asana-math`）；
- 中文字体 Noto Serif/Sans CJK（系统已装）；
- Manim：`~/Downloads/manim-env`（0.22.1）或 `~/Downloads/manim-env-021`（0.21.0），
  渲染见 `manim/README.md`（**必须**用 TeX Live 自带的 dvisvgm）。
