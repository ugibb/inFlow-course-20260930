#!/usr/bin/env python3
"""Generate CourseMap high-fidelity prototype with real course data."""

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

# Group segments into transcript lines (~12-18 seconds per line)
lines = []
current_text = ""
current_start = segments[0]['start']
LINE_DURATION = 14  # seconds per line

for seg in segments:
    if current_text and (seg['start'] - current_start) >= LINE_DURATION:
        lines.append({
            'start': current_start,
            'end': seg['start'],
            'text': current_text.strip()
        })
        current_text = seg['text']
        current_start = seg['start']
    else:
        current_text += seg['text']

if current_text.strip():
    lines.append({
        'start': current_start,
        'end': segments[-1]['end'],
        'text': current_text.strip()
    })

# Comprehensive knowledge tree (3 levels: L1 section → L2 topic → L3 detail)
knowledge_tree = [
    {
        'level': 1, 'text': '课程总览',
        'children': [
            {'level': 2, 'text': '核心框架与目标', 'time_range': (0, 30)},
            {'level': 2, 'text': '适用人群', 'time_range': (30, 43)},
            {'level': 2, 'text': '课程结构', 'time_range': (43, 78)},
        ]
    },
    {
        'level': 1, 'text': '雅思阅读考情介绍',
        'children': [
            {'level': 2, 'text': '考试基本信息', 'time_range': (78, 200)},
            {'level': 2, 'text': '主要题型', 'time_range': (200, 495)},
            {'level': 2, 'text': '评分标准与目标分数', 'time_range': (495, 975)},
        ]
    },
    {
        'level': 1, 'text': '复习计划与刷题策略',
        'children': [
            {'level': 2, 'text': '提分三大要素', 'time_range': (975, 1050)},
            {'level': 2, 'text': '刷题顺序（剑桥雅思系列）', 'time_range': (1050, 1260)},
            {'level': 2, 'text': '考试形式选择', 'time_range': (1260, 1320)},
            {'level': 2, 'text': '个性化计划申请', 'time_range': (1320, 1340)},
        ]
    },
    {
        'level': 1, 'text': '课程介绍与作业要求',
        'children': [
            {'level': 2, 'text': '课程内容', 'time_range': (1340, 1560)},
            {'level': 2, 'text': '作业提交要求', 'time_range': (1640, 2020)},
        ]
    },
    {
        'level': 1, 'text': '课后作业',
        'children': [
            {'level': 2, 'text': '基础积累', 'time_range': (2020, 2040)},
            {'level': 2, 'text': '真题练习', 'time_range': (2040, 2050)},
            {'level': 2, 'text': '其他要求', 'time_range': (2050, 2052)},
        ]
    },
]

# Preview cards with real content (matching detailed outline)
preview_cards = [
    {
        'title': '考试基本信息',
        'tag': '重点',
        'summary': '考试时间60分钟（含填答案时间），3篇文章共40题（每篇13-14题），难度逐篇递增。文体以议论文、说明文为主，不考记叙文。题材注意文理科平衡。建议先翻阅剑桥雅思4-13了解整体。',
        'highlight': '不管纸笔还是机考，60分钟都包含答题和填写答题卡的时间'
    },
    {
        'title': '题型分类与解题逻辑',
        'tag': '核心',
        'summary': '课程按难度递进：基础（定位+同义替换）→ 细节题（填空+判断）→ 过渡题（选择）→ 宏观题（匹配+Heading）。判断题有True/False/Not Given三个选项，False和NG的区分是难点。填空+判断占约20题/40题。',
        'highlight': '填空+判断占约20题（总共40题），是必须把握的核心拿分题型'
    },
    {
        'title': '目标分数与评分标准',
        'tag': '重点',
        'summary': '总分7分=四科≥27，6.5分≥25，6分≥23。阅读评分关键线：错≤7=7.5分，错≤10=7分，错≤13-14=6.5分。推荐策略：阅读/听力冲7-8分，弥补口语/写作短板。',
        'highlight': '错超过10个就低于7分，错超过13个就低于6.5分——每一个题都很重要'
    },
    {
        'title': '刷题顺序与策略',
        'tag': None,
        'summary': '提分三要素：语言能力（内功）、方法技巧（招式）、合理计划（策略）。刷题顺序：C13-14入门→C4-8专项→C9-12核心（整套完成）→C15-17考前模拟。正确率优先于速度。',
        'highlight': '一旦开始做剑桥真题，一定要整套完成，不能今天做一篇明天做一篇'
    },
    {
        'title': '课程安排与作业要求',
        'tag': None,
        'summary': '启航班（6次×1小时+赠课）：词汇→词性→句法→定位→题型，适合基础4-4.5分。飞跃班（5次×2小时+赠课）：定位→填空/判断→选择→匹配→Heading，适合基础5.5-6分。作业需标注日期+截图+标记错题。',
        'highlight': '有问题的题目一定要做好标记——打问号或写"老师XX题需要讲一讲"'
    },
]

# Generate transcript HTML
transcript_html = ""
for i, line in enumerate(lines):
    ts = fmt_time(line['start'])
    text_escaped = html.escape(line['text'])
    cls = 'transcript-line'
    if i < 8:
        cls += ' read'
    elif i == 8:
        cls += ' current'
    transcript_html += f'      <div class="{cls}" data-start="{line["start"]}" data-end="{line["end"]}"><span class="ts">{ts}</span>{text_escaped}</div>\n'

# Generate knowledge tree HTML (2 levels: L1 section → L2 topic)
def gen_tree_html():
    h = ""
    for node in knowledge_tree:
        h += f'      <div class="tree-item" data-start="{node["children"][0]["time_range"][0]}" data-end="{node["children"][-1]["time_range"][1]}"><span class="node-dot"></span>▾ {node["text"]}</div>\n'
        for child in node['children']:
            h += f'      <div class="tree-item tree-child" data-start="{child["time_range"][0]}" data-end="{child["time_range"][1]}"><span class="node-dot"></span>{child["text"]}</div>\n'
    return h

tree_html = gen_tree_html()

