#!/usr/bin/env python3
"""
Transcreve os reels baixados usando o Gemini (que ASSISTE ao vídeo, não só ouve).

Por que Gemini e não Whisper: vários vídeos dela ensinam pela imagem — texto na
tela, gráfico de retenção, mudança de entonação, corte de câmera. Whisper só
ouve o áudio e perde exatamente a parte que é a lição.

Pré-requisitos (uma vez só):
    pip install -U google-genai
    export GEMINI_API_KEY="sua-chave"      # https://aistudio.google.com/apikey

Uso:
    python3 2-transcrever.py               # transcreve tudo em videos/
    python3 2-transcrever.py videos/DW2Pp_tgFsO.mp4    # um só

Saída: transcricoes/<id>.md  — um arquivo por vídeo, pronto pra virar princípio.
Roda de novo sem medo: pula o que já está transcrito.
"""

import json
import os
import pathlib
import sys
import time

from google import genai

MODELO = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
DIR_VIDEOS = pathlib.Path(os.environ.get("DIR_VIDEOS", "videos"))
DIR_SAIDA = pathlib.Path(os.environ.get("DIR_SAIDA", "transcricoes"))

PROMPT = """Você está analisando um vídeo curto (Reel) da criadora Luíza Cureau,
que ensina método de criação de conteúdo. O objetivo é extrair TUDO que ela ensina,
incluindo o que está na imagem — não só o áudio.

Responda em português do Brasil, exatamente neste formato markdown:

## Transcrição da fala
[transcrição literal e completa do que ela fala, do começo ao fim. Sem resumir.
Marque pausas ou mudanças de tom relevantes entre colchetes, ex: [muda o tom, mais firme].]

## Texto na tela
[TODO texto que aparece escrito no vídeo, na ordem em que aparece: capa, legendas
queimadas, overlays, setas, anotações, prints de tela. Se houver um gráfico ou print
do Instagram, descreva os números e rótulos que dá pra ler.]

## O que acontece na imagem
[Só o que faz parte da lição: o que ela demonstra, mostra na tela, aponta, ou faz
com o corpo/voz. Se o vídeo demonstra uma técnica visualmente (entonação, corte,
movimento de câmera, gráfico), descreva a demonstração em detalhe. Ignore cenário
decorativo e roupa.]

## Regras que ela enuncia
[Liste em bullets cada REGRA aplicável que ela dá, com o racional dela quando houver.
Formato: "- REGRA — porque [racional dela]". Se ela não der racional, escreva
"- REGRA — (sem racional declarado)". Não invente racional que ela não falou.]

## Tema principal
[Escolha um ou mais: gancho | estrutura | retenção | CTA | algoritmo | outro]
"""


def cliente():
    chave = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not chave:
        sys.exit("Falta a variável GEMINI_API_KEY. Pegue em https://aistudio.google.com/apikey")
    return genai.Client(api_key=chave)


def data_do_post(video: pathlib.Path) -> str:
    """Lê a data do .info.json que o yt-dlp salvou. A data é obrigatória na base."""
    info = video.with_suffix("").with_suffix(".info.json")
    if not info.exists():
        info = video.parent / f"{video.stem}.info.json"
    if info.exists():
        try:
            dados = json.loads(info.read_text(encoding="utf-8"))
            bruto = str(dados.get("upload_date") or "")
            if len(bruto) == 8:
                return f"{bruto[6:8]}/{bruto[4:6]}/{bruto[0:4]}"
        except Exception:
            pass
    return "DESCONHECIDA — preencher à mão"


def aguardar_ativo(client, arquivo, limite=300):
    """A Files API precisa terminar de processar o vídeo antes do uso."""
    inicio = time.time()
    while arquivo.state.name == "PROCESSING":
        if time.time() - inicio > limite:
            raise TimeoutError("O Gemini demorou demais processando o vídeo.")
        time.sleep(3)
        arquivo = client.files.get(name=arquivo.name)
    if arquivo.state.name == "FAILED":
        raise RuntimeError("O Gemini falhou ao processar o vídeo.")
    return arquivo


def transcrever(client, video: pathlib.Path) -> str:
    enviado = aguardar_ativo(client, client.files.upload(file=str(video)))
    try:
        resposta = client.models.generate_content(model=MODELO, contents=[enviado, PROMPT])
        return resposta.text
    finally:
        try:
            client.files.delete(name=enviado.name)
        except Exception:
            pass


def main():
    client = cliente()
    DIR_SAIDA.mkdir(exist_ok=True)

    if len(sys.argv) > 1:
        videos = [pathlib.Path(a) for a in sys.argv[1:]]
    else:
        videos = sorted(DIR_VIDEOS.glob("*.mp4"))

    if not videos:
        sys.exit(f"Nenhum .mp4 encontrado em {DIR_VIDEOS}/. Rode ./1-baixar.sh antes.")

    falhas = []
    for i, video in enumerate(videos, 1):
        saida = DIR_SAIDA / f"{video.stem}.md"
        if saida.exists():
            print(f"[{i}/{len(videos)}] {video.stem}: já feito, pulando")
            continue

        print(f"[{i}/{len(videos)}] {video.stem}: enviando…", flush=True)
        try:
            corpo = transcrever(client, video)
        except Exception as erro:
            print(f"    ERRO: {erro}")
            falhas.append((video.stem, str(erro)))
            continue

        cabecalho = (
            f"# {video.stem}\n\n"
            f"- **Fonte:** https://www.instagram.com/lucureau/reel/{video.stem}/\n"
            f"- **Data do post:** {data_do_post(video)}\n"
            f"- **Transcrito em:** {time.strftime('%d/%m/%Y')} (Gemini {MODELO})\n\n---\n\n"
        )
        saida.write_text(cabecalho + corpo, encoding="utf-8")
        print(f"    ok → {saida}")

    print(f"\nPronto. {len(list(DIR_SAIDA.glob('*.md')))} transcrições em {DIR_SAIDA}/")
    if falhas:
        print("\nFalharam (rode de novo, ele pula o que já deu certo):")
        for nome, erro in falhas:
            print(f"  - {nome}: {erro[:120]}")


if __name__ == "__main__":
    main()
