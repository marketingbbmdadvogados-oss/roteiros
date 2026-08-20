# Como baixar e transcrever os vídeos da @lucureau

> 🟢 **Não é técnico? Não leia este arquivo.** Abra o `COMECE-AQUI.md` nesta mesma pasta:
> é o mesmo resultado, feito só clicando no navegador, sem instalar nada.
> Este aqui é a versão automática, para quem mexe com terminal.

## Resposta curta: eu não consigo fazer o download daqui

Testado agora, não é suposição:

| O que | Resultado |
|---|---|
| `instagram.com` a partir deste ambiente | **403** no túnel do proxy — bloqueado na rede |
| Assistir/ouvir vídeo nativamente | não faço — leio texto, imagem e PDF, não áudio nem vídeo |
| Rodar Whisper aqui | **não dá** — o HuggingFace e o CDN da OpenAI também estão bloqueados, não consigo baixar o modelo |
| Receber os `.mp4` por Drive e transcrever aqui | inviável — o Drive me entrega o arquivo em base64, e 30 vídeos estouram a janela de contexto |

O que eu **consigo** é a parte cara: pegar as transcrições em texto e virar princípio
numerado, com fonte, data e tradução para o perfil do Isaac.

**"Tem alguma IA que vê o vídeo e já transcreve?"** Tem, e é o que você quer usar:
o **Gemini** aceita o arquivo de vídeo e devolve transcrição + texto na tela + descrição
do que acontece na imagem. Isso importa muito aqui: vários vídeos dela ensinam pela imagem
(o gráfico de retenção, as 4 entonações do mesmo gancho, os cortes de câmera). Whisper só
ouve o áudio e perde justamente a lição.

---

## O caminho rápido (30–40 min no total, quase tudo esperando)

### 1. Instalar (uma vez só)

```bash
pip install -U yt-dlp google-genai
```

Pegue uma chave em https://aistudio.google.com/apikey e exporte:

```bash
export GEMINI_API_KEY="sua-chave"
```

### 2. Baixar

Precisa estar **logado no Instagram no navegador** — o `yt-dlp` reaproveita o cookie de lá.
Reel de terceiro não baixa deslogado.

```bash
python 1-baixar.py
```

Se você não usa Chrome: `python 1-baixar.py --navegador firefox` (aceita firefox, brave, edge, safari).

Leva uns 3–5 min para os 30. Salva em `videos/` e guarda um `.info.json` por vídeo —
**é dele que sai a data do post**, e data é campo obrigatório na base de princípios.

### 3. Transcrever

```bash
python3 2-transcrever.py
```

Um `.md` por vídeo em `transcricoes/`, já com fonte, data e a estrutura que eu preciso:
transcrição da fala, texto na tela, o que acontece na imagem, e as regras que ela enuncia
com o racional dela. Pode interromper e rodar de novo — pula o que já ficou pronto.

Custo: os 30 reels dão algo em torno de 45 min de vídeo. No `gemini-2.5-flash` isso fica
na casa de poucos dólares, e boa parte pode cair na cota gratuita do AI Studio.

### 4. Me entregar

Qualquer um serve:
- colar o conteúdo dos `.md` no chat;
- jogar a pasta `transcricoes/` num Doc ou pasta do Drive (eu leio Drive);
- commitar em `base-cureau/materia-prima/transcricoes/`.

---

## Comece pelo Tier 1, não pelos 30

O `urls.txt` está ordenado. Os **8 primeiros** cobrem os cinco temas e já destravam a base.
Especialmente estes três:

- `DW2Pp_tgFsO` — Ganchismo: os 4 tipos de gancho e o CTA como parte da receita
- `DbI9QcxgcUm` — o gráfico de retenção ligando queda no início ao gancho, no meio ao valor,
  no fim ao CTA. **Este é literalmente o diagnóstico que falta hoje**: ele transforma
  "o vídeo foi mal" em "a queda foi no segundo 4, então o problema é o gancho".
- `DbCV7PxgZT4` — a estrutura viral completa

Para rodar só o Tier 1:

```bash
grep -A20 'TIER 1' urls.txt | grep '^https' > tier1.txt
python 1-baixar.py tier1.txt
python3 2-transcrever.py
```

Me manda esses 8 e eu já devolvo a primeira leva de princípios com fonte e data. O resto
entra depois, sem travar o começo.

---

## Se der problema no download

O `yt-dlp` com cookie do navegador é o caminho mais confiável, mas o Instagram muda proteção
com frequência. Se falhar:

1. `pip install -U yt-dlp` — a correção quase sempre já saiu; a versão velha é a causa mais comum.
2. Exportar os cookies para um arquivo `cookies.txt` (extensão "Get cookies.txt" no navegador) e
   trocar no script: `--cookies cookies.txt` no lugar de `--cookies-from-browser`.
3. Último recurso, manual: abrir cada reel e usar um baixador web. Funciona, mas são 30 colagens —
   só vale se você for fazer apenas o Tier 1.

## Alternativa sem chave de API

Se não quiser mexer com chave: suba os `.mp4` direto no **Google AI Studio**
(https://aistudio.google.com), anexe os vídeos numa conversa e cole o prompt que está dentro de
`2-transcrever.py` (a constante `PROMPT`). Mesmo resultado, no braço. Vale para 8 vídeos;
para 30 o script compensa.

---

## Alternativa 100% local, sem chave de API (Whisper)

Se não quiser criar chave do Gemini, dá pra transcrever tudo offline com um comando só:

```bash
pip install -U openai-whisper
whisper videos/*.mp4 --model small --language pt \
        --output_format txt --output_dir transcricoes
```

Sem GPU, `--model small` roda os ~45 min de vídeo em torno de 15–25 min. Com GPU, minutos.
Se a qualidade ficar ruim em algum, sobe pra `--model medium` só naquele arquivo.

**A limitação:** Whisper só ouve. Ele não lê o texto na tela nem descreve o que ela demonstra —
e é aí que mora metade da aula dela (o gráfico de retenção, as 4 entonações, os cortes).
Serve como plano B, ou como complemento pro Gemini nos vídeos em que a fala é densa.

Mesma limitação vale pro Premiere: áudio apenas, um arquivo por vez.
