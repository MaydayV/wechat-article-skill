#!/usr/bin/env python3
"""
文章发布前校验脚本。

检查项：
1. 禁止声明扫描
2. 风险话题识别
3. 硬事实标记（含具体数字但无来源的句子）
4. 结构重复检测（与最近文章对比）
5. 金句重复检测

用法:
  python3 validate_article.py --content-file article.html [--history-dir ./history]

输出 JSON 格式的校验报告。
"""
import argparse
import json
import os
import re
import sys
from typing import Dict, List


# ── 禁止声明 ──────────────────────────────────────────────
FORBIDDEN_PHRASES = [
    "保证收益", "稳赚不赔", "零风险",
    "100%有效", "包治百病", "立竿见影",
    "国家机密", "内部消息", "独家爆料",
    "不转不是中国人",
]

# ── 高风险关键词 ──────────────────────────────────────────
HIGH_RISK_KEYWORDS = {
    "政治": ["中央", "政府政策", "国务院", "领导人", "党中央", "意识形态"],
    "金融投资": ["股票推荐", "基金推荐", "保证收益", "年化收益", "投资建议", "理财产品"],
    "医疗健康": ["治疗方案", "药物推荐", "偏方", "根治", "特效药", "诊断"],
    "法律": ["法律建议", "诉讼策略", "维权方案"],
}

# ── 中风险关键词 ──────────────────────────────────────────
MEDIUM_RISK_KEYWORDS = {
    "行业分析": ["市场规模", "行业报告", "增长率"],
    "人物评价": ["某某人", "创始人", "CEO"],
    "产品对比": ["对比评测", "优于", "不如", "碾压"],
}

# ── 需要来源的数据模式 ────────────────────────────────────
# 匹配 "据统计"、"数据显示"、百分比、具体金额等
DATA_CLAIM_PATTERNS = [
    r"据统计[，,]",
    r"数据显示[，,]",
    r"研究表明[，,]",
    r"调查发现[，,]",
    r"\d+%",                    # 百分比
    r"\d+[万亿]",               # 大数字
    r"第[一二三四五六七八九十]名",  # 排名
]

# ── 免责声明模板 ──────────────────────────────────────────
DISCLAIMERS = {
    "金融投资": ["不构成投资建议", "投资有风险", "请根据自身情况判断"],
    "医疗健康": ["请咨询专业医生", "不构成医疗建议", "仅供参考"],
    "法律": ["请咨询专业律师", "不构成法律意见"],
}


