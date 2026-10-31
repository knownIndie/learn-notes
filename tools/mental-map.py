import sys
branches = [
 ("Why it exists","#EEEDFE","#534AB7","#3C3489",["Same-origin policy: read only your own origin","so other sites can't read your logged-in data"]),
 ("Origin","#E6F1FB","#185FA5","#0C447C",["scheme + host + port, all three must match"]),
 ("Who checks","#FAEEDA","#854F0B","#633806",["The browser. curl and Postman ignore CORS"]),
 ("Two headers","#E1F5EE","#0F6E56","#085041",["Origin  (browser → server)","Access-Control-Allow-Origin  (back)"]),
 ("Preflight","#FCEBEB","#A32D2D","#791F1F",["OPTIONS \"may I?\" before PUT, DELETE, JSON"]),
 ("Cookies (credentials)","#EAF3DE","#3B6D11","#27500A",["need Allow-Credentials: true","and the exact origin, never *"]),
 ("Not CSRF protection","#F1EFE8","#5F5E5A","#2C2C2A",["request still runs on the server","CSRF fix: tokens + SameSite cookies"]),
]
y=72; parts=[]; ticks=[]
for title,fill,stroke,dark,lines in branches:
    h=28+16*len(lines)
    mid=y+h/2
    ticks.append(mid)
    parts.append(f'<path d="M36 {mid:.0f} H56" stroke="#b4b2a9" stroke-width="2"/>')
    parts.append(f'<rect x="56" y="{y}" width="288" height="{h}" rx="8" fill="{fill}" stroke="{stroke}"/>')
    parts.append(f'<text x="68" y="{y+18}" font-weight="600" fill="{dark}">{title}</text>')
    for i,l in enumerate(lines):
        mono = l.startswith(("Origin ","Access-"))
        f = ' font-family="ui-monospace,Menlo,monospace" font-size="11"' if mono else ''
        parts.append(f'<text x="68" y="{y+35+16*i}" fill="{stroke}"{f}>{l}</text>')
    y+=h+14
H=y+24
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="{H}" viewBox="0 0 360 {H}" role="img" font-family="system-ui,-apple-system,Segoe UI,sans-serif">
<title>CORS mental map</title>
<rect x="1" y="1" width="358" height="{H-2}" rx="12" fill="#faf9f5" stroke="#e3e1d9"/>
<rect x="120" y="16" width="120" height="40" rx="20" fill="#185FA5"/>
<text x="180" y="42" text-anchor="middle" font-size="16" font-weight="700" fill="#ffffff">CORS</text>
<path d="M120 36 H36 V{ticks[-1]:.0f}" stroke="#b4b2a9" stroke-width="2" fill="none"/>
<g font-size="12">
{chr(10).join(parts)}
</g>
<text x="180" y="{H-12}" text-anchor="middle" font-size="11" fill="#8a8984">Fix CORS on the server, never in the page</text>
</svg>'''
open(sys.argv[1],"w").write(svg)
