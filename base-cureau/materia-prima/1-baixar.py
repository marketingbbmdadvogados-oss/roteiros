#!/usr/bin/env python3
"""
Baixa os reels da @lucureau. Funciona igual no Windows, Mac e Linux.

Pré-requisitos:
    pip install -r requirements.txt
    estar LOGADO no Instagram no navegador (o yt-dlp reaproveita o cookie de lá)

Uso:
    python 1-baixar.py                    # baixa tudo que ainda falta
    python 1-baixar.py faltantes.txt      # baixa os links de um arquivo
    python 1-baixar.py --navegador firefox
    python 1-baixar.py --cookies cookies.txt   # se o cookie do navegador falhar

Os arquivos são salvos em videos/ já com o nome certo (o código do reel) e um
.info.json ao lado com a data do post.
"""

import argparse
import pathlib
import subprocess
import sys

import codigos

DIR_VIDEOS = pathlib.Path("videos")
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv"}


def links_faltantes():
    DIR_VIDEOS.mkdir(exist_ok=True)
    ja_tem = {p.stem for p in DIR_VIDEOS.iterdir() if p.suffix.lower() in VIDEO_EXT}
    return [codigos.url(c) for c, _, _ in codigos.TODOS if c not in ja_tem]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lista", nargs="?", help="arquivo com um link por linha")
    ap.add_argument("--navegador", default="chrome", help="chrome, firefox, edge, brave, safari")
    ap.add_argument("--cookies", help="caminho de um cookies.txt exportado")
    args = ap.parse_args()

    DIR_VIDEOS.mkdir(exist_ok=True)

    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--output", str(DIR_VIDEOS / "%(id)s.%(ext)s"),
        "--write-info-json",
        "--no-overwrites",
        "--ignore-errors",
        "--sleep-requests", "2",
        "--retries", "5",
    ]

    if args.cookies:
        cmd += ["--cookies", args.cookies]
    else:
        cmd += ["--cookies-from-browser", args.navegador]

    if args.lista:
        cmd += ["--batch-file", args.lista]
        print(f"Baixando os links de {args.lista}…\n")
    else:
        faltando = links_faltantes()
        if not faltando:
            print("Nada faltando — todos os vídeos já estão em videos/.")
            return
        cmd += faltando
        print(f"Baixando {len(faltando)} vídeo(s) que ainda faltam…\n")

    resultado = subprocess.run(cmd)

    baixados = len([p for p in DIR_VIDEOS.iterdir() if p.suffix.lower() in VIDEO_EXT])
    print(f"\n{baixados} vídeo(s) em {DIR_VIDEOS}/")
    print("Confira com:  python 0-conferir.py")

    if resultado.returncode != 0:
        print(
            "\nO yt-dlp reclamou de alguma coisa. As causas mais comuns:\n"
            "  1. versão velha       →  pip install -U yt-dlp\n"
            "  2. não está logado    →  abra o Instagram no navegador e faça login\n"
            "  3. navegador errado   →  python 1-baixar.py --navegador firefox\n"
            "  4. cookie bloqueado   →  exporte cookies.txt e use --cookies cookies.txt"
        )
        sys.exit(resultado.returncode)


if __name__ == "__main__":
    main()
