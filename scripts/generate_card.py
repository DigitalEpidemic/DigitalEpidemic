"""Generates a neofetch-style profile card (dark_mode.svg / light_mode.svg).

Static generator - every field is a real, verifiable fact (see the
resume/portfolio repos). Re-run this manually and commit the output
whenever a field needs updating; there is no auto-refresh workflow.
"""

import os

USERNAME = "DigitalEpidemic"
FULL_NAME = "Jeffrey Polasz"

# The actual 404-page illustration from jeffpolasz.com/fake, reused verbatim
# (plain ASCII only - no Unicode box-drawing/block glyphs, which render
# inconsistently across monospace fonts, confirmed by an earlier attempt).
ART = r"""
            XXXX
           X    XX
          X  ***  X                XXXXX
         X  *****  X            XXX     XX
      XXXX ******* XXX      XXXX          XX
    XX   X ******  XXXXXXXXX                XX XXX
  XX      X ****  X                           X** X
 X        XX    XX     X                      X***X
X         //XXXX       X                      XXXX
X         //   X                             XX
X         //    X          XXXXXXXXXXXXXXXXXX/
X     XXX//    X          X
X    X   X     X         X
X    X    X    X        X
X   X    X    X        X                    XX
X    X   X    X        X                 XXX  XX
X    XXX      X        X               X  X X  X
X             X         X              XX X  XXXX
 X             X         XXXXXXXX\     XX   XX  X
  XX            XX              X     X    X  XX
    XX            XXXX   XXXXXX/     X     XXXX
      XXX             XX***         X     X
         XXXXXXXXXXXXX *   *       X     X
                      *---* X     X     X
                     *-* *   XXX X     X
                     *- *       XXX   X
                    *- *X          XXX
                    *- *X  X          XXX
                   *- *X    X            XX
                   *- *XX    X             X
                  *  *X* X    X             X
                  *  *X * X    X             X
                 *  * X**  X   XXXX          X
                 *  * X**  XX     X          X
                *  ** X** X     XX          X
                *  **  X*  XXX   X         X
               *  **    XX   XXXX       XXX
              *  * *      XXXX      X     X
             *   * *          X     X     X
=======*******   * *           X     X      XXXXXXXX\
      *         * *      /XXXXX      XXXXXXXX\      )
 =====**********  *     X                     )  \  )
   ====*         *     X               \  \   )XXXXX
=========**********       XXXXXXXXXXXXXXXXXXXXXX
""".strip("\n").split("\n")


def build_art():
    return ART


def build_lines():
    lines = []
    lines.append(("field", "Name", FULL_NAME))
    lines.append(("field", "Age", "29"))
    lines.append(("field", "Country", "Canada"))
    lines.append(("blank", ""))
    lines.append(("category", "Career"))
    lines.append(("field", "Work", "Vehikl"))
    lines.append(("field", "Title", "Senior Full Stack Developer"))
    lines.append(("blank", ""))
    lines.append(("category", "Favourites"))
    lines.append(("field", "Languages", "TypeScript, C#, PHP, Python, Ruby"))
    lines.append(("field", "Frameworks", "React, React Native, Next.js, Node.js, Express, .NET, Laravel, Rails"))
    lines.append(("field", "Databases", "PostgreSQL, SQL Server, Redis, MongoDB, Firebase, SQLite"))
    lines.append(("field", "IDE", "VS Code, Rider"))
    lines.append(("blank", ""))
    lines.append(("category", "Game Dev"))
    lines.append(("field", "Engines", "Unity, Unreal Engine"))
    lines.append(("field", "Platforms", "Android, iOS"))
    lines.append(("field", "Shipped", "21 mobile games"))
    lines.append(("blank", ""))
    lines.append(("category", "Contact"))
    lines.append(("field", "Email", "jeff_polasz@hotmail.com"))
    lines.append(("field", "LinkedIn", "/in/jeffrey-polasz"))
    lines.append(("field", "Website", "jeffpolasz.com"))
    return lines