# Generate preview cards HTML
preview_html = ""
for card in preview_cards:
    tag_html = f' <span class="tag">{card["tag"]}</span>' if card['tag'] else ''
    highlight_html = f'      <div class="highlight-box">{html.escape(card["highlight"])}</div>\n' if card['highlight'] else ''
    preview_html += f'''    <div class="card">
      <h3>{html.escape(card["title"])}{tag_html}</h3>
      <p>{html.escape(card["summary"])}</p>
{highlight_html}    </div>
'''

# Generate review keypoints from highlights
review_keypoints_html = ""
for card in preview_cards[:3]:
    if card['highlight']:
        review_keypoints_html += f'''      <div class="keypoint-item">
        <div class="kp-icon kp-teacher">!</div>
        <div>{html.escape(card["highlight"])}</div>
      </div>
'''

# Generate timeline items from key content moments
timeline_items = [
    {'time': '00:00', 'label': '课程导入', 'desc': '导学视频目的：考情+计划+课程要求', 'cls': ''},
    {'time': '01:18', 'label': '考情：考试基本信息', 'desc': '60分钟/3篇40题/纸笔vs机考', 'cls': ''},
    {'time': '02:50', 'label': '难度与文体', 'desc': '难度递增/议论文+说明文/文理平衡', 'cls': ''},
    {'time': '03:20', 'label': '题型总览', 'desc': '课程逻辑：基础→细节→过渡→宏观', 'cls': ''},
    {'time': '04:10', 'label': '填空题', 'desc': '细节题，有细分类型，后续专课学习', 'cls': ''},
    {'time': '04:40', 'label': '判断题 T/F/NG', 'desc': '★ False vs Not Given 是难点', 'cls': 'highlight'},
    {'time': '05:50', 'label': '选择题', 'desc': '单选/多选，实际非常难', 'cls': ''},
    {'time': '06:20', 'label': '匹配题', 'desc': '人名/时间/地点/句子/信息匹配', 'cls': ''},
    {'time': '07:20', 'label': 'Heading题+简单题', 'desc': '标题配对；简单题方法接近填空', 'cls': ''},
    {'time': '08:15', 'label': '目标分数', 'desc': '7分≥27 / 6.5≥25 / 6≥23', 'cls': ''},
    {'time': '09:30', 'label': '小分要求与组合', 'desc': '分数组合方式+学校小分要求', 'cls': ''},
    {'time': '10:20', 'label': '考生优劣势', 'desc': '★ 阅读/听力冲7-8分弥补说写', 'cls': 'highlight'},
    {'time': '11:30', 'label': '★ 评分标准', 'desc': '错≤10=7分 / 错≤13=6.5分', 'cls': 'highlight'},
    {'time': '13:30', 'label': '★ 填空+判断=核心', 'desc': '占20题/40题，是拿分基础', 'cls': 'highlight'},
    {'time': '15:00', 'label': '每天练阅读听力', 'desc': '提分难度小，保证每天一定量', 'cls': ''},
    {'time': '16:15', 'label': '提分三要素', 'desc': '内功·招式·策略', 'cls': ''},
    {'time': '18:15', 'label': '刷题顺序', 'desc': 'C13入门→C4专项→C9核心→C15模拟', 'cls': ''},
    {'time': '19:20', 'label': '★ 整套完成', 'desc': '正确率>速度，不能今天一篇明天一篇', 'cls': 'highlight'},
    {'time': '21:00', 'label': '考试形式选择', 'desc': '选定后刷题方式保持一致', 'cls': ''},
    {'time': '22:20', 'label': '启航班大纲', 'desc': '词汇→词性→句法→定位→题型', 'cls': ''},
    {'time': '23:50', 'label': '飞跃班大纲', 'desc': '定位→填空/判断→选择→匹配→Heading', 'cls': ''},
    {'time': '25:00', 'label': '班型选择', 'desc': '★ 基础4-4.5启航/5.5-6飞跃', 'cls': 'highlight'},
    {'time': '27:20', 'label': '作业格式要求', 'desc': '日期+科目+截图+标记错题', 'cls': ''},
    {'time': '29:10', 'label': '★ 提交时间', 'desc': '统一在下次直播课前一天提交', 'cls': 'highlight'},
    {'time': '30:30', 'label': '作业示范', 'desc': '展示多种提交方式和标记方法', 'cls': ''},
    {'time': '32:30', 'label': '笔记要求', 'desc': '手写或截图均可，需体现反思', 'cls': ''},
    {'time': '33:40', 'label': '结语', 'desc': '有问题即时交流，期待有所收获', 'cls': ''},
]

timeline_html = ""
for item in timeline_items:
    cls = f' {item["cls"]}' if item["cls"] else ''
    timeline_html += f'''          <div class="event{cls}" onclick="seekTo({int(item["time"].split(":")[0])*60 + int(item["time"].split(":")[1])})">
            <span class="dot"></span>
            <b>{item["time"]} {item["label"]}</b>
            <p>{item["desc"]}</p>
          </div>
'''

duration_str = fmt_time(total_duration)

