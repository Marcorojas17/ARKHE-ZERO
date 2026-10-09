#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════
 ▓▒░ BUILD · ARKHÉ ZERO · ◯_● · 51/49/100 ░▒▓
 ─────────────────────────────────────────────────────────────────────────
 Genera todos los assets binarios: fonts, imágenes, audio.
═══════════════════════════════════════════════════════════════════════════
"""
import subprocess
import sys
from pathlib import Path

SEAL = "◯_● · 51/49/100"
ROOT = Path(__file__).parent.parent


def fonts():
    print("[ >> ] Descargando fuentes...")
    dest = ROOT / "assets" / "fonts" / "inter"
    dest.mkdir(parents=True, exist_ok=True)
    fuentes = [
        ("inter/files/inter-latin-400-normal.woff2", "Inter-400.woff2"),
        ("inter/files/inter-latin-700-normal.woff2", "Inter-700.woff2"),
        ("jetbrains-mono/files/jetbrains-mono-latin-400-normal.woff2", "JetBrainsMono-400.woff2"),
        ("jetbrains-mono/files/jetbrains-mono-latin-700-normal.woff2", "JetBrainsMono-700.woff2"),
    ]
    for src, out in fuentes:
        url = f"https://fonts.bunny.net/{src}"
        target = dest / out
        if target.exists():
            print(f"[ SKIP ] {out}")
            continue
        try:
            subprocess.run(["curl", "-fsSL", "-o", str(target), url], check=True)
            print(f"[ OK ] {out}")
        except subprocess.CalledProcessError:
            print(f"[ WARN ] no se pudo descargar {out}")


def img():
    print("[ >> ] Convirtiendo SVG a PNG...")
    svg_dir = ROOT / "assets" / "img"
    for svg in svg_dir.glob("*.svg"):
        png = svg.with_suffix(".png")
        try:
            subprocess.run(
                ["rsvg-convert", "-w", "1200", str(svg), "-o", str(png)],
                check=True,
            )
            print(f"[ OK ] {png.name}")
        except (FileNotFoundError, subprocess.CalledProcessError):
            print(f"[ WARN ] rsvg-convert no disponible · {svg.name}")


def audio():
    print("[ >> ] Generando audio ceremonial...")
    dest = ROOT / "assets" / "audio"
    dest.mkdir(parents=True, exist_ok=True)
    silence = dest / "silence-3s.mp3"
    if not silence.exists():
        try:
            subprocess.run([
                "ffmpeg", "-f", "lavfi",
                "-i", "anullsrc=r=44100:cl=mono",
                "-t", "3", "-q:a", "9",
                "-acodec", "libmp3lame",
                str(silence), "-y"
            ], check=True, capture_output=True)
            print(f"[ OK ] silence-3s.mp3")
        except (FileNotFoundError, subprocess.CalledProcessError):
            print(f"[ WARN ] ffmpeg no disponible")
    else:
        print(f"[ SKIP ] silence-3s.mp3")
    print("[ INFO ] kintsugi-theme.mp3 requiere grabación externa")


def main():
    print("╔═══════════════════════════════════════════════════════════╗")
    print(f"║  BUILD · ARKHÉ ZERO · {SEAL}              ║")
    print("╚═══════════════════════════════════════════════════════════╝")

    args = sys.argv[1:] or ["--all"]
    if "--all" in args or "--fonts" in args:
        fonts()
    if "--all" in args or "--img" in args:
        img()
    if "--all" in args or "--audio" in args:
        audio()

    print(f"\n[ ✓✓ ] BUILD COMPLETO · {SEAL}")


if __name__ == "__main__":
    main()