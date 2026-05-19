#!/usr/bin/env python3
"""
Generate PR Summary Dashboard SVG

Usage:
    python generate_summary_svg.py <pr_data.json> > summary.svg
"""

import json
import math
import sys
from pathlib import Path


# Color scheme (dark theme)
COLORS = {
    'bg': '#1a1a2e',
    'card': '#16213e',
    'border': '#252540',
    'text_primary': '#e2e8f0',
    'text_secondary': '#94a3b8',
    'text_muted': '#64748b',
    'accent': '#3b82f6',
    'risk_low': '#4ade80',
    'risk_medium': '#fbbf24',
    'risk_high': '#fb923c',
    'risk_critical': '#ef4444',
    'type_feature': '#3b82f6',
    'type_bugfix': '#22c55e',
    'type_refactor': '#a855f7',
    'type_security': '#dc2626',
    'type_deps': '#f59e0b',
    'type_docs': '#64748b',
    'type_tests': '#14b8a6',
    'type_ci': '#6366f1',
}

TYPE_ICONS = {
    'security': '🔒',
    'feature': '✨',
    'bugfix': '🐛',
    'refactor': '♻️',
    'deps': '📦',
    'docs': '📝',
    'tests': '🧪',
    'ci': '⚙️',
}


def escape_xml(text):
    """Escape XML special characters"""
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def truncate(text, max_len=50):
    """Truncate text with ellipsis"""
    if len(text) <= max_len:
        return text
    return text[:max_len-3] + '...'


def donut_chart(cx, cy, radius, percentage, color, label, sublabel):
    """Generate SVG for donut chart"""
    # Calculate arc
    angle = (percentage / 100) * 360
    end_angle = -90 + angle  # Start from top
    
    # Convert to radians
    start_rad = math.radians(-90)
    end_rad = math.radians(end_angle)
    
    # Arc path
    x1 = cx + radius * math.cos(start_rad)
    y1 = cy + radius * math.sin(start_rad)
    x2 = cx + radius * math.cos(end_rad)
    y2 = cy + radius * math.sin(end_rad)
    
    large_arc = 1 if angle > 180 else 0
    
    # Background circle
    bg = f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#334155" stroke-width="12"/>'
    
    # Foreground arc
    if percentage > 0:
        arc = f'<path d="M {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2}" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round"/>'
    else:
        arc = ''
    
    # Center text
    text = f'''
        <text x="{cx}" y="{cy - 5}" text-anchor="middle" fill="{COLORS["text_primary"]}" font-size="28" font-weight="bold">{percentage}</text>
        <text x="{cx}" y="{cy + 18}" text-anchor="middle" fill="{color}" font-size="12" font-weight="600">{label.upper()}</text>
        <text x="{cx}" y="{cy + 35}" text-anchor="middle" fill="{COLORS["text_muted"]}" font-size="10">{sublabel}</text>
    '''
    
    return bg + arc + text


def semicircle_gauge(cx, cy, radius, value, max_val, label):
    """Generate semicircle gauge for size"""
    # Determine size category
    if value < 100:
        category, color = 'XS', COLORS["risk_low"]
    elif value < 500:
        category, color = 'S', COLORS["risk_medium"]
    elif value < 1000:
        category, color = 'M', COLORS["risk_high"]
    elif value < 5000:
        category, color = 'L', '#ef4444'
    else:
        category, color = 'XL', COLORS["risk_critical"]
    
    # Semicircle background
    bg_path = f'M {cx - radius} {cy} A {radius} {radius} 0 0 1 {cx + radius} {cy}'
    bg = f'<path d="{bg_path}" fill="none" stroke="#334155" stroke-width="12" stroke-linecap="round"/>'
    
    # Fill arc
    percentage = min(value / max_val, 1)
    end_angle = 180 * percentage
    end_rad = math.radians(180 - end_angle)
    
    x2 = cx + radius * math.cos(end_rad)
    y2 = cy - radius * math.sin(end_rad)
    
    fill_path = f'M {cx - radius} {cy} A {radius} {radius} 0 0 1 {x2} {y2}'
    fill = f'<path d="{fill_path}" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round"/>'
    
    # Text
    text = f'''
        <text x="{cx}" y="{cy - 20}" text-anchor="middle" fill="{COLORS["text_primary"]}" font-size="24" font-weight="bold">{value:,}</text>
        <text x="{cx}" y="{cy + 5}" text-anchor="middle" fill="{COLORS["text_secondary"]}" font-size="11">{label}</text>
        <text x="{cx}" y="{cy + 25}" text-anchor="middle" fill="{color}" font-size="14" font-weight="600">{category}</text>
    '''
    
    return bg + fill + text


