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

ART_FONT_SIZE = 9

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
    art_font_size = ART_FONT_SIZE
    art_char_w = art_font_size * 0.6
    art_line_height = art_font_size + 3
    art_width_chars = max(len(row) for row in art)
    art_x = left
    divider_x = art_x + art_width_chars * art_char_w + 20
    info_x = divider_x + 24

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


def render_art_svg(palette_name, font_size=ART_FONT_SIZE, right_gap=18):
    """Standalone art-only SVG, transparent background, sized purely from
    font_size - lets embedders resize via the <img> width attribute or by
    regenerating with a different font_size, independent of the info panel.

    Draws its own divider line down the right edge (plus right_gap of blank
    margin past it) so the art/text boundary is baked into the image instead
    of coming from an HTML table border - a raw <table> gets GitHub's default
    grid-line CSS applied to every cell, which is the "boxes around
    everything" look we don't want; a floated <img> next to a <pre> avoids
    <table> entirely and has no such border.
    """
    p = PALETTES[palette_name]
    art = build_art()
    char_w = font_size * 0.6
    line_height = font_size + 3
    pad = 4
    art_width = int(max(len(row) for row in art) * char_w)
    height = int(len(art) * line_height) + pad * 2
    divider_x = pad + art_width + 8
    width = divider_x + right_gap

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT}" font-size="{font_size}">',
        FONT_STYLE,
        f'<line x1="{divider_x}" y1="{pad}" x2="{divider_x}" y2="{height - pad}" '
        f'stroke="{p["dots"]}" stroke-width="1"/>',
    ]
    for i, row in enumerate(art):
        y = pad + font_size + i * line_height
        svg.append(
            f'<text x="{pad}" y="{y}" fill="{p["name"]}" xml:space="preserve">{esc(row)}</text>'
        )
    svg.append("</svg>")
    return "\n".join(svg)


def render_readme_snippet(lines):
    min_dots = 3
    field_entries = [l for l in lines if l[0] == "field"]
    content_min = max(len(f". {label}:") + 2 + min_dots + len(str(value)) for _, label, value in field_entries)
    target_len = max(MIN_LINE_CHARS, content_min)

    text_lines = [rule(USERNAME, target_len)]
    for entry in lines:
        kind = entry[0]
        if kind == "blank":
            text_lines.append("")
        elif kind == "category":
            text_lines.append(rule(f"- {entry[1]}", target_len))
        elif kind == "field":
            _, label, value = entry
            prefix = f". {label}:"
            dots_len = max(min_dots, target_len - len(prefix) - len(str(value)) - 2)
            dots = "." * dots_len
            text_lines.append(f"{prefix} {dots} {value}")

    text_str = "\n".join(text_lines)

    # A standalone <pre>...</pre> is a CommonMark "type 1" raw HTML block,
    # which only ends at the literal closing tag - unlike a <table>, it is
    # NOT terminated by blank lines, so the real blank spacer lines here are
    # safe (no zero-width-space workaround needed like the table version).
    return (
        "<picture>\n"
        '  <source media="(prefers-color-scheme: dark)" srcset="art_dark.svg">\n'
        f'  <img src="art_light.svg" align="left" alt="{esc(USERNAME)} ascii art">\n'
        "</picture>\n"
        "\n"
        "<pre>\n"
        f"{esc(text_str)}\n"
        "</pre>\n"
    )


def main():
    lines = build_lines()
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Generate SVGs
    for theme in ("dark", "light"):
        svg = render_svg(lines, theme)
        out_path = os.path.join(repo_root, f"{theme}_mode.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {out_path}")

        art_svg = render_art_svg(theme)
        art_out_path = os.path.join(repo_root, f"art_{theme}.svg")
        with open(art_out_path, "w", encoding="utf-8") as f:
            f.write(art_svg)
        print(f"wrote {art_out_path}")

    # Generate copyable HTML snippet (for local preview) and the README
    # GitHub actually renders on the profile.
    readme_content = render_readme_snippet(lines)
    html_out_path = os.path.join(repo_root, "profile_snippet.html")
    with open(html_out_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"wrote {html_out_path}")

    readme_path = os.path.join(repo_root, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"wrote {readme_path}")


if __name__ == "__main__":
    main()
