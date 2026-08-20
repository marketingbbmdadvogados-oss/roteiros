#!/usr/bin/env python3
"""
Arruma os nomes DEPOIS de transcrever, usando o que o Gemini identificou.

Serve para quem baixou os vídeos por site e ficou com nome aleatório: você transcreve
assim mesmo, e este script usa a seção "Identificação" de cada transcrição para
descobrir qual vídeo é qual.

Passo 1:  python 3-organizar.py             → mostra o que ele identificou (não muda nada)
Passo 2:  python 3-organizar.py --aplicar   → renomeia vídeo + transcrição e corrige a fonte

Confiança 'baixa' nunca é aplicada automaticamente — fica para você resolver à mão.
"""

import re
import sys

import codigos
import config

VALIDOS = {c for c, _, _ in codigos.TODOS} | set(codigos.REPOSTS)
DESCRICAO = {c: d for c, _, d in codigos.TODOS}


def identificacao(texto):
    """Lê CODIGO e CONFIANCA da seção Identificação da transcrição."""
    cod = re.search(r"^\s*CODIGO:\s*([A-Za-z0-9_-]+)", texto, re.M)
    conf = re.search(r"^\s*CONFIANCA:\s*(\w+)", texto, re.M)
    codigo = cod.group(1).strip() if cod else None
    confianca = (conf.group(1).strip().lower() if conf else "desconhecida")
    if codigo not in VALIDOS:
        codigo = None
    return codigo, confianca


def video_de(stem):
    for p in config.videos_existentes():
        if p.stem == stem:
            return p
    return None


def main():
    aplicar = "--aplicar" in sys.argv
    md_dir = config.DIR_TRANSCRICOES
    if not md_dir.exists():
        sys.exit(f"Não achei {md_dir}. Rode 'python 2-transcrever.py' antes.")

    planos, pulados = [], []

    for md in sorted(md_dir.glob("*.md")):
        texto = md.read_text(encoding="utf-8")
        codigo, confianca = identificacao(texto)

        if md.stem in VALIDOS:
            continue  # já está com o nome certo
        if not codigo:
            pulados.append((md.name, "o Gemini não identificou o vídeo"))
            continue
        if confianca == "baixa":
            pulados.append((md.name, f"confiança baixa (sugeriu {codigo})"))
            continue
        if (md_dir / f"{codigo}.md").exists():
            pulados.append((md.name, f"{codigo}.md já existe"))
            continue

        planos.append((md, codigo, confianca, video_de(md.stem)))

    if not planos and not pulados:
        print("Tudo já está organizado.")
        return

    for md, codigo, confianca, video in planos:
        alvo_video = f" + {video.name} → {codigo}{video.suffix}" if video else " (vídeo não encontrado)"
        print(f"  {md.name} → {codigo}.md{alvo_video}")
        print(f"      confiança {confianca} · {DESCRICAO.get(codigo, '')[:60]}")

    if pulados:
        print("\n  Não mexi nestes:")
        for nome, motivo in pulados:
            print(f"    {nome}: {motivo}")

    if not aplicar:
        print(f"\n{len(planos)} pronto(s) para renomear. Confira acima e rode:")
        print("  python 3-organizar.py --aplicar")
        return

    for md, codigo, _, video in planos:
        texto = md.read_text(encoding="utf-8")
        texto = texto.replace(
            f"# {md.stem}", f"# {codigo}", 1
        ).replace(
            "- **Fonte:** DESCONHECIDA — arquivo com nome fora do padrão, rode 0-renomear.py",
            f"- **Fonte:** {codigos.url(codigo)}",
            1,
        )
        (md_dir / f"{codigo}.md").write_text(texto, encoding="utf-8")
        md.unlink()
        if video:
            video.rename(video.with_name(codigo + video.suffix))
        print(f"  ✓ {codigo}")

    print(f"\n{len(planos)} organizado(s). Confira com: python 0-conferir.py")
    print("\nFalta só a data de cada post (o download por site não traz).")
    print("Abra cada link e anote — os links estão em: python 0-conferir.py")


if __name__ == "__main__":
    main()
