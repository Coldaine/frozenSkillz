# Assembly Guide

Step-by-step process for building the PR review dashboard.

---

## Data Model

```python
pr_data = {
    "meta": {
        "number": int,
        "title": str,
        "author": str,
        "state": "open" | "closed" | "merged",
        "additions": int,
        "deletions": int,
        "files_changed": int,
        "created_at": str,
        "base_branch": str,
        "head_branch": str
    },
    
    "summary": {
        "risk_score": int,        # 0-100
        "risk_level": str,        # "low" | "medium" | "high" | "critical"
        "pr_type": str,           # "security" | "feature" | "bugfix" | "refactor" | "deps" | "docs" | "tests" | "ci"
        "total_lines": int,
        "file_types": dict,       # {".py": 12, ".md": 8, ...}
        "top_directories": dict,  # {"docs/": 15, "src/": 12, ...}
        "test_coverage_percent": float,
        "ci_status": str,         # "pass" | "fail" | "pending"
        "review_count": int,
        "comment_count": int,
        "unresolved_count": int
    },
    
    "architecture": {
        "components": [
            {
                "name": str,
                "path": str,
                "type": "added" | "modified" | "removed" | "unchanged",
                "layer": str  # "frontend" | "backend" | "database" | ...
            }
        ],
        "relationships": [
            {
                "from": str,
                "to": str,
                "type": "imports" | "calls" | "extends" | "uses"
            }
        ]
    },
    
    "flows": [
        {
            "name": str,
            "type": "data" | "control" | "sequence",
            "nodes": [
                {"id": str, "label": str, "type": "added" | "modified" | "removed" | "unchanged"}
            ],
            "edges": [
                {"from": str, "to": str, "label": str}
            ]
        }
    ],
    
    "files": [
        {
            "path": str,
            "filename": str,
            "status": "added" | "removed" | "modified" | "renamed",
            "additions": int,
            "deletions": int,
            "category": "core" | "mechanical",
            "patch": str,
            "annotation": str  # Optional reviewer note
        }
    ],
    
    "review_notes": [
        {
            "file": str,
            "line": int,
            "note": str,
            "severity": "info" | "warning" | "critical"
        }
    ]
}
```

---

## Step 1: Fetch PR Data

```bash
# Get PR metadata
gh api repos/{owner}/{repo}/pulls/{number}

# Get file list with stats  
gh api repos/{owner}/{repo}/pulls/{number}/files --paginate --slurp

# Get commits (for timeline data)
gh api repos/{owner}/{repo}/pulls/{number}/commits --paginate --slurp

# Get comments
gh api repos/{owner}/{repo}/pulls/{number}/comments

# Get check status
gh api repos/{owner}/{repo}/commits/{head_sha}/check-runs
```

---

## Step 2: Analyze and Curate

### Classify PR Type

```python
def classify_pr_type(pr_data, files):
    title_lower = pr_data['title'].lower()
    branch = pr_data['head_branch'].lower()
    
    # Security
    if any(k in title_lower or k in branch for k in ['security', 'vuln', 'cve', 'auth', 'token']):
        return 'security'
    
    # Bugfix
    if any(k in title_lower or k in branch for k in ['fix', 'bug', 'hotfix']):
        return 'bugfix'
    
    # Feature
    if any(k in title_lower or k in branch for k in ['feat', 'add', 'implement', 'feature']):
        return 'feature'
    
    # Deps
    dep_files = ['package.json', 'go.mod', 'requirements.txt', 'Cargo.toml', 'Gemfile']
    if all(f['filename'].endswith(('.lock', '.json', '.toml', '.txt')) and 
           any(d in f['filename'] for d in dep_files) for f in files):
        return 'deps'
    
    # Docs
    if all(f['filename'].endswith(('.md', '.rst', '.txt')) or 'docs/' in f['filename'] 
           for f in files):
        return 'docs'
    
    # Refactor (default for large changes)
    return 'refactor'
```

### Calculate Risk Score

```python
def calculate_risk(files, pr_data):
    score = 0
    total_lines = sum(f['additions'] + f['deletions'] for f in files)
    
    # Size
    if total_lines > 1000: score += 2
    if len(files) > 20: score += 2
    if len(files) > 50: score += 3
    
    # Complexity
    config_files = [f for f in files if f['filename'].endswith(('.json', '.yml', '.yaml', '.toml'))]
    if len(config_files) > 3: score += 2
    
    test_files = [f for f in files if 'test' in f['filename'] or 'spec' in f['filename']]
    src_files = [f for f in files if f['filename'].endswith(('.py', '.js', '.ts', '.go', '.rs')) 
                 and 'test' not in f['filename']]
    if src_files and not test_files:
        score += 3  # No test changes
    
    # Security-sensitive
    security_paths = ['auth', 'crypto', 'security', 'password', 'token', 'secret']
    if any(p in f['filename'] for f in files for p in security_paths):
        score += 2
    
    return min(score, 12)
```

