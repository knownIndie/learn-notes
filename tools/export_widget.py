#!/usr/bin/env python3
"""Turn a chat widget (visualize tool output) into a file that renders outside the chat app.

The chat app supplies CSS variables (--text-primary, --border, ...) and SVG classes
(c-purple, th, ts, arr, ...). Outside the app they don't exist, so this script inlines
a stylesheet that defines them for light and dark mode.

  SVG widget  -> content/assets/diagrams/<name>.svg   (embed with ![[<name>.svg]])
  HTML widget -> quartz/static/widgets/<name>.html    (embed with an <iframe>, served at static/widgets/)

Usage:
  python3 tools/export_widget.py <widget-file> [--name NAME]
  python3 tools/export_widget.py --from-transcript <session.jsonl> [--only TITLE ...]
"""
import argparse
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SVG_OUT = ROOT / "content" / "assets" / "diagrams"
HTML_OUT = ROOT / "quartz" / "static" / "widgets"

# Colour ramps: name -> (50, 100, 200, 400, 600, 800, 900)
RAMPS = {
    "purple": ("#EEEDFE", "#CECBF6", "#AFA9EC", "#7F77DD", "#534AB7", "#3C3489", "#26215C"),
    "teal": ("#E1F5EE", "#9FE1CB", "#5DCAA5", "#1D9E75", "#0F6E56", "#085041", "#04342C"),
    "coral": ("#FAECE7", "#F5C4B3", "#F0997B", "#D85A30", "#993C1D", "#712B13", "#4A1B0C"),
    "pink": ("#FBEAF0", "#F4C0D1", "#ED93B1", "#D4537E", "#993556", "#72243E", "#4B1528"),
    "gray": ("#F1EFE8", "#D3D1C7", "#B4B2A9", "#888780", "#5F5E5A", "#444441", "#2C2C2A"),
    "blue": ("#E6F1FB", "#B5D4F4", "#85B7EB", "#378ADD", "#185FA5", "#0C447C", "#042C53"),
    "green": ("#EAF3DE", "#C0DD97", "#97C459", "#639922", "#3B6D11", "#27500A", "#173404"),
    "amber": ("#FAEEDA", "#FAC775", "#EF9F27", "#BA7517", "#854F0B", "#633806", "#412402"),
    "red": ("#FCEBEB", "#F7C1C1", "#F09595", "#E24B4A", "#A32D2D", "#791F1F", "#501313"),
}

LIGHT_VARS = """
  --text-primary:#1f1e1d; --text-secondary:#5e5d59; --text-muted:#8a8984; --text-disabled:#b4b2a9;
  --text-accent:#185FA5; --text-danger:#A32D2D; --text-success:#3B6D11; --text-warning:#854F0B;
  --bg-accent:#E6F1FB; --bg-danger:#FCEBEB; --bg-success:#EAF3DE; --bg-warning:#FAEEDA;
  --border:rgba(31,30,29,.15); --border-strong:rgba(31,30,29,.3); --border-stronger:rgba(31,30,29,.4);
  --border-accent:#85B7EB; --border-danger:#F09595; --border-success:#97C459; --border-warning:#EF9F27;
  --surface-0:#f5f4ef; --surface-1:#faf9f5; --surface-2:#ffffff; --surface-3:#ffffff;
"""
DARK_VARS = """
  --text-primary:#ecebe6; --text-secondary:#b4b2a9; --text-muted:#888780; --text-disabled:#5F5E5A;
  --text-accent:#85B7EB; --text-danger:#F09595; --text-success:#97C459; --text-warning:#EF9F27;
  --bg-accent:#0C447C; --bg-danger:#791F1F; --bg-success:#27500A; --bg-warning:#633806;
  --border:rgba(236,235,230,.15); --border-strong:rgba(236,235,230,.3); --border-stronger:rgba(236,235,230,.4);
  --border-accent:#185FA5; --border-danger:#A32D2D; --border-success:#3B6D11; --border-warning:#854F0B;
  --surface-0:#1a1a19; --surface-1:#232321; --surface-2:#2b2b29; --surface-3:#333331;
"""
COMMON_VARS = """
  --font-sans:system-ui,-apple-system,"Segoe UI",sans-serif; --font-mono:ui-monospace,"SF Mono",Menlo,monospace;
  --font-voice:Georgia,serif; --radius:8px;
  --pad-sm:8px; --pad-md:12px; --pad-lg:16px; --pad-xl:24px;
  --gap-xs:4px; --gap-sm:8px; --gap-md:12px; --gap-lg:16px; --gap-xl:24px;
  --p:var(--text-primary); --s:var(--text-secondary); --t:var(--text-muted); --b:var(--border); --bg2:var(--surface-1);
"""


