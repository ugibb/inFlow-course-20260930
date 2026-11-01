#!/usr/bin/env python3
"""Generate CourseMap V3 prototype — V2 exploratory preview + V1 learn/review/practice."""

import json
import html
import os

INPUT_DIR = os.path.join(os.path.dirname(__file__), '03-input')
JSON_FILE = os.path.join(INPUT_DIR, '03-txt', 'R_001_录_阅读导学_视频1_阅读导学_003419上次看到_词性的区分及其意义_005716.json')
VIDEO_FILE = '03-input/01-mp4/R_001_录_阅读导学_视频1_阅读导学_003419上次看到_词性的区分及其意义_005716.mp4'

with open(JSON_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

segments = data['segments']
total_duration = segments[-1]['end']

def fmt_time(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

lines = []
current_text = ""
current_start = segments[0]['start']
LINE_DURATION = 14

for seg in segments:
    if current_text and (seg['start'] - current_start) >= LINE_DURATION:
        lines.append({'start': current_start, 'end': seg['start'], 'text': current_text.strip()})
        current_text = seg['text']
        current_start = seg['start']
    else:
        current_text += seg['text']

if current_text.strip():
    lines.append({'start': current_start, 'end': segments[-1]['end'], 'text': current_text.strip()})

# ── Exploratory chapter data (from V2) ──
chapters = [
    {
        'num': 1, 'text': '课程总览', 'icon': '🧭',
        'teaser': '这节课到底要讲什么？34 分钟能帮你解决哪些问题？',
        'modules': [
            {'text': '核心框架与目标', 'question': '这门课想帮你建立什么能力？', 'insight': '两大核心模块：基础能力（词汇+词性+句法）和解题技巧（定位+题型+同义替换）。课程会先打基础，再教招式。'},
            {'text': '适用人群', 'question': '你应该选启航班还是飞跃班？', 'insight': '不看目标分数，看当前基础。4-4.5 分 → 启航班；5.5-6 分 → 飞跃班。选错班型 = 浪费时间。'},
            {'text': '课程结构', 'question': '从导学课到技巧课，学习路径是什么？', 'insight': '导学课（考情+计划+要求）→ 基础课（词性区分及意义）→ 技巧课（定位+题型解法），循序渐进。'},
        ]
    },
    {
        'num': 2, 'text': '雅思阅读考情介绍', 'icon': '📋',
        'teaser': '雅思阅读到底考什么？60 分钟里藏着哪些你需要注意的规则？',
        'modules': [
            {'text': '考试基本信息', 'question': '60 分钟、3 篇文章、40 题——具体怎么分配？', 'insight': '60 分钟包含填答案时间。每篇约 13-14 题，难度整体递增，第 3 篇通常最难。文体只考议论文+说明文。'},
            {'text': '主要题型', 'question': '雅思阅读有几种题型？哪种最难？', 'insight': '5 大题型：填空 → 判断 → 选择 → 匹配 → Heading。判断题的 False vs Not Given 是最大难点。'},
            {'text': '评分标准与目标分数', 'question': '错多少题能拿 7 分？你的策略应该是什么？', 'insight': '错 ≤ 10 个 = 7 分，错 ≤ 7 个 = 7.5 分。填空+判断占约 20 题，是拿分基础。策略：阅读/听力冲高分，弥补口语/写作。'},
        ]
    },
    {
        'num': 3, 'text': '复习计划与刷题策略', 'icon': '🗺️',
        'teaser': '剑桥雅思 4-17，到底该按什么顺序刷？为什么不能随便挑？',
        'modules': [
            {'text': '提分三大要素', 'question': '提分靠什么？只是刷题就够了吗？', 'insight': '三要素：语言能力（内功）+ 方法技巧（招式）+ 合理计划（策略）。光刷题不练内功，天花板很低。'},
            {'text': '刷题顺序', 'question': 'C4 到 C17，正确的打开方式是什么？', 'insight': 'C13-14 入门 → C4-8 专项 → C9-12 核心（必须整套做）→ C15-17 模考。正确率 > 速度。'},
            {'text': '考试形式选择', 'question': '纸笔考和机考，对日常练习有什么影响？', 'insight': '选定考试方式后，平时刷题必须用同样方式。纸笔手感 ≠ PDF/APP，机考需要在模拟系统上练。'},
            {'text': '个性化计划申请', 'question': '通用的刷题顺序适合每个人吗？', 'insight': '老师给的是通用框架。个人情况（基础、备考时间）不同，可课后微信群联系老师获取专属方案。'},
        ]
    },
    {
        'num': 4, 'text': '课程介绍与作业要求', 'icon': '📝',
        'teaser': '两个班型课程分别怎么安排？作业怎么交才不会被老师"忽略"？',
        'modules': [
            {'text': '课程内容', 'question': '启航班和飞跃班的课程流程有什么区别？', 'insight': '启航班：先攻词汇+语法基础，再学题型（6 次×1h+8 节视频）。飞跃班：直接聚焦题型技巧（5 次×2h+7 节视频）。'},
            {'text': '作业提交要求', 'question': '作业怎么交？有什么"潜规则"？', 'insight': '注明日期+科目、附截图、错题必须标记（打问号或写"XX 题需讲解"）。下次直播课前 1 天提交，不要太早。'},
        ]
    },
    {
        'num': 5, 'text': '课后作业', 'icon': '✏️',
        'teaser': '听完导学课，第一件事应该做什么？',
        'modules': [
            {'text': '基础积累', 'question': '词汇怎么整理？核心词和认知词有什么区别？', 'insight': '启航班：整理词汇 List1，核心词记词意+词性+同义替换+搭配，认知词只记大意。飞跃班：真题生词结合语境记忆。'},
            {'text': '真题练习', 'question': '第一套真题应该选哪本剑桥？', 'insight': '启航班：C14-17 做 1 套完整阅读自测。飞跃班：C10-13 做填空专项，结合词性预判答案。'},
            {'text': '其他要求', 'question': '刷题时最容易忽略的一件事是什么？', 'insight': '按选定考试类型刷题保持手感。错题必须标注原因（词性判断错误/指代未明确/逻辑关系未识别）。'},
        ]
    },
]

# ── Knowledge tree for learn page (2 levels) ──
knowledge_tree = [
    {'level': 1, 'text': '课程总览', 'children': [
        {'level': 2, 'text': '核心框架与目标', 'time_range': (0, 30)},
        {'level': 2, 'text': '适用人群', 'time_range': (30, 43)},
        {'level': 2, 'text': '课程结构', 'time_range': (43, 78)},
    ]},
    {'level': 1, 'text': '雅思阅读考情介绍', 'children': [
        {'level': 2, 'text': '考试基本信息', 'time_range': (78, 200)},
        {'level': 2, 'text': '主要题型', 'time_range': (200, 495)},
        {'level': 2, 'text': '评分标准与目标分数', 'time_range': (495, 975)},
    ]},
    {'level': 1, 'text': '复习计划与刷题策略', 'children': [
        {'level': 2, 'text': '提分三大要素', 'time_range': (975, 1050)},
        {'level': 2, 'text': '刷题顺序（剑桥雅思系列）', 'time_range': (1050, 1260)},
        {'level': 2, 'text': '考试形式选择', 'time_range': (1260, 1320)},
        {'level': 2, 'text': '个性化计划申请', 'time_range': (1320, 1340)},
    ]},
    {'level': 1, 'text': '课程介绍与作业要求', 'children': [
        {'level': 2, 'text': '课程内容', 'time_range': (1340, 1560)},
        {'level': 2, 'text': '作业提交要求', 'time_range': (1640, 2020)},
    ]},
    {'level': 1, 'text': '课后作业', 'children': [
        {'level': 2, 'text': '基础积累', 'time_range': (2020, 2040)},
        {'level': 2, 'text': '真题练习', 'time_range': (2040, 2050)},
        {'level': 2, 'text': '其他要求', 'time_range': (2050, 2052)},
    ]},
]

# ── Preview cards (for review page) ──
preview_cards = [
    {'title': '考试基本信息', 'tag': '重点', 'summary': '考试时间 60 分钟（含填答案时间），3 篇文章共 40 题（每篇 13-14 题），难度逐篇递增。文体以议论文、说明文为主，不考记叙文。题材注意文理科平衡。建议先翻阅剑桥雅思 4-13 了解整体。', 'highlight': '不管纸笔还是机考，60 分钟都包含答题和填写答题卡的时间'},
    {'title': '题型分类与解题逻辑', 'tag': '核心', 'summary': '课程按难度递进：基础（定位+同义替换）→ 细节题（填空+判断）→ 过渡题（选择）→ 宏观题（匹配+Heading）。判断题有 True/False/Not Given 三个选项，False 和 NG 的区分是难点。填空+判断占约 20 题/40 题。', 'highlight': '填空+判断占约 20 题（总共 40 题），是必须把握的核心拿分题型'},
    {'title': '目标分数与评分标准', 'tag': '重点', 'summary': '总分 7 分=四科≥27，6.5 分≥25，6 分≥23。阅读评分关键线：错≤7=7.5 分，错≤10=7 分，错≤13-14=6.5 分。推荐策略：阅读/听力冲 7-8 分，弥补口语/写作短板。', 'highlight': '错超过 10 个就低于 7 分，错超过 13 个就低于 6.5 分——每一个题都很重要'},
    {'title': '刷题顺序与策略', 'tag': None, 'summary': '提分三要素：语言能力（内功）、方法技巧（招式）、合理计划（策略）。刷题顺序：C13-14 入门→C4-8 专项→C9-12 核心（整套完成）→C15-17 考前模拟。正确率优先于速度。', 'highlight': '一旦开始做剑桥真题，一定要整套完成，不能今天做一篇明天做一篇'},
    {'title': '课程安排与作业要求', 'tag': None, 'summary': '启航班（6 次×1 小时 + 赠课）：词汇→词性→句法→定位→题型，适合基础 4-4.5 分。飞跃班（5 次×2 小时 + 赠课）：定位→填空/判断→选择→匹配→Heading，适合基础 5.5-6 分。作业需标注日期+截图+标记错题。', 'highlight': '有问题的题目一定要做好标记——打问号或写"老师 XX 题需要讲一讲"'},
]

# ── Timeline items ──
timeline_items = [
    {'time': '00:00', 'label': '课程导入', 'desc': '导学视频目的：考情+计划+课程要求', 'cls': ''},
    {'time': '01:18', 'label': '考情：考试基本信息', 'desc': '60 分钟/3 篇 40 题/纸笔 vs 机考', 'cls': ''},
    {'time': '02:50', 'label': '难度与文体', 'desc': '难度递增/议论文+说明文/文理平衡', 'cls': ''},
    {'time': '03:20', 'label': '题型总览', 'desc': '课程逻辑：基础→细节→过渡→宏观', 'cls': ''},
    {'time': '04:10', 'label': '填空题', 'desc': '细节题，有细分类型，后续专课学习', 'cls': ''},
    {'time': '04:40', 'label': '判断题 T/F/NG', 'desc': '★ False vs Not Given 是难点', 'cls': 'highlight'},
    {'time': '05:50', 'label': '选择题', 'desc': '单选/多选，实际非常难', 'cls': ''},
    {'time': '06:20', 'label': '匹配题', 'desc': '人名/时间/地点/句子/信息匹配', 'cls': ''},
    {'time': '07:20', 'label': 'Heading 题 + 简单题', 'desc': '标题配对；简单题方法接近填空', 'cls': ''},
    {'time': '08:15', 'label': '目标分数', 'desc': '7 分≥27 / 6.5≥25 / 6≥23', 'cls': ''},
    {'time': '09:30', 'label': '小分要求与组合', 'desc': '分数组合方式 + 学校小分要求', 'cls': ''},
    {'time': '10:20', 'label': '考生优劣势', 'desc': '★ 阅读/听力冲 7-8 分弥补说写', 'cls': 'highlight'},
    {'time': '11:30', 'label': '★ 评分标准', 'desc': '错≤10=7 分 / 错≤13=6.5 分', 'cls': 'highlight'},
    {'time': '13:30', 'label': '★ 填空 + 判断=核心', 'desc': '占 20 题/40 题，是拿分基础', 'cls': 'highlight'},
    {'time': '15:00', 'label': '每天练阅读听力', 'desc': '提分难度小，保证每天一定量', 'cls': ''},
    {'time': '16:15', 'label': '提分三要素', 'desc': '内功·招式·策略', 'cls': ''},
    {'time': '18:15', 'label': '刷题顺序', 'desc': 'C13 入门→C4 专项→C9 核心→C15 模拟', 'cls': ''},
    {'time': '19:20', 'label': '★ 整套完成', 'desc': '正确率>速度，不能今天一篇明天一篇', 'cls': 'highlight'},
    {'time': '21:00', 'label': '考试形式选择', 'desc': '选定后刷题方式保持一致', 'cls': ''},
    {'time': '22:20', 'label': '启航班大纲', 'desc': '词汇→词性→句法→定位→题型', 'cls': ''},
    {'time': '23:50', 'label': '飞跃班大纲', 'desc': '定位→填空/判断→选择→匹配→Heading', 'cls': ''},
    {'time': '25:00', 'label': '班型选择', 'desc': '★ 基础 4-4.5 启航/5.5-6 飞跃', 'cls': 'highlight'},
    {'time': '27:20', 'label': '作业格式要求', 'desc': '日期+科目+截图+标记错题', 'cls': ''},
    {'time': '29:10', 'label': '★ 提交时间', 'desc': '统一在下次直播课前一天提交', 'cls': 'highlight'},
    {'time': '30:30', 'label': '作业示范', 'desc': '展示多种提交方式和标记方法', 'cls': ''},
    {'time': '32:30', 'label': '笔记要求', 'desc': '手写或截图均可，需体现反思', 'cls': ''},
    {'time': '33:40', 'label': '结语', 'desc': '有问题即时交流，期待有所收获', 'cls': ''},
]

# ── Generate HTML fragments ──
transcript_html = ""
for i, line in enumerate(lines):
    ts = fmt_time(line['start'])
    text_escaped = html.escape(line['text'])
    cls = 'transcript-line'
    if i < 8: cls += ' read'
    elif i == 8: cls += ' current'
    transcript_html += f'      <div class="{cls}" data-start="{line["start"]}" data-end="{line["end"]}"><span class="ts">{ts}</span>{text_escaped}</div>\n'

def gen_tree_html():
    h = ""
    for node in knowledge_tree:
        h += f'      <div class="tree-item" data-start="{node["children"][0]["time_range"][0]}" data-end="{node["children"][-1]["time_range"][1]}"><span class="node-dot"></span>▾ {node["text"]}</div>\n'
        for child in node['children']:
            h += f'      <div class="tree-item tree-child" data-start="{child["time_range"][0]}" data-end="{child["time_range"][1]}"><span class="node-dot"></span>{child["text"]}</div>\n'
    return h

def gen_nav_html():
    """Generate two-level navigation with icons from chapters data"""
    h = ""
    icons = ['🧭', '📋', '🗺️', '📝', '✏️']
    for i, ch in enumerate(chapters):
        ch_num = ch['num']
        icon = ch['icon']
        h += f'        <div class="tree-item" onclick="scrollToChapter({ch_num})"><span class="node-dot"></span>{icon} {ch_num:02d} {html.escape(ch["text"])}</div>\n'
        for mod in ch['modules']:
            h += f'        <div class="tree-item tree-child" onclick="scrollToChapter({ch_num})"><span class="node-dot"></span>{html.escape(mod["text"])}</div>\n'
    return h

def gen_learn_nav_html():
    """Generate two-level navigation for learn page with video time ranges"""
    h = ""
    for ch, node in zip(chapters, knowledge_tree):
        ch_start = node["children"][0]["time_range"][0]
        ch_end = node["children"][-1]["time_range"][1]
        h += f'        <div class="tree-item" data-start="{ch_start}" data-end="{ch_end}" onclick="seekTo({ch_start})"><span class="node-dot"></span>{ch["icon"]} {ch["num"]:02d} {html.escape(ch["text"])}</div>\n'
        for child in node['children']:
            s, e = child["time_range"]
            h += f'        <div class="tree-item tree-child" data-start="{s}" data-end="{e}" onclick="seekTo({s})"><span class="node-dot"></span>{html.escape(child["text"])}</div>\n'
    return h

tree_html = gen_tree_html()
nav_html = gen_nav_html()
learn_nav_html = gen_learn_nav_html()

# Chapter cards HTML (exploratory preview)
chapters_html = ""
for ch in chapters:
    mods_html = ""
    for mi, mod in enumerate(ch['modules']):
        mods_html += f'''<div class="mod-pill" data-chapter="{ch['num']}" data-module="{mi}" onclick="revealModule(this, {ch['num']}, {mi})">
          <span class="mod-dot"></span>{html.escape(mod['text'])}
        </div>\n'''
    insights_html = ""
    for mi, mod in enumerate(ch['modules']):
        insights_html += f'''<div class="insight-reveal" id="insight-{ch['num']}-{mi}">
          <div class="insight-q">{html.escape(mod['question'])}</div>
          <div class="insight-a">{html.escape(mod['insight'])}</div>
        </div>\n'''
    chapters_html += f'''<div class="explore-card" id="ch{ch['num']}" onclick="expandChapter({ch['num']})">
      <div class="explore-card-head">
        <div class="explore-num">{ch['num']:02d}</div>
        <div class="explore-info">
          <span class="explore-icon">{ch['icon']}</span>
          <b>{html.escape(ch['text'])}</b>
          <p class="explore-teaser">{html.escape(ch['teaser'])}</p>
        </div>
        <div class="explore-arrow">›</div>
      </div>
      <div class="explore-card-body" id="ch{ch['num']}-body">
        <div class="mod-pills">{mods_html}</div>
        <div class="insight-area" id="insight-area-{ch['num']}">{insights_html}</div>
      </div>
    </div>\n'''

# Timeline HTML
timeline_html = ""
for item in timeline_items:
    cls = f' {item["cls"]}' if item["cls"] else ''
    sec = int(item["time"].split(":")[0]) * 60 + int(item["time"].split(":")[1])
    timeline_html += f'''          <div class="event{cls}" onclick="seekTo({sec})">
            <span class="dot"></span>
            <b>{item["time"]} {item["label"]}</b>
            <p>{item["desc"]}</p>
          </div>\n'''

# Review keypoints
review_keypoints_html = ""
for card in preview_cards[:3]:
    if card['highlight']:
        review_keypoints_html += f'''      <div class="keypoint-item">
        <div class="kp-icon kp-teacher">!</div>
        <div>{html.escape(card["highlight"])}</div>
      </div>\n'''

total_modules = sum(len(c['modules']) for c in chapters)
duration_str = fmt_time(total_duration)

html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CourseMap V3 · 探索式预习 + 四阶段闭环</title>
<style>
  :root {{
    --bg: #f5f6f8; --surface: #ffffff; --text: #18202a;
    --text-secondary: #6c7480; --text-muted: #78818e;
    --border: #e7e9ee; --border-light: #edf0f3;
    --primary: #3157b7; --primary-light: #edf2ff; --primary-dark: #244bb3;
    --orange: #d59a20; --orange-light: #fff8e9; --orange-border: #efdfb2;
    --green: #4b7b59; --green-light: #edf8f0;
    --blue-note: #6a75d8; --blue-note-light: #f0f2ff; --blue-note-border: #dce1ff;
    --red: #a55353; --red-light: #fff1f1;
    --radius: 14px; --radius-sm: 10px;
    --shadow: 0 2px 8px rgba(20,28,40,.035);
    --shadow-md: 0 4px 16px rgba(20,28,40,.07);
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  button {{ font: inherit; border: 0; cursor: pointer; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.6;
    overflow: hidden; height: 100vh;
  }}
  .app {{ height: 100vh; display: flex; flex-direction: column; }}

  /* TOP BAR */
  .topbar {{
    height: 64px; background: var(--surface); border-bottom: 1px solid var(--border);
    display: flex; align-items: center; padding: 0 24px; gap: 24px; z-index: 100; flex-shrink: 0;
  }}
  .brand {{ font-weight: 800; font-size: 18px; letter-spacing: -0.5px; }}
  .version-tag {{ font-size: 10px; padding: 3px 7px; border-radius: 5px; background: var(--primary-light); color: var(--primary); font-weight: 600; margin-left: 8px; }}
  .phase-badge {{ font-size: 12px; padding: 5px 9px; border-radius: 999px; background: var(--primary-light); color: var(--primary); font-weight: 600; }}
  .topbar .spacer {{ flex: 1; }}
  .topbar-progress {{ font-size: 13px; color: var(--text-secondary); }}
  .topbar-progress b {{ color: var(--text); }}

  /* Phase navigation - progressive stepper */
  .phase-nav {{ display: flex; gap: 0; align-items: center; }}
  .phase-btn {{
    position: relative;
    padding: 8px 16px;
    font-size: 13px; font-weight: 500;
    background: transparent;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 0.25s ease;
  }}
  .phase-btn:hover {{
    color: var(--primary);
  }}
  .phase-btn.active {{
    color: var(--primary);
    font-weight: 600;
  }}
  .phase-btn.active::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 16px; right: 16px;
    height: 2px;
    background: var(--primary);
    border-radius: 2px 2px 0 0;
  }}
  /* Arrow separator between buttons */
  .phase-separator {{
    width: 0; height: 0;
    border-top: 5px solid transparent;
    border-bottom: 5px solid transparent;
    border-left: 7px solid var(--border);
    margin: 0 6px;
    transition: border-color 0.25s ease;
  }}
  .phase-separator.passed {{
    border-left-color: var(--primary);
  }}
  .topbar-crumb {{ font-size: 13px; color: var(--text-muted); }}
  .topbar-crumb a {{ color: var(--text-secondary); cursor: pointer; text-decoration: none; }}
  .topbar-crumb a:hover {{ color: var(--primary); }}
  .topbar-crumb .current {{ color: var(--text); font-weight: 500; }}

  /* PAGE */
  .page {{ display: none; flex: 1; min-height: 0; }}
  .page.active {{ display: flex; flex-direction: column; }}

  /* ══════ EXPLORATORY PREVIEW ══════ */
  .preview-layout {{ flex: 1; min-height: 0; display: grid; grid-template-columns: 250px 1fr 300px; }}
  .preview-nav {{ background: var(--surface); border-right: 1px solid var(--border); overflow-y: auto; padding: 24px 0; }}
  .preview-nav h3 {{ font-size: 14px; font-weight: 600; padding: 0 20px 12px; margin: 0; }}
  .preview-main {{ overflow-y: auto; padding: 32px 36px; }}
  .preview-rail {{ background: var(--surface); border-left: 1px solid var(--border); overflow-y: auto; padding: 24px 20px; }}

  .preview-hero {{ margin-bottom: 28px; }}
  .preview-hero h1 {{ font-size: 26px; font-weight: 700; margin-bottom: 6px; }}
  .preview-hero .subtitle {{ color: var(--text-secondary); font-size: 14px; line-height: 1.7; }}

  .guiding-qs {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }}
  .gq {{
    padding: 8px 14px; border-radius: 999px; font-size: 13px;
    background: var(--surface); border: 1px solid var(--border);
    cursor: pointer; transition: all 0.2s; color: var(--text-secondary);
  }}
  .gq:hover {{ border-color: var(--primary); color: var(--primary); background: var(--primary-light); }}
  .gq.answered {{ background: var(--green-light); border-color: #b8d4c0; color: var(--green); }}

  .explore-cards {{ display: flex; flex-direction: column; gap: 10px; margin-bottom: 24px; }}
  .explore-card {{
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
    box-shadow: var(--shadow); overflow: hidden; transition: all 0.25s ease;
  }}
  .explore-card:hover {{ box-shadow: var(--shadow-md); border-color: #c8cdd6; }}
  .explore-card.expanded {{ border-color: var(--primary); }}
  .explore-card.discovered {{ border-color: var(--green); }}
  .explore-card-head {{
    display: flex; align-items: center; gap: 14px; padding: 18px 20px; cursor: pointer;
  }}
  .explore-num {{
    width: 36px; height: 36px; border-radius: 10px;
    background: var(--bg); display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 700; color: var(--text-muted); flex-shrink: 0;
    transition: all 0.2s;
  }}
  .explore-card.expanded .explore-num {{ background: var(--primary); color: #fff; }}
  .explore-card.discovered .explore-num {{ background: var(--green); color: #fff; }}
  .explore-info {{ flex: 1; }}
  .explore-info .explore-icon {{ margin-right: 6px; }}
  .explore-info b {{ font-size: 15px; }}
  .explore-teaser {{ font-size: 13px; color: var(--text-muted); margin-top: 2px; line-height: 1.5; }}
  .explore-arrow {{
    font-size: 20px; color: var(--text-muted); transition: transform 0.25s; flex-shrink: 0;
  }}
  .explore-card.expanded .explore-arrow {{ transform: rotate(90deg); }}

  .explore-card-body {{
    max-height: 0; overflow: hidden; transition: max-height 0.35s ease;
    padding: 0 20px;
  }}
  .explore-card.expanded .explore-card-body {{
    max-height: 600px; padding: 0 20px 20px;
  }}

  .mod-pills {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }}
  .mod-pill {{
    padding: 7px 14px; border-radius: 8px; font-size: 12px;
    background: var(--bg); border: 1px solid var(--border-light);
    cursor: pointer; transition: all 0.15s; display: flex; align-items: center; gap: 6px;
    color: var(--text-secondary);
  }}
  .mod-pill:hover {{ border-color: var(--primary); color: var(--primary); }}
  .mod-pill.revealed {{ background: var(--primary-light); border-color: #b8c8e8; color: var(--primary); font-weight: 500; }}
  .mod-dot {{ width: 6px; height: 6px; border-radius: 50%; background: #ccd1d8; transition: background 0.2s; }}
  .mod-pill.revealed .mod-dot {{ background: var(--primary); }}

  .insight-reveal {{
    display: none; margin-top: 10px; padding: 14px 16px;
    background: var(--orange-light); border: 1px solid var(--orange-border);
    border-radius: var(--radius-sm); animation: fadeSlide 0.3s ease;
  }}
  .insight-reveal.show {{ display: block; }}
  .insight-q {{ font-size: 13px; font-weight: 600; color: #7c5e00; margin-bottom: 6px; }}
  .insight-a {{ font-size: 13px; color: #8a6d1a; line-height: 1.7; }}

  @keyframes fadeSlide {{
    from {{ opacity: 0; transform: translateY(-8px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}

  .discovery-header {{ margin-bottom: 20px; }}
  .discovery-header h3 {{ font-size: 14px; font-weight: 600; margin-bottom: 4px; }}
  .discovery-header p {{ font-size: 12px; color: var(--text-muted); }}

  .progress-ring {{
    width: 100%; padding: 20px; text-align: center;
    background: var(--bg); border-radius: var(--radius); margin-bottom: 16px;
  }}
  .progress-ring .big {{ font-size: 36px; font-weight: 800; color: var(--primary); }}
  .progress-ring .label {{ font-size: 12px; color: var(--text-muted); margin-top: 4px; }}
  .progress-bar-v2 {{ height: 6px; background: var(--border-light); border-radius: 6px; overflow: hidden; margin-top: 12px; }}
  .progress-bar-v2 .fill {{ height: 100%; background: var(--primary); border-radius: 6px; transition: width 0.4s ease; }}

  .chapter-status {{ display: flex; flex-direction: column; gap: 6px; margin-bottom: 20px; }}
  .ch-status {{
    display: flex; align-items: center; gap: 10px; padding: 8px 12px;
    border-radius: 8px; font-size: 12px; cursor: pointer; transition: background 0.15s;
  }}
  .ch-status:hover {{ background: var(--bg); }}
  .ch-status .ch-dot {{ width: 8px; height: 8px; border-radius: 50%; background: var(--border); flex-shrink: 0; }}
  .ch-status.partial .ch-dot {{ background: var(--orange); }}
  .ch-status.complete .ch-dot {{ background: var(--green); }}
  .ch-status .ch-label {{ flex: 1; color: var(--text-secondary); }}
  .ch-status .ch-count {{ font-size: 11px; color: var(--text-muted); }}

  .teacher-tip {{
    padding: 14px; background: var(--orange-light); border: 1px solid var(--orange-border);
    border-radius: var(--radius-sm); margin-bottom: 16px;
  }}
  .teacher-tip .tip-label {{ font-size: 11px; font-weight: 600; color: var(--orange); margin-bottom: 6px; }}
  .teacher-tip p {{ font-size: 13px; color: #7c5e00; line-height: 1.65; }}

  .cta-area {{ margin-top: auto; padding-top: 16px; }}
  .cta-btn {{
    width: 100%; padding: 14px; border-radius: var(--radius-sm);
    background: var(--primary); color: #fff; font-size: 14px; font-weight: 600;
    transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 8px;
  }}
  .cta-btn:hover {{ background: var(--primary-dark); }}
  .cta-btn.locked {{ background: var(--bg); color: var(--text-muted); border: 1px solid var(--border); cursor: not-allowed; }}

  /* ══════ LEARN PAGE ══════ */
  #page-learn .layout {{ grid-template-columns: 260px minmax(560px, 1fr) 330px; }}
  .layout {{ flex: 1; min-height: 0; display: grid; }}
  .side {{ background: var(--surface); overflow-y: auto; }}
  .side.left {{ border-right: 1px solid var(--border); }}
  .side.right {{ border-left: 1px solid var(--border); overflow-y: auto; }}
  .side h3 {{ font-size: 13px; font-weight: 600; margin: 0; padding: 20px 18px 10px; color: var(--text-muted); }}
  .main {{ min-width: 0; overflow: auto; }}
  #page-learn .main {{ padding: 0; background: #eef0f3; }}

  .tree-item {{
    padding: 9px 18px; font-size: 13px; color: #515b68;
    display: flex; gap: 8px; align-items: center;
    cursor: pointer; transition: background 0.1s;
  }}
  .tree-item:hover {{ background: #f6f7f9; }}
  .tree-item.active {{ font-weight: 650; color: var(--primary); background: var(--primary-light); }}
  .tree-child {{ padding-left: 34px; }}
  .tree-item .node-dot {{ width: 6px; height: 6px; border-radius: 50%; background: #ccd1d8; flex-shrink: 0; }}
  .tree-item.active .node-dot {{ background: var(--primary); }}
  .tree-item.in-range .node-dot {{ background: rgba(49,87,183,0.4); }}

  .video {{
    background: #121820; border-radius: var(--radius); overflow: hidden;
    color: #fff; box-shadow: 0 8px 30px rgba(15,20,28,.16); margin: 18px 18px 0;
  }}
  .video video {{ width: 100%; display: block; max-height: 38vh; }}
  .video-controls {{
    padding: 11px 14px; background: #171e27;
    display: flex; align-items: center; gap: 10px;
  }}
  .video-controls .bar {{ flex: 1; height: 4px; background: #3a434e; border-radius: 4px; cursor: pointer; }}
  .video-controls .bar i {{ display: block; height: 100%; background: #fff; border-radius: 4px; transition: width 0.3s; }}
  .video-controls .time-label {{ font-size: 12px; color: #8a95a3; font-variant-numeric: tabular-nums; min-width: 90px; }}
  .speed-btn {{
    font-size: 12px; padding: 5px 9px; border: 1px solid #3a434e;
    border-radius: 8px; background: transparent; color: #8a95a3; cursor: pointer;
  }}

  .knowledge-card {{ margin: 16px 18px 0; padding: 18px; background: var(--surface); border-radius: var(--radius); border: 1px solid #e6e8ed; }}
  .knowledge-card h2 {{ font-size: 19px; margin: 8px 0; }}
  .knowledge-card p {{ line-height: 1.7; font-size: 13px; color: #59636f; }}
  .insight {{
    padding: 14px; border-radius: 11px;
    background: var(--orange-light); border: 1px solid var(--orange-border); margin-top: 14px;
  }}
  .insight p {{ font-size: 14px; line-height: 1.65; color: #7c5e00; margin-top: 8px; }}

  .transcript-sidebar {{
    border-bottom: 1px solid var(--border);
  }}
  .transcript-sidebar .ts-header {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 16px; flex-shrink: 0;
  }}
  .transcript-sidebar .ts-header b {{ font-size: 13px; }}
  .transcript-scroll {{ padding: 0 16px 12px; }}
  .transcript-line {{
    padding: 5px 7px; font-size: 13px; line-height: 1.7;
    color: var(--text-muted); cursor: pointer; transition: all 0.2s;
    border-radius: 6px;
  }}
  .transcript-line:hover {{ color: var(--text-secondary); background: #f6f7f9; }}
  .transcript-line.read {{ color: var(--text); }}
  .transcript-line.current {{
    color: var(--primary); font-weight: 500;
    background: var(--primary-light);
  }}
  .transcript-line .ts {{
    font-size: 11px; color: var(--text-muted); margin-right: 8px;
    font-variant-numeric: tabular-nums; opacity: 0.6;
  }}
  .transcript-line.current .ts {{ opacity: 1; color: var(--primary); }}

  .rail {{ padding: 18px; }}
  .railtitle {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
  .timeline {{ position: relative; }}
  .timeline::before {{
    content: ""; position: absolute; left: 20px; top: 8px; bottom: 8px;
    width: 2px; background: #e3e6eb;
  }}
  .event {{
    position: relative; padding: 0 12px 18px 48px; cursor: pointer;
  }}
  .dot {{
    position: absolute; left: 15px; top: 2px;
    width: 12px; height: 12px; border: 3px solid #fff;
    border-radius: 50%; background: #718096;
    box-shadow: 0 0 0 1px #ccd1d8;
  }}
  .event.highlight .dot {{ background: var(--orange); }}
  .event b {{ font-size: 12px; }}
  .event p {{ margin: 5px 0 0; font-size: 12px; line-height: 1.5; color: #69727e; }}
  .event:hover b {{ color: var(--primary); }}

  /* ══════ REVIEW PAGE ══════ */
  #page-review .layout {{ grid-template-columns: 250px 1fr 330px; }}
  #page-review .main {{ padding: 22px 26px; background: var(--bg); }}
  .reviewhead {{ display: flex; justify-content: space-between; align-items: end; margin-bottom: 18px; }}
  .reviewhead h1 {{ margin: 0; font-size: 26px; }}
  .scoregrid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px; }}
  .stat {{ padding: 15px; background: var(--surface); border-radius: var(--radius); border: 1px solid #e6e8ed; }}
  .stat b {{ font-size: 23px; display: block; margin-top: 7px; }}
  .reviewgrid {{ display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 14px; }}
  .panel {{ padding: 18px; background: var(--surface); border-radius: var(--radius); border: 1px solid #e6e8ed; }}
  .recall {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  .recallcard {{
    border: 1px solid #e2e6eb; border-radius: 11px;
    padding: 14px; cursor: pointer; transition: border-color 0.15s;
  }}
  .recallcard:hover {{ border-color: #b9c4d7; }}
  .recallcard .ans {{ display: none; margin-top: 10px; color: #59636f; line-height: 1.6; font-size: 13px; }}
  .recallcard.open .ans {{ display: block; }}
  .weak {{ padding: 12px; border: 1px solid #e6e8ed; border-radius: 10px; margin-top: 10px; }}
  .barline {{ height: 8px; background: #edf0f3; border-radius: 8px; overflow: hidden; }}
  .barline i {{ display: block; height: 100%; background: #6878a8; border-radius: 8px; }}
  .mini-timeline {{ margin-top: 8px; }}
  .mini {{
    display: flex; gap: 12px; padding: 10px 0;
    border-bottom: 1px solid var(--border-light); cursor: pointer;
  }}
  .mini .when {{ width: 52px; font-size: 11px; color: #6b7480; flex-shrink: 0; }}
  .mini b {{ font-size: 12px; }}
  .mini p {{ margin: 3px 0 0; font-size: 11px; color: #7a828d; }}
  .sourcejump {{
    padding: 12px; border-radius: 10px;
    background: #f7f8fa; border: 1px solid #e4e7ec; margin-top: 12px;
  }}

  /* ══════ PRACTICE PAGE ══════ */
  #page-practice .layout {{ grid-template-columns: 250px 1fr 330px; }}
  #page-practice .main {{ padding: 26px 30px; background: var(--bg); overflow-y: auto; }}
  .practice-header {{ margin-bottom: 20px; }}
  .practice-header h1 {{ font-size: 24px; margin-bottom: 6px; }}
  .practice-header p {{ color: var(--text-secondary); font-size: 14px; }}
  .practice-stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }}
  .practice-stat {{ padding: 16px; text-align: center; background: var(--surface); border-radius: var(--radius); border: 1px solid #e6e8ed; }}
  .practice-stat b {{ font-size: 28px; display: block; margin-top: 6px; color: var(--primary); }}
  .question-card {{ padding: 20px; background: var(--surface); border-radius: var(--radius); border: 1px solid #e6e8ed; margin-bottom: 16px; }}
  .question-card h3 {{ font-size: 15px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }}
  .question-type {{ font-size: 11px; padding: 3px 8px; border-radius: 5px; background: var(--primary-light); color: var(--primary); font-weight: 600; }}
  .question-text {{ font-size: 14px; line-height: 1.7; margin-bottom: 14px; color: var(--text); }}
  .options {{ display: flex; flex-direction: column; gap: 8px; }}
  .option {{
    padding: 12px 14px; border: 1px solid #e4e7ec; border-radius: 9px;
    cursor: pointer; transition: all 0.15s; font-size: 13px;
    display: flex; align-items: center; gap: 10px;
  }}
  .option:hover {{ border-color: var(--primary); background: #fafbff; }}
  .option.selected {{ border-color: var(--primary); background: var(--primary-light); }}
  .option.correct {{ border-color: var(--green); background: var(--green-light); }}
  .option.incorrect {{ border-color: var(--red); background: var(--red-light); }}
  .option-marker {{
    width: 22px; height: 22px; border-radius: 50%; border: 2px solid #ccd1d8;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 600; color: #68717d; flex-shrink: 0;
  }}
  .option.selected .option-marker {{ border-color: var(--primary); color: var(--primary); }}
  .option.correct .option-marker {{ border-color: var(--green); color: var(--green); background: var(--green-light); }}
  .option.incorrect .option-marker {{ border-color: var(--red); color: var(--red); background: var(--red-light); }}
  .fill-input {{
    width: 100%; padding: 10px 12px; border: 1px solid #dfe3e9;
    border-radius: 8px; font-size: 13px; outline: none;
  }}
  .fill-input:focus {{ border-color: var(--primary); }}
  .fill-input.correct {{ border-color: var(--green); background: var(--green-light); }}
  .fill-input.incorrect {{ border-color: var(--red); background: var(--red-light); }}
  .feedback {{
    margin-top: 12px; padding: 12px 14px; border-radius: 9px;
    font-size: 13px; line-height: 1.6; display: none;
  }}
  .feedback.show {{ display: block; }}
  .feedback.correct {{ background: var(--green-light); border: 1px solid #b8d4c0; color: #3d6347; }}
  .feedback.incorrect {{ background: var(--red-light); border: 1px solid #e0c4c4; color: #7a4545; }}
  .check-btn {{
    margin-top: 12px; padding: 9px 16px; background: var(--primary);
    color: #fff; border-radius: 8px; font-size: 13px; font-weight: 500;
  }}
  .check-btn:hover {{ background: var(--primary-dark); }}
  .check-btn:disabled {{ background: #ccd1d8; cursor: not-allowed; }}
  .progress-section {{ margin-top: 24px; }}
  .progress-section h2 {{ font-size: 16px; margin-bottom: 12px; }}
  .progress-bar-large {{
    height: 12px; background: #edf0f3; border-radius: 12px;
    overflow: hidden; margin-bottom: 8px;
  }}
  .progress-bar-large i {{
    display: block; height: 100%; background: var(--primary);
    border-radius: 12px; transition: width 0.3s;
  }}

  /* MISC */
  .muted {{ color: var(--text-muted); }}
  .small {{ font-size: 12px; }}
  .btn {{
    padding: 9px 13px; border-radius: 9px;
    background: #eef1f5; color: #34404d; font-size: 13px;
  }}
  .btn.primary {{ background: #1e293b; color: #fff; }}
  .btn.ghost {{ background: var(--surface); border: 1px solid #dfe3e9; }}
  .btn.primary-blue {{ background: var(--primary); color: #fff; }}
  .row {{ display: flex; align-items: center; gap: 10px; }}
  .pill {{
    font-size: 11px; padding: 4px 7px; border-radius: 6px;
    background: #f0f2f5; color: #68717d;
  }}
  .pill.active {{ background: var(--primary-light); color: var(--primary); }}
  .tag {{
    display: inline-block; font-size: 10px; padding: 3px 6px;
    border-radius: 5px; background: var(--primary-light); color: #4a5ea4;
  }}
  .tag.danger {{ background: var(--red-light); color: var(--red); }}
  .tag.success {{ background: var(--green-light); color: var(--green); }}
  .spacer {{ flex: 1; }}

  /* NOTE MODAL */
  .note-quick-btn {{
    padding: 5px 12px; background: var(--primary); color: #fff;
    border-radius: 8px; font-size: 12px; font-weight: 500;
    margin-left: auto; border: 0; cursor: pointer;
  }}
  .note-quick-btn:hover {{ background: var(--primary-dark); }}
  .my-note {{
    padding: 14px; border-radius: 11px;
    background: var(--blue-note-light); border: 1px solid var(--blue-note-border); margin-top: 12px;
  }}
  .my-note p {{ font-size: 13px; line-height: 1.6; color: #4a5080; margin-top: 8px; }}
  .notequick {{
    padding: 14px; background: var(--blue-note-light); border: 1px solid var(--blue-note-border);
    border-radius: var(--radius); margin-bottom: 14px;
  }}
  .notequick p {{ line-height: 1.6; }}

  /* SELECTION MODE */
  .selection-banner {{
    display: none; padding: 10px 16px; background: var(--primary-light);
    border-bottom: 1px solid #c8d4f0; font-size: 13px; color: var(--primary);
    align-items: center; gap: 8px;
  }}
  .selection-banner.active {{ display: flex; }}
  .selection-banner b {{ font-weight: 600; }}
  .transcript-line.selectable {{ cursor: pointer; }}
  .transcript-line.selectable:hover {{ background: #e8edf8; color: var(--text); }}
  .transcript-line.selected {{
    background: var(--primary-light); color: var(--primary);
    border-left: 3px solid var(--primary); padding-left: 4px;
  }}
  .selection-action-bar {{
    display: none; padding: 12px 16px;
    border-top: 1px solid var(--border);
    align-items: center; justify-content: space-between; gap: 12px;
  }}
  .selection-action-bar.active {{ display: flex; }}
  .selection-count {{ font-size: 13px; color: var(--text-secondary); }}
  .selection-count b {{ color: var(--primary); font-weight: 600; }}
  .selection-actions {{ display: flex; gap: 8px; }}
  .selection-actions .btn {{ font-size: 12px; padding: 7px 14px; }}

  .sidebar-bottom-wrapper {{
    position: sticky; bottom: 0; z-index: 6;
    display: flex; flex-direction: column;
    background: var(--surface);
    border-top: 1px solid var(--border);
  }}
  .scroll-back-btn {{
    position: sticky; top: 12px; z-index: 15;
    display: none; align-items: center; gap: 5px;
    padding: 6px 12px; margin-left: auto; margin-right: 12px; width: fit-content;
    background: var(--surface); color: var(--primary); border: 1px solid var(--primary); border-radius: 8px;
    font-size: 12px; font-weight: 500; cursor: pointer;
    box-shadow: 0 2px 8px rgba(49,87,183,0.15);
    transition: all 0.2s;
  }}
  .scroll-back-btn:hover {{ background: var(--primary-light); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(49,87,183,0.2); }}
  .modal {{
    position: fixed; inset: 0; z-index: 200;
    background: rgba(20,25,32,.42); display: none;
    align-items: center; justify-content: center;
  }}
  .modal.open {{ display: flex; }}
  .modalbox {{
    width: 520px; background: var(--surface); border-radius: 16px;
    padding: 22px; box-shadow: 0 20px 60px rgba(0,0,0,.18);
  }}
  .modalbox textarea {{
    width: 100%; min-height: 130px; border: 1px solid #dfe3e9;
    border-radius: 10px; padding: 12px; resize: vertical;
    font: inherit; outline: none;
  }}
  .modalbox textarea:focus {{ border-color: var(--primary); }}

  .toast {{
    position: fixed; right: 22px; bottom: 22px;
    background: #202832; color: #fff; padding: 11px 15px;
    border-radius: 9px; font-size: 13px;
    opacity: 0; transform: translateY(8px); transition: 0.2s;
    pointer-events: none; z-index: 300;
  }}
  .toast.show {{ opacity: 1; transform: none; }}
</style>
</head>
<body>
<div class="app">

<!-- TOP BAR -->
<header class="topbar" id="topbar">
  <div class="brand">CourseMap<span class="version-tag">V3</span></div>
  <span class="phase-badge" id="phaseBadge">PREVIEW · 预习</span>
  <span class="topbar-crumb" id="breadcrumb">
    <span>雅思备考</span> · <span class="current">阅读</span>
  </span>
  <div class="spacer"></div>
  <div class="phase-nav">
    <button class="phase-btn" onclick="switchPhase('preview')">预习</button>
    <div class="phase-separator"></div>
    <button class="phase-btn" onclick="switchPhase('learn')">学习</button>
    <div class="phase-separator"></div>
    <button class="phase-btn" onclick="switchPhase('review')">复习</button>
    <div class="phase-separator"></div>
    <button class="phase-btn" onclick="switchPhase('practice')">练习</button>
  </div>
  <span class="topbar-progress">总时长 <b>{duration_str}</b></span>
</header>

<!-- ══════ PREVIEW PAGE (Exploratory) ══════ -->
<div class="page active" id="page-preview">
  <div class="preview-layout">
    <aside class="preview-nav">
      <h3>课程目录</h3>
      <div id="preview-tree">
{nav_html}
      </div>
    </aside>
    <div class="preview-main">
      <div class="preview-hero">
        <h1>先探索，再学习</h1>
        <p class="subtitle">不用急着看视频。先花 3-5 分钟探索这节课的知识地图，带着问题听课，效果翻倍。</p>
        <div class="guiding-qs">
          <div class="gq" onclick="this.classList.toggle('answered')">这节课讲什么？</div>
          <div class="gq" onclick="this.classList.toggle('answered')">哪些是重点？</div>
          <div class="gq" onclick="this.classList.toggle('answered')">我需要解决什么问题？</div>
        </div>
      </div>

      <div class="explore-cards">
{chapters_html}
      </div>

      <div style="text-align:center; padding: 20px 0 40px;">
        <button class="btn ghost" style="padding: 12px 28px; font-size: 14px;" onclick="switchPhase('learn')">
          开始学习 →
        </button>
      </div>
    </div>

    <div class="preview-rail">
      <div class="discovery-header">
        <h3>探索进度</h3>
        <p>点击章节卡片，逐步发现课程内容</p>
      </div>

      <div class="progress-ring">
        <div class="big" id="discoveredCount">0</div>
        <div class="label">已发现 <span id="discoveredTotal">/{total_modules}</span> 个模块</div>
        <div class="progress-bar-v2"><div class="fill" id="discoveryBar" style="width:0%"></div></div>
      </div>

      <div class="chapter-status" id="chapterStatus">
        <!-- filled by JS -->
      </div>

      <div class="teacher-tip">
        <div class="tip-label">💡 老师提示</div>
        <p>不要急着看全部内容。先想想你对哪些最好奇，点进去探索。带着问题听课，效果翻倍。</p>
      </div>

      <div class="cta-area">
        <button class="cta-btn locked" id="ctaBtn" onclick="switchPhase('learn')">
          🔒 探索完再开始学习
        </button>
      </div>
    </div>
  </div>
</div>

<!-- ══════ LEARN PAGE ══════ -->
<div class="page" id="page-learn">
  <div class="layout">
    <aside class="side left">
      <h3>课程目录</h3>
      <div id="learn-tree">
{learn_nav_html}
      </div>
    </aside>
    <div class="main">
      <div class="video">
        <video id="mainVideo" src="{VIDEO_FILE}"></video>
        <div class="video-controls">
          <button class="speed-btn" id="playBtn" onclick="togglePlay()">▶ 播放</button>
          <div class="bar" onclick="seekBar(event)"><i id="bar" style="width:0%"></i></div>
          <span class="time-label"><span id="curTime">00:00</span> / {duration_str}</span>
          <button class="speed-btn" id="speed" onclick="cycleSpeed()">1×</button>
          <button class="note-quick-btn" onclick="enterSelectionMode()">＋ 记录想法</button>
        </div>
      </div>
      <div class="knowledge-card">
        <span class="pill">当前知识节点</span>
        <h2 id="kcTitle">课程总览</h2>
        <p id="kcDesc">导学视频概览：考情介绍 + 学习计划 + 课程要求</p>
        <div class="insight">
          <span class="pill">★ 老师敲黑板</span>
          <p id="kcInsight">即使已经上过第一次直播课，也一定要把这个导学视频看完。</p>
        </div>
        <div class="my-note">
          <span class="pill">💭 我的思考</span>
          <p id="kcNote">"先了解考试整体结构，再进入具体题型的学习。"</p>
          <button class="btn" style="margin-top:9px" onclick="openNoteModal()">编辑我的思考</button>
        </div>
        <div style="margin-top:14px;display:flex;gap:8px">
          <button class="btn ghost" onclick="switchPhase('practice')">📝 去练习</button>
          <button class="btn ghost" onclick="switchPhase('review')">🔄 去复习</button>
        </div>
      </div>
    </div>
    <aside class="side right">
      <button class="scroll-back-btn" id="scrollBackBtn" onclick="scrollToCurrentLine()">↩ 回到当前播放位置</button>
      <div class="transcript-sidebar">
        <div class="ts-header">
          <b>原文字幕</b>
          <span class="pill" id="tsModePill">点击跳转</span>
        </div>
        <div class="selection-banner" id="selectionBanner">
          <b>🎯</b> 点击选择相关原文（可多选）
        </div>
        <div class="transcript-scroll">
{transcript_html}
        </div>
      </div>
      <div class="sidebar-bottom-wrapper">
        <div class="selection-action-bar" id="selectionActionBar">
          <span class="selection-count">已选择 <b id="selectionCount">0</b> 段</span>
          <div class="selection-actions">
            <button class="btn ghost" onclick="exitSelectionMode()">取消</button>
            <button class="btn primary-blue" onclick="confirmSelection()">确认并记录想法 →</button>
          </div>
        </div>
        <div class="notequick">
          <b style="font-size:13px">此刻发生了什么？</b>
          <p class="muted small">视频正在讲一个知识点。你的笔记会自动绑定当前时间，并在课后归入对应节点。</p>
          <button class="btn primary-blue" style="width:100%;margin-top:10px" onclick="enterSelectionMode()">＋ 记录此刻想法</button>
        </div>
      </div>
    </aside>
  </div>
</div>

<!-- ══════ REVIEW PAGE ══════ -->
<div class="page" id="page-review">
  <div class="layout">
    <aside class="side left">
      <h3>课程目录</h3>
      <div id="review-tree">
{nav_html}
      </div>
    </aside>
    <div class="main">
      <div class="reviewhead">
        <div>
          <h1>2 分钟，把整节课重新想一遍</h1>
          <div class="muted small" style="margin-top:6px">复习不是重看视频，而是先回忆 → 再验证 → 最后溯源。</div>
        </div>
        <button class="btn primary" onclick="startReview()">开始快速复习</button>
        <button class="btn primary-blue" style="margin-left:8px" onclick="switchPhase('practice')">进入练习 →</button>
      </div>
      <div class="scoregrid">
        <div class="stat"><span class="muted small">知识模块</span><b>{sum(len(n["children"]) for n in knowledge_tree)}</b><span class="muted small">本节覆盖</span></div>
        <div class="stat"><span class="muted small">老师重点</span><b>7</b><span class="muted small">可回溯</span></div>
        <div class="stat"><span class="muted small">我的想法</span><b>2</b><span class="muted small">自动挂到知识点</span></div>
        <div class="stat"><span class="muted small">待掌握</span><b>2</b><span class="muted small">建议优先复习</span></div>
      </div>
      <div class="reviewgrid">
        <section class="panel">
          <div class="row" style="justify-content:space-between">
            <div><b>① 先回忆，不看答案</b><div class="muted small" style="margin-top:4px">点击卡片，写在脑中的答案会被揭示</div></div>
            <span class="tag success">主动回忆</span>
          </div>
          <div class="recall" style="margin-top:14px">
            <div class="recallcard" onclick="this.classList.toggle('open')">
              <b>填空和判断占多少题？</b>
              <div class="ans">{html.escape(preview_cards[1]["highlight"])}</div>
            </div>
            <div class="recallcard" onclick="this.classList.toggle('open')">
              <b>7 分需要错几题以内？</b>
              <div class="ans">{html.escape(preview_cards[2]["highlight"])}</div>
            </div>
            <div class="recallcard" onclick="this.classList.toggle('open')">
              <b>剑桥真题怎么用？</b>
              <div class="ans">{html.escape(preview_cards[3]["highlight"])}</div>
            </div>
            <div class="recallcard" onclick="this.classList.toggle('open')">
              <b>为什么要整套做真题？</b>
              <div class="ans">{html.escape(preview_cards[3]["highlight"])}</div>
            </div>
          </div>
          <div style="margin-top:18px">
            <b>② 你的薄弱点</b>
            <div class="weak">
              <div class="row"><span>评分标准细节</span><div class="spacer"></div><span class="tag danger">还没掌握</span></div>
              <div class="barline" style="margin-top:9px"><i style="width:28%"></i></div>
              <button class="btn" style="margin-top:10px" onclick="seekTo(720)">回到 12:00 老师原文</button>
            </div>
            <div class="weak">
              <div class="row"><span>题型整体框架</span><div class="spacer"></div><span class="tag">模糊</span></div>
              <div class="barline" style="margin-top:9px"><i style="width:55%"></i></div>
            </div>
          </div>
        </section>
        <section class="panel">
          <div class="row" style="justify-content:space-between">
            <b>③ 课程知识时间轴</b>
            <span class="tag success">快速回看</span>
          </div>
          <p class="muted small" style="line-height:1.6">只看关键节点；需要深入时，再回到老师原文和视频。</p>
          <div class="mini-timeline">
            <div class="mini" onclick="seekTo(78)"><span class="when">01:18</span><div><b>考试基本信息</b><p>建立考试整体框架</p></div></div>
            <div class="mini" onclick="seekTo(200)"><span class="when">03:20</span><div><b>题型总览</b><p>基础→细节→过渡→宏观</p></div></div>
            <div class="mini" onclick="seekTo(720)"><span class="when">12:00</span><div><b>★ 评分标准</b><p>错 10 题=7 分关键线</p></div></div>
            <div class="mini" onclick="seekTo(1095)"><span class="when">18:15</span><div><b>刷题顺序</b><p>C13→C4→C9→C15</p></div></div>
            <div class="mini" onclick="seekTo(1340)"><span class="when">22:20</span><div><b>课程大纲</b><p>启航班 vs 飞跃班</p></div></div>
          </div>
          <div class="sourcejump">
            <b style="font-size:13px">④ 最后再溯源</b>
            <p class="muted small" style="line-height:1.6">你刚才没记住的，不需要重新看 34 分钟。直接跳到对应老师原文 / 视频位置。</p>
            <button class="btn primary" style="margin-top:10px" onclick="seekTo(720)">▶ 定位老师原文 12:00</button>
          </div>
        </section>
      </div>
    </div>
    <aside class="side right">
      <h3>本次复习结果</h3>
      <div style="padding:0 16px">
        <div class="card" style="padding:15px;margin-bottom:11px;background:var(--surface);border-radius:var(--radius);border:1px solid #e6e8ed">
          <b style="font-size:13px">知识掌握</b>
          <div style="font-size:30px;font-weight:800;margin:7px 0">{sum(len(n["children"]) for n in knowledge_tree) - 2} / {sum(len(n["children"]) for n in knowledge_tree)}</div>
          <div class="barline"><i style="width:78%"></i></div>
          <p class="muted small" style="line-height:1.6">你已经覆盖大部分知识点。剩下 2 个薄弱点可以直接进入原文。</p>
        </div>
        <div class="card" style="padding:15px;margin-bottom:11px;background:var(--surface);border-radius:var(--radius);border:1px solid #e6e8ed">
          <b style="font-size:13px">老师重点</b>
          <p class="muted small">★ {html.escape(preview_cards[0]["highlight"][:25])}...</p>
          <p class="muted small">★ {html.escape(preview_cards[1]["highlight"][:25])}...</p>
          <p class="muted small">★ {html.escape(preview_cards[2]["highlight"][:25])}...</p>
          <button class="btn" style="width:100%;margin-top:8px" onclick="toast('已打开老师重点列表')">查看全部重点</button>
        </div>
        <div class="card" style="padding:15px;background:var(--surface);border-radius:var(--radius);border:1px solid #e6e8ed">
          <b style="font-size:13px">我的学习轨迹</b>
          <p class="muted small">💭 2 条想法</p>
          <p class="muted small">🔗 2 个自动归类节点</p>
          <p class="muted small">🎯 2 个待掌握</p>
          <button class="btn primary-blue" style="width:100%;margin-top:8px" onclick="toast('已生成下一次复习入口')">安排下一次复习</button>
        </div>
      </div>
    </aside>
  </div>
</div>

<!-- ══════ PRACTICE PAGE ══════ -->
<div class="page" id="page-practice">
  <div class="layout">
    <aside class="side left">
      <h3>课程目录</h3>
      <div id="practice-tree">
{nav_html}
      </div>
    </aside>
    <div class="main">
      <div class="practice-header">
        <h1>练一练，检验学习效果</h1>
        <p>基于本节课程内容，练习雅思阅读核心题型。答完即时反馈，薄弱点自动标记。</p>
      </div>
      <div class="practice-stats">
        <div class="practice-stat"><span class="muted small">总题数</span><b>7</b></div>
        <div class="practice-stat"><span class="muted small">已完成</span><b id="doneCount">0</b></div>
        <div class="practice-stat"><span class="muted small">正确率</span><b id="accuracy">--</b></div>
        <div class="practice-stat"><span class="muted small">预计用时</span><b>5 min</b></div>
      </div>

      <div id="questionList">
        <!-- Q1 -->
        <div class="question-card" data-qid="0" data-type="choice" data-answer="1">
          <h3><span class="question-type">选择题</span> 第 1 题</h3>
          <div class="question-text">雅思阅读考试的总时长是多少？</div>
          <div class="options">
            <div class="option" onclick="selectOption(this, 0)"><span class="option-marker">A</span>30 分钟</div>
            <div class="option" onclick="selectOption(this, 1)"><span class="option-marker">B</span>60 分钟</div>
            <div class="option" onclick="selectOption(this, 2)"><span class="option-marker">C</span>90 分钟</div>
            <div class="option" onclick="selectOption(this, 3)"><span class="option-marker">D</span>120 分钟</div>
          </div>
          <button class="check-btn" onclick="checkAnswer(this)" disabled>检查答案</button>
          <div class="feedback correct">✓ 正确！雅思阅读考试时间为 60 分钟（含填写答题卡时间），3 篇文章共 40 题。</div>
          <div class="feedback incorrect">✗ 再想想。提示：回忆老师说的"不管纸笔还是机考，60 分钟都包含答题和填写答题卡的时间"。</div>
        </div>

        <!-- Q2 -->
        <div class="question-card" data-qid="1" data-type="choice" data-answer="2">
          <h3><span class="question-type">选择题</span> 第 2 题</h3>
          <div class="question-text">雅思阅读想要考到 7 分，最多可以错几道题？</div>
          <div class="options">
            <div class="option" onclick="selectOption(this, 0)"><span class="option-marker">A</span>7 个</div>
            <div class="option" onclick="selectOption(this, 1)"><span class="option-marker">B</span>10 个</div>
            <div class="option" onclick="selectOption(this, 2)"><span class="option-marker">C</span>13 个</div>
            <div class="option" onclick="selectOption(this, 3)"><span class="option-marker">D</span>15 个</div>
          </div>
          <button class="check-btn" onclick="checkAnswer(this)" disabled>检查答案</button>
          <div class="feedback correct">✓ 正确！错 10 个以内 = 7 分以上。错 7 个以内 = 7.5 分，错 13-14 个 = 6.5 分。</div>
          <div class="feedback incorrect">✗ 再想想。提示：老师说"错超过 10 个就低于 7 分"——所以 7 分的关键线是 10 个以内。</div>
        </div>

        <!-- Q3 -->
        <div class="question-card" data-qid="2" data-type="choice" data-answer="1">
          <h3><span class="question-type">选择题</span> 第 3 题</h3>
          <div class="question-text">以下哪种题型组合在雅思阅读中占比最大（约 20 题 / 40 题）？</div>
          <div class="options">
            <div class="option" onclick="selectOption(this, 0)"><span class="option-marker">A</span>选择题 + 匹配题</div>
            <div class="option" onclick="selectOption(this, 1)"><span class="option-marker">B</span>填空题 + 判断题</div>
            <div class="option" onclick="selectOption(this, 2)"><span class="option-marker">C</span>Heading 题 + 填空题</div>
            <div class="option" onclick="selectOption(this, 3)"><span class="option-marker">D</span>匹配题 + 判断题</div>
          </div>
          <button class="check-btn" onclick="checkAnswer(this)" disabled>检查答案</button>
          <div class="feedback correct">✓ 正确！填空题 + 判断题占约 20 题（总共 40 题），是必须把握的核心拿分题型。</div>
          <div class="feedback incorrect">✗ 再想想。提示：老师说"填空 + 判断占约 20 题，是必须把握的基础题型"。</div>
        </div>

        <!-- Q4 -->
        <div class="question-card" data-qid="3" data-type="tfng" data-answer="true">
          <h3><span class="question-type">判断题</span> 第 4 题</h3>
          <div class="question-text">雅思阅读考试的 3 篇文章难度是逐篇递增的，第 3 篇通常最难。</div>
          <div class="options">
            <div class="option" onclick="selectOption(this, 0)" data-val="true"><span class="option-marker">✓</span>True</div>
            <div class="option" onclick="selectOption(this, 1)" data-val="false"><span class="option-marker">✗</span>False</div>
            <div class="option" onclick="selectOption(this, 2)" data-val="ng"><span class="option-marker">?</span>Not Given</div>
          </div>
          <button class="check-btn" onclick="checkAnswer(this)" disabled>检查答案</button>
          <div class="feedback correct">✓ 正确！老师明确说"难度逐篇递增，第 3 篇通常最难（不一定，但基本上如此）"。</div>
          <div class="feedback incorrect">✗ 再想想。提示：回忆老师关于文章难度分布的描述——"难度递增"是基本规律。</div>
        </div>

        <!-- Q5 -->
        <div class="question-card" data-qid="4" data-type="tfng" data-answer="false">
          <h3><span class="question-type">判断题</span> 第 5 题</h3>
          <div class="question-text">使用剑桥雅思真题刷题时，可以每天只做一篇，不需要整套完成。</div>
          <div class="options">
            <div class="option" onclick="selectOption(this, 0)" data-val="true"><span class="option-marker">✓</span>True</div>
            <div class="option" onclick="selectOption(this, 1)" data-val="false"><span class="option-marker">✗</span>False</div>
            <div class="option" onclick="selectOption(this, 2)" data-val="ng"><span class="option-marker">?</span>Not Given</div>
          </div>
          <button class="check-btn" onclick="checkAnswer(this)" disabled>检查答案</button>
          <div class="feedback correct">✓ 正确！老师强调"一旦开始做剑 9-12，一定要整套完成，不能今天做一篇明天做一篇"。</div>
          <div class="feedback incorrect">✗ 再想想。提示：老师特别强调过刷题要"整套完成"，不能零散地做。</div>
        </div>

        <!-- Q6 -->
        <div class="question-card" data-qid="5" data-type="fill" data-answer="定位">
          <h3><span class="question-type">填空题</span> 第 6 题</h3>
          <div class="question-text">雅思阅读解题的基础能力是 ______ 和同义替换。（填入两个字的关键词）</div>
          <input class="fill-input" type="text" placeholder="输入你的答案…" oninput="onFillInput(this)">
          <button class="check-btn" onclick="checkFill(this)" disabled>检查答案</button>
          <div class="feedback correct">✓ 正确！"定位"和"同义替换"是所有题型的基础，课程会先从这里开始。</div>
          <div class="feedback incorrect">✗ 再想想。提示：老师说"____ 和同义替换是所有题型的基础知识"——回忆课程解题逻辑的起点。</div>
        </div>

        <!-- Q7 -->
        <div class="question-card" data-qid="6" data-type="fill" data-answer="正确率">
          <h3><span class="question-type">填空题</span> 第 7 题</h3>
          <div class="question-text">做真题时，______ 的重要性大于速度，先保证它再慢慢提速。（填入三个字）</div>
          <input class="fill-input" type="text" placeholder="输入你的答案…" oninput="onFillInput(this)">
          <button class="check-btn" onclick="checkFill(this)" disabled>检查答案</button>
          <div class="feedback correct">✓ 正确！老师说"正确率的重要性大于速度，先保证正确率再慢慢提速"。</div>
          <div class="feedback incorrect">✗ 再想想。提示：老师说的是做题时先保证什么，再提速？不是速度，而是另一个维度。</div>
        </div>
      </div>

      <div class="progress-section">
        <div class="card" style="padding:18px;background:var(--surface);border-radius:var(--radius);border:1px solid #e6e8ed">
          <div class="row" style="justify-content:space-between;margin-bottom:10px">
            <b>练习进度</b>
            <span class="muted small" id="progressLabel">0 / 7 已完成</span>
          </div>
          <div class="progress-bar-large"><i id="practiceProgress" style="width:0%"></i></div>
          <div class="row" style="margin-top:12px">
            <button class="btn ghost" onclick="resetPractice()">重新练习</button>
            <div class="spacer"></div>
            <button class="btn primary-blue" onclick="switchPhase('review')">进入复习 →</button>
          </div>
        </div>
      </div>
    </div>
    <aside class="side right">
      <h3>练习结果</h3>
      <div style="padding:0 16px">
        <div class="card" style="padding:15px;margin-bottom:11px;background:var(--surface);border-radius:var(--radius);border:1px solid #e6e8ed">
          <b style="font-size:13px">答题统计</b>
          <div id="resultSummary" style="margin-top:10px">
            <p class="muted small">还没有完成任何题目</p>
          </div>
        </div>
        <div class="card" style="padding:15px;margin-bottom:11px;background:var(--surface);border-radius:var(--radius);border:1px solid #e6e8ed">
          <b style="font-size:13px">薄弱知识点</b>
          <div id="weakPoints" style="margin-top:10px">
            <p class="muted small">答完题后自动标记</p>
          </div>
        </div>
        <div class="card" style="padding:15px;background:var(--surface);border-radius:var(--radius);border:1px solid #e6e8ed">
          <b style="font-size:13px">关联课程节点</b>
          <div style="margin-top:10px">
            <div class="tree-item" onclick="seekTo(78)" style="padding:8px 0;font-size:12px">📖 考试基本信息 → 01:18</div>
            <div class="tree-item" onclick="seekTo(495)" style="padding:8px 0;font-size:12px">📖 评分标准 → 08:15</div>
            <div class="tree-item" onclick="seekTo(1050)" style="padding:8px 0;font-size:12px">📖 刷题策略 → 17:30</div>
          </div>
        </div>
      </div>
    </aside>
  </div>
</div>

</div><!-- .app -->

<!-- NOTE MODAL -->
<div class="modal" id="noteModal">
  <div class="modalbox">
    <div class="row">
      <b>记录我的想法</b>
      <div class="spacer"></div>
      <span class="pill" id="modalTime">00:00 · 知识节点</span>
    </div>
    <div id="modalSelectedTranscript" style="display:none;margin:10px 0;padding:10px 12px;background:#f6f8fc;border:1px solid #e0e6f0;border-radius:8px">
      <div style="font-size:12px;color:var(--text-secondary);margin-bottom:6px">📌 针对以下原文：</div>
      <div id="modalTranscriptSummary" style="font-size:12px;color:var(--text);line-height:1.6;max-height:80px;overflow-y:auto"></div>
    </div>
    <p class="muted small" style="margin:8px 0">保存后会自动绑定时间；AI 稍后把它归入对应知识节点。</p>
    <textarea id="noteText" placeholder="例如：这里老师说填空和判断最容易混，我想回去找一个具体例子……"></textarea>
    <div class="row" style="justify-content:flex-end;margin-top:12px">
      <button class="btn" onclick="closeNoteModal()">取消</button>
      <button class="btn primary" onclick="saveNote()">保存想法</button>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
  // Set initial active phase button
  document.addEventListener('DOMContentLoaded', function() {{
    const firstBtn = document.querySelector('.phase-btn');
    if (firstBtn) firstBtn.classList.add('active');
  }});

  const video = document.getElementById('mainVideo');
  const transcriptLines = document.querySelectorAll('.transcript-line');
  const treeNodes = document.querySelectorAll('#learn-tree .tree-item');

  // Navigation
  function switchPhase(phase) {{
    const pages = {{ preview: 'page-preview', learn: 'page-learn', review: 'page-review', practice: 'page-practice' }};
    const badges = {{ preview: 'PREVIEW · 预习', learn: 'CLASS · 网课', review: 'REVIEW · 复习', practice: 'PRACTICE · 练习' }};
    const btnTexts = {{ preview: '预习', learn: '学习', review: '复习', practice: '练习' }};
    const phaseOrder = ['preview', 'learn', 'review', 'practice'];
    const currentIdx = phaseOrder.indexOf(phase);
    
    document.querySelectorAll('.page').forEach(p => {{
      if (Object.values(pages).includes(p.id)) p.classList.remove('active');
    }});
    document.getElementById(pages[phase]).classList.add('active');
    document.getElementById('phaseBadge').textContent = badges[phase];
    
    // Update phase button active state
    document.querySelectorAll('.phase-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.phase-btn').forEach(btn => {{
      if (btn.textContent.trim() === btnTexts[phase]) btn.classList.add('active');
    }});
    
    // Update arrow separators - passed arrows turn blue
    const separators = document.querySelectorAll('.phase-separator');
    separators.forEach((sep, i) => {{
      sep.classList.toggle('passed', i < currentIdx);
    }});
  }}

  // Video controls
  let playing = false;
  let speeds = [1, 1.25, 1.5];
  let speedIdx = 0;

  function togglePlay() {{
    if (!video) return;
    if (playing) {{ video.pause(); document.getElementById('playBtn').textContent = '▶ 播放'; }}
    else {{ video.play(); document.getElementById('playBtn').textContent = '❚❚ 暂停'; }}
    playing = !playing;
  }}

  function cycleSpeed() {{
    speedIdx = (speedIdx + 1) % speeds.length;
    if (video) video.playbackRate = speeds[speedIdx];
    document.getElementById('speed').textContent = speeds[speedIdx] + '×';
  }}

  function seekBar(e) {{
    if (!video) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const pct = (e.clientX - rect.left) / rect.width;
    video.currentTime = pct * video.duration;
  }}

  function seekTo(sec) {{
    if (!video) return;
    video.currentTime = sec;
    video.play();
    playing = true;
    document.getElementById('playBtn').textContent = '❚❚ 暂停';
    switchPhase('learn');
    // Scroll transcript to matching line
    transcriptLines.forEach(line => {{
      const start = parseFloat(line.dataset.start);
      const end = parseFloat(line.dataset.end);
      if (sec >= start && sec < end) {{
        line.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      }}
    }});
    userHasScrolled = false;
    if (scrollBackBtn) scrollBackBtn.style.display = 'none';
    toast('已定位到 ' + fmtTime(sec));
  }}

  // Video + Transcript sync
  let userHasScrolled = false;
  const rightSidebar = document.querySelector('#page-learn .side.right');
  const scrollBackBtn = document.getElementById('scrollBackBtn');
  if (rightSidebar) {{
    rightSidebar.addEventListener('wheel', () => {{
      userHasScrolled = true;
      if (scrollBackBtn) scrollBackBtn.style.display = 'flex';
    }}, {{ passive: true }});
    rightSidebar.addEventListener('touchmove', () => {{
      userHasScrolled = true;
      if (scrollBackBtn) scrollBackBtn.style.display = 'flex';
    }}, {{ passive: true }});
  }}

  function scrollToCurrentLine() {{
    const current = document.querySelector('.transcript-line.current');
    if (current && rightSidebar) {{
      current.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      userHasScrolled = false;
      if (scrollBackBtn) scrollBackBtn.style.display = 'none';
    }}
  }}

  if (video) {{
    video.addEventListener('timeupdate', function() {{
      const t = video.currentTime;
      document.getElementById('bar').style.width = (t / video.duration * 100) + '%';
      document.getElementById('curTime').textContent = fmtTime(t);

      transcriptLines.forEach(line => {{
        const start = parseFloat(line.dataset.start);
        const end = parseFloat(line.dataset.end);
        line.classList.remove('read', 'current');
        if (t >= start && t < end) {{
          line.classList.add('current');
        }} else if (t >= end) {{
          line.classList.add('read');
        }}
      }});

      treeNodes.forEach(node => {{
        const start = parseFloat(node.dataset.start);
        const end = parseFloat(node.dataset.end);
        node.classList.remove('active', 'in-range');
        if (t >= start && t < end) {{
          node.classList.add('in-range');
        }}
        if (t >= start && t < end && !node.classList.contains('tree-child')) {{
          node.classList.add('active');
        }}
        if (t >= start && t < end && node.classList.contains('tree-child')) {{
          node.classList.add('active');
          node.classList.remove('in-range');
        }}
      }});
    }});

    video.addEventListener('ended', function() {{
      playing = false;
      document.getElementById('playBtn').textContent = '▶ 播放';
    }});

    transcriptLines.forEach(line => {{
      line.addEventListener('click', function() {{
        if (selectionMode) return;
        video.currentTime = parseFloat(this.dataset.start);
        video.play();
        playing = true;
        document.getElementById('playBtn').textContent = '❚❚ 暂停';
      }});
    }});
  }}

  // ══════ EXPLORATORY PREVIEW ══════
  const discovered = new Set();
  const chapterModules = {json.dumps({str(ch['num']): len(ch['modules']) for ch in chapters})};

  function expandChapter(num) {{
    const card = document.getElementById('ch' + num);
    card.classList.toggle('expanded');
  }}

  function scrollToChapter(num) {{
    const card = document.getElementById('ch' + num);
    if (card) {{
      if (!card.classList.contains('expanded')) card.classList.add('expanded');
      card.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}
  }}

  function revealModule(el, chNum, modIdx) {{
    event.stopPropagation();
    const key = chNum + '-' + modIdx;
    if (discovered.has(key)) return;
    discovered.add(key);
    el.classList.add('revealed');
    const insight = document.getElementById('insight-' + chNum + '-' + modIdx);
    if (insight) insight.classList.add('show');
    updateDiscoveryUI();
  }}

  function updateDiscoveryUI() {{
    const count = discovered.size;
    const total = {total_modules};
    document.getElementById('discoveredCount').textContent = count;
    document.getElementById('discoveryBar').style.width = (count / total * 100) + '%';

    // Update chapter status
    const statusEl = document.getElementById('chapterStatus');
    statusEl.innerHTML = '';
    for (let ch = 1; ch <= 5; ch++) {{
      const mods = chapterModules[ch];
      let revealed = 0;
      for (let m = 0; m < mods; m++) {{
        if (discovered.has(ch + '-' + m)) revealed++;
      }}
      const pct = revealed / mods;
      let cls = '';
      if (pct > 0 && pct < 1) cls = 'partial';
      if (pct === 1) cls = 'complete';
      statusEl.innerHTML += '<div class="ch-status ' + cls + '" onclick="expandChapter(' + ch + ')">' +
        '<div class="ch-dot"></div>' +
        '<div class="ch-label">第' + ch + '章</div>' +
        '<div class="ch-count">' + revealed + '/' + mods + '</div>' +
        '</div>';
    }}

    // Update CTA button
    const ctaBtn = document.getElementById('ctaBtn');
    if (count >= 5) {{
      ctaBtn.classList.remove('locked');
      ctaBtn.innerHTML = '🚀 开始学习 →';
    }} else {{
      ctaBtn.classList.add('locked');
      ctaBtn.innerHTML = '🔒 再探索 ' + (5 - count) + ' 个模块解锁';
    }}

    // Update chapter card states
    for (let ch = 1; ch <= 5; ch++) {{
      const card = document.getElementById('ch' + ch);
      const mods = chapterModules[ch];
      let revealed = 0;
      for (let m = 0; m < mods; m++) {{
        if (discovered.has(ch + '-' + m)) revealed++;
      }}
      if (revealed === mods) {{
        card.classList.add('discovered');
      }} else {{
        card.classList.remove('discovered');
      }}
    }}
  }}

  // ══════ PRACTICE ══════
  const practiceState = {{ answered: new Set(), correct: new Set() }};

  function selectOption(el, idx) {{
    const card = el.closest('.question-card');
    if (card.classList.contains('answered')) return;
    card.querySelectorAll('.option').forEach(o => o.classList.remove('selected'));
    el.classList.add('selected');
    card.querySelector('.check-btn').disabled = false;
    card.dataset.selected = idx;
  }}

  function checkAnswer(btn) {{
    const card = btn.closest('.question-card');
    if (card.classList.contains('answered')) return;
    card.classList.add('answered');
    const qid = parseInt(card.dataset.qid);
    const answerIdx = parseInt(card.dataset.answer);
    const selectedIdx = parseInt(card.dataset.selected);
    const isCorrect = selectedIdx === answerIdx;

    card.querySelectorAll('.option').forEach((o, i) => {{
      o.style.cursor = 'default';
      if (i === answerIdx) o.classList.add('correct');
      else if (i === selectedIdx && !isCorrect) o.classList.add('incorrect');
    }});

    btn.style.display = 'none';
    card.querySelector(isCorrect ? '.feedback.correct' : '.feedback.incorrect').classList.add('show');

    practiceState.answered.add(qid);
    if (isCorrect) practiceState.correct.add(qid);
    updatePracticeUI();
  }}

  function onFillInput(input) {{
    const card = input.closest('.question-card');
    card.querySelector('.check-btn').disabled = !input.value.trim();
    card.dataset.selected = input.value.trim();
  }}

  function checkFill(btn) {{
    const card = btn.closest('.question-card');
    if (card.classList.contains('answered')) return;
    card.classList.add('answered');
    const qid = parseInt(card.dataset.qid);
    const answer = card.dataset.answer;
    const selected = card.dataset.selected || '';
    const isCorrect = selected === answer;

    const input = card.querySelector('.fill-input');
    input.classList.add(isCorrect ? 'correct' : 'incorrect');
    input.readOnly = true;
    btn.style.display = 'none';

    card.querySelector(isCorrect ? '.feedback.correct' : '.feedback.incorrect').classList.add('show');

    practiceState.answered.add(qid);
    if (isCorrect) practiceState.correct.add(qid);
    updatePracticeUI();
  }}

  function updatePracticeUI() {{
    const total = 7;
    const done = practiceState.answered.size;
    const correct = practiceState.correct.size;
    document.getElementById('doneCount').textContent = done;
    document.getElementById('accuracy').textContent = done > 0 ? Math.round(correct / done * 100) + '%' : '--';
    document.getElementById('practiceProgress').style.width = (done / total * 100) + '%';
    document.getElementById('progressLabel').textContent = done + ' / ' + total + ' 已完成';

    const summaryEl = document.getElementById('resultSummary');
    if (done > 0) {{
      const weakNames = [];
      document.querySelectorAll('.question-card').forEach(c => {{
        const qid = parseInt(c.dataset.qid);
        if (practiceState.answered.has(qid) && !practiceState.correct.has(qid)) {{
          weakNames.push('第 ' + (qid + 1) + ' 题');
        }}
      }});
      summaryEl.innerHTML =
        '<div style="font-size:24px;font-weight:800;color:var(--primary);margin-bottom:6px">' + correct + ' / ' + done + '</div>' +
        '<p class="muted small">正确 ' + correct + ' 题，错误 ' + (done - correct) + ' 题</p>' +
        (weakNames.length > 0 ? '<div style="margin-top:8px"><span class="tag danger">需复习</span> <span class="muted small">' + weakNames.join('、') + '</span></div>' : '<div style="margin-top:8px"><span class="tag success">全部正确</span></div>');

      const weakEl = document.getElementById('weakPoints');
      if (weakNames.length > 0) {{
        weakEl.innerHTML = weakNames.map(n => '<p class="muted small" style="margin-bottom:4px">🔴 ' + n + ' → <a style="color:var(--primary);cursor:pointer" onclick="switchPhase(\\"learn\\")">回到课程</a></p>').join('');
      }} else {{
        weakEl.innerHTML = '<p class="muted small" style="color:var(--green)">✓ 暂无薄弱点</p>';
      }}
    }}
  }}

  function resetPractice() {{
    practiceState.answered.clear();
    practiceState.correct.clear();
    document.querySelectorAll('.question-card').forEach(c => {{
      c.classList.remove('answered');
      c.querySelectorAll('.option').forEach(o => {{
        o.classList.remove('selected', 'correct', 'incorrect');
        o.style.cursor = 'pointer';
      }});
      c.querySelectorAll('.feedback').forEach(f => f.classList.remove('show'));
      c.querySelector('.check-btn').style.display = '';
      c.querySelector('.check-btn').disabled = true;
      const input = c.querySelector('.fill-input');
      if (input) {{ input.classList.remove('correct', 'incorrect'); input.value = ''; input.readOnly = false; }}
    }});
    updatePracticeUI();
    document.getElementById('resultSummary').innerHTML = '<p class="muted small">还没有完成任何题目</p>';
    document.getElementById('weakPoints').innerHTML = '<p class="muted small">答完题后自动标记</p>';
  }}

  function scrollToQuestion(idx) {{
    const cards = document.querySelectorAll('.question-card');
    if (cards[idx]) cards[idx].scrollIntoView({{ behavior: 'smooth', block: 'center' }});
  }}

  // Review
  function startReview() {{ toast('进入主动回忆模式：先点卡片，不急着看答案'); }}

  // ══════ SELECTION MODE ══════
  let selectionMode = false;
  let selectionStart = null;
  let selectionEnd = null;

  function enterSelectionMode() {{
    selectionMode = true;
    selectionEnd = null;
    document.getElementById('selectionBanner').classList.add('active');
    document.getElementById('selectionActionBar').classList.add('active');
    document.getElementById('tsModePill').textContent = '选择模式';
    document.getElementById('tsModePill').classList.add('active');
    transcriptLines.forEach(line => {{
      line.classList.add('selectable');
      line.classList.remove('selected');
    }});
    if (video) {{ video.pause(); playing = false; document.getElementById('playBtn').textContent = '▶ 播放'; }}

    // Auto-select current line
    const currentTime = video ? video.currentTime : 0;
    let currentIdx = 0;
    transcriptLines.forEach((line, idx) => {{
      const start = parseFloat(line.dataset.start);
      const end = parseFloat(line.dataset.end);
      if (currentTime >= start && currentTime < end) {{
        currentIdx = idx;
      }}
    }});
    selectionStart = currentIdx;
    transcriptLines[currentIdx].classList.add('selected');
    document.getElementById('selectionBanner').innerHTML = '<b>🎯</b> 点击选择结束行，或直接提交想法';
    document.getElementById('selectionCount').textContent = '1';
    transcriptLines[currentIdx].scrollIntoView({{ behavior: 'smooth', block: 'center' }});
  }}

  function exitSelectionMode() {{
    selectionMode = false;
    selectionStart = null;
    selectionEnd = null;
    document.getElementById('selectionBanner').classList.remove('active');
    document.getElementById('selectionBanner').innerHTML = '<b>🎯</b> 点击选择相关原文（可多选）';
    document.getElementById('selectionActionBar').classList.remove('active');
    document.getElementById('tsModePill').textContent = '点击跳转';
    document.getElementById('tsModePill').classList.remove('active');
    transcriptLines.forEach(line => {{
      line.classList.remove('selectable', 'selected');
    }});
  }}

  function highlightRange() {{
    transcriptLines.forEach(line => line.classList.remove('selected'));
    if (selectionStart === null) return;
    const end = selectionEnd !== null ? selectionEnd : selectionStart;
    const from = Math.min(selectionStart, end);
    const to = Math.max(selectionStart, end);
    for (let i = from; i <= to; i++) {{
      transcriptLines[i].classList.add('selected');
    }}
    document.getElementById('selectionCount').textContent = (to - from + 1);
  }}

  function handleLineClick(line) {{
    if (!selectionMode) return;
    const idx = Array.from(transcriptLines).indexOf(line);
    if (selectionStart === null) {{
      selectionStart = idx;
      selectionEnd = null;
      document.getElementById('selectionBanner').innerHTML = '<b>🎯</b> 点击选择结束行';
    }} else if (selectionEnd === null) {{
      selectionEnd = idx;
      document.getElementById('selectionBanner').innerHTML = '<b>✓</b> 已选定范围，可点击其他行重新选择';
    }} else {{
      selectionStart = idx;
      selectionEnd = null;
      document.getElementById('selectionBanner').innerHTML = '<b>🎯</b> 点击选择结束行';
    }}
    highlightRange();
  }}

  function confirmSelection() {{
    if (selectionStart === null) {{
      toast('请先选择起始行');
      return;
    }}
    const end = selectionEnd !== null ? selectionEnd : selectionStart;
    const from = Math.min(selectionStart, end);
    const to = Math.max(selectionStart, end);
    const indices = [];
    for (let i = from; i <= to; i++) indices.push(i);

    const firstLine = transcriptLines[from];
    const lastLine = transcriptLines[to];
    const startTime = fmtTime(parseFloat(firstLine.dataset.start));
    const endTime = fmtTime(parseFloat(lastLine.dataset.end));

    let summaryHtml = '';
    indices.forEach(idx => {{
      const line = transcriptLines[idx];
      const ts = line.querySelector('.ts') ? line.querySelector('.ts').textContent : '';
      const text = line.textContent.replace(ts, '').trim();
      const preview = text.length > 40 ? text.substring(0, 40) + '...' : text;
      summaryHtml += '<div style="margin-bottom:4px"><span style="color:var(--primary);font-weight:500">' + ts + '</span> ' + preview + '</div>';
    }});

    document.getElementById('modalTranscriptSummary').innerHTML = summaryHtml;
    document.getElementById('modalSelectedTranscript').style.display = 'block';

    const activeNode = document.querySelector('#learn-tree .tree-item.active');
    const nodeName = activeNode ? activeNode.textContent.trim() : '知识节点';
    document.getElementById('modalTime').textContent = startTime + '~' + endTime + ' · ' + nodeName;

    exitSelectionMode();
    document.getElementById('noteModal').classList.add('open');
    document.getElementById('noteText').focus();
  }}

  transcriptLines.forEach(line => {{
    line.addEventListener('click', function() {{
      handleLineClick(this);
    }});
  }});

  // Note modal
  function openNoteModal() {{
    document.getElementById('modalSelectedTranscript').style.display = 'none';
    if (video) {{
      video.pause();
      playing = false;
      document.getElementById('playBtn').textContent = '▶ 播放';
      const t = fmtTime(video.currentTime);
      const activeNode = document.querySelector('#learn-tree .tree-item.active');
      const nodeName = activeNode ? activeNode.textContent.trim() : '知识节点';
      document.getElementById('modalTime').textContent = t + ' · ' + nodeName;
    }}
    document.getElementById('noteModal').classList.add('open');
    document.getElementById('noteText').focus();
  }}
  function closeNoteModal() {{
    document.getElementById('noteModal').classList.remove('open');
    document.getElementById('modalSelectedTranscript').style.display = 'none';
    if (selectionMode) exitSelectionMode();
    if (video) {{ video.play(); playing = true; document.getElementById('playBtn').textContent = '❚❚ 暂停'; }}
  }}
  function saveNote() {{
    if (!document.getElementById('noteText').value.trim()) return;
    closeNoteModal();
    toast('已保存想法 · 稍后自动归类');
    document.getElementById('noteText').value = '';
  }}

  function fmtTime(s) {{
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return String(m).padStart(2, '0') + ':' + String(sec).padStart(2, '0');
  }}

  // Toast
  function toast(s) {{
    const t = document.getElementById('toast');
    t.textContent = s;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 1600);
  }}

  // Init discovery UI
  updateDiscoveryUI();
</script>
</body>
</html>
'''

output_path = os.path.join(os.path.dirname(__file__), 'prototype-v3.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated prototype-v3.html (V2 exploratory preview + V1 learn/review/practice)")
print(f"Chapters: {len(chapters)}, Total modules: {total_modules}")
print(f"Knowledge tree: {sum(len(n['children']) for n in knowledge_tree)} sub-nodes in {len(knowledge_tree)} groups")
print(f"Video duration: {duration_str}")
