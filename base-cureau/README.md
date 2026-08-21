# Base de princípios — Luíza Cureau (@lucureau)

**Status: PREENCHIDA E AUDITADA — 25 vídeos, 26 transcrições, 47 princípios.**

Última atualização relevante: a **live de roteirização** (`DbOMz_RgGdj`, 25/07/2026) corroborou a
estrutura (`CUR-008`) e o mapa de CTA (`CUR-013`), que eram as peças de fonte única, e corrigiu
três coisas que estavam escritas errado. Detalhe na seção 9 de `principios.md`.

- `principios.md` — a base numerada (CUR-001…CUR-029), com fonte e tradução para o Isaac
- `auditoria-das-fontes.md` — **leia antes de usar**: corroboração, contradições e pontos soltos
- `materia-prima/transcricoes/` — as 26 transcrições brutas (25 vídeos; `aula-carrossel-longa`
  é a versão longa da mesma aula de `Db9aIvrgAMY`, não conta como fonte independente)
- `materia-prima/datas-dos-videos.md` — data de publicação dos 30 links, conferida

## Por que está vazia (leia antes de cobrar)

Tentei levantar o método dela por conta própria e não deu. O que foi tentado e o resultado:

| Tentativa | Resultado |
|---|---|
| `instagram.com/lucureau` | bloqueado pelo proxy de rede deste ambiente |
| Canal do YouTube dela | bloqueado pelo proxy de rede |
| Busca aberta pelo método (5 buscas, PT-BR) | só o perfil biográfico: especialista em conteúdo e crescimento orgânico sem tráfego pago, começou no YouTube aos 12 anos morando na Coreia do Sul, recomeçou do zero no Instagram em 2021, tem material tipo "50 ganchos virais", passou no Bianchi Podcast (EP15, abr/2026) |
| Google Drive do escritório (`Cureau`) | zero arquivos |

Ou seja: **o método dela não está indexado em texto em lugar nenhum.** Ele vive dentro dos vídeos
do Instagram — que é exatamente onde eu não chego daqui.

Isso não é um detalhe contornável. Se eu preencher esta base "no espírito dela", eu produzo
exatamente o problema que o repositório existe para matar: justificativa que soa embasada e não é.
Um princípio atribuído a ela sem fonte é pior do que princípio nenhum, porque ninguém vai auditar
depois.

**Regra dura: nada entra nesta pasta sem fonte verificável (vídeo + data).**

## O que eu preciso de vocês

A lista de vídeos já existe (30 links únicos, varredura de ~830 posts do perfil). Ela está
em `materia-prima/urls.txt`, deduplicada e ordenada por prioridade.

**O que falta é transcrever.** Dois caminhos, mesmo resultado:

- **Sem terminal, clicando** → `materia-prima/COMECE-AQUI.md` (8 vídeos, ~40 min)
- **Automático, para quem é técnico** → `materia-prima/COMO-RODAR.md` (30 vídeos, ~10 min)

A versão automática, em resumo:

1. `./1-baixar.sh` — yt-dlp com o cookie do navegador, baixa os reels e guarda a data de cada post
2. `python3 2-transcrever.py` — Gemini assiste ao vídeo e devolve fala + texto na tela +
   o que acontece na imagem + as regras que ela enuncia
3. as transcrições voltam para `materia-prima/transcricoes/` (ou Drive, ou coladas no chat)

Comece pelos **8 do Tier 1** — cobrem os cinco temas e destravam a base. Não espere os 30.

O download não sai daqui: o Instagram está bloqueado na rede deste ambiente (403 no proxy),
e o HuggingFace e o CDN da OpenAI também, então nem Whisper local eu consigo rodar.
Detalhes e alternativas em `COMO-RODAR.md`.

## O que eu faço quando a matéria-prima chegar

Cada vídeo dela vira um ou mais princípios neste formato fixo:

```markdown
### CUR-014 — Gancho não pode entregar a resposta
**Enunciado:** [regra em uma frase, do jeito que dá pra aplicar]
**Racional dela:** [por que ela diz que funciona]
**Fonte:** Reel @lucureau, 12/06/2026 — "título que mata o vídeo"
**Capturado em:** 20/08/2026
**Aplica-se a:** gancho
**Confiança:** ⬜ não testado no perfil · 🟡 1 teste · 🟢 confirmado · 🔴 derrubado
**Tradução para o @isaacbertolini:** [como isso muda num perfil jurídico falando com pares]
```

O campo **"Tradução para o @isaacbertolini"** é obrigatório e é a parte que exige cabeça, não
transcrição. O público dela é de criadores e experts digitais; o do Isaac é de advogados,
empresários e profissionais liberais de 25 a 45 anos, falando **para pares** — não para trabalhador
buscando defesa. Princípio bom no perfil dela pode ter tom errado no dele. Onde a tradução mudar a
regra, isso fica escrito.

## Índice de princípios

*(vazio — preencher)*

| ID | Enunciado | Aplica-se a | Confiança |
|---|---|---|---|
| — | — | — | — |
