# 教学反思

教师课后写。一课时一条，三段固定：**达成情况 → 意外之处 → 下次调整**。

## 定位与分工

| 文档 | 时间 | 内容 |
| --- | --- | --- |
| 教案 `../lesson/` | 课前 | 打算怎么教 |
| **教学反思（本目录）** | **课后** | **实际发生了什么、下次改什么** |
| 课件 `../slides/` | 课中 | 课堂上展示什么 |

## 结构

每课时三段，都用 `teachreflect` 环境（`../common/envs.tex`）：

```latex
\section{第 N 次课：课题}

\begin{teachreflect}{达成情况}
...
\end{teachreflect}

\begin{teachreflect}{意外之处}
...
\end{teachreflect}

\begin{teachreflect}{下次调整}
...
\end{teachreflect}
```

## 三条原则

- **写具体行为，不写形容词**。「约一半学生仍停留在背结论」可以，「效果一般」不行；
- **意外之处只记真正意外的**，没意外就写「无」，不要凑；
- **下次调整必须可执行**，且尽量只改一两条，改太多等于没改。

## 编译

```bash
cd reflection
latexmk -xelatex -g main
```

## 文件

```
main.tex            导言区 + 封面
chapters/01.tex     第 1 次课
chapters/README.md
```
