# 右侧栏滚动交互方案

> 2026-11-01 · CourseMap V3

## 问题

学习页右侧栏被「原文字幕」的自动滚动锁死，用户无法自由查看下方的时间轴和笔记区域。

## 方案对比

| 方案 | 描述 | 优劣 |
|------|------|------|
| A. 定时自动恢复 | 用户停止滚动 5 秒后自动回到当前播放位置 | 5 秒可能打断阅读；突然跳转体验差 |
| **B. 手动回位按钮** | 用户滚动后显示「↩ 回到当前」浮动按钮，点击才回位 | 用户完全掌控；Slack/YouTube 评论区主流做法 |

## 选定方案：B

### 交互逻辑

1. **右侧栏整体可滚动**：移除字幕区固定高度，`.side.right` 作为唯一滚动容器
2. **字幕高亮照常更新**：视频播放时，当前行的 `.current` 样式实时变化，但不强制滚动
3. **用户滚动后**：显示右下角浮动按钮「↩ 回到当前」
4. **点击按钮**：平滑滚动到当前字幕行位置，按钮消失
5. **seekTo 跳转时**：自动滚动到对应位置（用户主动跳转，预期行为）

### 行业参考

- Slack：新消息提示「↑ 跳转到最新」
- YouTube 评论区：「↑ 最新」浮动按钮
- 终端 `less`：无自动恢复，用户完全控制

### CSS 改动

- `.side.right` → `overflow-y: auto`
- `.transcript-sidebar` → 去掉固定高度 `height: calc(38vh + 50px)` 和 flex 布局
- `.transcript-scroll` → 去掉 `overflow-y: auto; flex: 1`

### JS 改动

- 监听 `.side.right` 的 `wheel` / `touchmove` 事件，设置 `userHasScrolled = true`
- `timeupdate` 中只更新高亮样式，不调用 `scrollIntoView`
- 用户滚动后显示浮动按钮
- 点击按钮调用 `scrollToCurrentLine()`，滚动到 `.current` 行，隐藏按钮
- `seekTo()` 中保留 `scrollIntoView`（主动跳转场景）
