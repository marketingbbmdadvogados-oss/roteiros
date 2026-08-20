# Método Isaac

Método de roteiro de vídeo curto do perfil **@isaacbertolini**.

Repositório do **método justificável** de roteiro de vídeo curto.

## O problema que este repositório resolve

Hoje os roteiros são escritos por instinto e por imitação de referências. Quando alguém pergunta
*"por que esse título?"*, *"por que esse enredo?"*, *"por que esse trecho e não outro?"*,
*"por que esse CTA?"* — não existe resposta escrita. Só opinião.

O objetivo aqui **não é escrever roteiros melhores por acaso**. É tornar cada decisão de roteiro
**rastreável**: toda escolha aponta para um princípio, todo princípio aponta para uma fonte, e toda
fonte é depois confrontada com o número real do post.

Regra central do repositório:

> **Nenhuma justificativa sem fonte nomeada. "Ainda não sei" é uma resposta válida — e visível.**

E uma regra de fronteira: **o método só aceita regra que saia do acervo da Luíza Cureau ou de
número real do perfil.** Prática boa sem lastro vai para `analises/praticas-do-time.md` e espera
corroboração ou teste. É isso que impede o método de virar colcha de retalhos de opinião.

Isso é o que separa embasamento de achismo bem escrito. Um roteiro pode ir ao ar com uma decisão
marcada como hipótese; o que não pode é a hipótese se disfarçar de certeza.

## Arquitetura (4 camadas)

| Camada | Arquivo | O que responde |
|---|---|---|
| **0. O Método Isaac** | **`metodo/01-o-metodo.md`** | ***Como se escreve um roteiro deste perfil?*** — comece aqui |
| 0b. O modelo | `metodo/05-modelo-de-roteiro.md` | *Onde eu escrevo?* — formulário para copiar e preencher |
| 1. Base de princípios | `base-cureau/` | *De onde vem a regra?* — o método da Luíza Cureau, extraído e datado |
| 2. Ficha de justificativa | `metodo/02-ficha-de-justificativa.md` | *Por que cada elemento deste roteiro é assim?* |
| 3. Protocolo de captura | `metodo/03-protocolo-de-captura.md` | *Como a base se mantém atualizada quando o algoritmo muda?* |
| 4. Loop de validação | `metodo/04-loop-de-validacao.md` | *A justificativa se confirmou no número real?* |

**Comece por `metodo/01-o-metodo.md`** — é o documento operacional: quem for escrever um roteiro
segue ele do começo ao fim e não precisa de mais nada aberto. As outras camadas são o que
sustenta, audita e valida o que está escrito lá.

A arquitetura de como isso foi montado está em `metodo/00-arquitetura.md`.

## Status atual

- [x] Arquitetura das 4 camadas definida
- [x] Ficha de justificativa (template obrigatório) pronta
- [x] Protocolo de captura definido
- [x] Loop de validação definido
- [x] Engenharia reversa das referências que já estavam no Drive (`analises/`)
- [x] **Base Cureau preenchida** — 23 vídeos, 35 princípios em `base-cureau/principios.md`
- [x] **Auditoria das fontes** — `base-cureau/auditoria-das-fontes.md`
- [x] **Ficha de justificativa v2** — princípios reais no lugar dos `[PROVISÓRIO]`
- [x] **O método escrito** — `metodo/01-o-metodo.md`, operacional, 9 batidas, todas as regras com fonte
- [x] Ficha rodada num roteiro real (`analises/fichas/001-golpe…`, com PDF para envio)
- [ ] **Primeiro ciclo de validação fechado** — nenhum roteiro publicado ainda seguindo o método

As fichas já rodam com princípios reais. Cada decisão de roteiro aponta para um `CUR-xxx` com
fonte, e **carrega o nível de confiança do princípio** — uma decisão sustentada por 🟢 e uma
sustentada por 🔴 não são igualmente defensáveis, e a ficha mostra a diferença.
