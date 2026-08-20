# Trabalhando em equipe com o OneDrive

## Primeiro, o aviso que importa

**Não coloque a pasta do repositório dentro do OneDrive.**

O Git guarda todo o histórico numa pasta escondida chamada `.git`, com milhares de
arquivinhos que ele reescreve o tempo todo. O OneDrive tenta sincronizar isso enquanto o
Git escreve, e com duas pessoas mexendo ao mesmo tempo o resultado é repositório corrompido
e trabalho perdido. Não é raro nem teórico — é o modo clássico de quebrar um repo.

Então a regra é: **repositório fora do OneDrive, arquivos pesados dentro.**

---

## A divisão que funciona

Cada coisa no lugar em que ela é boa:

| O quê | Onde | Por quê |
|---|---|---|
| Scripts, método, fichas | **GitHub** (pasta local fora do OneDrive) | versionado, histórico, sem conflito de sync |
| **Transcrições** (`.md`) | **GitHub** | é o entregável; texto versiona bem e eu leio direto do repo |
| **Vídeos** (`.mp4`) | **OneDrive** | arquivo grande e binário — não deve entrar no Git, e o time inteiro precisa ver |

Quem é da equipe e **não é dev** não precisa instalar nada: o GitHub abre no navegador e o
conteúdo é tudo texto. `github.com/marketingbbmdadvogados-oss/roteiros` → trocar para a
branch `claude/roteiros-metodo-perfil-4jcnhh` → ler ali mesmo.

---

## Como apontar os scripts para o OneDrive

Os scripts agora leem o caminho das pastas de fora. Duas formas:

### Forma 1 — arquivo `caminhos.txt` (recomendada)

Crie um arquivo chamado `caminhos.txt` dentro de `base-cureau\materia-prima`:

```
DIR_VIDEOS=C:\Users\seu-usuario\OneDrive\Marketing\Luiza\videos
```

Pronto. Todos os scripts passam a usar essa pasta. O `caminhos.txt` fica **fora do Git**,
então cada pessoa da equipe pode ter o caminho da própria máquina sem atrapalhar as outras
— o que importa, porque o `C:\Users\...` de cada um é diferente.

Confira se pegou:

```
python 0-conferir.py
```

As duas primeiras linhas mostram as pastas que ele está usando.

### Forma 2 — variável de ambiente

Se preferir não criar arquivo:

```
$env:DIR_VIDEOS="C:\Users\seu-usuario\OneDrive\Marketing\Luiza\videos"    # PowerShell
set DIR_VIDEOS=C:\Users\seu-usuario\OneDrive\Marketing\Luiza\videos       # CMD
```

Vale só no terminal aberto, igual à chave do Gemini.

> As duas variáveis disponíveis são `DIR_VIDEOS` e `DIR_TRANSCRICOES`. Se você definir
> só a primeira, as transcrições continuam indo pra dentro do repositório — que é
> exatamente o que a gente quer.

---

## Montando na prática

**1. Crie a pasta compartilhada no OneDrive**

```
OneDrive\Marketing\Luiza\videos
```

Compartilhe com a equipe pelo próprio OneDrive (botão direito → Compartilhar).

**2. Clone o repositório FORA do OneDrive**

```
mkdir C:\projetos
cd C:\projetos
git clone https://github.com/marketingbbmdadvogados-oss/roteiros.git
cd roteiros
git checkout claude/roteiros-metodo-perfil-4jcnhh
```

Repare: `C:\projetos`, não `C:\Users\...\OneDrive\...`.

**3. Aponte os vídeos para o OneDrive**

Crie o `caminhos.txt` como acima.

**4. Mova os vídeos que você já baixou para lá**

Arrastando no Explorer mesmo.

**5. Confira**

```
cd base-cureau\materia-prima
python 0-conferir.py
```

Daí em diante é o fluxo normal: `python 1-baixar.py`, `python 2-transcrever.py`.

---

## Uma pegadinha do OneDrive: "Arquivos Sob Demanda"

Por padrão o OneDrive deixa os arquivos só na nuvem e baixa quando alguém abre. Os scripts
podem falhar com erro estranho de leitura por causa disso.

Se acontecer: clique com o botão direito na pasta `videos` → **"Sempre manter neste
dispositivo"**. Aí o Windows garante que os arquivos estão de verdade no disco.

---

## Se a equipe inteira preferir só OneDrive

Dá pra fazer, mas você perde o histórico e o controle de versão. Se for o caso, o desenho
muda para:

- o repositório continua sendo o lugar onde o trabalho acontece (fora do OneDrive);
- e você **copia** as transcrições e o método prontos para uma pasta do OneDrive, como
  entrega, quando fecha uma etapa.

Copiar de vez em quando é seguro. Trabalhar direto dentro do OneDrive com Git junto, não.