### Categorize Files

```python
def categorize_files(files):
    core_indicators = [
        lambda f: f['additions'] + f['deletions'] > 100,
        lambda f: 'test' not in f['filename'] and f['filename'].endswith(('.py', '.js', '.ts', '.go')),
        lambda f: any(p in f['filename'] for p in ['auth', 'api', 'core', 'main']),
        lambda f: f['status'] == 'added' and f['additions'] > 50
    ]
    
    mechanical_patterns = [
        lambda f: f['filename'].endswith('.lock'),
        lambda f: f['filename'].endswith('.snap'),
        lambda f: 'vendor/' in f['filename'] or 'node_modules/' in f['filename'],
        lambda f: f['status'] == 'removed' and f['deletions'] > 100
    ]
    
    for f in files:
        if any(m(f) for m in mechanical_patterns):
            f['category'] = 'mechanical'
        elif any(c(f) for c in core_indicators):
            f['category'] = 'core'
        else:
            f['category'] = 'mechanical'  # Default to collapsed
    
    # Select top 5 core files by change size
    core_files = [f for f in files if f['category'] == 'core']
    core_files.sort(key=lambda f: f['additions'] + f['deletions'], reverse=True)
    
    for f in core_files[5:]:
        f['category'] = 'mechanical'  # Demote excess
    
    return files
```

---

## Step 3: Generate Views

### Summary SVG

Generate SVG following the layout in view-specs.md.

Key calculations:
- Donut chart: `stroke-dasharray` based on risk percentage
- Treemap: Simple squarified layout or even just horizontal bars by percentage
- Directory bars: Normalize to longest = 100%

### Architecture Mermaid

```python
def generate_architecture_mermaid(arch_data):
    layers = {}
    for comp in arch_data['components']:
        layer = comp['layer']
        if layer not in layers:
            layers[layer] = []
        layers[layer].append(comp)
    
    lines = ['graph TB']
    
    for layer_name, components in layers.items():
        lines.append(f'    subgraph "{layer_name.title()}"')
        for comp in components:
            icon = {'added': '🆕', 'modified': '✏️', 'removed': '🗑️'}.get(comp['type'], '')
            safe_name = comp['name'].replace('.', '_').replace('/', '_').replace('-', '_')
            lines.append(f'        {safe_name}[{comp["name"]}<br/>{icon} {comp["type"]}]')
        lines.append('    end')
    
    for rel in arch_data['relationships']:
        from_name = rel['from'].replace('.', '_').replace('/', '_').replace('-', '_')
        to_name = rel['to'].replace('.', '_').replace('/', '_').replace('-', '_')
        lines.append(f'    {from_name} -->|{rel["type"]}| {to_name}')
    
    return '\n'.join(lines)
```

### Flow Mermaid

```python
def generate_flow_mermaid(flow):
    if flow['type'] == 'sequence':
        lines = ['sequenceDiagram']
        for edge in flow['edges']:
            lines.append(f'    {edge["from"]}->>{edge["to"]}: {edge["label"]}')
    else:
        lines = ['flowchart TD']
        for node in flow['nodes']:
            icon = {'added': '🆕', 'modified': '✏️', 'removed': '🗑️'}.get(node['type'], '')
            safe_id = node['id'].replace('-', '_')
            lines.append(f'    {safe_id}[{icon} {node["label"]}]')
        for edge in flow['edges']:
            from_id = edge['from'].replace('-', '_')
            to_id = edge['to'].replace('-', '_')
            lines.append(f'    {from_id} --> {to_id}')
    
    return '\n'.join(lines)
```

### Changes HTML