def treemap(x, y, width, height, file_types):
    """Generate simple treemap as horizontal bars"""
    if not file_types:
        return ''
    
    total = sum(file_types.values())
    if total == 0:
        return ''
    
    colors = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#64748b']
    
    svg = f'<g transform="translate({x}, {y})">'
    
    # Title
    svg += f'<text x="0" y="-10" fill="{COLORS["text_secondary"]}" font-size="12" font-weight="600">FILE DISTRIBUTION</text>'
    
    # Calculate positions
    current_x = 0
    for i, (ext, count) in enumerate(sorted(file_types.items(), key=lambda x: -x[1])[:5]):
        pct = count / total
        bar_width = width * pct
        color = colors[i % len(colors)]
        
        # Bar
        svg += f'<rect x="{current_x}" y="0" width="{bar_width - 2}" height="{height}" fill="{color}" rx="4" opacity="0.8"/>'
        
        # Label (if bar is wide enough)
        if bar_width > 60:
            svg += f'<text x="{current_x + bar_width/2}" y="{height/2 + 4}" text-anchor="middle" fill="white" font-size="11" font-weight="600">{ext}</text>'
            svg += f'<text x="{current_x + bar_width/2}" y="{height/2 + 18}" text-anchor="middle" fill="white" font-size="9" opacity="0.8">{pct*100:.0f}%</text>'
        
        current_x += bar_width
    
    svg += '</g>'
    return svg


def directory_bars(x, y, width, directories):
    """Generate horizontal bar chart for directories"""
    if not directories:
        return ''
    
    svg = f'<g transform="translate({x}, {y})">'
    svg += f'<text x="0" y="-10" fill="{COLORS["text_secondary"]}" font-size="12" font-weight="600">TOP DIRECTORIES</text>'
    
    max_count = max(directories.values())
    row_height = 28
    
    for i, (dir_name, count) in enumerate(sorted(directories.items(), key=lambda x: -x[1])[:6]):
        row_y = i * row_height
        bar_width = (count / max_count) * (width - 100)
        
        # Directory name
        svg += f'<text x="0" y="{row_y + 14}" fill="{COLORS["text_primary"]}" font-size="12" font-family="monospace">{dir_name[:20]}</text>'
        
        # Bar
        svg += f'<rect x="120" y="{row_y + 4}" width="{bar_width}" height="12" fill="#3b82f6" rx="6" opacity="0.8"/>'
        
        # Count
        svg += f'<text x="{120 + bar_width + 8}" y="{row_y + 14}" fill="{COLORS["text_secondary"]}" font-size="11">{count} files</text>'
    
    svg += '</g>'
    return svg


def status_badges(x, y, ci_status, review_count, comment_count, unresolved_count):
    """Generate status badges"""
    badges = []
    
    # CI badge
    ci_colors = {'pass': COLORS["risk_low"], 'fail': COLORS["risk_critical"], 'pending': COLORS["risk_medium"]}
    ci_color = ci_colors.get(ci_status, COLORS["text_muted"])
    ci_icon = '✅' if ci_status == 'pass' else '❌' if ci_status == 'fail' else '⏳'
    badges.append((f'{ci_icon} CI:{ci_status.upper()}', ci_color))
    
    # Reviews
    badges.append((f'👀 {review_count} REVIEWS', COLORS["accent"]))
    
    # Comments
    badges.append((f'💬 {comment_count} CMNTS', COLORS["text_secondary"]))
    
    # Unresolved
    if unresolved_count > 0:
        badges.append((f'⚠️ {unresolved_count} UNRESOLVED', COLORS["risk_high"]))
    
    svg = f'<g transform="translate({x}, {y})">'
    current_x = 0
    
    for text, color in badges:
        # Badge background
        width = len(text) * 7 + 16
        svg += f'<rect x="{current_x}" y="0" width="{width}" height="24" fill="{color}" opacity="0.15" rx="12"/>'
        svg += f'<rect x="{current_x}" y="0" width="{width}" height="24" fill="none" stroke="{color}" stroke-width="1" rx="12"/>'
        
        # Badge text
        svg += f'<text x="{current_x + width/2}" y="16" text-anchor="middle" fill="{color}" font-size="10" font-weight="600">{text}</text>'
        
        current_x += width + 8
    
    svg += '</g>'
    return svg


def type_badge(pr_type):
    """Get badge color and icon for PR type"""
    icon = TYPE_ICONS.get(pr_type, '📝')
    color = {
        'security': COLORS["type_security"],
        'feature': COLORS["type_feature"],
        'bugfix': COLORS["type_bugfix"],
        'refactor': COLORS["type_refactor"],
        'deps': COLORS["type_deps"],
        'docs': COLORS["type_docs"],
        'tests': COLORS["type_tests"],
        'ci': COLORS["type_ci"],
    }.get(pr_type, COLORS["text_secondary"])
    
    return icon, color, pr_type.upper()