html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CourseMap - 雅思阅读导学</title>
<style>
  :root {{
    --bg: #f5f6f8;
    --surface: #ffffff;
    --text: #18202a;
    --text-secondary: #6c7480;
    --text-muted: #78818e;
    --border: #e7e9ee;
    --border-light: #edf0f3;
    --primary: #3157b7;
    --primary-light: #edf2ff;
    --primary-dark: #244bb3;
    --orange: #d59a20;
    --orange-light: #fff8e9;
    --orange-border: #efdfb2;
    --green: #4b7b59;
    --green-light: #edf8f0;
    --blue-note: #6a75d8;
    --blue-note-light: #f0f2ff;
    --blue-note-border: #dce1ff;
    --red: #a55353;
    --red-light: #fff1f1;
    --radius: 14px;
    --radius-sm: 10px;
    --shadow: 0 2px 8px rgba(20,28,40,.035);
    --shadow-md: 0 4px 16px rgba(20,28,40,.07);
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  button {{ font: inherit; border: 0; cursor: pointer; }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    overflow: hidden;
    height: 100vh;
  }}

  .app {{ height: 100vh; display: flex; flex-direction: column; }}

  /* TOP BAR */
  .topbar {{
    height: 64px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    padding: 0 24px;
    gap: 24px;
    z-index: 100;
    flex-shrink: 0;
  }}
  .brand {{ font-weight: 800; font-size: 18px; letter-spacing: -0.5px; color: var(--text); }}
  .phase-badge {{
    font-size: 12px; padding: 5px 9px; border-radius: 999px;
    background: var(--primary-light); color: var(--primary); font-weight: 600;
  }}
  .topbar .spacer {{ flex: 1; }}
  .topbar-progress {{ font-size: 13px; color: var(--text-secondary); }}
  .topbar-progress b {{ color: var(--text); }}
  .topbar-crumb {{ font-size: 13px; color: var(--text-muted); }}
  .topbar-crumb a {{ color: var(--text-secondary); cursor: pointer; text-decoration: none; }}
  .topbar-crumb a:hover {{ color: var(--primary); }}
  .topbar-crumb .current {{ color: var(--text); font-weight: 500; }}

  /* PAGE */
  .page {{ display: none; flex: 1; min-height: 0; }}
  .page.active {{ display: flex; flex-direction: column; }}

  /* CATALOG */
  .catalog-page {{ padding: 32px; overflow-y: auto; flex: 1; }}
  .catalog-header {{ margin-bottom: 28px; }}
  .catalog-header h1 {{ font-size: 24px; font-weight: 700; margin-bottom: 4px; }}
  .catalog-header p {{ color: var(--text-secondary); font-size: 14px; }}

  .subject-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 32px;
  }}
  .subject-card {{
    background: var(--surface); border-radius: var(--radius);
    padding: 20px; border: 1px solid var(--border);
    cursor: pointer; transition: all 0.2s; box-shadow: var(--shadow);
  }}
  .subject-card:hover {{ border-color: var(--primary); box-shadow: var(--shadow-md); transform: translateY(-2px); }}
  .subject-card.active {{ border-color: var(--primary); background: var(--primary-light); }}
  .subject-icon {{
    width: 40px; height: 40px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; margin-bottom: 12px;
  }}
  .subject-card:nth-child(1) .subject-icon {{ background: #e7f5ff; }}
  .subject-card:nth-child(2) .subject-icon {{ background: #fff8e6; }}
  .subject-card:nth-child(3) .subject-icon {{ background: #edf8f0; }}
  .subject-card:nth-child(4) .subject-icon {{ background: #f0f2ff; }}
  .subject-name {{ font-size: 16px; font-weight: 600; margin-bottom: 4px; }}
  .subject-meta {{ font-size: 12px; color: var(--text-secondary); margin-bottom: 12px; }}
  .progress-bar {{ height: 4px; background: var(--border-light); border-radius: 4px; overflow: hidden; }}
  .progress-fill {{ height: 100%; border-radius: 4px; transition: width 0.3s; }}
  .subject-card:nth-child(1) .progress-fill {{ background: var(--green); width: 100%; }}
  .subject-card:nth-child(2) .progress-fill {{ background: var(--orange); width: 0%; }}
  .subject-card:nth-child(3) .progress-fill {{ background: var(--green); width: 0%; }}
  .subject-card:nth-child(4) .progress-fill {{ background: var(--blue-note); width: 0%; }}
  .progress-label {{ font-size: 11px; color: var(--text-muted); margin-top: 6px; }}

  .lesson-section-header {{
    display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;
  }}
  .lesson-section-header h2 {{ font-size: 18px; font-weight: 600; }}

  .lesson-list {{ display: flex; flex-direction: column; gap: 8px; }}
  .lesson-item {{
    background: var(--surface); border-radius: var(--radius-sm);
    padding: 14px 18px; border: 1px solid var(--border);
    display: flex; align-items: center; gap: 14px;
    cursor: pointer; transition: all 0.15s; box-shadow: var(--shadow);
  }}
  .lesson-item:hover {{ border-color: var(--primary); box-shadow: var(--shadow-md); }}
  .lesson-item.current {{ border-color: var(--primary); background: var(--primary-light); }}
  .lesson-num {{
    width: 28px; height: 28px; border-radius: 50%;
    background: var(--bg); display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 600; color: var(--text-secondary); flex-shrink: 0;
  }}
  .lesson-info {{ flex: 1; min-width: 0; }}
  .lesson-title {{ font-size: 14px; font-weight: 500; margin-bottom: 2px; }}
  .lesson-subtitle {{ font-size: 12px; color: var(--text-muted); }}
  .badge {{ font-size: 11px; padding: 4px 8px; border-radius: 6px; font-weight: 500; }}
  .badge-learning {{ background: var(--orange-light); color: var(--orange); }}

  /* THREE-COLUMN LAYOUT */
  .layout {{ flex: 1; min-height: 0; display: grid; }}
  .side {{
    background: var(--surface); overflow-y: auto;
  }}
  .side.left {{ border-right: 1px solid var(--border); }}
  .side.right {{ border-left: 1px solid var(--border); }}
  .side h3 {{
    font-size: 13px; font-weight: 600; margin: 0;
    padding: 20px 18px 10px; color: var(--text-muted);
  }}
  .main {{ min-width: 0; overflow: auto; }}

  /* Preview layout */
  #page-preview .layout {{ grid-template-columns: 250px 1fr 310px; }}
  #page-preview .main {{ padding: 26px 30px; background: var(--bg); }}

  /* Learn layout */
  #page-learn .layout {{ grid-template-columns: 260px minmax(560px, 1fr) 330px; }}
  #page-learn .main {{ padding: 0; background: #eef0f3; }}

  /* Review layout */
  #page-review .layout {{ grid-template-columns: 250px 1fr 330px; }}
  #page-review .main {{ padding: 22px 26px; background: var(--bg); }}

  /* Practice layout */
  #page-practice .layout {{ grid-template-columns: 250px 1fr 330px; }}
  #page-practice .main {{ padding: 26px 30px; background: var(--bg); overflow-y: auto; }}

  .practice-header {{ margin-bottom: 20px; }}
  .practice-header h1 {{ font-size: 24px; margin-bottom: 6px; }}
  .practice-header p {{ color: var(--text-secondary); font-size: 14px; }}

  .practice-stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }}
  .practice-stat {{ padding: 16px; text-align: center; }}
  .practice-stat b {{ font-size: 28px; display: block; margin-top: 6px; color: var(--primary); }}

  .question-card {{ padding: 20px; margin-bottom: 16px; }}
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

  /* TREE ITEMS (white sidebar) */
  .tree-item {{
    padding: 9px 18px; font-size: 13px; color: #515b68;
    display: flex; gap: 8px; align-items: center;
    cursor: pointer; transition: background 0.1s;
  }}
  .tree-item:hover {{ background: #f6f7f9; }}
  .tree-item.active {{ font-weight: 650; color: var(--primary); background: var(--primary-light); }}
  .tree-child {{ padding-left: 34px; }}
  .tree-grandchild {{ padding-left: 50px; font-size: 12px; color: #7a828d; }}
  .tree-grandchild .node-dot {{ width: 4px; height: 4px; background: #d5d9e0; }}
  .tree-grandchild.active {{ color: var(--primary); }}
  .tree-grandchild.active .node-dot {{ background: var(--primary); }}
  .tree-item .node-dot {{
    width: 6px; height: 6px; border-radius: 50%;
    background: #ccd1d8; flex-shrink: 0;
  }}
  .tree-item.active .node-dot {{ background: var(--primary); }}
  .tree-item.in-range .node-dot {{ background: rgba(49,87,183,0.4); }}

  /* CARD */
  .card {{
    background: var(--surface); border: 1px solid #e6e8ed;
    border-radius: var(--radius); box-shadow: var(--shadow);
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

  /* ===== PREVIEW PAGE ===== */
  .hero {{ display: grid; grid-template-columns: 1fr 310px; gap: 18px; margin-bottom: 18px; }}
  .hero h1 {{ margin: 0 0 8px; font-size: 27px; }}
  .hero p {{ margin: 0; line-height: 1.65; color: #68727e; font-size: 14px; }}
  .metric {{ padding: 17px; }}
  .metric strong {{ font-size: 26px; display: block; margin-top: 6px; }}
  .check {{ display: flex; align-items: center; gap: 9px; padding: 7px 0; font-size: 13px; }}
  .check input {{ accent-color: var(--primary); }}

  /* Exploratory preview styles */
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

  .map-section {{ padding: 20px; margin-bottom: 18px; }}
  .maphead {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }}
  .nodes {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }}
  .node {{
    padding: 15px; border: 1px solid #e4e7ec; border-radius: 11px;
    cursor: pointer; transition: border-color 0.15s;
  }}
  .node:hover {{ border-color: #b9c4d7; }}
  .node.active {{ border-color: var(--primary); background: var(--primary-light); }}
  .node strong {{ font-size: 14px; }}
  .node span {{ display: block; color: var(--text-muted); font-size: 12px; margin-top: 7px; line-height: 1.5; }}

  .preview-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
  .preview-grid .card {{ padding: 18px; }}
  .preview-grid .card h3 {{ font-size: 15px; font-weight: 600; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }}
  .preview-grid .card h3 .tag {{ font-size: 10px; padding: 2px 6px; border-radius: 3px; background: var(--orange-light); color: var(--orange); font-weight: 600; }}
  .preview-grid .card p {{ font-size: 13px; color: var(--text-secondary); line-height: 1.7; }}
  .highlight-box {{
    margin-top: 10px; padding: 10px 14px;
    background: var(--orange-light); border-left: 3px solid var(--orange);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    font-size: 13px; color: #7c5e00;
  }}
  .source-entry {{
    border-left: 3px solid #d9dde5; padding-left: 12px;
    font-size: 13px; line-height: 1.65; color: #59636f;
  }}

  .cta-btn {{
    background: #17202b; color: #fff; padding: 13px 16px;
    border-radius: 10px; font-size: 14px; font-weight: 500;
  }}

  /* ===== LEARN PAGE ===== */
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
  .note-quick-btn {{
    padding: 7px 14px; background: var(--primary); color: #fff;
    border-radius: 8px; font-size: 12px; font-weight: 500;
    margin-left: auto;
  }}

  .knowledge-card {{ margin: 16px 18px 0; padding: 18px; }}
  .knowledge-card h2 {{ font-size: 19px; margin: 8px 0; }}
  .knowledge-card p {{ line-height: 1.7; font-size: 13px; color: #59636f; }}
  .insight {{
    padding: 14px; border-radius: 11px;
    background: var(--orange-light); border: 1px solid var(--orange-border); margin-top: 14px;
  }}
  .insight p {{ font-size: 14px; line-height: 1.65; color: #7c5e00; margin-top: 8px; }}
  .my-note {{
    padding: 14px; border-radius: 11px;
    background: var(--blue-note-light); border: 1px solid var(--blue-note-border); margin-top: 12px;
  }}
  .my-note p {{ font-size: 13px; line-height: 1.6; color: #4a5080; margin-top: 8px; }}

  /* Transcript in right sidebar */
  .transcript-sidebar {{
    border-bottom: 1px solid var(--border);
    display: flex; flex-direction: column;
    height: calc(38vh + 50px);
  }}
  .transcript-sidebar .ts-header {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 16px; flex-shrink: 0;
  }}
  .transcript-sidebar .ts-header b {{ font-size: 13px; }}
  .transcript-scroll {{
    overflow-y: auto; flex: 1; padding: 0 16px 12px;
  }}
  .transcript-section {{
    margin: 12px 18px 18px; padding: 14px;
    background: var(--surface); border: 1px solid #e6e8ed;
    border-radius: 11px; box-shadow: var(--shadow);
  }}
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

  /* ===== REVIEW PAGE ===== */
  .reviewhead {{ display: flex; justify-content: space-between; align-items: end; margin-bottom: 18px; }}
  .reviewhead h1 {{ margin: 0; font-size: 26px; }}
  .scoregrid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px; }}
  .stat {{ padding: 15px; }}
  .stat b {{ font-size: 23px; display: block; margin-top: 7px; }}
  .reviewgrid {{ display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 14px; }}
  .panel {{ padding: 18px; }}

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

  /* RIGHT SIDEBAR COMMON */
  .rail {{ padding: 18px; }}
  .railtitle {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
  .notequick {{
    padding: 14px; background: #f8f9fb;
    border: 1px solid #e4e7ec; border-radius: 11px; margin-bottom: 16px;
  }}
  .notequick p {{ line-height: 1.6; }}

  /* TIMELINE (right sidebar) */
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
  .event.note .dot {{ background: var(--blue-note); }}
  .event b {{ font-size: 12px; }}
  .event p {{ margin: 5px 0 0; font-size: 12px; line-height: 1.5; color: #69727e; }}
  .event:hover b {{ color: var(--primary); }}

  /* NOTE MODAL */
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

  /* TOAST */
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
  <div class="brand">CourseMap</div>
  <span class="phase-badge" id="phaseBadge">PREVIEW · 预习</span>
  <span class="topbar-crumb" id="breadcrumb">
    <span>雅思备考</span> · <span class="current">阅读</span>
  </span>
  <div class="spacer"></div>
  <span class="topbar-progress" id="topProgress">总时长 <b>{duration_str}</b></span>
</header>

<!-- ===== CATALOG PAGE ===== -->
<div class="page active" id="page-catalog">
  <div class="catalog-page">
    <div class="catalog-header">
      <h1>雅思备考课程</h1>
      <p>共 4 个科目 · 阅读导学课程</p>
    </div>
    <div class="subject-grid">
      <div class="subject-card" onclick="selectSubject(0)">
        <div class="subject-icon">🎧</div>
        <div class="subject-name">听力</div>
        <div class="subject-meta">即将开放</div>
        <div class="progress-bar"><div class="progress-fill"></div></div>
        <div class="progress-label">敬请期待</div>
      </div>
      <div class="subject-card" onclick="selectSubject(1)">
        <div class="subject-icon">🗣️</div>
        <div class="subject-name">口语</div>
        <div class="subject-meta">即将开放</div>
        <div class="progress-bar"><div class="progress-fill"></div></div>
        <div class="progress-label">敬请期待</div>
      </div>
      <div class="subject-card active" onclick="selectSubject(2)">
        <div class="subject-icon">📖</div>
        <div class="subject-name">阅读</div>
        <div class="subject-meta">导学课 · {duration_str}</div>
        <div class="progress-bar"><div class="progress-fill"></div></div>
        <div class="progress-label">当前课程</div>
      </div>
      <div class="subject-card" onclick="selectSubject(3)">
        <div class="subject-icon">✍️</div>
        <div class="subject-name">写作</div>
        <div class="subject-meta">即将开放</div>
        <div class="progress-bar"><div class="progress-fill"></div></div>
        <div class="progress-label">敬请期待</div>
      </div>
    </div>
    <div class="lesson-section-header">
      <h2>阅读课程</h2>
    </div>
    <div class="lesson-list">
      <div class="lesson-item current" onclick="enterLesson('阅读导学')">
        <div class="lesson-num">1</div>
        <div class="lesson-info">
          <div class="lesson-title">阅读导学</div>
          <div class="lesson-subtitle">考情介绍 · 题型总览 · 评分标准 · 复习计划 · 课程安排</div>
        </div>
        <span class="badge badge-learning">学习中</span>
      </div>
    </div>
  </div>
</div>

<!-- ===== PREVIEW PAGE ===== -->
<div class="page" id="page-preview">
  <div class="layout">
    <aside class="side left">
      <h3>本节知识地图</h3>
      <div id="preview-tree">
{tree_html}
      </div>
    </aside>
    <main class="main">
      <section class="hero">
        <div class="card" style="padding:24px">
          <h1>先看懂这节课讲了什么</h1>
          <p>不用播放完整视频。先用 2-5 分钟建立知识地图，知道老师会讲哪些东西、哪些地方值得特别留意，再决定进入网课。</p>
          <div style="margin-top:18px" class="row">
            <button class="cta-btn" onclick="switchPhase('learn')">开始预习</button>
            <button class="btn ghost" onclick="switchPhase('practice')">📝 直接练习</button>
            <button class="btn ghost" onclick="toast('已标记：稍后重点看')">☆ 稍后重点看</button>
          </div>
        </div>
        <div class="card metric">
          <span class="muted small">预计预习时间</span>
          <strong>03:20</strong>
          <span class="muted small">覆盖 {sum(len(n['children']) for n in knowledge_tree)} 个知识模块 · 7 个老师重点</span>
          <div style="margin-top:16px">
            <div class="check"><input type="checkbox" checked> 我已知道考试结构</div>
            <div class="check"><input type="checkbox"> 我知道本课重点</div>
            <div class="check"><input type="checkbox"> 我知道要解决的问题</div>
          </div>
        </div>
      </section>
      <section class="card map-section">
        <div class="maphead">
          <div><b>课程知识地图</b><div class="muted small" style="margin-top:4px">只放"知识点"，不把重点/笔记混进树里</div></div>
          <span class="pill">点击节点查看预习卡片</span>
        </div>
        <div class="nodes" id="nodes">
{"".join(f'''          <div class="node{' active' if i==0 else ''}" data-node="n{i}"><strong>{i+1:02d} · {html.escape(n["text"])}</strong><span>{len(n['children'])} 个知识模块</span></div>
''' for i, n in enumerate(knowledge_tree))}
        </div>
      </section>
      <section class="preview-grid">
{preview_html}
      </section>
    </main>
    <aside class="side right">
      <h3>预习清单</h3>
      <div style="padding:0 16px">
        <div class="card" style="padding:14px;margin-bottom:11px">
          <b style="font-size:13px">我需要知道</b>
          <div class="check"><input type="checkbox"> 课程整体结构</div>
          <div class="check"><input type="checkbox"> 老师重点在哪里</div>
          <div class="check"><input type="checkbox"> 哪些内容需要进视频深学</div>
        </div>
        <div class="card" style="padding:14px;margin-bottom:11px">
          <b style="font-size:13px">老师重点预览</b>
          <div style="margin-top:10px;padding:13px;border-radius:10px;background:var(--orange-light);border:1px solid var(--orange-border)">
            <span class="pill">★ 老师敲黑板</span>
            <p style="margin:9px 0 0;line-height:1.65;font-size:13px">{html.escape(preview_cards[0]["highlight"])}</p>
          </div>
          <div style="margin-top:10px;padding:13px;border-radius:10px;background:var(--orange-light);border:1px solid var(--orange-border)">
            <span class="pill">★ 核心题型</span>
            <p style="margin:9px 0 0;line-height:1.65;font-size:13px">{html.escape(preview_cards[1]["highlight"])}</p>
          </div>
        </div>
        <div class="card" style="padding:14px">
          <b style="font-size:13px">进入网课前</b>
          <p class="muted small" style="line-height:1.6">预习不是背知识，而是先知道"等会儿要听什么"。</p>
          <button class="btn primary-blue" style="width:100%;margin-top:10px" onclick="switchPhase('learn')">进入网课 →</button>
        </div>
      </div>
    </aside>
  </div>
</div>

<!-- ===== LEARN PAGE ===== -->
<div class="page" id="page-learn">
  <div class="layout">
    <aside class="side left">
      <h3>知识节点</h3>
      <div id="learn-tree">
{tree_html}
      </div>
      <h3>我的标记</h3>
      <div class="tree-item" onclick="seekTo(318)">💭 05:18 为什么 F ≠ NG？</div>
      <div class="tree-item" onclick="seekTo(1175)">💭 19:35 为什么要整套做真题？</div>
    </aside>
    <main class="main">
      <div class="video">
        <video id="mainVideo" src="{VIDEO_FILE}"></video>
        <div class="video-controls">
          <button class="btn" style="background:#26303b;color:#fff;font-size:12px" onclick="togglePlay()" id="playBtn">▶ 播放</button>
          <div class="bar" onclick="seekBar(event)"><i id="bar" style="width:0%"></i></div>
          <span class="time-label" id="time">00:00 / {duration_str}</span>
          <button class="speed-btn" onclick="cycleSpeed()" id="speed">1×</button>
          <button class="note-quick-btn" onclick="openNoteModal()">＋ 记录想法</button>
        </div>
      </div>
      <section class="card knowledge-card">
        <span class="pill">当前知识点</span>
        <h2 id="ktitle">雅思阅读考情介绍</h2>
        <p id="kbody">老师正在介绍雅思阅读考试的基本信息，包括考试时间、文章结构和题型分布。</p>
        <div class="insight">
          <span class="pill">★ 老师敲黑板</span>
          <p id="insight">{html.escape(preview_cards[0]["highlight"])}</p>
          <button class="btn" style="margin-top:10px" onclick="seekTo(0)">▶ 回到老师原话</button>
        </div>
        <div class="my-note">
          <span class="pill">💭 我的思考</span>
          <p>"先了解考试整体结构，再进入具体题型的学习。"</p>
          <button class="btn" style="margin-top:9px" onclick="openNoteModal()">编辑我的思考</button>
        </div>
        <div style="margin-top:14px;display:flex;gap:8px">
          <button class="btn ghost" onclick="switchPhase('practice')">📝 去练习</button>
          <button class="btn ghost" onclick="switchPhase('review')">🔄 去复习</button>
        </div>
      </section>
    </main>
    <aside class="side right">
      <div class="transcript-sidebar">
        <div class="ts-header">
          <b>老师原文 · {len(lines)} 段</b>
          <button class="btn" style="font-size:12px" onclick="toast('已展开完整转录')">展开</button>
        </div>
        <div class="transcript-scroll">
{transcript_html}
        </div>
      </div>
      <div class="rail">
        <div class="railtitle">
          <b style="font-size:14px">课程知识时间轴</b>
          <span class="pill">边看边记</span>
        </div>
        <div class="notequick">
          <b style="font-size:13px">此刻发生了什么？</b>
          <p class="muted small">视频正在讲一个知识点。你的笔记会自动绑定当前时间，并在课后归入对应节点。</p>
          <button class="btn primary-blue" style="width:100%;margin-top:10px" onclick="openNoteModal()">＋ 记录此刻想法</button>
        </div>
        <div class="timeline">
{timeline_html}
        </div>
      </div>
    </aside>
  </div>
</div>

<!-- ===== REVIEW PAGE ===== -->
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
    <main class="main">
      <div class="reviewhead">
        <div>
          <h1>2 分钟，把整节课重新想一遍</h1>
          <div class="muted small" style="margin-top:6px">复习不是重看视频，而是先回忆 → 再验证 → 最后溯源。</div>
        </div>
        <button class="btn primary" onclick="startReview()">开始快速复习</button>
        <button class="btn primary-blue" style="margin-left:8px" onclick="switchPhase('practice')">进入练习 →</button>
      </div>
      <div class="scoregrid">
        <div class="card stat"><span class="muted small">知识模块</span><b>{sum(len(n['children']) for n in knowledge_tree)}</b><span class="muted small">本节全部覆盖</span></div>
        <div class="card stat"><span class="muted small">老师重点</span><b>7</b><span class="muted small">全部可回溯</span></div>
        <div class="card stat"><span class="muted small">我的想法</span><b>2</b><span class="muted small">自动挂到知识点</span></div>
        <div class="card stat"><span class="muted small">待掌握</span><b id="weaknum">2</b><span class="muted small">建议优先复习</span></div>
      </div>
      <div class="reviewgrid">
        <section class="card panel">
          <div class="row" style="justify-content:space-between">
            <div><b>① 先回忆，不看答案</b><div class="muted small" style="margin-top:4px">点击卡片，写在脑中的答案会被揭示</div></div>
            <span class="tag">主动回忆</span>
          </div>
          <div class="recall" style="margin-top:14px">
            <div class="recallcard" onclick="this.classList.toggle('open')">
              <b>填空和判断占多少题？</b>
              <div class="ans">{html.escape(preview_cards[1]["highlight"])}</div>
            </div>
            <div class="recallcard" onclick="this.classList.toggle('open')">
              <b>7分需要错几题以内？</b>
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
        <section class="card panel">
          <div class="row" style="justify-content:space-between">
            <b>③ 课程知识时间轴</b>
            <span class="tag success">快速回看</span>
          </div>
          <p class="muted small" style="line-height:1.6">只看关键节点；需要深入时，再回到老师原文和视频。</p>
          <div class="mini-timeline">
            <div class="mini" onclick="seekTo(78)"><span class="when">01:18</span><div><b>考试基本信息</b><p>建立考试整体框架</p></div></div>
            <div class="mini" onclick="seekTo(200)"><span class="when">03:20</span><div><b>题型总览</b><p>基础→细节→过渡→宏观</p></div></div>
            <div class="mini" onclick="seekTo(720)"><span class="when">12:00</span><div><b>★ 评分标准</b><p>错10题=7分关键线</p></div></div>
            <div class="mini" onclick="seekTo(1095)"><span class="when">18:15</span><div><b>刷题顺序</b><p>C13→C4→C9→C15</p></div></div>
            <div class="mini" onclick="seekTo(1340)"><span class="when">22:20</span><div><b>课程大纲</b><p>启航班vs飞跃班</p></div></div>
          </div>
          <div class="sourcejump">
            <b style="font-size:13px">④ 最后再溯源</b>
            <p class="muted small" style="line-height:1.6">你刚才没记住的，不需要重新看 34 分钟。直接跳到对应老师原文 / 视频位置。</p>
            <button class="btn primary" style="margin-top:10px" onclick="seekTo(720)">▶ 定位老师原文 12:00</button>
          </div>
        </section>
      </div>
    </main>
    <aside class="side right">
      <h3>本次复习结果</h3>
      <div style="padding:0 16px">
        <div class="card" style="padding:15px;margin-bottom:11px">
          <b style="font-size:13px">知识掌握</b>
          <div style="font-size:30px;font-weight:800;margin:7px 0">{sum(len(n['children']) for n in knowledge_tree) - 2} / {sum(len(n['children']) for n in knowledge_tree)}</div>
          <div class="barline"><i style="width:78%"></i></div>
          <p class="muted small" style="line-height:1.6">你已经覆盖大部分知识点。剩下 2 个薄弱点可以直接进入原文。</p>
        </div>
        <div class="card" style="padding:15px;margin-bottom:11px">
          <b style="font-size:13px">老师重点</b>
          <p class="muted small">★ {html.escape(preview_cards[0]["highlight"][:25])}...</p>
          <p class="muted small">★ {html.escape(preview_cards[1]["highlight"][:25])}...</p>
          <p class="muted small">★ {html.escape(preview_cards[2]["highlight"][:25])}...</p>
          <button class="btn" style="width:100%;margin-top:8px" onclick="toast('已打开老师重点列表')">查看全部重点</button>
        </div>
        <div class="card" style="padding:15px">
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

<!-- ===== PRACTICE PAGE ===== -->
<div class="page" id="page-practice">
  <div class="layout">
    <aside class="side left">
      <h3>练习导航</h3>
      <div class="tree-item active" onclick="scrollToQuestion(0)">📝 选择题 · 3 题</div>
      <div class="tree-item" onclick="scrollToQuestion(3)">⭕ 判断题 · 2 题</div>
      <div class="tree-item" onclick="scrollToQuestion(5)">✏️ 填空题 · 2 题</div>
      <h3>题型分布</h3>
      <div style="padding: 0 16px;">
        <div class="card" style="padding:14px;margin-bottom:11px">
          <b style="font-size:13px">本节练习</b>
          <div style="margin-top:8px;font-size:13px;color:var(--text-secondary)">
            <div>选择题 × 3</div>
            <div>判断题 × 2</div>
            <div>填空题 × 2</div>
          </div>
        </div>
        <div class="card" style="padding:14px">
          <b style="font-size:13px">考试题型占比</b>
          <div style="margin-top:8px">
            <div class="row" style="margin-bottom:6px"><span style="font-size:12px">填空+判断</span><div class="spacer"></div><span class="tag success">~50%</span></div>
            <div class="row" style="margin-bottom:6px"><span style="font-size:12px">选择题</span><div class="spacer"></div><span class="tag">过渡</span></div>
            <div class="row"><span style="font-size:12px">匹配+Heading</span><div class="spacer"></div><span class="tag">宏观</span></div>
          </div>
        </div>
      </div>
    </aside>
    <main class="main">
      <div class="practice-header">
        <h1>练一练，检验学习效果</h1>
        <p>基于本节课程内容，练习雅思阅读核心题型。答完即时反馈，薄弱点自动标记。</p>
      </div>
      <div class="practice-stats">
        <div class="card practice-stat"><span class="muted small">总题数</span><b>7</b></div>
        <div class="card practice-stat"><span class="muted small">已完成</span><b id="doneCount">0</b></div>
        <div class="card practice-stat"><span class="muted small">正确率</span><b id="accuracy">--</b></div>
        <div class="card practice-stat"><span class="muted small">预计用时</span><b>5 min</b></div>
      </div>

      <div id="questionList">
        <!-- Q1: 选择题 -->
        <div class="card question-card" data-qid="0" data-type="choice" data-answer="1">
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

        <!-- Q2: 选择题 -->
        <div class="card question-card" data-qid="1" data-type="choice" data-answer="2">
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

        <!-- Q3: 选择题 -->
        <div class="card question-card" data-qid="2" data-type="choice" data-answer="1">
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
          <div class="feedback incorrect">✗ 再想想。提示：老师说"填空+判断占约 20 题，是必须把握的基础题型"。</div>
        </div>

        <!-- Q4: 判断题 -->
        <div class="card question-card" data-qid="3" data-type="tfng" data-answer="true">
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

        <!-- Q5: 判断题 -->
        <div class="card question-card" data-qid="4" data-type="tfng" data-answer="false">
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

        <!-- Q6: 填空题 -->
        <div class="card question-card" data-qid="5" data-type="fill" data-answer="定位">
          <h3><span class="question-type">填空题</span> 第 6 题</h3>
          <div class="question-text">雅思阅读解题的基础能力是 ______ 和同义替换。（填入两个字的关键词）</div>
          <input class="fill-input" type="text" placeholder="输入你的答案…" oninput="onFillInput(this)">
          <button class="check-btn" onclick="checkFill(this)" disabled>检查答案</button>
          <div class="feedback correct">✓ 正确！"定位"和"同义替换"是所有题型的基础，课程会先从这里开始。</div>
          <div class="feedback incorrect">✗ 再想想。提示：老师说"____ 和同义替换是所有题型的基础知识"——回忆课程解题逻辑的起点。</div>
        </div>

        <!-- Q7: 填空题 -->
        <div class="card question-card" data-qid="6" data-type="fill" data-answer="正确率">
          <h3><span class="question-type">填空题</span> 第 7 题</h3>
          <div class="question-text">做真题时，______ 的重要性大于速度，先保证它再慢慢提速。（填入三个字）</div>
          <input class="fill-input" type="text" placeholder="输入你的答案…" oninput="onFillInput(this)">
          <button class="check-btn" onclick="checkFill(this)" disabled>检查答案</button>
          <div class="feedback correct">✓ 正确！老师说"正确率的重要性大于速度，先保证正确率再慢慢提速"。</div>
          <div class="feedback incorrect">✗ 再想想。提示：老师说的是做题时先保证什么，再提速？不是速度，而是另一个维度。</div>
        </div>
      </div>

      <div class="progress-section">
        <div class="card" style="padding:18px">
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
    </main>
    <aside class="side right">
      <h3>练习结果</h3>
      <div style="padding:0 16px">
        <div class="card" style="padding:15px;margin-bottom:11px">
          <b style="font-size:13px">答题统计</b>
          <div id="resultSummary" style="margin-top:10px">
            <p class="muted small">还没有完成任何题目</p>
          </div>
        </div>
        <div class="card" style="padding:15px;margin-bottom:11px">
          <b style="font-size:13px">薄弱知识点</b>
          <div id="weakPoints" style="margin-top:10px">
            <p class="muted small">答完题后自动标记</p>
          </div>
        </div>
        <div class="card" style="padding:15px">
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
    <p class="muted small" style="margin:8px 0">保存后会自动绑定时间；AI稍后把它归入对应知识节点。</p>
    <textarea id="noteText" placeholder="例如：这里老师说填空和判断最容易混，我想回去找一个具体例子……"></textarea>
    <div class="row" style="justify-content:flex-end;margin-top:12px">
      <button class="btn" onclick="closeNoteModal()">取消</button>
      <button class="btn primary" onclick="saveNote()">保存想法</button>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
  const video = document.getElementById('mainVideo');
  const transcriptLines = document.querySelectorAll('.transcript-line');
  const treeNodes = document.querySelectorAll('#learn-tree .tree-item');

  // Navigation
  function selectSubject(idx) {{
    document.querySelectorAll('.subject-card').forEach((c, i) => c.classList.toggle('active', i === idx));
  }}

  function enterLesson(title) {{
    document.getElementById('page-catalog').classList.remove('active');
    document.getElementById('page-preview').classList.add('active');
    document.getElementById('phaseBadge').textContent = 'PREVIEW · 预习';
    document.getElementById('breadcrumb').innerHTML =
      '<a onclick="backToCatalog()">雅思备考</a> · <span class="current">' + title + '</span>';
  }}

  function backToCatalog() {{
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById('page-catalog').classList.add('active');
    document.getElementById('breadcrumb').innerHTML =
      '<span>雅思备考</span> · <span class="current">阅读</span>';
    document.getElementById('phaseBadge').textContent = '';
  }}

  function switchPhase(phase) {{
    const pages = {{ preview: 'page-preview', learn: 'page-learn', review: 'page-review', practice: 'page-practice' }};
    const badges = {{ preview: 'PREVIEW · 预习', learn: 'CLASS · 网课', review: 'REVIEW · 复习', practice: 'PRACTICE · 练习' }};
    document.querySelectorAll('.page').forEach(p => {{
      if (Object.values(pages).includes(p.id)) p.classList.remove('active');
    }});
    document.getElementById(pages[phase]).classList.add('active');
    document.getElementById('phaseBadge').textContent = badges[phase];
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
    toast('已定位到 ' + fmtTime(sec));
  }}

  // Video + Transcript sync (karaoke style)
  if (video) {{
    video.addEventListener('timeupdate', function() {{
      const t = video.currentTime;

      // Update progress bar
      document.getElementById('bar').style.width = (t / video.duration * 100) + '%';
      document.getElementById('time').textContent = fmtTime(t) + ' / ' + fmtTime(video.duration);

      // Update transcript highlight
      transcriptLines.forEach(line => {{
        const start = parseFloat(line.dataset.start);
        const end = parseFloat(line.dataset.end);
        line.classList.remove('read', 'current');
        if (t >= start && t < end) {{
          line.classList.add('current');
          line.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        }} else if (t >= end) {{
          line.classList.add('read');
        }}
      }});

      // Update tree highlight (2 levels)
      treeNodes.forEach(node => {{
        const start = parseFloat(node.dataset.start);
        const end = parseFloat(node.dataset.end);
        node.classList.remove('active', 'in-range');
        if (t >= start && t < end) {{
          node.classList.add('in-range');
        }}
        // L1 active (parent section)
        if (t >= start && t < end && !node.classList.contains('tree-child')) {{
          node.classList.add('active');
        }}
        // L2 active (topic)
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

    // Click transcript to seek video
    transcriptLines.forEach(line => {{
      line.addEventListener('click', function() {{
        video.currentTime = parseFloat(this.dataset.start);
        video.play();
        playing = true;
        document.getElementById('playBtn').textContent = '❚❚ 暂停';
      }});
    }});
  }}

  // Note modal
  function openNoteModal() {{
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
  }}
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

  // Review
  function startReview() {{ toast('进入主动回忆模式：先点卡片，不急着看答案'); }}

  // Practice
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

  // Toast
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

output_path = os.path.join(os.path.dirname(__file__), 'prototype.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated prototype.html with {len(lines)} transcript lines")
print(f"Video duration: {duration_str}")
print(f"Knowledge tree: {sum(len(n['children']) for n in knowledge_tree)} sub-nodes in {len(knowledge_tree)} groups")
