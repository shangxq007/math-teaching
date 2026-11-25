# 函数的概念与结构演化 · Manim 动画

配套 `../../hv-guide/chapters/01.tex`（高观点导学案）与 `../../slides/outline-function.md`（PPT 大纲）。

## 场景

| 文件 | 场景类 | 内容 | 草稿时长 |
| --- | --- | --- | --- |
| `scene1_concept.py` | `FunctionConceptEvolution` | 六幕：离散三视角 → 单值性筛选 → 连续区间黑块 → 垂线过滤 → 解析式吸附 → 点集交集求解 | ~31 s |
| `scene2_explog.py` | `ExpLogSetSymmetry` | 指数曲线关键点 → 对称轴 \(y=x\) → 点 \((x,y)\) 翻转到 \((y,x)\) → 连成对数曲线 | ~22 s |

## 渲染

```bash
cd manim/function-evolution
export MANIM_BIN=~/Downloads/manim-env/bin/manim
sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh -qh scene1_concept.py FunctionConceptEvolution
sh ~/.hermes/skills/creative/manim-video/scripts/manim-run.sh -qh scene2_explog.py ExpLogSetSymmetry
```

成品在 `media/videos/<脚本名>/1080p60/`。

## 六幕与 PPT 时间轴的对应

| 幕 | 内容 | 插在 |
| --- | --- | --- |
| 1 | 离散三视角（数对 / 箭头 / 坐标点） | 导入与建构 0–5 min |
| 2 | 单值性筛选（一对多非法 vs 唯一对应） | 导入与建构 5–10 min |
| 3 | 连续区间推广，混沌黑块 | 泛化与痛点 10–14 min |
| 4 | 垂线过滤为一般函数 | 层层特化 18–22 min |
| 5 | 解析式吸附为光滑曲线 | 层层特化 22–28 min |
| 6 | 点集交集即方程的解 | 大一统实战 32–37 min |
| 场景 2 全程 | 指数↔对数的点集互换 | 大一统实战 37–41 min |
