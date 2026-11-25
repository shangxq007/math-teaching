# 小工具

- `make_cover.py`：生成低多边形山峦封面横幅（3:1），一次输出三张，配色对应三个主题：
  `cover_blue.png`（教案／ElegantBook blue）、`cover_green.png`（题库／green）、
  `cover_cyan.png`（导学案／ElegantNote cyan）。各册封面统一由它产出，不手改图片。

用法（在 `tools/` 下）：

```bash
python3 make_cover.py            # 默认输出到 ../figures/
python3 make_cover.py <输出目录>
```