```python
def generate_changes_html(files, notes):
    core_files = [f for f in files if f['category'] == 'core'][:5]
    mechanical_files = [f for f in files if f['category'] == 'mechanical']
    
    html_parts = ['<div class="changes-view">']
    
    # Core files
    html_parts.append('<div class="section-title">Core Changes</div>')
    for f in core_files:
        # Add risk badges
        badges = []
        if f['additions'] + f['deletions'] > 500:
            badges.append('<span class="badge large">Large</span>')
        if any(p in f['filename'] for p in ['auth', 'crypto', 'security']):
            badges.append('<span class="badge security">Security</span>')
        
        note = f.get('annotation', '')
        note_html = f'<div class="annotation">{note}</div>' if note else ''
        
        html_parts.append(f'''
        <div class="file-card core">
            <div class="file-header">
                <span class="filename">{f["filename"]}</span>
                <span class="stats">+{f["additions"]}/-{f["deletions"]}</span>
                {''.join(badges)}
            </div>
            {note_html}
            <div class="diff-container" data-diff="{f["path"].replace('/', '_').replace('.', '_")}"></div>
        </div>
        ''')
    
    # Mechanical files (collapsed)
    if mechanical_files:
        total_lines = sum(f['additions'] + f['deletions'] for f in mechanical_files)
        html_parts.append(f'''
        <div class="section-title">Mechanical Changes</div>
        <div class="bp-section">
            <div class="bp-header" onclick="toggle(this)">
                {len(mechanical_files)} files ({total_lines} lines) — click to expand
            </div>
            <div class="bp-body">
                <ul>{''.join(f"<li>{f['filename']}</li>" for f in mechanical_files)}</ul>
            </div>
        </div>
        ''')
    
    # Checklist
    html_parts.append('''
    <div class="checklist">
        <h3>Review Checklist</h3>
        <ul>
            <li><input type="checkbox"> Logic correctness verified</li>
            <li><input type="checkbox"> Edge cases considered</li>
            <li><input type="checkbox"> Tests adequate</li>
            <li><input type="checkbox"> Documentation updated</li>
        </ul>
    </div>
    </div>
    ''')
    
    return '\n'.join(html_parts)
```

---

## Step 4: Assemble Dashboard

```python
def assemble_dashboard(pr_data, template_path, output_path):
    template = Path(template_path).read_text()
    
    # Generate all views
    summary_svg = generate_summary_svg(pr_data['summary'])
    arch_mermaid = generate_architecture_mermaid(pr_data['architecture'])
    flow_mermaid = generate_flow_mermaid(pr_data['flows'][0]) if pr_data['flows'] else ''
    changes_html = generate_changes_html(pr_data['files'], pr_data['review_notes'])
    
    # Create patches JSON for diffs
    patches = {
        f['path'].replace('/', '_').replace('.', '_'): f.get('patch', '')
        for f in pr_data['files']
    }
    safe_patches = json.dumps(patches).replace('<', '\\u003c').replace('>', '\\u003e')
    
    # Inject into template
    dashboard = (template
        .replace('{{TITLE}}', pr_data['meta']['title'])
        .replace('{{NUMBER}}', str(pr_data['meta']['number']))
        .replace('{{AUTHOR}}', pr_data['meta']['author'])
        .replace('{{SUMMARY_SVG}}', summary_svg)
        .replace('{{ARCHITECTURE_DIAGRAM}}', arch_mermaid)
        .replace('{{FLOW_DIAGRAM}}', flow_mermaid)
        .replace('{{CHANGES_HTML}}', changes_html)
        .replace('"{{PATCHES_JSON}}"', safe_patches)
    )
    
    Path(output_path).write_text(dashboard)
    return output_path
```

---

## Step 5: Serve

```bash
# Serve on fixed port
cd /tmp && python3 -m http.server 8432 --bind 127.0.0.1

# URL: http://127.0.0.1:8432/pr-dashboard-{number}.html
```

---

## Conditional View Generation

Skip views that don't add value:

```python
def should_generate_architecture(files):
    return len(files) >= 5 and not all(
        f['filename'].endswith(('.md', '.json', '.yml', '.lock'))
        for f in files
    )

def should_generate_flow(pr_data, files):
    keywords = ['flow', 'pipeline', 'process', 'workflow', 'async', 'queue', 'stream']
    text_to_check = pr_data['title'] + ' ' + pr_data.get('body', '')
    return any(k in text_to_check.lower() for k in keywords)

def generate_dashboard(pr_data):
    views = {
        'summary': True,  # Always
        'architecture': should_generate_architecture(pr_data['files']),
        'flow': should_generate_flow(pr_data['meta'], pr_data['files']),
        'changes': True   # Always, but curated
    }
    
    # Generate only enabled views
    if not views['architecture']:
        pr_data['architecture'] = {'components': [], 'relationships': []}
    if not views['flow']:
        pr_data['flows'] = []
    
    return assemble_dashboard(pr_data, ...)
```

---

## File Structure

```
/tmp/
├── pr-dashboard-{number}.html    # Final output
├── pr-data-{number}.json         # Intermediate data (optional)
└── pr-patches-{number}.json      # Patches for diff rendering
```
