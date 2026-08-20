#!/usr/bin/env python3
"""
Transcreve os reels baixados usando o Gemini, que ASSISTE ao vídeo (não só ouve).

Por que Gemini e não Whisper/Premiere: vários vídeos dela ensinam pela imagem —
texto na tela, gráfico de retenção, mudança de entonação, corte de câmera.
Transcrição de áudio perde exatamente a parte que é a lição.

Setup:
    pip install -r requirements.txt
    export GEMINI_API_KEY="..."          # https://aistudio.google.com/apikey

Uso:
    python3 2-transcrever.py                          # tudo que estiver em videos/
    python3 2-transcrever.py videos/DW2Pp_tgFsO.mp4   # só um
    WORKERS=5 python3 2-transcrever.py                # mais paralelismo

Saída: transcricoes/<id>.md — um por vídeo. Idempotente: pula o que já existe,
então pode interromper e rodar de novo à vontade.
"""

import json
import os
import pathlib
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from google import genai
from google.genai import errors as genai_errors
from google.genai import types

import codigos
import config

CODIGOS_VALIDOS = {c for c, _, _ in codigos.TODOS} | set(codigos.REPOSTS)

MODELO = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
DIR_VIDEOS = config.DIR_VIDEOS
DIR_SAIDA = config.DIR_TRANSCRICOES
WORKERS = int(os.environ.get("WORKERS", "3"))
CONFIG = types.GenerateContentConfig(
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
)
MAX_TENTATIVAS = int(os.environ.get("MAX_TENTATIVAS", "4"))

_log = threading.Lock()


def log(msg):
    with _log:
        print(msg, flush=True)


PROMPT = """Você está analisando um vídeo curto (Reel) da criadora Luíza Cureau,
que ensina método de criação de conteúdo. O objetivo é extrair TUDO que ela ensina,
incluindo o que está na imagem — não só o áudio.

Responda em português do Brasil, exatamente neste formato markdown:

## Transcrição da fala
[transcrição literal e completa do que ela fala, do começo ao fim. Sem resumir.
Marque mudanças de tom relevantes entre colchetes, ex: [muda o tom, mais firme].]

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

## Identificação
Abaixo está a lista de vídeos conhecidos deste perfil, com o que cada um ensina.
Diga qual deles é ESTE vídeo, comparando com o conteúdo que você acabou de analisar.
Responda em duas linhas, exatamente neste formato:

CODIGO: <o código da lista, ou NENHUM se não corresponder a nenhum>
CONFIANCA: <alta, media ou baixa>

Lista de vídeos conhecidos:
{catalogo}
"""

_CATALOGO = "\n".join(f"- {cod}: {desc}" for cod, _, desc in codigos.TODOS)
PROMPT = PROMPT.format(catalogo=_CATALOGO)


def cliente():
    chave = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not chave:
        sys.exit("Falta GEMINI_API_KEY. Pegue em https://aistudio.google.com/apikey")
    return genai.Client(api_key=chave)


def conferir_modelo(client):
    """Falha cedo e com clareza se o modelo não existir para esta chave.

    O Google aposenta modelo sem aviso, e sem isso o script cospe o mesmo 404
    uma vez por vídeo — o que esconde a causa real no meio da saída.
    """
    try:
        client.models.get(model=MODELO)
        return
    except genai_errors.APIError as erro:
        if getattr(erro, "code", None) != 404:
            return  # outro problema: deixa estourar no uso real

    print(f"O modelo '{MODELO}' não está disponível para a sua chave.\n")
    try:
        nomes = [
            m.name.removeprefix("models/")
            for m in client.models.list()
            if "generateContent" in (getattr(m, "supported_actions", None) or [])
        ]
        flashes = [n for n in nomes if "flash" in n and "image" not in n and "tts" not in n]
        print("Modelos disponíveis para você (os 'flash' são os mais baratos e rápidos):")
        for n in sorted(flashes or nomes)[:15]:
            print(f"  {n}")
    except Exception:
        print("Veja a lista em https://aistudio.google.com")

    print("\nEscolha um e rode de novo, por exemplo:")
    print('  $env:GEMINI_MODEL="gemini-3.6-flash"   (PowerShell)')
    print("  set GEMINI_MODEL=gemini-3.6-flash      (CMD)")
    sys.exit(1)


