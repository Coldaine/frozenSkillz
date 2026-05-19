# SVG Component Examples

Reference implementations for key visual components.

## 1. Risk Score Donut

```svg
<!-- Risk Donut - 75% Medium Risk (Orange) -->
<g transform="translate(100, 100)">
  <!-- Background circle -->
  <circle cx="0" cy="0" r="50" fill="none" stroke="#334155" stroke-width="10"/>
  
  <!-- Progress arc (75% = 270 degrees) -->
  <path d="M 0,-50 A 50,50 0 1,1 -35.35,35.35" 
        fill="none" stroke="#fb923c" stroke-width="10" 
        stroke-linecap="round"/>
  
  <!-- Center text -->
  <text x="0" y="-5" text-anchor="middle" fill="#e2e8f0" font-size="24" font-weight="bold">75</text>
  <text x="0" y="15" text-anchor="middle" fill="#94a3b8" font-size="10">RISK</text>
  <text x="0" y="28" text-anchor="middle" fill="#fb923c" font-size="9">MEDIUM</text>
</g>
```

## 2. Size Gauge (Semicircle)

```svg
<!-- Size Gauge - 1200 LOC (Large) -->
<g transform="translate(300, 100)">
  <!-- Background arc -->
  <path d="M -60,0 A 60,60 0 0,1 60,0" fill="none" stroke="#334155" stroke-width="8"/>
  
  <!-- Fill arc (scale: 1200 is ~80% between M and L) -->
  <path d="M -60,0 A 60,60 0 0,1 40,-44" fill="none" stroke="#f59e0b" stroke-width="8" stroke-linecap="round"/>
  
  <!-- Tick marks -->
  <line x1="-60" y1="0" x2="-50" y2="0" stroke="#64748b" stroke-width="2"/>
  <line x1="-30" y1="-52" x2="-25" y2="-43" stroke="#64748b" stroke-width="2"/>
  <line x1="0" y1="-60" x2="0" y2="-50" stroke="#64748b" stroke-width="2"/>
  <line x1="30" y1="-52" x2="25" y2="-43" stroke="#64748b" stroke-width="2"/>
  <line x1="60" y1="0" x2="50" y2="0" stroke="#64748b" stroke-width="2"/>
  
  <!-- Labels -->
  <text x="-55" y="15" fill="#64748b" font-size="8">XS</text>
  <text x="-25" y="-50" fill="#64748b" font-size="8">S</text>
  <text x="0" y="-70" fill="#64748b" font-size="8" text-anchor="middle">M</text>
  <text x="25" y="-50" fill="#64748b" font-size="8" text-anchor="end">L</text>
  <text x="55" y="15" fill="#64748b" font-size="8" text-anchor="end">XL</text>
  
  <!-- Value -->
  <text x="0" y="-25" text-anchor="middle" fill="#e2e8f0" font-size="20" font-weight="bold">1.2k</text>
  <text x="0" y="-10" text-anchor="middle" fill="#94a3b8" font-size="9">LOC</text>
</g>
```

## 3. Type Badge

```svg
<!-- Security Type Badge -->
<g transform="translate(600, 30)">
  <rect x="0" y="0" width="100" height="32" rx="16" fill="#dc2626"/>
  <text x="28" y="21" fill="white" font-size="13" font-weight="600">SECURITY</text>
  <!-- Shield icon -->
  <path d="M12 6l-6 3v4c0 3 2 6 6 8 4-2 6-5 6-8V9l-6-3z" 
        fill="none" stroke="white" stroke-width="1.5" transform="translate(8, 6) scale(0.8)"/>
</g>
```

## 4. Treemap Cell

