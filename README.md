# Método de Roteiro — perfil @isaacbertolini

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

Isso é o que separa embasamento de achismo bem escrito. Um roteiro pode ir ao ar com uma decisão
marcada como hipótese; o que não pode é a hipótese se disfarçar de certeza.

## Arquitetura (4 camadas)

| Camada | Arquivo | O que responde |
|---|---|---|
| 1. Base de princípios | `base-cureau/` | *De onde vem a regra?* — o método da Luíza Cureau, extraído e datado |
| 2. Ficha de justificativa | `metodo/02-ficha-de-justificativa.md` | *Por que cada elemento deste roteiro é assim?* |
| 3. Protocolo de captura | `metodo/03-protocolo-de-captura.md` | *Como a base se mantém atualizada quando o algoritmo muda?* |
| 4. Loop de validação | `metodo/04-loop-de-validacao.md` | *A justificativa se confirmou no número real?* |

Comece por `metodo/00-arquitetura.md`.

## Status atual

- [x] Arquitetura das 4 camadas definida
- [x] Ficha de justificativa (template obrigatório) pronta
- [x] Protocolo de captura definido
- [x] Loop de validação definido
- [x] Engenharia reversa das referências que já estavam no Drive (`analises/`)
- [x] **Base Cureau preenchida** — 22 vídeos transcritos, 29 princípios em `base-cureau/principios.md`
- [x] **Auditoria das fontes** — `base-cureau/auditoria-das-fontes.md`
- [ ] Ficha de justificativa reescrita com os princípios reais no lugar dos `[PROVISÓRIO]`
- [ ] Ficha rodada num roteiro real do Isaac

Enquanto a camada 1 não estiver preenchida, as fichas rodam com princípios provisórios
(marcados como `[PROVISÓRIO]`) vindos do acervo próprio e de dados reais do perfil.
