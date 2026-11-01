#!/usr/bin/env python3
"""Generate CourseMap V2 prototype — exploratory preview design."""

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

# ── Exploratory chapter data ──
chapters = [
    {
        'num': 1, 'text': '课程总览', 'icon': '🧭',
        'teaser': '这节课到底要讲什么？34分钟能帮你解决哪些问题？',
        'modules': [
            {'text': '核心框架与目标', 'question': '这门课想帮你建立什么能力？', 'insight': '两大核心模块：基础能力（词汇+词性+句法）和解题技巧（定位+题型+同义替换）。课程会先打基础，再教招式。'},
            {'text': '适用人群', 'question': '你应该选启航班还是飞跃班？', 'insight': '不看目标分数，看当前基础。4-4.5分 → 启航班；5.5-6分 → 飞跃班。选错班型 = 浪费时间。'},
            {'text': '课程结构', 'question': '从导学课到技巧课，学习路径是什么？', 'insight': '导学课（考情+计划+要求）→ 基础课（词性区分及意义）→ 技巧课（定位+题型解法），循序渐进。'},
        ]
    },
    {
        'num': 2, 'text': '雅思阅读考情介绍', 'icon': '📋',
        'teaser': '雅思阅读到底考什么？60分钟里藏着哪些你需要注意的规则？',
        'modules': [
            {'text': '考试基本信息', 'question': '60分钟、3篇文章、40题——具体怎么分配？', 'insight': '60分钟包含填答案时间。每篇约13-14题，难度整体递增，第3篇通常最难。文体只考议论文+说明文。'},
            {'text': '主要题型', 'question': '雅思阅读有几种题型？哪种最难？', 'insight': '5大题型：填空 → 判断 → 选择 → 匹配 → Heading。判断题的 False vs Not Given 是最大难点。'},
            {'text': '评分标准与目标分数', 'question': '错多少题能拿7分？你的策略应该是什么？', 'insight': '错 ≤ 10 个 = 7分，错 ≤ 7 个 = 7.5分。填空+判断占约20题，是拿分基础。策略：阅读/听力冲高分，弥补口语/写作。'},
        ]
    },
    {
        'num': 3, 'text': '复习计划与刷题策略', 'icon': '🗺️',
        'teaser': '剑桥雅思4-17，到底该按什么顺序刷？为什么不能随便挑？',
        'modules': [
            {'text': '提分三大要素', 'question': '提分靠什么？只是刷题就够了吗？', 'insight': '三要素：语言能力（内功）+ 方法技巧（招式）+ 合理计划（策略）。光刷题不练内功，天花板很低。'},
            {'text': '刷题顺序', 'question': 'C4到C17，正确的打开方式是什么？', 'insight': 'C13-14 入门 → C4-8 专项 → C9-12 核心（必须整套做）→ C15-17 模考。正确率 > 速度。'},
            {'text': '考试形式选择', 'question': '纸笔考和机考，对日常练习有什么影响？', 'insight': '选定考试方式后，平时刷题必须用同样方式。纸笔手感 ≠ PDF/APP，机考需要在模拟系统上练。'},
            {'text': '个性化计划申请', 'question': '通用的刷题顺序适合每个人吗？', 'insight': '老师给的是通用框架。个人情况（基础、备考时间）不同，可课后微信群联系老师获取专属方案。'},
        ]
    },
    {
        'num': 4, 'text': '课程介绍与作业要求', 'icon': '📝',
        'teaser': '两个班型课程分别怎么安排？作业怎么交才不会被老师"忽略"？',
        'modules': [
            {'text': '课程内容', 'question': '启航班和飞跃班的课程流程有什么区别？', 'insight': '启航班：先攻词汇+语法基础，再学题型（6次×1h+8节视频）。飞跃班：直接聚焦题型技巧（5次×2h+7节视频）。'},
            {'text': '作业提交要求', 'question': '作业怎么交？有什么"潜规则"？', 'insight': '注明日期+科目、附截图、错题必须标记（打问号或写"XX题需讲解"）。下次直播课前1天提交，不要太早。'},
        ]
    },
    {
        'num': 5, 'text': '课后作业', 'icon': '✏️',
        'teaser': '听完导学课，第一件事应该做什么？',
        'modules': [
            {'text': '基础积累', 'question': '词汇怎么整理？核心词和认知词有什么区别？', 'insight': '启航班：整理词汇List1，核心词记词意+词性+同义替换+搭配，认知词只记大意。飞跃班：真题生词结合语境记忆。'},
            {'text': '真题练习', 'question': '第一套真题应该选哪本剑桥？', 'insight': '启航班：C14-17 做1套完整阅读自测。飞跃班：C10-13 做填空专项，结合词性预判答案。'},
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

# ── Timeline items ──
timeline_items = [
    {'time': '00:00', 'label': '课程导入', 'desc': '导学视频目的', 'cls': ''},
    {'time': '01:18', 'label': '考情概览', 'desc': '60分钟/3篇40题', 'cls': ''},
    {'time': '03:20', 'label': '题型分类', 'desc': '基础→细节→过渡→宏观', 'cls': ''},
    {'time': '08:15', 'label': '目标分数', 'desc': '7分≥27 / 6.5≥25 / 6≥23', 'cls': ''},
    {'time': '11:30', 'label': '★ 评分标准', 'desc': '错≤10=7分', 'cls': 'highlight'},
    {'time': '16:15', 'label': '提分三要素', 'desc': '内功·招式·策略', 'cls': ''},
    {'time': '18:15', 'label': '刷题顺序', 'desc': 'C13→C4→C9→C15', 'cls': ''},
    {'time': '22:20', 'label': '课程大纲', 'desc': '启航班+飞跃班', 'cls': ''},
    {'time': '27:20', 'label': '作业要求', 'desc': '日期+标记+截图', 'cls': ''},
    {'time': '33:40', 'label': '结语', 'desc': '课程结束', 'cls': ''},
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

tree_html = gen_tree_html()

total_modules = sum(len(c['modules']) for c in chapters)

# Chapter cards HTML
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

duration_str = fmt_time(total_duration)

html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CourseMap V2 · 探索式预习</title>
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
  .version-tag {{ font-size: 10px; padding: 3px 7px; border-radius: 5px; background: var(--primary-light); color: var(--primary); font-weight: 600; }}
  .phase-badge {{ font-size: 12px; padding: 5px 9px; border-radius: 999px; background: var(--primary-light); color: var(--primary); font-weight: 600; }}
  .topbar .spacer {{ flex: 1; }}
  .topbar-crumb {{ font-size: 13px; color: var(--text-muted); }}
  .topbar-crumb a {{ color: var(--text-secondary); cursor: pointer; text-decoration: none; }}
  .topbar-crumb a:hover {{ color: var(--primary); }}
  .topbar-crumb .current {{ color: var(--text); font-weight: 500; }}

  /* PAGE */
  .page {{ display: none; flex: 1; min-height: 0; }}
  .page.active {{ display: flex; flex-direction: column; }}

  /* ══════ EXPLORATORY PREVIEW ══════ */
  #page-preview .layout {{ grid-template-columns: 1fr 300px; }}
  .preview-layout {{ flex: 1; min-height: 0; display: grid; grid-template-columns: 1fr 300px; }}
  .preview-main {{ overflow-y: auto; padding: 32px 36px; }}
  .preview-rail {{ background: var(--surface); border-left: 1px solid var(--border); overflow-y: auto; padding: 24px 20px; }}

  /* Hero */
  .preview-hero {{ margin-bottom: 28px; }}
  .preview-hero h1 {{ font-size: 26px; font-weight: 700; margin-bottom: 6px; }}
  .preview-hero .subtitle {{ color: var(--text-secondary); font-size: 14px; line-height: 1.7; }}

  /* Guiding questions */
  .guiding-qs {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }}
  .gq {{
    padding: 8px 14px; border-radius: 999px; font-size: 13px;
    background: var(--surface); border: 1px solid var(--border);
    cursor: pointer; transition: all 0.2s; color: var(--text-secondary);
  }}
  .gq:hover {{ border-color: var(--primary); color: var(--primary); background: var(--primary-light); }}
  .gq.answered {{ background: var(--green-light); border-color: #b8d4c0; color: var(--green); }}

  /* Explore cards */
  .explore-cards {{ display: flex; flex-direction: column; gap: 10px; margin-bottom: 24px; }}
  .explore-card {{
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
    box-shadow: var(--shadow); overflow: hidden; transition: all 0.25s ease;
  }}
  .explore-card:hover {{ box-shadow: var(--shadow-md); border-color: #c8cdd6; }}
  .explore-card.expanded {{ border-color: var(--primary); }}
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

  /* Card body (hidden by default) */
  .explore-card-body {{
    max-height: 0; overflow: hidden; transition: max-height 0.35s ease;
    padding: 0 20px;
  }}
  .explore-card.expanded .explore-card-body {{
    max-height: 600px; padding: 0 20px 20px;
  }}

  /* Module pills */
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

  /* Insight reveal */
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

  /* Discovery progress (right rail) */
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
  .cta-btn.locked {{ background: var(--bg); color: var(--text-muted); border: 1px solid var(--border); }}

  /* ══════ LEARN PAGE (same as V1) ══════ */
  #page-learn .layout {{ grid-template-columns: 260px minmax(560px, 1fr) 330px; }}
  .layout {{ flex: 1; min-height: 0; display: grid; }}
  .side {{ background: var(--surface); overflow-y: auto; }}
  .side.left {{ border-right: 1px solid var(--border); }}
  .side.right {{ border-left: 1px solid var(--border); }}
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

  .knowledge-card {{ margin: 16px 18px 0; padding: 18px; background: var(--surface); border: 1px solid #e6e8ed; border-radius: var(--radius); box-shadow: var(--shadow); }}
  .knowledge-card h2 {{ font-size: 19px; margin: 8px 0; }}
  .knowledge-card p {{ line-height: 1.7; font-size: 13px; color: #59636f; }}
  .insight {{
    padding: 14px; border-radius: 11px;
    background: var(--orange-light); border: 1px solid var(--orange-border); margin-top: 14px;
  }}
  .insight p {{ font-size: 14px; line-height: 1.65; color: #7c5e00; margin-top: 8px; }}

  .transcript-sidebar {{ border-bottom: 1px solid var(--border); display: flex; flex-direction: column; height: calc(38vh + 50px); }}
  .transcript-sidebar .ts-header {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 16px; flex-shrink: 0; }}
  .transcript-sidebar .ts-header b {{ font-size: 13px; }}
  .transcript-scroll {{ overflow-y: auto; flex: 1; padding: 0 16px 12px; }}
  .transcript-line {{
    padding: 5px 7px; font-size: 13px; line-height: 1.7;
    color: var(--text-muted); cursor: pointer; transition: all 0.2s; border-radius: 6px;
  }}
  .transcript-line:hover {{ color: var(--text-secondary); background: #f6f7f9; }}
  .transcript-line.read {{ color: var(--text); }}
  .transcript-line.current {{ color: var(--primary); font-weight: 500; background: var(--primary-light); }}
  .transcript-line .ts {{ font-size: 11px; color: var(--text-muted); margin-right: 8px; font-variant-numeric: tabular-nums; opacity: 0.6; }}
  .transcript-line.current .ts {{ opacity: 1; color: var(--primary); }}

  /* ══════ REVIEW PAGE ══════ */
  #page-review .layout {{ grid-template-columns: 250px 1fr 330px; }}
  #page-review .main {{ padding: 22px 26px; background: var(--bg); overflow-y: auto; }}
  .reviewhead {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }}
  .reviewhead h1 {{ font-size: 26px; }}
  .scoregrid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px; }}
  .stat {{ padding: 15px; background: var(--surface); border: 1px solid #e6e8ed; border-radius: var(--radius); box-shadow: var(--shadow); }}
  .stat b {{ font-size: 23px; display: block; margin-top: 7px; }}
  .muted {{ color: var(--text-muted); }}
  .small {{ font-size: 12px; }}

  .recall {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  .recallcard {{
    border: 1px solid #e2e6eb; border-radius: 11px; padding: 14px;
    cursor: pointer; transition: border-color 0.15s; background: var(--surface);
  }}
  .recallcard .ans {{ display: none; margin-top: 10px; color: #59636f; line-height: 1.6; font-size: 13px; }}
  .recallcard.open .ans {{ display: block; }}

  .timeline {{ position: relative; }}
  .timeline::before {{ content: ""; position: absolute; left: 20px; top: 8px; bottom: 8px; width: 2px; background: #e3e6eb; }}
  .event {{ position: relative; padding: 0 12px 18px 48px; cursor: pointer; }}
  .dot {{
    position: absolute; left: 15px; top: 2px;
    width: 12px; height: 12px; border: 3px solid #fff;
    border-radius: 50%; background: #718096; box-shadow: 0 0 0 1px #ccd1d8;
  }}
  .event.highlight .dot {{ background: var(--orange); }}
  .event b {{ font-size: 12px; }}
  .event p {{ margin: 5px 0 0; font-size: 12px; line-height: 1.5; color: #69727e; }}
  .event:hover b {{ color: var(--primary); }}

  /* COMMON */
  .btn {{ padding: 9px 13px; border-radius: 9px; background: #eef1f5; color: #34404d; font-size: 13px; }}
  .btn.primary {{ background: #1e293b; color: #fff; }}
  .btn.ghost {{ background: var(--surface); border: 1px solid #dfe3e9; }}
  .pill {{ font-size: 11px; padding: 4px 7px; border-radius: 6px; background: #f0f2f5; color: #68717d; }}
  .tag {{ display: inline-block; font-size: 10px; padding: 3px 6px; border-radius: 5px; background: var(--primary-light); color: #4a5ea4; }}
  .tag.success {{ background: var(--green-light); color: var(--green); }}
  .row {{ display: flex; align-items: center; gap: 10px; }}

  /* NOTE MODAL */
  .modal {{ position: fixed; inset: 0; z-index: 200; background: rgba(20,25,32,.42); display: none; align-items: center; justify-content: center; }}
  .modal.open {{ display: flex; }}
  .modalbox {{ width: 520px; background: var(--surface); border-radius: var(--radius); padding: 24px; box-shadow: 0 20px 60px rgba(0,0,0,.15); }}
  .modalbox textarea {{ width: 100%; min-height: 100px; border: 1px solid var(--border); border-radius: 8px; padding: 10px; font: inherit; font-size: 13px; resize: vertical; margin-top: 10px; }}
  .modalbox textarea:focus {{ outline: none; border-color: var(--primary); }}

  .toast {{
    position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%) translateY(20px);
    background: #1e293b; color: #fff; padding: 10px 20px; border-radius: 10px;
    font-size: 13px; opacity: 0; transition: all 0.3s; z-index: 300; pointer-events: none;
  }}
  .toast.show {{ opacity: 1; transform: translateX(-50%) translateY(0); }}
</style>
</head>
<body>
<div class="app">

<!-- TOP BAR -->
<div class="topbar">
  <span class="brand">CourseMap</span>
  <span class="version-tag">V2 探索版</span>
  <span class="phase-badge" id="phaseBadge">预习</span>
  <div class="spacer"></div>
  <div class="topbar-crumb">
    <a onclick="showPage('preview')">预习</a> ·
    <a onclick="showPage('learn')">学习</a> ·
    <a onclick="showPage('review')">复习</a>
  </div>
</div>

<!-- ══════ PREVIEW PAGE (EXPLORATORY) ══════ -->
<div class="page active" id="page-preview">
  <div class="preview-layout">
    <div class="preview-main">
      <div class="preview-hero">
        <h1>雅思阅读导学课</h1>
        <p class="subtitle">34分钟 · 5个章节 · 带你了解雅思阅读的全貌</p>
        <div class="guiding-qs">
          <div class="gq" onclick="this.classList.toggle('answered')">雅思阅读到底考什么？</div>
          <div class="gq" onclick="this.classList.toggle('answered')">我的水平该选哪个班？</div>
          <div class="gq" onclick="this.classList.toggle('answered')">剑桥真题该怎么刷？</div>
          <div class="gq" onclick="this.classList.toggle('answered')">错多少题能拿7分？</div>
          <div class="gq" onclick="this.classList.toggle('answered')">作业怎么交？</div>
        </div>
      </div>

      <div class="explore-cards">
{chapters_html}
      </div>

      <div style="text-align:center; padding: 20px 0 40px;">
        <button class="btn ghost" style="padding: 12px 28px; font-size: 14px;" onclick="showPage('learn')">
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
        <button class="cta-btn locked" id="ctaBtn" onclick="showPage('learn')">
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
      <h3>知识大纲</h3>
      <div id="learn-tree">
{tree_html}
      </div>
      <div style="padding:12px 18px">
        <div class="tree-item" onclick="seekTo(318)">💭 05:18 为什么 F ≠ NG？</div>
        <div class="tree-item" onclick="seekTo(1175)">💭 19:35 为什么要整套做真题？</div>
      </div>
    </aside>
    <div class="main">
      <div class="video">
        <video id="video" src="{VIDEO_FILE}"></video>
        <div class="video-controls">
          <button class="speed-btn" id="playBtn" onclick="togglePlay()">▶ 播放</button>
          <div class="bar" onclick="seekBar(event)"><i id="progress" style="width:0%"></i></div>
          <span class="time-label"><span id="curTime">00:00</span> / {duration_str}</span>
          <button class="speed-btn" id="speed" onclick="cycleSpeed()">1×</button>
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
      </div>
    </div>
    <aside class="side right">
      <div class="transcript-sidebar">
        <div class="ts-header">
          <b>原文字幕</b>
          <span class="pill">点击跳转</span>
        </div>
        <div class="transcript-scroll">
{transcript_html}
        </div>
      </div>
      <div style="padding:14px 16px">
        <button class="btn primary" style="width:100%;margin-bottom:8px" onclick="openNoteModal()">💭 记录我的想法</button>
        <button class="btn ghost" style="width:100%" onclick="toast('已标记：稍后重点看')">☆ 稍后重点看</button>
      </div>
    </aside>
  </div>
</div>

<!-- ══════ REVIEW PAGE ══════ -->
<div class="page" id="page-review">
  <div class="layout">
    <aside class="side left">
      <h3>复习导航</h3>
      <div class="tree-item active">▾ 本节知识地图</div>
{"".join(f'      <div class="tree-item tree-child">{html.escape(c["text"])}</div>\n' for n in knowledge_tree for c in n["children"][:2])}
      <h3>我的状态</h3>
      <div class="tree-item">🔴 还没掌握 · 2</div>
      <div class="tree-item">🟡 模糊 · 3</div>
      <div class="tree-item">🟢 已掌握 · 4</div>
    </aside>
    <div class="main">
      <div class="reviewhead">
        <div>
          <h1>2 分钟，把整节课重新想一遍</h1>
          <div class="muted small" style="margin-top:6px">复习不是重看视频，而是先回忆 → 再验证 → 最后溯源。</div>
        </div>
        <button class="btn primary" onclick="startReview()">开始快速复习</button>
      </div>
      <div class="scoregrid">
        <div class="stat"><span class="muted small">知识模块</span><b>{sum(len(n['children']) for n in knowledge_tree)}</b><span class="muted small">本节覆盖</span></div>
        <div class="stat"><span class="muted small">老师重点</span><b>7</b><span class="muted small">可回溯</span></div>
        <div class="stat"><span class="muted small">我的想法</span><b>2</b><span class="muted small">自动挂到知识点</span></div>
        <div class="stat"><span class="muted small">待掌握</span><b>2</b><span class="muted small">建议优先复习</span></div>
      </div>
      <div style="display:grid; grid-template-columns:1.15fr 0.85fr; gap:14px;">
        <section class="stat">
          <div class="row" style="justify-content:space-between">
            <div><b>① 先回忆，不看答案</b><div class="muted small" style="margin-top:4px">点击卡片，写在脑中的答案会被揭示</div></div>
            <span class="tag success">主动回忆</span>
          </div>
          <div class="recall" style="margin-top:14px">
            <div class="recallcard" onclick="this.classList.toggle('open')">
              <b>雅思阅读几种题型？</b>
              <div class="ans">5种：填空、判断、选择、匹配、Heading。填空+判断占约20题，是拿分基础。</div>
            </div>
            <div class="recallcard" onclick="this.classList.toggle('open')">
              <b>7分要错几个以内？</b>
              <div class="ans">错 ≤ 10个 = 7分。错 ≤ 7个 = 7.5分。每一题都很重要。</div>
            </div>
            <div class="recallcard" onclick="this.classList.toggle('open')">
              <b>刷题顺序是什么？</b>
              <div class="ans">C13-14入门 → C4-8专项 → C9-12核心（整套完成）→ C15-17模考。</div>
            </div>
            <div class="recallcard" onclick="this.classList.toggle('open')">
              <b>提分三要素？</b>
              <div class="ans">语言能力（内功）+ 方法技巧（招式）+ 合理计划（策略）。</div>
            </div>
          </div>
        </section>
        <section class="stat">
          <div class="row" style="justify-content:space-between">
            <b>③ 课程知识时间轴</b>
            <span class="tag success">快速回看</span>
          </div>
          <p class="muted small" style="line-height:1.6">只看关键节点；需要深入时，再回到老师原文和视频。</p>
          <div class="timeline" style="margin-top:12px">
{timeline_html}
          </div>
        </section>
      </div>
    </div>
    <aside class="side right">
      <h3>复习工具</h3>
      <div style="padding:14px 16px">
        <button class="btn primary" style="width:100%;margin-bottom:8px" onclick="startReview()">🧠 开始主动回忆</button>
        <button class="btn ghost" style="width:100%;margin-bottom:16px" onclick="toast('已导出复习卡片')">📤 导出复习卡片</button>
        <div style="padding:14px;background:var(--surface);border:1px solid #e6e8ed;border-radius:11px;margin-bottom:12px">
          <b style="font-size:13px">知识掌握</b>
          <div style="margin-top:10px">
            <div class="row" style="justify-content:space-between"><span>评分标准细节</span><span class="tag" style="background:var(--red-light);color:var(--red)">还没掌握</span></div>
            <div class="row" style="justify-content:space-between;margin-top:6px"><span>题型整体框架</span><span class="tag">模糊</span></div>
          </div>
        </div>
        <p class="muted small">🎯 2 个待掌握</p>
      </div>
    </aside>
  </div>
</div>

<!-- NOTE MODAL -->
<div class="modal" id="noteModal">
  <div class="modalbox">
    <div class="row">
      <b>记录我的想法</b>
      <div class="spacer"></div>
      <span class="pill" id="modalTime">00:00 · 知识节点</span>
    </div>
    <p class="muted small" style="margin:8px 0">保存后会自动绑定时间；AI稍后把它归入对应知识节点。</p>
    <textarea id="noteText" placeholder="例如：这里老师说填空和判断最容易混，我想回去找一个具体例子……"></textarea>
    <div class="row" style="justify-content:flex-end;margin-top:12px">
      <button class="btn" onclick="closeNoteModal()">取消</button>
      <button class="btn primary" style="background:var(--primary);color:#fff" onclick="saveNote()">保存想法</button>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

</div>

<script>
// ── Page navigation ──
function showPage(name) {{
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById('page-' + name).classList.add('active');
  const labels = {{ preview: '预习', learn: '学习', review: '复习' }};
  document.getElementById('phaseBadge').textContent = labels[name];
}}

// ── Exploratory preview ──
const chapterData = {json.dumps([{
    'num': c['num'], 'text': c['text'], 'icon': c['icon'],
    'moduleCount': len(c['modules']),
    'modules': [{'text': m['text']} for m in c['modules']]
} for c in chapters], ensure_ascii=False)};

const discovered = new Set();
const expandedChapters = new Set();

function expandChapter(num) {{
  const card = document.getElementById('ch' + num);
  const wasExpanded = card.classList.contains('expanded');
  if (wasExpanded) {{
    card.classList.remove('expanded');
  }} else {{
    card.classList.add('expanded');
    expandedChapters.add(num);
  }}
  updateDiscoveryUI();
}}

function revealModule(el, chNum, modIdx) {{
  event.stopPropagation();
  const key = chNum + '-' + modIdx;
  if (discovered.has(key)) return;
  discovered.add(key);

  el.classList.add('revealed');

  // Hide all insights in this chapter, show the selected one
  const area = document.getElementById('insight-area-' + chNum);
  area.querySelectorAll('.insight-reveal').forEach(i => i.classList.remove('show'));
  const insight = document.getElementById('insight-' + chNum + '-' + modIdx);
  insight.classList.add('show');

  // Check if chapter is fully discovered
  const ch = chapterData.find(c => c.num === chNum);
  const allRevealed = chapterData
    .filter(c => c.num === chNum)[0]
    .modules.every((_, i) => discovered.has(chNum + '-' + i));
  if (allRevealed) {{
    document.getElementById('ch' + chNum).classList.add('discovered');
  }}

  updateDiscoveryUI();
}}

function updateDiscoveryUI() {{
  const total = {total_modules};
  const count = discovered.size;
  document.getElementById('discoveredCount').textContent = count;
  document.getElementById('discoveryBar').style.width = (count / total * 100) + '%';

  // Chapter status
  const statusEl = document.getElementById('chapterStatus');
  statusEl.innerHTML = chapterData.map(ch => {{
    const revealed = ch.modules.filter((_, i) => discovered.has(ch.num + '-' + i)).length;
    const cls = revealed === 0 ? '' : revealed === ch.modules.length ? 'complete' : 'partial';
    const label = revealed === 0 ? '未探索' : revealed === ch.modules.length ? '✓ 已发现' : revealed + '/' + ch.modules.length;
    return '<div class="ch-status ' + cls + '" onclick="expandChapter(' + ch.num + ')">' +
      '<span class="ch-dot"></span>' +
      '<span class="ch-label">' + ch.icon + ' ' + ch.text + '</span>' +
      '<span class="ch-count">' + label + '</span></div>';
  }}).join('');

  // CTA button
  const cta = document.getElementById('ctaBtn');
  if (count >= 5) {{
    cta.classList.remove('locked');
    cta.innerHTML = '开始学习 →';
    cta.onclick = function() {{ showPage('learn'); }};
  }}
}}

// Init chapter status
updateDiscoveryUI();

// ── Learn page ──
const video = document.getElementById('video');
const progress = document.getElementById('progress');
const curTime = document.getElementById('curTime');
const transcriptLines = document.querySelectorAll('.transcript-line');
const treeNodes = document.querySelectorAll('#learn-tree .tree-item');

if (video) {{
  video.addEventListener('timeupdate', function() {{
    const t = video.currentTime;
    const d = video.duration || 1;
    progress.style.width = (t / d * 100) + '%';
    const m = Math.floor(t / 60);
    const s = Math.floor(t % 60);
    curTime.textContent = String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');

    transcriptLines.forEach(line => {{
      line.classList.remove('current');
      const start = parseFloat(line.dataset.start);
      const end = parseFloat(line.dataset.end);
      if (t >= start && t < end) {{
        line.classList.add('current');
        line.scrollIntoView({{ block: 'center', behavior: 'smooth' }});
      }}
    }});

    treeNodes.forEach(node => {{
      const start = parseFloat(node.dataset.start);
      const end = parseFloat(node.dataset.end);
      node.classList.remove('active', 'in-range');
      if (t >= start && t < end) node.classList.add('in-range');
      if (t >= start && t < end && !node.classList.contains('tree-child')) node.classList.add('active');
      if (t >= start && t < end && node.classList.contains('tree-child')) {{
        node.classList.add('active');
        node.classList.remove('in-range');
      }}
    }});
  }});

  transcriptLines.forEach(line => {{
    line.addEventListener('click', function() {{
      video.currentTime = parseFloat(this.dataset.start);
      video.play();
    }});
  }});
}}

function togglePlay() {{
  if (!video) return;
  if (playing) {{ video.pause(); document.getElementById('playBtn').textContent = '▶ 播放'; }}
  else {{ video.play(); document.getElementById('playBtn').textContent = '❚❚ 暂停'; }}
  playing = !playing;
}}
let playing = false;
let speeds = [1, 1.25, 1.5];
let speedIdx = 0;
function cycleSpeed() {{
  speedIdx = (speedIdx + 1) % speeds.length;
  if (video) video.playbackRate = speeds[speedIdx];
  document.getElementById('speed').textContent = speeds[speedIdx] + '×';
}}
function seekBar(e) {{
  if (!video) return;
  const rect = e.currentTarget.getBoundingClientRect();
  video.currentTime = ((e.clientX - rect.left) / rect.width) * video.duration;
}}
function seekTo(sec) {{
  showPage('learn');
  if (!video) return;
  video.currentTime = sec;
  video.play();
  playing = true;
  document.getElementById('playBtn').textContent = '❚❚ 暂停';
}}

function openNoteModal() {{
  if (video) {{
    video.pause(); playing = false;
    document.getElementById('playBtn').textContent = '▶ 播放';
    const t = fmtTime(video.currentTime);
    document.getElementById('modalTime').textContent = t + ' · 知识节点';
  }}
  document.getElementById('noteModal').classList.add('open');
  document.getElementById('noteText').focus();
}}
function closeNoteModal() {{ document.getElementById('noteModal').classList.remove('open'); }}
function saveNote() {{
  if (!document.getElementById('noteText').value.trim()) return;
  closeNoteModal();
  toast('已保存想法 · 稍后自动归类');
  document.getElementById('noteText').value = '';
  if (video) {{ video.play(); playing = true; document.getElementById('playBtn').textContent = '❚❚ 暂停'; }}
}}
function fmtTime(s) {{
  const m = Math.floor(s / 60);
  const sec = Math.floor(s % 60);
  return String(m).padStart(2, '0') + ':' + String(sec).padStart(2, '0');
}}
function startReview() {{ toast('进入主动回忆模式'); }}
function toast(s) {{
  const t = document.getElementById('toast');
  t.textContent = s;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 1600);
}}
</script>
</body>
</html>
'''

output_path = os.path.join(os.path.dirname(__file__), 'prototype-v2.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated prototype-v2.html (exploratory preview)")
print(f"Chapters: {len(chapters)}, Total modules: {total_modules}")
print(f"Knowledge tree: {sum(len(n['children']) for n in knowledge_tree)} sub-nodes in {len(knowledge_tree)} groups")