```svg
<!-- Treemap Cell - Python Files -->
<g>
  <rect x="20" y="180" width="200" height="100" fill="#3b82f6" opacity="0.8" rx="4"/>
  <rect x="20" y="180" width="200" height="100" fill="none" stroke="#1e40af" stroke-width="1" rx="4"/>
  <text x="120" y="225" text-anchor="middle" fill="white" font-size="18" font-weight="bold">.py</text>
  <text x="120" y="245" text-anchor="middle" fill="#bfdbfe" font-size="12">52%</text>
  <text x="120" y="260" text-anchor="middle" fill="#93c5fd" font-size="10">14 files</text>
</g>
```

## 5. Directory Bar

```svg
<!-- Directory Impact Bar -->
<g transform="translate(20, 350)">
  <text x="0" y="15" fill="#94a3b8" font-size="11" font-family="monospace">src/auth/</text>
  <rect x="80" y="5" width="400" height="12" rx="6" fill="#1e3a5f"/>
  <rect x="80" y="5" width="400" height="12" rx="6" fill="#3b82f6"/>
  <text x="490" y="15" fill="#94a3b8" font-size="11">12 files</text>
</g>
```

## 6. Status Badge

```svg
<!-- CI Pass Badge -->
<g transform="translate(20, 450)">
  <rect x="0" y="0" width="80" height="24" rx="12" fill="#166534"/>
  <circle cx="16" cy="12" r="3" fill="#4ade80"/>
  <text x="28" y="16" fill="#4ade80" font-size="10" font-weight="600">CI:PASS</text>
</g>

<!-- Review Badge -->
<g transform="translate(110, 450)">
  <rect x="0" y="0" width="90" height="24" rx="12" fill="#1e3a5f"/>
  <text x="12" y="16" fill="#60a5fa" font-size="10" font-weight="600">✓ 2 REVIEWS</text>
</g>

<!-- Comments Badge -->
<g transform="translate(210, 450)">
  <rect x="0" y="0" width="90" height="24" rx="12" fill="#1e3a5f"/>
  <text x="12" y="16" fill="#94a3b8" font-size="10">💬 5 CMNTS</text>
</g>
```

## Complete Mini Example

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="400" height="200" fill="url(#bg)" rx="8"/>
  
  <!-- Header -->
  <text x="20" y="30" fill="#e2e8f0" font-size="14" font-weight="bold">PR #123: Fix auth bug</text>
  <text x="20" y="48" fill="#64748b" font-size="10">by @alice • 2 days ago</text>
  
  <!-- Risk Donut -->
  <g transform="translate(80, 110)">
    <circle cx="0" cy="0" r="40" fill="none" stroke="#334155" stroke-width="8"/>
    <path d="M 0,-40 A 40,40 0 0,1 34.6,20" fill="none" stroke="#22c55e" stroke-width="8" stroke-linecap="round"/>
    <text x="0" y="5" text-anchor="middle" fill="#e2e8f0" font-size="16" font-weight="bold">25</text>
    <text x="0" y="25" text-anchor="middle" fill="#22c55e" font-size="9">LOW</text>
  </g>
  
  <!-- Stats -->
  <g transform="translate(160, 80)">
    <text x="0" y="0" fill="#94a3b8" font-size="10">CHANGES</text>
    <text x="0" y="20" fill="#22c55e" font-size="14">+156</text>
    <text x="0" y="40" fill="#ef4444" font-size="14">-42</text>
    
    <text x="80" y="0" fill="#94a3b8" font-size="10">FILES</text>
    <text x="80" y="20" fill="#e2e8f0" font-size="14">8</text>
    
    <text x="140" y="0" fill="#94a3b8" font-size="10">COMMITS</text>
    <text x="140" y="20" fill="#e2e8f0" font-size="14">3</text>
  </g>
  
  <!-- Type Badge -->
  <g transform="translate(300, 15)">
    <rect x="0" y="0" width="80" height="24" rx="12" fill="#22c55e"/>
    <text x="40" y="16" text-anchor="middle" fill="white" font-size="10" font-weight="600">BUGFIX</text>
  </g>
</svg>
```
