# 视频 ↔ 教案差异总清单（26 个 Manim 视频 × hv-guide）

> 本文件是索引与汇总；逐单元细节见四个分片：
> - `video_lesson_diff_fragment.md`（logic-weapons / real-line-genesis / function-evolution ↔ 第 0/1 章）
> - `VIDEO_GUIDE_DIFF.md`（euler-rotation / vector-space ↔ 第 2/3 章）
> - `video_guide_diff.md`（affine-conics / affine-rotation / function-transform ↔ 第 4/8/1 章）
> - `video_lesson_diff_05-07.md`（sequence-dynamics / local-linearization / probability-ls ↔ 第 5/6/7 章）
>
> 调研时间：2026-11-25。只做对照，未改动任何 .tex。补图必须在治理完结构问题后按本清单执行。
>
> 当前基线（2026-11-25 晚）：`build_all.py` 四版本全绿——教师版 111／学生版 90／
> 薄弱生教师版 110／薄弱生学生版 89，0 error；新增第 9 章「不动点」与第 8 章
> 「手术刀之五」后已重新核对。

## 1. 覆盖总览

| 单元（视频数） | 对应章节 | 覆盖度 | 主要缺口 |
|---|---|---|---|
| logic-weapons（2） | 第 0 章 | 高 | 反证法只画结论态，缺「反设态」红月牙图 |
| real-line-genesis（1） | 第 1 章前置 | 中 | 弹珠袋、Lv.2 数轴、R² 平面无图 |
| function-evolution（3） | 第 1 章 | 中 | 图像线（散点→竖截→每列一点→曲线）全程无图；`fig:grid9` 名不副实 |
| euler-rotation（3） | 第 2 章 | 高 | 缺「α 加转 β」叠加图、乘 i 分量倒置图 |
| vector-space（5） | 第 3 章 | 中 | 缺二面角几何图；换基底相似律 A′=P⁻¹AP、镜面反射 a′=2proj−a 两整块缺失 |
| affine-conics（2） | 第 4 章 | 完全 | 仅参数取值不同 |
| affine-rotation（1） | 第 5/8 章 | 错位 | 旋转消交叉项只在第 5 章（有图）；第 8 章零覆盖；复特征值螺旋无图 |
| function-transform（4） | 第 1 章 | 三缺一 | 主被动对偶无专节；平方算子只有表格一行 |
| sequence-dynamics（3） | 第 5 章 | 切片 | 视频数据与教案不一致；且视频脚本本身有错（见 §2） |
| local-linearization（2） | 第 6 章 | 切片 | 半圆已覆盖；切线放缩缺 ln x 镜像幕（见 §2） |
| probability-ls（1） | 第 7 章 | 切片 | 最小二乘已覆盖；条件概率第二幕分子硬编码 5 |

结论：**不是「视频内容普遍没进教案」，而是若干具体缺口 + 少数归属错误 + 1 处视频自身数学错误。**

## 2. 已核实的问题（不含补图）

1. **视频脚本数学错误**：`manim/sequence-dynamics/scene2_fixed_point_compare.py`
   左图 `f(x)=0.5x+1` 的真不动点是 `x*=2`，原脚本 `XSTAR=1.0`、标题/结语全按 1 处理。
   **已修（2026-11-25）**：左图改 `XSTAR_L=2.0`，右图 `XSTAR_R=1.0` 保持；标题改为
   「左 x\*=2 压缩型 vs 右 x\*=1 扩张型」，docstring/字幕同步；已 `-ql` 重渲并通过 SVG 自检。
2. **教案图文不符**：`chapters/06.tex` 正文说图 `fig:tangent-exp` 同时说明 `e^x` 与 `ln x`，
   实际只有 `e^x`；`ln x` 的镜像幕只存在于视频。**待办**（补图或改措辞）。
3. **引用错位**：`appB_honors_bridge.tex` 两处、`chapters/04.tex` 两处失准引用。
   **已修**（2026-11-25）。
4. **数据各自为政**：蛛网不动点（视频 2/1 vs 教案 4/2）、特征矩阵、半圆尺寸、
   最小二乘数据集（视频 8 点 vs 第 7 章 5 点）不一致——**待决策**（建议统一到教案数值或明确标注「示意取值」）。
5. **术语冲突**：视频把一维斜率 λ=f′(x\*) 叫「特征方向」，教案该词专指特征向量方向。
   **已随第 9 章建立统一定位**：第 9 章 §1 用斜率判据，矩阵特征方向归第 5 章/第 9 章 §4。
6. **视频硬编码**：`probability-ls/scene1_least_squares.py` 第二幕分子硬编码 5。
   **已修**：改为 `n_b=min(5,len(inner))` 并加断言；已 `-ql` 重渲。
7. 其他已记录待核验项（概率测度比与有限样本频率混同、采样框窄于 Ω、残差方块缩放视觉差等）见各分片，暂列观察。

## 3. 补图优先级（结构治理完成后执行）

已完成（2026-11-25，均原生 TikZ，主版本 0 error）：
- ① 第 1 章图像线四联图 `fig:orderline`
- ② 第 3 章二面角几何图 `fig:dihedral-angle`（含直角符号与跨棱 θ 弧）
- ③ 第 5 章复特征值螺线图 `fig:spiral-complex`
- ④ 第 0 章反证法反设态图 `fig:contradiction-assumption`
- ⑤ 第 1 章 Lv.1→Lv.2 双联图 `fig:bag2axis`、R² 定场图 `fig:r2plane`
- ⑥ 第 1 章主被动对偶（方法框＋图 `fig:activepassive`，已修标签拥挤）
- ⑦ 第 1 章指对互逆图 `fig:expinvlog`
- ⑧ 第 2 章旋转叠加图 `fig:rotate-sum`、乘 i 分量倒置图 `fig:i-component-flip`（已修 α/β/α+β 标注层叠）

同步入正文的超纲块（advancedonly，仅完整版渲染）：
- 第 3 章「换基底与相似律 A′=P⁻¹AP」「镜面反射 a′=2proj−a」；
- 第 1 章主被动对偶；第 8 章「手术刀之五 旋转消交叉项」（公式入第 8 章，实例仍在第 5 章）。

仍待做：低优先级 ⑨ 修 `fig:grid9` caption（已改为与实际一致，待核）；
⑩ R² 之外的其余小图按需。**新增第 9 章「不动点」**（用户批准，已建 `chapters/09_fixed_point.tex`）。

## 4. 待决策项

- 数据不一致（视频 vs 教案）：统一到教案数值，还是明确标注「示意取值」。
- 第 6 章 `fig:tangent-exp` 是否补 `ln x` 镜像幕，或把正文措辞改为只讲 `e^x`。
- 视频侧其余观察项（概率测度比、采样框、残差方块视觉缩放）是否本轮一并修。
