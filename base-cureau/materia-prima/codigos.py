"""Fonte única de verdade dos vídeos da @lucureau: código, lote e o que ensina.

30 links levantados → 5 são repost de outros → 25 distintos.
Destes, 24 são os que valem transcrever (lotes 1 a 4) e 1 é chamariz curto (opcional).
"""

PRINCIPAIS = [
    # (código, lote, o que ensina)
    ("DbI9QcxgcUm", 1, "Gráfico de retenção: saída no começo=gancho, meio=conteúdo, fim=CTA"),
    ("DW2Pp_tgFsO", 1, "Os 4 tipos de gancho (o do hambúrguer) + onde entra o CTA"),
    ("DbCV7PxgZT4", 1, "Estrutura completa de um vídeo viral"),
    ("DbOMz_RgGdj", 1, "Como ela escreve um roteiro na prática"),
    ("DP4APHagIqk", 1, "O que faz alguém virar seguidor depois de ver o vídeo"),
    ("DTL_sqsAHbi", 1, "Passo a passo de criar conteúdo em 2026"),
    ("DPH3pNygOxW", 1, "Quais métricas o algoritmo valoriza"),
    ("DUZI63ngIuo", 1, "Mesmo gancho, 4 entonações"),
    ("DatVkudAUYR", 2, "Estrutura de roteiro + lista de ganchos virais"),
    ("DaY7azbgieD", 2, "8 formatos de conteúdo + ganchos"),
    ("DZ8mDS3gGYp", 2, "Análise da estrutura do @thekumarmethod"),
    ("DLupBqrsd-z", 2, "Seu primeiro vídeo não vai viralizar: como diagnosticar o erro"),
    ("Db9aIvrgAMY", 2, "Passo a passo de carrossel viral"),
    ("DOXJDffjASd", 2, "Planejamento de uma semana de conteúdo"),
    ("DcJY3KwAoZE", 2, "Estrutura replicável para milhões de views"),
    ("Db6AOo5g6l0", 3, "5 formas de deixar o vídeo dinâmico"),
    ("Da1RVdLAc3H", 3, "Cortes simples que seguram a atenção"),
    ("DbBPFeXAlZ2", 3, "Melhores formas de gravar / mudar cenário"),
    ("Da20LYvgl8I", 3, "Comunicação não verbal desalinhada derruba retenção"),
    ("DZ_ITwJgNX6", 4, "Função nova do Instagram; compara algoritmos"),
    ("DYYNqlHA_yE", 4, 'Atualização "Instants" e o que sinaliza'),
    ("DLnwTEdP9zs", 4, "Construir confiança com o algoritmo via frequência"),
    ("DKxu7K_PTaA", 4, "Checklist de como não irritar o algoritmo"),
    ("DKgD25mtage", 4, "Atualização para menores de 18"),
]

OPCIONAIS = [
    ("DbRoKmfgAyN", 5, "Chamariz da lista de +50 ganchos (curto, baixo valor)"),
]

# Reposts: mesmo conteúdo de outro vídeo. Não transcrever.
REPOSTS = {
    "DYn0GF9MyDf": "DcJY3KwAoZE",
    "DXp53zLDP0K": "DcJY3KwAoZE",
    "DWsQV8rjGyL": "DcJY3KwAoZE",
    "DanfRcVgw4w": "DbBPFeXAlZ2",
    "DWaKLTTgLlz": "DbRoKmfgAyN",
}

TODOS = PRINCIPAIS + OPCIONAIS


def url(codigo: str) -> str:
    return f"https://www.instagram.com/lucureau/reel/{codigo}/"


def por_lote(lotes):
    return [item for item in TODOS if item[1] in lotes]
