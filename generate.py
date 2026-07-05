#!/usr/bin/env python3
import json
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent
TEAM_FILE = ROOT / "team.json"
OUT_DIR = ROOT / "team"
VIEW_DIR = ROOT / "view"


def photo_url(member: dict) -> str:
    if member.get("foto"):
        return member["foto"]
    name = urllib.parse.quote(member["nombre"])
    return f"https://ui-avatars.com/api/?name={name}&size=160&background=D4837A&color=ffffff&bold=true"


def cargo_row(member: dict) -> str:
    cargo = member["cargo"]
    titulo = member.get("titulo")
    if titulo:
        return f"""            <span style="font-size: 13px; color: #1A1F2E; font-weight: 500;">
              {cargo}
            </span>
            <span style="font-size: 13px; color: #D4837A;"> · </span>
            <span style="font-size: 13px; color: #888888;">
              {titulo}
            </span>"""
    return f"""            <span style="font-size: 13px; color: #1A1F2E; font-weight: 500;">
              {cargo}
            </span>"""


def links_row(member: dict) -> str:
    linkedin = member.get("linkedin")
    if linkedin:
        return f"""            <table cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td style="vertical-align: middle; padding: 0; line-height: 13px;">
                  <a href="https://alfondo.cl" style="color: #D4837A; text-decoration: none; font-size: 13px; line-height: 13px;">
                    alfondo.cl
                  </a>
                </td>
                <td style="vertical-align: middle; padding: 0 8px; line-height: 13px; color: #DDDDDD; font-size: 12px;">
                  ·
                </td>
                <td style="vertical-align: middle; padding: 0; line-height: 13px;">
                  <a href="{linkedin}" style="text-decoration: none; line-height: 13px;">
                    <span style="display: inline-block; width: 14px; height: 14px; background-color: #C4C4C4; color: #FFFFFF; font-family: Arial, Helvetica, sans-serif; font-size: 8px; font-weight: 700; line-height: 14px; text-align: center; border-radius: 2px; letter-spacing: -0.3px; vertical-align: middle;">in</span>
                  </a>
                </td>
              </tr>
            </table>"""
    return """            <a href="https://alfondo.cl" style="color: #D4837A; text-decoration: none; font-size: 13px; line-height: 13px;">
              alfondo.cl
            </a>"""


def build_signature(member: dict) -> str:
    return f"""<!-- Firma Alfondo — {member["nombre"]} -->
<table cellpadding="0" cellspacing="0" border="0" style="font-family: -apple-system, 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 14px; line-height: 1.5; color: #3D3D3D; max-width: 480px;">
  <tr>
    <td style="padding: 0 18px 0 0; vertical-align: top;">
      <img
        src="{photo_url(member)}"
        alt="{member["nombre"]}"
        width="72"
        height="72"
        style="display: block; border-radius: 50%; border: 0; object-fit: cover;"
      />
    </td>
    <td style="vertical-align: top; border-left: 2px solid #D4837A; padding: 0 0 0 18px;">
      <table cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td style="padding: 0 0 1px 0;">
            <span style="font-size: 17px; font-weight: 600; color: #1A1F2E; letter-spacing: -0.3px;">
              {member["nombre"]}
            </span>
          </td>
        </tr>
        <tr>
          <td style="padding: 0 0 10px 0;">
{cargo_row(member)}
          </td>
        </tr>
        <tr>
          <td style="padding: 0 0 14px 0;">
{links_row(member)}
          </td>
        </tr>
        <tr>
          <td style="padding: 0;">
            <a href="https://alfondo.cl" style="text-decoration: none;">
              <img
                src="https://alfondo.cl/logo-negro-sinfondo.png"
                alt="alfondo"
                width="100"
                height="auto"
                style="display: block; border: 0;"
              />
            </a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
"""


def build_view_page(member: dict, signature: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Firma — {member["nombre"]}</title>
  <style>
    body {{
      font-family: -apple-system, sans-serif;
      margin: 40px;
      color: #333;
    }}
    button {{
      font-family: inherit;
      font-size: 13px;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
      border: 1px solid #1A1F2E;
      background: #1A1F2E;
      color: #fff;
      margin-bottom: 24px;
    }}
    button:hover {{ opacity: 0.88; }}
    .hint {{
      margin-top: 24px;
      font-size: 13px;
      color: #888;
      max-width: 480px;
      line-height: 1.6;
    }}
  </style>
</head>
<body>
  <button type="button" onclick="copySignature()">Copiar firma</button>
  <div id="signature">
{signature}
  </div>
  <p class="hint">Pega en Gmail → Configuración → Firma con Cmd+V</p>
  <script>
    function copySignature() {{
      const el = document.getElementById('signature');
      const range = document.createRange();
      range.selectNodeContents(el);
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
      document.execCommand('copy');
      sel.removeAllRanges();
    }}
  </script>
</body>
</html>
"""


def generate(verbose: bool = True) -> int:
    team = json.loads(TEAM_FILE.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(exist_ok=True)
    VIEW_DIR.mkdir(exist_ok=True)

    for member in team:
        signature = build_signature(member)
        path = OUT_DIR / f"{member['slug']}.html"
        path.write_text(signature, encoding="utf-8")

        view_path = VIEW_DIR / f"{member['slug']}.html"
        view_path.write_text(build_view_page(member, signature), encoding="utf-8")

        if verbose:
            print(f"✓ {path.name} + view/{member['slug']}.html")

    if verbose:
        print(f"\n{len(team)} firmas generadas")

    return len(team)


def main():
    generate(verbose=True)


if __name__ == "__main__":
    main()
