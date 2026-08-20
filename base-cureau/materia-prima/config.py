"""Onde ficam os vídeos e as transcrições.

Por padrão, dentro desta pasta (videos/ e transcricoes/). Para apontar pra uma pasta
compartilhada do OneDrive, defina as variáveis de ambiente antes de rodar os scripts:

    PowerShell:
        $env:DIR_VIDEOS="C:\\Users\\voce\\OneDrive\\Marketing\\Luiza\\videos"
        $env:DIR_TRANSCRICOES="C:\\Users\\voce\\OneDrive\\Marketing\\Luiza\\transcricoes"

    CMD:
        set DIR_VIDEOS=C:\\Users\\voce\\OneDrive\\Marketing\\Luiza\\videos
        set DIR_TRANSCRICOES=C:\\Users\\voce\\OneDrive\\Marketing\\Luiza\\transcricoes

    Mac/Linux:
        export DIR_VIDEOS=~/OneDrive/Marketing/Luiza/videos

Ou crie um arquivo `caminhos.txt` nesta pasta, com uma linha por variável:

    DIR_VIDEOS=C:\\Users\\voce\\OneDrive\\Marketing\\Luiza\\videos
    DIR_TRANSCRICOES=C:\\Users\\voce\\OneDrive\\Marketing\\Luiza\\transcricoes

O `caminhos.txt` é pessoal (fica fora do Git), então cada um da equipe pode ter o seu
sem atrapalhar os outros.
"""

import os
import pathlib

AQUI = pathlib.Path(__file__).resolve().parent
ARQUIVO_CAMINHOS = AQUI / "caminhos.txt"


def _do_arquivo():
    if not ARQUIVO_CAMINHOS.exists():
        return {}
    valores = {}
    for linha in ARQUIVO_CAMINHOS.read_text(encoding="utf-8").splitlines():
        linha = linha.split("#")[0].strip()
        if "=" in linha:
            chave, _, valor = linha.partition("=")
            valores[chave.strip()] = valor.strip().strip('"').strip("'")
    return valores


_ARQUIVO = _do_arquivo()


def _caminho(chave: str, padrao: str) -> pathlib.Path:
    """Ordem de prioridade: variável de ambiente > caminhos.txt > padrão local."""
    bruto = os.environ.get(chave) or _ARQUIVO.get(chave) or padrao
    return pathlib.Path(bruto).expanduser()


DIR_VIDEOS = _caminho("DIR_VIDEOS", str(AQUI / "videos"))
DIR_TRANSCRICOES = _caminho("DIR_TRANSCRICOES", str(AQUI / "transcricoes"))

VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv"}


def resumo() -> str:
    return f"vídeos:       {DIR_VIDEOS}\ntranscrições: {DIR_TRANSCRICOES}"


def videos_existentes():
    if not DIR_VIDEOS.exists():
        return []
    return sorted(p for p in DIR_VIDEOS.iterdir() if p.suffix.lower() in VIDEO_EXT)
