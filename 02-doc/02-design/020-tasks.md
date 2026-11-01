# 开发任务清单 —— CourseMap 课程知识时间轴

> 基于 `010-prd.md` 拆解，按开发阶段组织。每个任务含完成标准，完成后勾选。

---

## Phase 1：数据流 + 交互闭环（不接 AI）

**目标**：用人工构造的 course.json 跑通前端交互，验证核心体验。

### 1.1 项目初始化

- [ ] **T-001** 初始化 Next.js 项目
  - 完成标准：`npx create-next-app@latest` 创建项目，TypeScript + Tailwind + App Router
  - 目录：`06-src/`
  - 验证：`npm run dev` 可启动，访问 localhost:3000 显示默认页

- [ ] **T-002** 安装依赖
  - 完成标准：安装 better-sqlite3、uuid、zod
  - 命令：`npm install better-sqlite3 uuid zod`
  - 验证：`package.json` 中包含上述依赖

- [ ] **T-003** 创建数据目录结构
  - 完成标准：创建 `coursemap-data/courses/` 目录
  - 验证：目录存在，可写入文件

### 1.2 数据库

- [ ] **T-004** 初始化 SQLite 数据库
  - 完成标准：创建 `coursemap-data/coursemap.db`，包含 courses / user_notes / ai_processing_jobs 三张表
  - 文件：`06-src/lib/db.ts`
  - 验证：运行初始化脚本后，`sqlite3 coursemap.db ".tables"` 显示三张表

- [ ] **T-005** 实现数据库 CRUD 封装
  - 完成标准：封装 courses / notes / jobs 的增删改查方法
  - 文件：`06-src/lib/db-courses.ts`、`06-src/lib/db-notes.ts`、`06-src/lib/db-jobs.ts`
  - 验证：单元测试覆盖所有方法

### 1.3 Transcript 处理

- [ ] **T-006** 实现 Transcript 标准化
  - 完成标准：读取 Whisper JSON → 统一格式（id/start/end/text），过滤空 segment，合并 <1s 短 segment
  - 文件：`06-src/lib/transcript-normalizer.ts`
  - 输入示例：Whisper 原始 JSON（多种格式兼容）
  - 输出示例：标准化 transcript_segments 数组
  - 验证：用真实 Whisper JSON 测试，输出格式正确

- [ ] **T-007** 实现 Transcript 存储
  - 完成标准：标准化后的 transcript 写入 `coursemap-data/courses/{id}/transcript.json`
  - 文件：`06-src/lib/transcript-store.ts`
  - 验证：文件存在，内容可读取

### 1.4 课程导入 API

- [ ] **T-008** 实现课程导入 API
  - 完成标准：`POST /api/courses` 接收 Whisper JSON + 视频路径，创建课程记录，执行 Transcript 标准化
  - 文件：`06-src/app/api/courses/route.ts`
  - 验证：调用 API 后，courses 表新增记录，transcript.json 生成

- [ ] **T-009** 实现课程列表 API
  - 完成标准：`GET /api/courses` 返回所有课程（含知识点数量、笔记数量）
  - 文件：`06-src/app/api/courses/route.ts`
  - 验证：返回 JSON 数组，字段完整

- [ ] **T-010** 实现课程详情 API
  - 完成标准：`GET /api/courses/:id` 返回课程详情 + course.json 内容
  - 文件：`06-src/app/api/courses/[id]/route.ts`
  - 验证：返回完整课程数据（知识树 + 老师重点 + transcript）

- [ ] **T-011** 实现视频文件服务
  - 完成标准：`GET /api/video/:courseId` 返回视频流（支持 Range 请求）
  - 文件：`06-src/app/api/video/[courseId]/route.ts`
  - 验证：`<video src="/api/video/{id}">` 可正常播放

### 1.5 人工构造测试数据

- [ ] **T-012** 人工构造一份 course.json
  - 完成标准：选择一节真实课程，手动编写知识树（5-10 个节点）+ 老师重点（2-3 个）+ 概述
  - 文件：`coursemap-data/courses/{id}/course.json`
  - 验证：JSON Schema 校验通过，内容与 Transcript 一致