def ramp_rules(dark):
    out = []
    for name, (s50, s100, s200, _s400, s600, s800, _s900) in RAMPS.items():
        fill, stroke, title, sub = (s800, s200, s100, s200) if dark else (s50, s600, s800, s600)
        sel = f".c-{name}"
        out.append(
            f"{sel}>rect,{sel}>circle,{sel}>ellipse,{sel}>polygon,rect{sel},circle{sel},ellipse{sel}"
            f"{{fill:{fill};stroke:{stroke}}}"
            f"{sel}>.t,{sel}>.th{{fill:{title}}}{sel}>.ts{{fill:{sub}}}"
        )
    return "\n".join(out)


BASE_RULES = """
.t{font:400 14px var(--font-sans);fill:var(--text-primary)}
.ts{font:400 12px var(--font-sans);fill:var(--text-secondary)}
.th{font:500 14px var(--font-sans);fill:var(--text-primary)}
.box{fill:var(--surface-1);stroke:var(--border-strong)}
.arr{stroke:var(--text-secondary);stroke-width:1.5;fill:none}
.leader{stroke:var(--text-muted);stroke-width:.5;stroke-dasharray:3 3;fill:none}
.node{cursor:default}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
"""

HTML_RULES = """
html,body{margin:0;background:var(--surface-2);color:var(--text-primary);font:400 16px/1.7 var(--font-sans)}
body{padding:16px}
h1,h2,h3{font-weight:500;color:var(--text-primary)}
code,pre{font-family:var(--font-mono)}
button{font:inherit;font-size:14px;color:var(--text-primary);background:transparent;border:.5px solid var(--border-strong);
  border-radius:var(--radius);padding:6px 12px;cursor:pointer}
button:hover{background:var(--surface-1)}
button:active{transform:scale(.98)}
input,select,textarea{font:inherit;color:var(--text-primary);background:var(--surface-2);border:.5px solid var(--border-strong);
  border-radius:var(--radius);padding:6px 10px}
"""


def stylesheet(for_html):
    css = (
        ":root{" + COMMON_VARS + LIGHT_VARS + "}\n"
        "@media (prefers-color-scheme: dark){:root{" + DARK_VARS + "}\n" + ramp_rules(True) + "}\n"
        ":root[data-theme=dark]{" + DARK_VARS + "}\n"
        + ramp_rules(False) + "\n" + BASE_RULES
    )
    if for_html:
        css += HTML_RULES
    return css


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def export(code, name):
    code = code.strip()
    if code.startswith("<svg"):
        # SVG: put the stylesheet inside the <svg> so it also works as an <img>.
        if "xmlns=" not in code[:200]:
            code = code.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
        head_end = code.index(">") + 1
        code = code[:head_end] + "\n<style>" + stylesheet(False) + "</style>" + code[head_end:]
        # width="100%" makes an <img> collapse; use the viewBox width instead.
        vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', code)
        if vb:
            code = code.replace('width="100%"', f'width="{vb.group(1)}" height="{vb.group(2)}"', 1)
        path = SVG_OUT / f"{name}.svg"
    else:
        # HTML: a full page that reports its height so the parent iframe can fit it.
        code = (
            "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
            f"<title>{name}</title>\n<style>{stylesheet(True)}</style>\n"
            "<script>window.sendPrompt=function(t){alert(t)};window.openLink=function(u){window.open(u,'_blank')};</script>\n"
            "</head>\n<body>\n" + code + "\n</body>\n</html>\n"
        )
        path = HTML_OUT / f"{name}.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(code)
    return path


def widgets_in_transcript(jsonl):
    found = {}
    for line in open(jsonl):
        try:
            msg = json.loads(line).get("message", {})
        except json.JSONDecodeError:
            continue
        content = msg.get("content") if isinstance(msg, dict) else None
        for part in content if isinstance(content, list) else []:
            if part.get("type") == "tool_use" and part.get("name") == "mcp__visualize__show_widget":
                found[part["input"].get("title", "widget")] = part["input"]["widget_code"]  # last version wins
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("--name")
    ap.add_argument("--from-transcript")
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()
    if args.from_transcript:
        for title, code in widgets_in_transcript(args.from_transcript).items():
            if args.only and title not in args.only:
                continue
            print(export(code, slug(title)).relative_to(ROOT))
    else:
        src = pathlib.Path(args.file)
        print(export(src.read_text(), args.name or slug(src.stem)).relative_to(ROOT))


if __name__ == "__main__":
    main()