PALETTES = {
    "dark": {
        "bg": "#0d1117",
        "name": "#c9d1d9",
        "label": "#ffa657",
        "dots": "#616e7f",
        "value": "#a5d6ff",
    },
    "light": {
        "bg": "#ffffff",
        "name": "#24292f",
        "label": "#953800",
        "dots": "#c2cfde",
        "value": "#0a3069",
    },
}

FONT = "ConsolasFallback,Consolas,monospace"
FONT_STYLE = (
    "<style>@font-face {"
    "src: local('Consolas'), local('Consolas Bold');"
    "font-family: 'ConsolasFallback';"
    "font-display: swap;"
    "-webkit-size-adjust: 109%;"
    "size-adjust: 109%;"
    "}</style>"
)
FONT_SIZE = 13
CHAR_W = FONT_SIZE * 0.6
MIN_LINE_CHARS = 68


def esc(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def rule(prefix, total_chars):
    pad = max(3, total_chars - len(prefix) - 1)
    return f"{prefix} " + "-" * pad


def render_svg(lines, palette_name):
    p = PALETTES[palette_name]
    line_height = 22
    top_pad = 34
    left = 24

    art = build_art()
    art_font_size = 9
    art_char_w = art_font_size * 0.6
    art_line_height = art_font_size + 3
    art_width_chars = max(len(row) for row in art)
    art_x = left
    divider_x = art_x + art_width_chars * art_char_w + 20
    info_x = divider_x + 24

    # Dots are sized so every value's *right* edge lands on the same column
    # as the header/category rules - not just far enough to clear the
    # longest label. The shared line width grows past MIN_LINE_CHARS if any
    # field's own content needs more room, so nothing ever clips.
    field_entries = [l for l in lines if l[0] == "field"]
    min_dots = 3
    content_min = max(len(f". {label}:") + 2 + min_dots + len(str(value)) for _, label, value in field_entries)
    target_len = max(MIN_LINE_CHARS, content_min)

    info_rows = len(lines) + 1
    content_height = max(len(art) * art_line_height, info_rows * line_height)
    height = int(top_pad + content_height + 10)
    width = int(info_x + target_len * CHAR_W + left)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT}" font-size="{FONT_SIZE}">',
        FONT_STYLE,
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="{p["bg"]}"/>',
        f'<line x1="{divider_x}" y1="{top_pad - 20}" x2="{divider_x}" y2="{height - 14}" '
        f'stroke="{p["dots"]}" stroke-width="1"/>',
    ]

    for i, art_row in enumerate(art):
        y = top_pad - 8 + i * art_line_height
        svg.append(
            f'<text x="{art_x}" y="{y}" font-size="{art_font_size}" '
            f'fill="{p["name"]}" xml:space="preserve">{esc(art_row)}</text>'
        )

    header_rule = rule(USERNAME, target_len)
    svg.append(
        f'<text x="{info_x}" y="{top_pad}" fill="{p["name"]}" xml:space="preserve">{esc(header_rule)}</text>'
    )

    row = 1
    for entry in lines:
        kind = entry[0]
        y = top_pad + row * line_height
        if kind == "blank":
            row += 1
            continue
        if kind == "category":
            text = entry[1]
            r = rule(f"- {text}", target_len)
            svg.append(
                f'<text x="{info_x}" y="{y}" fill="{p["name"]}" xml:space="preserve">{esc(r)}</text>'
            )
        elif kind == "field":
            _, label, value = entry
            prefix = f". {label}:"
            dots_len = max(min_dots, target_len - len(prefix) - len(str(value)) - 2)
            dots = "." * dots_len
            svg.append(
                f'<text x="{info_x}" y="{y}" xml:space="preserve">'
                f'<tspan fill="{p["label"]}">{esc(prefix)}</tspan>'
                f'<tspan fill="{p["dots"]}"> {esc(dots)} </tspan>'
                f'<tspan fill="{p["value"]}">{esc(value)}</tspan></text>'
            )
        row += 1

    svg.append("</svg>")
    return "\n".join(svg)


def main():
    lines = build_lines()
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for theme in ("dark", "light"):
        svg = render_svg(lines, theme)
        out_path = os.path.join(repo_root, f"{theme}_mode.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
