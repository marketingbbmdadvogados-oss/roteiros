# Passo a passo no Windows

Use o **terminal do VS Code** (`Ctrl` + `'`, ou menu *Terminal → New Terminal*).
Serve tanto PowerShell quanto CMD — os comandos abaixo funcionam nos dois.

Não use o CMD solto do Windows: no VS Code você vê os arquivos do lado enquanto roda,
e é bem mais fácil de acompanhar.

---

## PASSO 1 — Trazer o repositório para a sua máquina

O `git pull` só funciona depois que o projeto já existe no seu computador. Como é a
primeira vez, o comando é `git clone`.

Escolha onde quer guardar (o exemplo usa `C:\projetos`):

```
mkdir C:\projetos
cd C:\projetos
git clone https://github.com/marketingbbmdadvogados-oss/roteiros.git
cd roteiros
git checkout claude/roteiros-metodo-perfil-4jcnhh
```

Aquele `git checkout` é importante: todo o material está nessa branch, não na principal.

Depois, no VS Code: *File → Open Folder* → `C:\projetos\roteiros`.

> Das próximas vezes, aí sim: `git pull` para trazer o que eu subir de novo.

---

## PASSO 2 — Entrar na pasta e instalar

```
cd base-cureau\materia-prima
pip install -r requirements.txt
```

Repare na **barra invertida** `\` — é assim no Windows.

Se `pip` não for reconhecido, tente `py -m pip install -r requirements.txt`.

---

## PASSO 3 — A chave do Gemini

O comando muda conforme o terminal:

**PowerShell** (é o padrão do VS Code — o prompt começa com `PS`):
```
$env:GEMINI_API_KEY="cole-sua-chave-aqui"
```

**CMD** (o prompt é tipo `C:\projetos\roteiros>`):
```
set GEMINI_API_KEY=cole-sua-chave-aqui
```

⚠️ Isso vale só **enquanto aquele terminal estiver aberto**. Se você fechar e abrir outro,
precisa rodar de novo. Se der erro de "falta GEMINI_API_KEY", é quase sempre isso.

---

> 👥 **Vai compartilhar com o time pelo OneDrive?** Leia o `ONEDRIVE.md` antes deste
> passo — tem um cuidado importante sobre onde o repositório NÃO pode ficar.

## PASSO 4 — Colocar os vídeos que você já baixou

Crie a pasta `videos` dentro de `base-cureau\materia-prima` e mova os arquivos dos lotes
1 e 2 para lá. Pode fazer arrastando no Explorer do Windows mesmo, ou:

```
mkdir videos
move %USERPROFILE%\Downloads\*.mp4 videos\
```

(No PowerShell: `move $env:USERPROFILE\Downloads\*.mp4 videos\`)

---

## PASSO 5 — Ver a situação

```
python 0-conferir.py
```

No Windows o comando é `python`, não `python3`. Se não funcionar, tente `py 0-conferir.py`.

Ele mostra os 25 vídeos por lote, marcando o que está baixado, transcrito e faltando.

---

## PASSO 6 — Transcrever, mesmo com os nomes errados

Antes de gastar API, dá pra ver exatamente o que ele vai fazer:

```
python 2-transcrever.py --listar
```

Isso não envia nada. Só mostra duas listas: o que já está transcrito (será pulado) e o que
será transcrito agora. Use sempre que adicionar um lote novo de vídeos.

**Não precisa renomear antes.** Se você baixou por site, os arquivos vieram com nome tipo
`snapinsta_8823.mp4` — tudo bem. O script transcreve qualquer nome.

```
python 2-transcrever.py
```

Os 15 vídeos dos lotes 1 e 2 saem em uns 4–6 minutos. As transcrições aparecem na pasta
`transcricoes`. Pode parar com `Ctrl+C` e rodar de novo — ele pula o que já ficou pronto.

Junto da transcrição, o Gemini também **identifica qual vídeo é aquele**, comparando o
conteúdo com a lista dos 25 que a gente conhece. É isso que resolve o problema do nome.

---

> **Se aparecer erro 404 dizendo que o modelo não está disponível:** o Google aposenta
> modelo de tempos em tempos. O script agora avisa logo no começo e lista os que a sua
> chave alcança. Escolha um da lista e rode assim:
>
> ```
> $env:GEMINI_MODEL="nome-do-modelo"
> python 2-transcrever.py
> ```

---

## PASSO 7 — Arrumar os nomes automaticamente

```
python 3-organizar.py
```

Ele lê a identificação de cada transcrição e mostra o que pretende renomear — **sem mudar
nada ainda**. Confira a lista. Se estiver certa:

```
python 3-organizar.py --aplicar
python 0-conferir.py
```

Isso renomeia o vídeo e a transcrição para o código certo e corrige o link da fonte
dentro do arquivo.

O que ele identificar com **confiança baixa** não é renomeado sozinho — fica listado pra
você resolver à mão com o `0-renomear.py`. É de propósito: chute errado aqui contamina a
base inteira depois.

> **Uma coisa que o download por site não traz: a data do post.** Depois de organizar, abra
> os links (o `0-conferir.py` lista todos) e anote as datas. Nos 5 vídeos sobre algoritmo
> isso é essencial — são os que envelhecem rápido.

---

## PASSO 8 — Baixar o resto

Antes: abra o Instagram no navegador e confirme que **está logado**.

```
python 1-baixar.py
```

Ele descobre sozinho o que falta e baixa, já com o nome certo e a data do post.

Se você não usa Chrome: `python 1-baixar.py --navegador firefox` (ou `edge`, `brave`).

Deu erro de autenticação? Nesta ordem:
1. `pip install -U yt-dlp` (versão velha é a causa mais comum)
2. confirme o login no navegador
3. tente com `--navegador` do que você realmente usa
4. último recurso: instale a extensão "Get cookies.txt", exporte o arquivo e rode
   `python 1-baixar.py --cookies cookies.txt`

Depois:

```
python 2-transcrever.py
```

---

## PASSO 9 — Me mandar

```
git add transcricoes
git commit -m "Transcricoes dos videos da @lucureau"
git push
```

Se o `git push` pedir usuário e senha, use seu usuário do GitHub e um **token** no lugar da
senha (GitHub → Settings → Developer settings → Personal access tokens).

Me avise que subiu.

---

## Cola rápida

| O que fazer | Comando |
|---|---|
| ver a situação | `python 0-conferir.py` |
| ver o que será transcrito, sem enviar | `python 2-transcrever.py --listar` |
| arrumar nomes depois de transcrever | `python 3-organizar.py` → confere → `--aplicar` |
| renomear à mão (casos duvidosos) | `python 0-renomear.py` → confere → `--aplicar` |
| baixar o que falta | `python 1-baixar.py` |
| transcrever | `python 2-transcrever.py` |
| mandar pra mim | `git add transcricoes` → `git commit -m "..."` → `git push` |

Roda na ordem. Todos são seguros de repetir: nenhum refaz trabalho já feito.
