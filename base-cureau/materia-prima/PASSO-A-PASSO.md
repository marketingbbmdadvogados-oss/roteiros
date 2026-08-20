# Passo a passo — do vídeo baixado à transcrição

> 🪟 **No Windows? Abra o `WINDOWS.md`** nesta mesma pasta — tem os comandos certos
> (`git clone`, `set`/`$env:`, barra invertida) e onde rodar. Este arquivo aqui usa
> sintaxe de Mac/Linux.

Situação de partida: os lotes 1 e 2 já estão baixados na sua máquina, os lotes 3 a 5 não.
Você já tem a API key do Gemini.

Tudo abaixo roda dentro de `base-cureau/materia-prima/`.

---

## Preparo (uma vez)

```bash
git pull
cd base-cureau/materia-prima
pip install -r requirements.txt
export GEMINI_API_KEY="sua-chave-aqui"
```

Coloque os vídeos que você já baixou numa pasta chamada **`videos/`** aqui dentro:

```bash
mkdir -p videos
mv ~/Downloads/*.mp4 videos/      # ajuste o caminho de onde você salvou
```

---

## Parte 1 — Os vídeos que você JÁ baixou

### 1.1 Ver a situação

```bash
python3 0-conferir.py
```

Ele lista os 25 vídeos por lote e marca cada um: `✅ transcrito`, `📥 baixado, falta
transcrever` ou `⬜ falta baixar`. E avisa se tem arquivo com nome que ele não reconhece.

### 1.2 Se aparecer "arquivos com nome que eu não reconheço"

Acontece quando você baixou por site (o arquivo vem tipo `snapinsta_8823.mp4`). O script
identifica cada vídeo pelo **nome do arquivo**, que precisa ser o código do reel
(`DbI9QcxgcUm.mp4`). Se você baixou com o `1-baixar.py` (yt-dlp), já veio certo — pule esta parte.

```bash
python3 0-renomear.py
```

Isso **não renomeia nada ainda**. Ele gera um arquivo `renomear.txt` propondo o mapa,
assumindo que você baixou na ordem da checklist (mais antigo primeiro):

```
snapinsta_8823.mp4 -> DbI9QcxgcUm   # Gráfico de retenção: saída no começo=gancho...
snapinsta_8824.mp4 -> DW2Pp_tgFsO   # Os 4 tipos de gancho (o do hambúrguer)...
```

**Abra o `renomear.txt` e confira.** Se alguma linha estiver trocada, corrija o código ali
mesmo. Se quiser pular um arquivo, apague a linha. Aí:

```bash
python3 0-renomear.py --aplicar
python3 0-conferir.py        # confirma que ficou tudo certo
```

### 1.3 Transcrever

```bash
python3 2-transcrever.py
```

Roda 3 em paralelo. Os 15 vídeos dos lotes 1 e 2 saem em uns 4–6 minutos.
Resultado: um `.md` por vídeo em `transcricoes/`.

Quer mais rápido e sua cota aguentar: `WORKERS=5 python3 2-transcrever.py`.

Pode interromper com Ctrl+C e rodar de novo — ele pula o que já está pronto.

---

## Parte 2 — Os vídeos que ainda FALTAM

### 2.1 Gerar a lista do que falta

```bash
python3 0-conferir.py --faltantes
```

Grava `faltantes.txt` com os links exatos que ainda não estão em `videos/`.

### 2.2 Baixar

```bash
python 1-baixar.py faltantes.txt
```

Precisa estar logado no Instagram no navegador — o yt-dlp reaproveita o cookie.
Se você usa outro navegador: `python 1-baixar.py --navegador firefox faltantes.txt`.

Vantagem: o yt-dlp já salva com o nome certo e guarda a data do post no `.info.json`,
então **não precisa renomear nem anotar data à mão**.

Se der erro de autenticação, atualize primeiro (`pip install -U yt-dlp`) — versão velha é a
causa mais comum. O plano B com `cookies.txt` está no `COMO-RODAR.md`.

### 2.3 Transcrever o resto

```bash
python3 2-transcrever.py
```

Mesmo comando. Ele pula os que já foram e faz só os novos.

---

## Parte 3 — Me mandar

Confira que está tudo lá:

```bash
python3 0-conferir.py
ls transcricoes/ | wc -l
```

Aí commite:

```bash
git add transcricoes/
git commit -m "Transcricoes dos videos da @lucureau"
git push
```

Me avise que subiu. Eu leio direto do repositório e começo a transformar em princípios
numerados, com fonte, data e a tradução para o perfil do Isaac.

**Não precisa esperar os 25.** Assim que os lotes 1 e 2 estiverem transcritos, sobe e me
avisa — eu trabalho neles enquanto você baixa o resto.

---

## Sobre a data dos posts

Os vídeos baixados pelo yt-dlp trazem a data automaticamente. Os que você baixou por site,
não — vão sair com `Data do post: DESCONHECIDA`.

Não é bloqueante, mas a data importa mais nos **5 vídeos do lote 4 (algoritmo)**: são os que
envelhecem rápido, e sem data eu não sei daqui a seis meses se ainda dá pra confiar na regra.
Esses vão ser baixados pelo yt-dlp de qualquer forma, então já vêm resolvidos.

Se quiser preencher os dos lotes 1 e 2 à mão, é só abrir o link e editar a linha
`- **Data do post:**` no topo de cada `.md`.

---

## Resumo dos comandos

| Comando | O que faz |
|---|---|
| `python3 0-conferir.py` | mostra o que está baixado, transcrito e faltando |
| `python3 0-conferir.py --faltantes` | + grava `faltantes.txt` |
| `python3 0-renomear.py` | propõe mapa de renomeação (não aplica) |
| `python3 0-renomear.py --aplicar` | aplica o mapa do `renomear.txt` |
| `python 1-baixar.py faltantes.txt` | baixa os que faltam, com nome e data corretos |
| `python3 2-transcrever.py` | transcreve tudo que ainda não tem `.md` |