### 1.6 前端页面

- [ ] **T-013** 实现课程列表页
  - 完成标准：显示所有课程卡片（标题、时长、知识点数、笔记数、状态）
  - 文件：`06-src/app/courses/page.tsx`
  - 验证：页面渲染正确，点击卡片跳转

- [ ] **T-014** 实现课程预习页
  - 完成标准：显示知识地图（可展开/折叠）+ 老师重点汇总 + 概述 + "开始学习"按钮
  - 文件：`06-src/app/courses/[id]/preview/page.tsx`
  - 验证：知识树可交互，点击节点展开内容

- [ ] **T-015** 实现课程学习页 - 三栏布局
  - 完成标准：左栏知识树 + 中栏视频 + 右栏时间轴，响应式布局
  - 文件：`06-src/app/courses/[id]/learn/page.tsx`
  - 验证：三栏正确渲染，布局合理

- [ ] **T-016** 实现视频播放器组件
  - 完成标准：播放/暂停/倍速/拖动/时间显示，支持从指定时间开始播放
  - 文件：`06-src/components/VideoPlayer.tsx`
  - 验证：视频可正常播放，控件功能完整

- [ ] **T-017** 实现知识树组件
  - 完成标准：多级可展开/折叠，当前播放位置对应节点高亮，点击节点跳转视频
  - 文件：`06-src/components/KnowledgeTree.tsx`
  - 验证：树结构正确，交互正常

- [ ] **T-018** 实现知识时间轴组件
  - 完成标准：垂直时间轴，显示知识节点(●)/老师重点(★)/笔记(💭)，点击跳转视频，跟随播放位置自动滚动
  - 文件：`06-src/components/KnowledgeTimeline.tsx`
  - 验证：时间轴正确渲染，点击跳转准确

- [ ] **T-019** 实现知识树-视频-时间轴联动
  - 完成标准：三者状态同步（点击任一项，其他两项跟随更新）
  - 文件：学习页组件内状态管理
  - 验证：点击知识树 → 视频跳转 + 时间轴滚动；点击时间轴 → 视频跳转 + 知识树高亮

- [ ] **T-020** 实现"记录我的想法"功能
  - 完成标准：弹出输入框，显示当前时间和知识节点，保存后笔记立即出现
  - 文件：`06-src/components/NoteDialog.tsx`
  - 验证：笔记保存成功，出现在时间轴和知识树

- [ ] **T-021** 实现笔记 API
  - 完成标准：`POST /api/courses/:id/notes` 保存笔记，`GET` 获取笔记列表
  - 文件：`06-src/app/api/courses/[id]/notes/route.ts`
  - 验证：笔记持久化，杀进程不丢

- [ ] **T-022** 实现"查看老师原文"功能
  - 完成标准：点击后弹出对话框，显示对应 Transcript segment 内容
  - 文件：学习页组件内
  - 验证：原文内容正确，source_segment_ids 指向真实 segment

- [ ] **T-023** 实现溯源跳转
  - 完成标准：从知识节点/老师重点/笔记 → 一键跳转视频对应时间点（误差 <2s）
  - 文件：各组件内
  - 验证：跳转准确，视频播放位置正确

### 1.7 Phase 1 验收

- [ ] **T-024** Phase 1 端到端测试
  - 完成标准：用人工构造的 course.json，完成以下流程：
    1. 导入课程
    2. 进入预习页，查看知识地图
    3. 进入学习页，三栏联动
    4. 播放视频，知识树跟随
    5. 点击知识节点，视频跳转
    6. 点击时间轴，视频跳转
    7. 记录笔记，绑定时间
    8. 查看原文
    9. 溯源跳转
    10. 杀进程重开，数据不丢
  - 验证：所有步骤通过

---

## Phase 2：AI Pipeline

**目标**：接入 LLM API，自动解析生成 course.json。

### 2.1 AI Pipeline 基础设施

- [ ] **T-025** 实现 LLM API 客户端
  - 完成标准：封装国内模型 API 调用（glm 系列），支持流式/非流式，错误重试
  - 文件：`06-src/lib/llm-client.ts`
  - 验证：调用 API 返回正确响应