def generate_summary_svg(data):
    """Generate complete summary dashboard SVG"""
    
    # Canvas dimensions
    width = 800
    height = 420
    
    # Extract data
    title = data.get('title', 'PR Title')
    author = data.get('author', 'unknown')
    number = data.get('number', 0)
    risk_score = data.get('risk_score', 50)
    risk_level = data.get('risk_level', 'medium')
    pr_type = data.get('pr_type', 'refactor')
    total_lines = data.get('total_lines', 0)
    additions = data.get('additions', 0)
    deletions = data.get('deletions', 0)
    file_types = data.get('file_types', {})
    directories = data.get('top_directories', {})
    ci_status = data.get('ci_status', 'unknown')
    review_count = data.get('review_count', 0)
    comment_count = data.get('comment_count', 0)
    unresolved_count = data.get('unresolved_count', 0)
    
    # Get risk color
    risk_colors = {
        'low': COLORS["risk_low"],
        'medium': COLORS["risk_medium"],
        'high': COLORS["risk_high"],
        'critical': COLORS["risk_critical"],
    }
    risk_color = risk_colors.get(risk_level, COLORS["risk_medium"])
    
    # Type badge
    type_icon, type_color, type_label = type_badge(pr_type)
    
    # Start SVG
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
<defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" style="stop-color:{COLORS["bg"]}"/>
        <stop offset="100%" style="stop-color:{COLORS["card"]}"/>
    </linearGradient>
</defs>

<!-- Background -->
<rect width="{width}" height="{height}" fill="url(#bg)" rx="12"/>

<!-- Header -->
<g transform="translate(30, 35)">
    <text x="0" y="0" fill="{COLORS["text_primary"]}" font-size="18" font-weight="600">📄 {escape_xml(truncate(title, 55))}</text>
    
    <!-- Type badge -->
    <g transform="translate({width - 150}, -18)">
        <rect width="120" height="28" fill="{type_color}" opacity="0.15" rx="14"/>
        <rect width="120" height="28" fill="none" stroke="{type_color}" stroke-width="1" rx="14"/>
        <text x="60" y="19" text-anchor="middle" fill="{type_color}" font-size="12" font-weight="600">{type_icon} {type_label}</text>
    </g>
    
    <text x="0" y="22" fill="{COLORS["text_secondary"]}" font-size="13">#{number} by @{author} • Review Dashboard</text>
</g>

<!-- Separator -->
<line x1="30" y1="75" x2="{width - 30}" y2="75" stroke="{COLORS["border"]}" stroke-width="1"/>

<!-- Metrics Cards -->
<g transform="translate(0, 95)">
    <!-- Risk Donut -->
    <g transform="translate(130, 90)">
        <rect x="-110" y="-100" width="220" height="200" fill="{COLORS["card"]}" rx="12"/>
        {donut_chart(0, 0, 55, risk_score, risk_color, risk_level, 'RISK')}
    </g>
    
    <!-- Size Gauge -->
    <g transform="translate(380, 90)">
        <rect x="-110" y="-100" width="220" height="200" fill="{COLORS["card"]}" rx="12"/>
        {semicircle_gauge(0, 40, 60, total_lines, 10000, 'LINES')}
    </g>
    
    <!-- Change Bars -->
    <g transform="translate(630, 90)">
        <rect x="-110" y="-100" width="220" height="200" fill="{COLORS["card"]}" rx="12"/>
        <text x="0" y="-50" text-anchor="middle" fill="{COLORS["text_secondary"]}" font-size="12" font-weight="600">📊 CHANGES</text>
        
        <text x="0" y="-20" text-anchor="middle" fill="{COLORS["risk_low"]}" font-size="16" font-weight="600">▲ +{additions:,} added</text>
        <text x="0" y="5" text-anchor="middle" fill="{COLORS["risk_critical"]}" font-size="16" font-weight="600">▼ -{deletions:,} deleted</text>
        
        <!-- Mini bar -->
        <rect x="-70" y="30" width="140" height="8" fill="#334155" rx="4"/>
        <rect x="-70" y="30" width="{70 * additions / max(additions + deletions, 1)}" height="8" fill="{COLORS["risk_low"]}" rx="4"/>
        <rect x="{ -70 + 140 * additions / max(additions + deletions, 1) }" y="30" width="{70 * deletions / max(additions + deletions, 1)}" height="8" fill="{COLORS["risk_critical"]}" rx="4"/>
    </g>
</g>

<!-- Treemap -->
{treemap(30, 320, 400, 50, file_types)}

<!-- Directory Bars -->
{directory_bars(450, 295, 320, directories)}

<!-- Status Badges -->
{status_badges(30, 390, ci_status, review_count, comment_count, unresolved_count)}

</svg>'''
    
    return svg


def main():
    if len(sys.argv) < 2:
        # Demo with sample data
        sample_data = {
            'title': 'Reset corpus review surface',
            'author': 'Coldaine',
            'number': 18,
            'risk_score': 50,
            'risk_level': 'medium',
            'pr_type': 'refactor',
            'total_lines': 5383,
            'additions': 876,
            'deletions': 4507,
            'file_types': {'.md': 18, '.py': 3, '.jsonl': 11, '.tsv': 1},
            'top_directories': {'docs/': 18, 'data/': 11, 'scripts/': 3, 'quarantine/': 1},
            'ci_status': 'pass',
            'review_count': 0,
            'comment_count': 1,
            'unresolved_count': 1,
        }
        print(generate_summary_svg(sample_data))
    else:
        # Read from file
        with open(sys.argv[1]) as f:
            data = json.load(f)
        print(generate_summary_svg(data))


if __name__ == '__main__':
    main()
