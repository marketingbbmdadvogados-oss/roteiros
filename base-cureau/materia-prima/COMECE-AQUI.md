# Como pegar as aulas da Luíza Cureau — versão sem terminal

Este guia é para fazer tudo pelo navegador, clicando. Não precisa instalar nada,
não precisa digitar comando nenhum, não precisa saber programar.

Tempo: cerca de **40 minutos**, quase tudo esperando upload.

---

## O que você vai fazer, em uma frase

Baixar 8 vídeos dela do Instagram → subir esses vídeos num site do Google que
assiste ao vídeo e escreve tudo → mandar esse texto para o Claude.

---

## Por que 8 e não os 30

A lista tem 30 vídeos. Não precisa de todos para começar.
Estes 8 já cobrem os cinco assuntos que interessam (gancho, estrutura, retenção,
CTA e algoritmo). Os outros 22 entram depois, sem pressa.

**Os 8 para começar:**

| # | Link | O que ele ensina |
|---|---|---|
| 1 | https://www.instagram.com/lucureau/reel/DbI9QcxgcUm/ | **O mais importante.** Como ler o gráfico de retenção: se o povo sai no começo o problema é o gancho, se sai no meio é o conteúdo, se sai no fim é o CTA |
| 2 | https://www.instagram.com/lucureau/reel/DW2Pp_tgFsO/ | Os 4 tipos de gancho (o do hambúrguer) e onde entra o CTA |
| 3 | https://www.instagram.com/lucureau/reel/DbCV7PxgZT4/ | A estrutura completa de um vídeo viral, do início ao fim |
| 4 | https://www.instagram.com/lucureau/reel/DbOMz_RgGdj/ | Como ela escreve um roteiro na prática |
| 5 | https://www.instagram.com/lucureau/reel/DP4APHagIqk/ | O que faz alguém virar seguidor depois de ver o vídeo |
| 6 | https://www.instagram.com/lucureau/reel/DTL_sqsAHbi/ | O passo a passo dela para criar conteúdo em 2026 |
| 7 | https://www.instagram.com/lucureau/reel/DPH3pNygOxW/ | Quais métricas o algoritmo realmente valoriza |
| 8 | https://www.instagram.com/lucureau/reel/DUZI63ngIuo/ | O mesmo gancho falado de 4 jeitos: como a entonação muda o resultado |

Se você só tiver ânimo para três, faça o **1, o 2 e o 3**.

---

## PASSO 1 — Baixar os vídeos (uns 10 minutos)

O Instagram não tem botão de baixar vídeo dos outros. Então use um site que faz isso.

1. Abra `https://snapinsta.app` (ou `https://igram.world` — servem para a mesma coisa).
2. Copie o link do vídeo 1 da tabela acima.
3. Cole no campo do site e clique em **Download**.
4. Salve o arquivo numa pasta do seu computador. Sugestão: crie uma pasta na Área de
   Trabalho chamada **`videos-luiza`** e salve tudo lá.
5. Repita para os 8.

**Renomeie cada arquivo** com o código que aparece no final do link, para não se perder.
Exemplo: o vídeo 1 vira `DbI9QcxgcUm.mp4`.

> ⚠️ Esses sites de download são cheios de propaganda e de botões falsos escritos
> "Download" que abrem outra coisa. Não instale nada que eles ofereçam, não clique em
> "permitir notificações". Só baixe o arquivo de vídeo. Se um site estiver muito ruim,
> tente o outro.

> 💡 **Atalho:** quem fez a varredura do perfil dela (aquela lista de 830 posts) já tem
> ferramenta que baixa em lote. Se essa pessoa estiver por perto, peça os 8 arquivos
> direto para ela e pule este passo inteiro.

---

## PASSO 2 — Anotar a data de cada vídeo (2 minutos)

Isso parece burocracia, mas é o que impede o método de apodrecer: quando o Instagram
mudar o algoritmo, a gente precisa saber qual regra é velha demais para confiar.

Abra cada um dos 8 links no Instagram e anote a data que aparece no post.
Faz uma listinha simples num bloco de notas:

```
DbI9QcxgcUm — 14/01/2026
DW2Pp_tgFsO — 02/12/2025
...
```

---

## PASSO 3 — Transcrever com o Google (uns 20 minutos)

Aqui é onde a inteligência artificial assiste ao vídeo e escreve tudo o que ela fala,
tudo o que está escrito na tela e o que ela demonstra na imagem.

1. Abra **https://aistudio.google.com** e entre com sua conta Google. É gratuito.
2. Clique em **"Create Prompt"** (ou "Novo prompt").
3. Clique no ícone de **+** ou de clipe de papel e escolha **Upload File**. Suba o
   primeiro vídeo.
4. Espere aparecer que o arquivo terminou de processar (alguns segundos).
5. **Cole o texto abaixo** na caixa de mensagem e aperte Enter:

```
Você está analisando um vídeo curto da criadora Luíza Cureau, que ensina método
de criação de conteúdo. Extraia tudo o que ela ensina, incluindo o que está na
imagem — não só o áudio. Responda em português do Brasil, neste formato:

## Transcrição da fala
[tudo o que ela fala, do começo ao fim, sem resumir]

## Texto na tela
[todo texto escrito que aparece no vídeo, na ordem: capa, legendas, setas,
anotações, prints. Se houver gráfico ou print do Instagram, descreva os números
e rótulos que dá para ler]

## O que acontece na imagem
[só o que faz parte da lição: o que ela demonstra, mostra, aponta, ou faz com a
voz e o corpo. Se o vídeo demonstra uma técnica visualmente, descreva em detalhe]

## Regras que ela enuncia
[liste cada regra prática que ela dá, com o motivo que ELA deu. Formato:
"- REGRA — porque [motivo dela]". Se ela não deu motivo, escreva
"- REGRA — (sem motivo declarado)". Não invente motivo que ela não falou]

## Tema principal
[escolha: gancho, estrutura, retenção, CTA, algoritmo]
```

6. Copie a resposta que ele der e cole num documento.
7. Clique em **"New chat"** (conversa nova) e repita para o próximo vídeo.
   Uma conversa nova por vídeo — não empilhe os 8 na mesma.

---

## PASSO 4 — Me mandar

Escolha o que for mais fácil para você:

- **Colar direto no chat com o Claude.** Um vídeo por mensagem, com a data junto.
- **Ou** jogar tudo num Documento do Google Drive chamado `CUREAU — transcrições`
  (o Claude lê o seu Drive) e avisar que está lá.

Não precisa organizar nem formatar. Pode colar bruto, do jeito que o Google cuspiu.
Eu organizo daqui.

---

## E se você preferir que alguém técnico faça

Se tiver alguém de TI ou um dev por perto, existe a versão automática que faz os
30 vídeos sozinha, em uns 10 minutos: está em `COMO-RODAR.md`, nesta mesma pasta,
com os scripts prontos (`1-baixar.py` e `2-transcrever.py`). Aí é só entregar a
pasta para a pessoa.