- [ ] **T-026** 实现 JSON Schema 校验
  - 完成标准：所有 AI 输出通过 zod schema 校验，校验失败时标记错误
  - 文件：`06-src/lib/schemas.ts`
  - 验证：非法 JSON 被正确拦截

- [ ] **T-027** 实现异步任务管理
  - 完成标准：创建 ai_processing_jobs 记录，更新 stage/progress/status
  - 文件：`06-src/lib/job-manager.ts`
  - 验证：任务状态正确流转

### 2.2 AI Pipeline 7 步实现

- [ ] **T-028** 实现 Step 2: Semantic Chunking
  - 完成标准：AI 按语义切分 transcript，输出 chunks[]（chunk_id/start/end/topic）
  - 文件：`06-src/lib/ai-pipeline/step2-chunking.ts`
  - Prompt：见方案.md / 方案2.md
  - 验证：chunk 覆盖完整 transcript，topic 描述准确

- [ ] **T-029** 实现 Step 3: Knowledge Extraction
  - 完成标准：对每个 chunk 提取知识节点（title/summary/source_segment_ids/children）
  - 文件：`06-src/lib/ai-pipeline/step3-knowledge-extraction.ts`
  - 验证：知识节点与 transcript 内容一致，source_segment_ids 正确

- [ ] **T-030** 实现 Step 4: Teacher Insight Extraction
  - 完成标准：识别老师明确强调的内容（teacher_highlight/common_mistake/teacher_experience）
  - 文件：`06-src/lib/ai-pipeline/step4-teacher-insight.ts`
  - 验证：老师重点与 transcript 一致，不编造

- [ ] **T-031** 实现 Step 5: Knowledge Tree Merge
  - 完成标准：合并所有 chunk 的知识节点，去重、建立父子关系
  - 文件：`06-src/lib/ai-pipeline/step5-tree-merge.ts`
  - 验证：知识树结构合理，无重复节点

- [ ] **T-032** 实现 Step 6: Knowledge Summary
  - 完成标准：生成课程概述 + 各节点 summary
  - 文件：`06-src/lib/ai-pipeline/step6-summary.ts`
  - 验证：概述准确，summary 与内容一致

- [ ] **T-033** 实现 Step 7: Source Validation
  - 完成标准：检查每条 AI 生成内容的 source_segment_ids 是否真实存在且支持该 claim
  - 文件：`06-src/lib/ai-pipeline/step7-validation.ts`
  - 验证：无效 source 被标记 needs_review

- [ ] **T-034** 实现 Pipeline 编排
  - 完成标准：按顺序执行 7 步，每步更新 job progress，失败时标记 failed 并保留已完成步骤
  - 文件：`06-src/lib/ai-pipeline/index.ts`
  - 验证：完整 Pipeline 可运行，进度正确更新

### 2.3 AI API 集成

- [ ] **T-035** 实现启动解析 API
  - 完成标准：`POST /api/courses/:id/parse` 创建 job，异步执行 Pipeline
  - 文件：`06-src/app/api/courses/[id]/parse/route.ts`
  - 验证：调用后 job 状态变为 processing

- [ ] **T-036** 实现解析进度 API
  - 完成标准：`GET /api/courses/:id/parse/status` 返回 stage + progress
  - 文件：`06-src/app/api/courses/[id]/parse/status/route.ts`
  - 验证：前端可轮询获取进度

- [ ] **T-037** 前端解析进度显示
  - 完成标准：课程卡片显示"解析中" + 进度条，解析完成后自动刷新
  - 文件：课程列表页组件
  - 验证：进度实时更新

### 2.4 Phase 2 验收

- [ ] **T-038** Phase 2 端到端测试
  - 完成标准：用真实 Whisper JSON，完成以下流程：
    1. 导入课程
    2. 启动 AI 解析
    3. 观察解析进度
    4. 解析完成后查看知识树
    5. 人工抽查知识节点准确性
    6. 人工抽查老师重点准确性
    7. 验证所有 source_segment_ids 有效
  - 验证：所有步骤通过，知识树基本准确

---

## Phase 3：复习视图 + 打磨