def data_do_post(video: pathlib.Path) -> str:
    """Lê a data do .info.json do yt-dlp. Data é campo obrigatório na base."""
    info = video.parent / f"{video.stem}.info.json"
    if info.exists():
        try:
            bruto = str(json.loads(info.read_text(encoding="utf-8")).get("upload_date") or "")
            if len(bruto) == 8:
                return f"{bruto[6:8]}/{bruto[4:6]}/{bruto[0:4]}"
        except Exception:
            pass
    return "DESCONHECIDA — preencher à mão"


def aguardar_ativo(client, arquivo, limite=600):
    """A Files API precisa terminar de processar o vídeo antes de usá-lo."""
    inicio = time.time()
    while arquivo.state.name == "PROCESSING":
        if time.time() - inicio > limite:
            raise TimeoutError("Gemini demorou demais processando o vídeo")
        time.sleep(3)
        arquivo = client.files.get(name=arquivo.name)
    if arquivo.state.name == "FAILED":
        raise RuntimeError("Gemini falhou ao processar o vídeo")
    return arquivo


def transcrever(client, video: pathlib.Path) -> str:
    """Sobe, pergunta, limpa. Com backoff em rate limit (429) e erro transitório."""
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        enviado = None
        try:
            enviado = aguardar_ativo(client, client.files.upload(file=str(video)))
            return client.models.generate_content(
                model=MODELO, contents=[enviado, PROMPT], config=CONFIG
            ).text
        except genai_errors.APIError as erro:
            transitorio = getattr(erro, "code", None) in (429, 500, 503)
            if not transitorio or tentativa == MAX_TENTATIVAS:
                raise
            espera = min(60, 2**tentativa) + random.uniform(0, 2)
            log(f"    {video.stem}: {erro.code}, nova tentativa em {espera:.0f}s")
            time.sleep(espera)
        finally:
            if enviado is not None:
                try:
                    client.files.delete(name=enviado.name)
                except Exception:
                    pass
    raise RuntimeError("tentativas esgotadas")


def processar(client, video: pathlib.Path):
    saida = DIR_SAIDA / f"{video.stem}.md"
    if saida.exists():
        log(f"  {video.stem}: já feito")
        return None

    log(f"  {video.stem}: enviando…")
    corpo = transcrever(client, video)

    if video.stem in CODIGOS_VALIDOS:
        fonte = f"https://www.instagram.com/lucureau/reel/{video.stem}/"
    else:
        fonte = "DESCONHECIDA — arquivo com nome fora do padrão, rode 0-renomear.py"

    cabecalho = (
        f"# {video.stem}\n\n"
        f"- **Fonte:** {fonte}\n"
        f"- **Data do post:** {data_do_post(video)}\n"
        f"- **Transcrito em:** {time.strftime('%d/%m/%Y')} (Gemini {MODELO})\n\n---\n\n"
    )
    saida.write_text(cabecalho + corpo, encoding="utf-8")
    log(f"  {video.stem}: ok → {saida}")
    return saida


def main():
    client = cliente()
    conferir_modelo(client)
    DIR_SAIDA.mkdir(parents=True, exist_ok=True)

    videos = (
        [pathlib.Path(a) for a in sys.argv[1:]]
        if len(sys.argv) > 1
        else config.videos_existentes()
    )
    if not videos:
        sys.exit(f"Nenhum vídeo em {DIR_VIDEOS}. Rode: python 1-baixar.py")

    log(config.resumo())
    log(f"\n{len(videos)} vídeos, {WORKERS} em paralelo, modelo {MODELO}\n")
    inicio = time.time()
    falhas = []

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        tarefas = {pool.submit(processar, client, v): v for v in videos}
        for tarefa in as_completed(tarefas):
            video = tarefas[tarefa]
            try:
                tarefa.result()
            except Exception as erro:
                log(f"  {video.stem}: ERRO — {erro}")
                falhas.append((video.stem, str(erro)))

    prontos = len(list(DIR_SAIDA.glob("*.md")))
    log(f"\n{prontos} transcrições em {DIR_SAIDA}/ ({time.time() - inicio:.0f}s)")
    if falhas:
        log("\nFalharam (rode de novo — ele pula o que já deu certo):")
        for nome, erro in falhas:
            log(f"  - {nome}: {erro[:140]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
