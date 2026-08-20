#!/usr/bin/env python3
"""
Renomeia vídeos baixados com nome aleatório (de site downloader) para o código do reel.

O script NÃO adivinha sozinho: ele propõe um mapa por ordem de download
(mais antigo primeiro = ordem da checklist) e deixa VOCÊ conferir antes de aplicar.

Passo 1:  python3 0-renomear.py             → gera e mostra renomear.txt
Passo 2:  confira/edite renomear.txt        → uma linha por arquivo: nome_atual -> CODIGO
Passo 3:  python3 0-renomear.py --aplicar   → renomeia de verdade
"""

import pathlib
import sys

import codigos
import config

DIR_VIDEOS = config.DIR_VIDEOS
MAPA = pathlib.Path(__file__).resolve().parent / "renomear.txt"
VIDEO_EXT = config.VIDEO_EXT


def nao_identificados():
    conhecidos = {c for c, _, _ in codigos.TODOS} | set(codigos.REPOSTS)
    return sorted(
        (p for p in config.videos_existentes() if p.stem not in conhecidos),
        key=lambda p: p.stat().st_mtime,
    )


def codigos_livres():
    ja_tem = {p.stem for p in config.videos_existentes()}
    return [(c, d) for c, _, d in codigos.TODOS if c not in ja_tem]


def propor():
    pendentes = nao_identificados()
    if not pendentes:
        print("Nenhum arquivo com nome desconhecido. Nada a renomear.")
        return

    livres = codigos_livres()
    linhas = [
        "# Confira cada linha antes de aplicar. Formato:  nome_do_arquivo -> CODIGO",
        "# A proposta assume que você baixou na ordem da checklist (mais antigo primeiro).",
        "# Se estiver errado, é só trocar o CODIGO na linha. Apague a linha pra pular o arquivo.",
        "#",
    ]
    for i, arquivo in enumerate(pendentes):
        if i < len(livres):
            cod, desc = livres[i]
            linhas.append(f"{arquivo.name} -> {cod}   # {desc}")
        else:
            linhas.append(f"{arquivo.name} -> ???   # sem código livre — preencha à mão")

    MAPA.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print("\n".join(linhas))
    print(f"\n→ Proposta gravada em {MAPA}")
    print("  CONFIRA se cada arquivo corresponde mesmo ao vídeo do código.")
    print("  Depois rode:  python3 0-renomear.py --aplicar")


def aplicar():
    if not MAPA.exists():
        sys.exit(f"{MAPA} não existe. Rode 'python3 0-renomear.py' primeiro.")

    validos = {c for c, _, _ in codigos.TODOS} | set(codigos.REPOSTS)
    renomeados = erros = 0

    for linha in MAPA.read_text(encoding="utf-8").splitlines():
        linha = linha.split("#")[0].strip()
        if not linha or "->" not in linha:
            continue
        nome, _, cod = linha.partition("->")
        nome, cod = nome.strip(), cod.strip()

        origem = DIR_VIDEOS / nome
        if not origem.exists():
            print(f"  ✗ {nome}: não encontrado em {DIR_VIDEOS}/")
            erros += 1
            continue
        if cod not in validos:
            print(f"  ✗ {nome}: código '{cod}' não está na lista")
            erros += 1
            continue

        destino = origem.with_name(cod + origem.suffix)
        if destino.exists():
            print(f"  ✗ {nome}: {destino.name} já existe")
            erros += 1
            continue

        origem.rename(destino)
        print(f"  ✓ {nome} → {destino.name}")
        renomeados += 1

    print(f"\n{renomeados} renomeado(s), {erros} erro(s).")
    if renomeados:
        MAPA.unlink()
        print("Confira com:  python3 0-conferir.py")


if __name__ == "__main__":
    DIR_VIDEOS.mkdir(parents=True, exist_ok=True)
    aplicar() if "--aplicar" in sys.argv else propor()