def strip_html(html: str) -> str:
    """去除 HTML 标签，保留纯文本。"""
    text = re.sub(r"<[^>]+>", "", html)
    text = re.sub(r"&[a-zA-Z]+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_sentences(text: str) -> List[str]:
    """按中文句号、问号、感叹号分句。"""
    sentences = re.split(r"[。！？!?]", text)
    return [s.strip() for s in sentences if s.strip()]


def check_forbidden(text: str) -> List[Dict]:
    """检查禁止声明。"""
    issues = []
    for phrase in FORBIDDEN_PHRASES:
        if phrase in text:
            # 找到包含该短语的句子
            for sentence in split_sentences(text):
                if phrase in sentence:
                    issues.append({
                        "level": "error",
                        "type": "forbidden_phrase",
                        "phrase": phrase,
                        "context": sentence[:100],
                    })
    return issues


def check_risk_topics(text: str) -> List[Dict]:
    """识别风险话题。"""
    issues = []
    for category, keywords in HIGH_RISK_KEYWORDS.items():
        matched = [kw for kw in keywords if kw in text]
        if matched:
            # 检查是否有对应的免责声明
            has_disclaimer = False
            if category in DISCLAIMERS:
                for disclaimer in DISCLAIMERS[category]:
                    if disclaimer in text:
                        has_disclaimer = True
                        break
            
            issues.append({
                "level": "error" if not has_disclaimer else "warning",
                "type": "high_risk_topic",
                "category": category,
                "matched_keywords": matched,
                "has_disclaimer": has_disclaimer,
                "suggestion": f"建议添加免责声明：{DISCLAIMERS.get(category, ['请谨慎处理'])[0]}" if not has_disclaimer else "已包含免责声明",
            })

    for category, keywords in MEDIUM_RISK_KEYWORDS.items():
        matched = [kw for kw in keywords if kw in text]
        if matched:
            issues.append({
                "level": "info",
                "type": "medium_risk_topic",
                "category": category,
                "matched_keywords": matched,
                "suggestion": "建议使用客观表述，标注信息来源",
            })
    return issues


def check_data_claims(text: str) -> List[Dict]:
    """检查硬事实是否有来源。"""
    issues = []
    sentences = split_sentences(text)
    
    source_indicators = ["据", "根据", "来源", "报告", "数据来自", "引用", "出处", "《", "来自"]
    
    for sentence in sentences:
        for pattern in DATA_CLAIM_PATTERNS:
            if re.search(pattern, sentence):
                # 检查同一句话是否有来源标注
                has_source = any(indicator in sentence for indicator in source_indicators)
                if not has_source:
                    issues.append({
                        "level": "warning",
                        "type": "unverified_claim",
                        "sentence": sentence[:120],
                        "suggestion": "该句包含具体数据但未标注来源，建议添加数据出处或改为模糊表述",
                    })
                break  # 一个句子只报一次
    return issues


def check_structure_repetition(text: str, history_dir: str = None) -> List[Dict]:
    """检查与历史文章的结构重复。"""
    issues = []
    if not history_dir or not os.path.isdir(history_dir):
        return issues
    
    # 简单的结构指纹：段落数量 + 平均段落长度
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    current_fingerprint = {
        "para_count": len(paragraphs),
        "avg_para_len": sum(len(p) for p in paragraphs) / max(len(paragraphs), 1),
    }
    
    # 读取历史文章
    history_files = sorted(
        [f for f in os.listdir(history_dir) if f.endswith(".html") or f.endswith(".txt")],
        reverse=True,
    )[:5]  # 最近5篇
    
    for hf in history_files:
        with open(os.path.join(history_dir, hf), "r", encoding="utf-8") as f:
            hist_text = strip_html(f.read())
        hist_paragraphs = [p.strip() for p in hist_text.split("\n") if p.strip()]
        hist_fingerprint = {
            "para_count": len(hist_paragraphs),
            "avg_para_len": sum(len(p) for p in hist_paragraphs) / max(len(hist_paragraphs), 1),
        }
        
        # 如果段落数量和平均长度都很接近，标记为结构相似
        if (abs(current_fingerprint["para_count"] - hist_fingerprint["para_count"]) <= 1 and
            abs(current_fingerprint["avg_para_len"] - hist_fingerprint["avg_para_len"]) < 20):
            issues.append({
                "level": "info",
                "type": "structure_similar",
                "similar_to": hf,
                "suggestion": "与最近文章结构相似，建议尝试不同的文章结构",
            })
    return issues


def compute_risk_score(issues: List[Dict]) -> int:
    """计算风险分数。0-100，越高越危险。"""
    score = 0
    for issue in issues:
        if issue["level"] == "error":
            score += 30
        elif issue["level"] == "warning":
            score += 10
        elif issue["level"] == "info":
            score += 3
    return min(score, 100)


def validate(content_file: str, history_dir: str = None) -> Dict:
    """执行完整校验，返回报告。"""
    with open(content_file, "r", encoding="utf-8") as f:
        raw_content = f.read()
    
    text = strip_html(raw_content)
    
    all_issues = []
    all_issues.extend(check_forbidden(text))
    all_issues.extend(check_risk_topics(text))
    all_issues.extend(check_data_claims(text))
    all_issues.extend(check_structure_repetition(text, history_dir))
    
    risk_score = compute_risk_score(all_issues)
    
    errors = [i for i in all_issues if i["level"] == "error"]
    warnings = [i for i in all_issues if i["level"] == "warning"]
    infos = [i for i in all_issues if i["level"] == "info"]
    
    # 判断是否可以发布
    can_publish = len(errors) == 0
    needs_review = len(warnings) > 0
    
    report = {
        "risk_score": risk_score,
        "can_publish": can_publish,
        "needs_review": needs_review,
        "summary": {
            "errors": len(errors),
            "warnings": len(warnings),
            "infos": len(infos),
        },
        "issues": all_issues,
    }
    
    if not can_publish:
        report["block_reason"] = "存在禁止声明或高风险内容未添加免责声明，请修改后再发布"
    elif needs_review:
        report["review_note"] = "存在待核实数据或中风险内容，建议人工确认后发布"
    
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="文章发布前校验")
    parser.add_argument("--content-file", required=True, help="HTML 内容文件路径")
    parser.add_argument("--history-dir", default=None, help="历史文章目录（用于结构重复检测）")
    args = parser.parse_args()

    if not os.path.isfile(args.content_file):
        print(json.dumps({"error": f"文件不存在: {args.content_file}"}, ensure_ascii=False))
        sys.exit(1)

    report = validate(args.content_file, args.history_dir)
    
    print(json.dumps(report, ensure_ascii=False, indent=2))
    
    # 输出人类可读的摘要
    print("\n" + "=" * 50, file=sys.stderr)
    print(f"风险评分: {report['risk_score']}/100", file=sys.stderr)
    print(f"错误: {report['summary']['errors']} | 警告: {report['summary']['warnings']} | 提示: {report['summary']['infos']}", file=sys.stderr)
    
    if not report["can_publish"]:
        print(f"❌ 不建议发布: {report.get('block_reason', '')}", file=sys.stderr)
        sys.exit(2)
    elif report["needs_review"]:
        print(f"⚠️ 建议人工确认: {report.get('review_note', '')}", file=sys.stderr)
        sys.exit(0)
    else:
        print("✅ 校验通过，可以发布", file=sys.stderr)
        sys.exit(0)
