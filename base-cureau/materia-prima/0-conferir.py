#!/usr/bin/env python3
"""
Inventário: o que já está baixado, o que falta, o que já foi transcrito.

Uso:
    python3 0-conferir.py            # mostra a situação
    python3 0-conferir.py --faltantes   # + grava faltantes.txt pro yt-dlp

Reconhece um vídeo pelo NOME do arquivo (o código do reel, ex: DbI9QcxgcUm.mp4).
Arquivo com nome aleatório aparece como "não identificado" — use 0-renomear.py.
"""

import pathlib
import sys

import codigos
import config

DIR_VIDEOS = config.DIR_VIDEOS
DIR_SAIDA = config.DIR_TRANSCRICOES


def main():
    DIR_VIDEOS.mkdir(parents=True, exist_ok=True)
    arquivos = config.videos_existentes()
    print(config.resumo() + "\n")
    conhecidos = {c for c, _, _ in codigos.TODOS} | set(codigos.REPOSTS)

    baixados = {p.stem for p in arquivos if p.stem in conhecidos}
    nao_identificados = [p for p in arquivos if p.stem not in conhecidos]
    transcritos = {p.stem for p in DIR_SAIDA.glob("*.md")} if DIR_SAIDA.exists() else set()

    print(f"{len(arquivos)} arquivo(s) de vídeo\n")

    faltantes = []
    for lote in (1, 2, 3, 4, 5):
        itens = codigos.por_lote({lote})
        if not itens:
            continue
        print(f"── Lote {lote} " + "─" * 40)
        for cod, _, desc in itens:
            if cod in transcritos:
                marca = "✅ transcrito"
            elif cod in baixados:
                marca = "📥 baixado, falta transcrever"
            else:
                marca = "⬜ falta baixar"
                faltantes.append(cod)
            print(f"  {marca:32} {cod}  {desc[:48]}")
        print()

    if nao_identificados:
        print("⚠️  Arquivos com nome que eu não reconheço (precisam ser renomeados):")
        for p in nao_identificados:
            print(f"     {p.name}")
        print("     → rode: python3 0-renomear.py")
        print()

    repostos = [p.stem for p in arquivos if p.stem in codigos.REPOSTS]
    if repostos:
        print("ℹ️  Baixados mas são repost (não precisa transcrever):")
        for c in repostos:
            print(f"     {c} = mesmo conteúdo de {codigos.REPOSTS[c]}")
        print()

    print(
        f"Resumo: {len(baixados)} baixados · {len(transcritos)} transcritos · "
        f"{len(faltantes)} faltando baixar"
    )

    if "--faltantes" in sys.argv:
        if faltantes:
            destino = pathlib.Path("faltantes.txt")
            destino.write_text(
                "\n".join(codigos.url(c) for c in faltantes) + "\n", encoding="utf-8"
            )
            print(f"\n→ {destino} gravado com {len(faltantes)} link(s).")
            print("  Baixe com:  ./1-baixar.sh faltantes.txt")
        else:
            print("\nNada faltando — tudo já está em videos/.")


if __name__ == "__main__":
    main()