**目标**：完成复习模式，实现笔记异步归类，打磨交互细节。

### 3.1 复习视图

- [ ] **T-039** 实现复习视图页面
  - 完成标准：知识地图 + 选中节点详情（摘要+重点+笔记）+ 时间轴，视频默认隐藏
  - 文件：`06-src/app/courses/[id]/review/page.tsx`
  - 验证：页面渲染正确，交互流畅

- [ ] **T-040** 实现"跳转视频"功能
  - 完成标准：复习模式下点击"跳转视频"，展开视频播放器并跳转到对应时间
  - 文件：复习页组件
  - 验证：视频展开并跳转准确

### 3.2 笔记异步归类

- [ ] **T-041** 实现笔记 AI 归类
  - 完成标准：笔记保存后异步调用 AI 判断归属知识节点，根据 confidence 更新
  - 文件：`06-src/lib/note-classifier.ts`
  - 验证：笔记归类正确，低置信度时保持原归属

- [ ] **T-042** 实现笔记手动归类（N-01）
  - 完成标准：用户可手动修改笔记归属的知识节点
  - 文件：笔记组件
  - 验证：手动归类后，笔记出现在正确位置

### 3.3 交互打磨

- [ ] **T-043** 知识节点手动编辑（N-02）
  - 完成标准：用户可修改知识节点标题/摘要
  - 文件：知识树组件
  - 验证：编辑后保存，刷新页面仍显示修改后内容

- [ ] **T-044** 全文搜索（N-03）
  - 完成标准：在 Transcript 中搜索关键词，定位到对应时间
  - 文件：学习页组件
  - 验证：搜索结果正确，点击跳转

- [ ] **T-045** 课程间导航（N-04）
  - 完成标准：同一科目下多节课的进度追踪
  - 文件：课程列表页
  - 验证：显示科目下所有课程及完成状态

- [ ] **T-046** 导出复习笔记（N-05）
  - 完成标准：将某节课的所有笔记导出为 Markdown
  - 文件：复习页组件
  - 验证：导出文件内容正确

- [ ] **T-047** 重新解析（N-06）
  - 完成标准：对已解析课程重新运行 AI Pipeline
  - 文件：课程详情页
  - 验证：重新解析后 course.json 更新

### 3.4 Phase 3 验收

- [ ] **T-048** Phase 3 端到端测试
  - 完成标准：完整三阶段闭环跑通：
    1. 预习：查看知识地图，建立认知
    2. 学习：看视频，记录笔记，溯源
    3. 复习：快速浏览知识时间轴，跳转视频
  - 验证：所有步骤通过，用户体验流畅

---

## 任务统计

| 阶段 | 任务数 | 预估工时 |
| --- | --- | --- |
| Phase 1：数据流 + 交互 | 24 | 3-5 天 |
| Phase 2：AI Pipeline | 14 | 2-3 天 |
| Phase 3：复习 + 打磨 | 10 | 1-2 天 |
| **总计** | **48** | **6-10 天** |

---

## 开发顺序建议

1. **先跑通数据流**：T-001 → T-012（项目初始化 + 数据库 + Transcript + 测试数据）
2. **再做前端交互**：T-013 → T-023（三个页面 + 核心组件）
3. **Phase 1 验收**：T-024（确保交互闭环跑通）
4. **接入 AI**：T-025 → T-037（LLM 客户端 + 7 步 Pipeline + API）
5. **Phase 2 验收**：T-038（确保 AI 解析质量）
6. **最后打磨**：T-039 → T-047（复习视图 + 交互优化）

---

## 注意事项

- **Phase 1 不接 AI**：用人工构造的 course.json 验证交互，避免 AI 质量问题阻塞前端开发
- **所有 AI 输出必须 JSON Schema 校验**：防止模型返回非法格式
- **时间统一用秒数（float）**：不要存字符串，方便计算和跳转
- **笔记立即保存**：不等待 AI 归类，用户体验优先
- **source_segment_ids 是核心**：所有 AI 内容必须携带，否则无法溯源
- **宁缺毋滥**：AI 无法确定时标记 needs_review，不编造
