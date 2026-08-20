# Arquitetura do Método Isaac

## Por que "justificar" é um problema de sistema, não de talento

Um roteiro tem 4 decisões que hoje ficam sem defesa. Cada uma delas responde a uma pergunta
diferente, e é por isso que "escrever melhor" não resolve — são quatro perguntas separadas:

| Decisão | Pergunta que ninguém consegue responder hoje | O que a decisão realmente controla |
|---|---|---|
| **Título / gancho** | por que ESSA primeira frase? | quem para de rolar nos 3 primeiros segundos |
| **Enredo / estrutura** | por que a informação vem NESSA ordem? | quantos ficam até o fim |
| **Trechos / cortes** | por que esse pedaço entrou e aquele saiu? | onde a retenção cai no meio |
| **CTA** | por que pedir ISSO e não outra coisa? | qual sinal o algoritmo recebe no fim |

Repare que cada decisão tem uma **métrica-dona** diferente. Isso não é detalhe: é o motivo de
"o vídeo foi mal" ser uma frase inútil. Um vídeo com gancho ruim e um vídeo com CTA ruim falham
de formas diferentes, aparecem diferente no insight, e se consertam diferente.

## As 4 camadas

### Camada 1 — Base de princípios (`base-cureau/`)
O corpo de regras que dá autoridade externa às escolhas. A fonte escolhida foi a **Luíza Cureau
(@lucureau)**, por dois motivos declarados pela equipe: ela ensina construção de vídeo e
posicionamento de forma sistemática, e acompanha mudança de algoritmo em tempo real.

Cada princípio na base tem obrigatoriamente: **enunciado + fonte (vídeo/post/data) + data de
captura**. Princípio sem data apodrece sem avisar — e essa é justamente a falha que a equipe quer
evitar, já que o algoritmo muda.

### Camada 2 — Ficha de justificativa (`metodo/02-ficha-de-justificativa.md`)
Anexo obrigatório de todo roteiro. Uma linha por decisão: o que foi escolhido, qual princípio
sustenta, qual a fonte, qual métrica deve provar, e qual foi a alternativa descartada.

A coluna "alternativa descartada" é a que mais dói e a mais importante: só existe justificativa
onde existiu escolha. Se não havia outra opção na mesa, não houve decisão — houve reflexo.

### Camada 3 — Protocolo de captura (`metodo/03-protocolo-de-captura.md`)
Como a base se alimenta e se atualiza. Um método baseado em "o algoritmo muda o tempo todo"
precisa de rotina de reabastecimento, ou vira dogma de 2024 aplicado em 2026.

### Camada 4 — Loop de validação (`metodo/04-loop-de-validacao.md`)
O que transforma isso em método e não em teoria bonita: depois de publicado, o número real
confirma ou derruba a justificativa. Princípio derrubado três vezes sai da base.

## O fluxo, do começo ao fim

```
tema  →  escolhe princípios na base  →  escreve o roteiro
                                              ↓
                                     preenche a ficha
                                     (decisão → princípio → fonte → métrica prevista)
                                              ↓
                                          publica
                                              ↓
                                  confere métrica real (7 dias)
                                              ↓
                       princípio confirmado ────→ sobe de confiança na base
                       princípio derrubado  ────→ marca 1 falha; 3 falhas = sai da base
```

## O que este método NÃO é

- **A estrutura de roteiro deste perfil é a de 9 batidas** (`metodo/01-o-metodo.md`), derivada do
  método da Luíza Cureau. A fórmula GRAVA, usada antes, foi substituída — não convivem duas
  estruturas concorrentes, porque aí ninguém sabe qual defender quando perguntam o porquê.
- Não é cópia do conteúdo da Cureau. É a extração dos **princípios** que ela ensina, aplicados a um
  perfil jurídico/empresarial com público e restrições próprias.
- Não substitui dado próprio. Onde houver número real do @isaacbertolini, o número real ganha do
  princípio externo — sempre. Autoridade externa serve para decidir onde ainda não há dado.
