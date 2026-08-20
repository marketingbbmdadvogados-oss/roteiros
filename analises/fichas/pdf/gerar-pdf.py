# -*- coding: utf-8 -*-
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, HRFlowable,
)

SAIDA = "/home/user/roteiros/analises/fichas/pdf/analise-roteiro-golpe.pdf"

TINTA = colors.HexColor("#1A1A1A")
CINZA = colors.HexColor("#6B6B6B")
LINHA = colors.HexColor("#DDDDD8")
FUNDO = colors.HexColor("#F5F4F0")
ACENTO = colors.HexColor("#8C1D18")   # vinho sóbrio, tom jurídico
VERDE = colors.HexColor("#2F5D3A")

ss = getSampleStyleSheet()

def st(nome, **kw):
    base = dict(fontName="Helvetica", fontSize=9.8, leading=13.6, textColor=TINTA,
                spaceBefore=0, spaceAfter=0)
    base.update(kw)
    return ParagraphStyle(nome, **base)

TITULO     = st("titulo", fontName="Helvetica-Bold", fontSize=21, leading=25, spaceAfter=3)
SUBTITULO  = st("subtitulo", fontSize=10.5, leading=15, textColor=CINZA, spaceAfter=2)
H1         = st("h1", fontName="Helvetica-Bold", fontSize=13.5, leading=17,
                spaceBefore=13, spaceAfter=6, textColor=ACENTO)
H2         = st("h2", fontName="Helvetica-Bold", fontSize=11, leading=14,
                spaceBefore=11, spaceAfter=4)
CORPO      = st("corpo", alignment=TA_JUSTIFY, spaceAfter=6)
CORPO_AP   = st("corpo_ap", alignment=TA_JUSTIFY, spaceAfter=5, leftIndent=9)
CITACAO    = st("citacao", fontName="Helvetica-Oblique", fontSize=11, leading=16,
                leftIndent=13, rightIndent=13, spaceBefore=3, spaceAfter=7)
MONO       = st("mono", fontName="Courier-Bold", fontSize=10.5, leading=15,
                textColor=TINTA)
CELULA     = st("celula", fontSize=9, leading=12.5)
CELULA_B   = st("celula_b", fontName="Helvetica-Bold", fontSize=9, leading=12.5)
RODAPE     = st("rodape", fontSize=7.5, leading=10, textColor=CINZA)

LARGURA_UTIL = A4[0] - 44 * mm


def p(txt, estilo=CORPO):
    return Paragraph(txt, estilo)


def bloco_destaque(titulo, texto, cor=FUNDO, borda=ACENTO):
    """Caixa com barra lateral, para o problema/por quê/correção."""
    interno = []
    if titulo:
        interno.append(p(titulo, CELULA_B))
        interno.append(Spacer(1, 2))
    interno.append(p(texto, CELULA))
    t = Table([[interno]], colWidths=[LARGURA_UTIL])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), cor),
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, borda),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def tabela(dados, larguras, cabecalho=True):
    linhas = []
    for i, linha in enumerate(dados):
        estilo = CELULA_B if (cabecalho and i == 0) else CELULA
        linhas.append([Paragraph(c, estilo) for c in linha])
    t = Table(linhas, colWidths=larguras, repeatRows=1 if cabecalho else 0)
    estilos = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5.5),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINHA),
    ]
    if cabecalho:
        estilos += [
            ("BACKGROUND", (0, 0), (-1, 0), FUNDO),
            ("LINEBELOW", (0, 0), (-1, 0), 0.8, CINZA),
        ]
    t.setStyle(TableStyle(estilos))
    return t


def regua():
    return HRFlowable(width="100%", thickness=0.5, color=LINHA,
                      spaceBefore=13, spaceAfter=3)


# ------------------------------------------------------------------ conteúdo
h = []

h.append(p("Análise do roteiro &ldquo;GOLPE&rdquo;", TITULO))
h.append(p("Estudante de direito que ensinava a não cair em golpe, presa por aplicar golpe &nbsp;·&nbsp; "
           "Reel curto, ~50s &nbsp;·&nbsp; Público: advogados e empresários", SUBTITULO))
h.append(p("Documento gerado a partir do método de roteiro em construção, baseado no conteúdo "
           "de Luíza Cureau (@lucureau) e nos dados de 90 dias do perfil @isaacbertolini.", SUBTITULO))
h.append(regua())

# --- o que está bom
h.append(p("O que já está bom", H1))
h.append(p("<b>O gancho tem um paradoxo de verdade.</b> Quem ensinava a não cair em golpe foi presa "
           "por golpe. Isso trava o dedo sozinho, sem truque.", CORPO))
h.append(p("<b>O caso é concreto.</b> Loja cenográfica com caixa vazia, Pix, o namorado com passagem "
           "anterior. São detalhes que a pessoa consegue visualizar e repetir depois.", CORPO))
h.append(p("<b>A virada é a melhor parte do roteiro.</b>", CORPO))
h.append(p("&ldquo;Perfil profissional, foto boa, discurso de autoridade — isso não é prova de nada. "
           "Isso é produção.&rdquo;", CITACAO))
h.append(p("Curta, em antítese, e sobrevive fora do vídeo. É o que sustenta tudo.", CORPO))

# --- achado 1
h.append(p("Achado 1 &nbsp;—&nbsp; Não tem texto na tela", H1))
h.append(bloco_destaque("O problema",
    "O roteiro tem só a fala. Nenhum texto grande na tela, nenhum recurso visual nos primeiros segundos."))
h.append(Spacer(1, 8))
h.append(p("<b>Por que importa.</b> É a correção com a maior evidência disponível. A Luíza ensina que "
           "o texto na tela contextualiza o vídeo antes de a pessoa ouvir qualquer palavra. E os números "
           "de 90 dias do próprio perfil dizem a mesma coisa: bastidores publicados como Story deram o "
           "<b>pior alcance da conta</b>; o mesmo tema, virado em Reel com gancho de legenda, deu o "
           "<b>melhor alcance para não-seguidor de toda a conta</b>.", CORPO))
h.append(p("O tema nunca foi o problema. Era o formato sem gancho.", CORPO))
h.append(p("<b>Como corrigir.</b> Texto grande, que troca na tela:", CORPO))
h.append(bloco_destaque(None,
    '<font face="Courier-Bold">ELA ENSINAVA A NÃO CAIR EM GOLPE</font> &nbsp;&rarr;&nbsp; '
    '<font face="Courier-Bold">FOI PRESA POR APLICAR GOLPE</font>', cor=colors.white, borda=VERDE))
h.append(Spacer(1, 8))
h.append(p("Junto com isso: print do perfil dela (borrado) ao lado da notícia da prisão, e uma batida "
           "seca de áudio no momento da troca. São três canais entrando de uma vez, <b>sem mudar uma "
           "palavra do que ele fala</b>.", CORPO))

# --- achado 2
h.append(p("Achado 2 &nbsp;—&nbsp; O meio do vídeo não tem respiro", H1))
h.append(bloco_destaque("O problema",
    "Do &ldquo;o esquema era esse&rdquo; até o namorado são sete fatos seguidos, sem nenhuma pausa de "
    "tensão: sétimo semestre, estágio, nome da operação, perfil clonado, loja cenográfica, Pix, fuga."))
h.append(Spacer(1, 8))
h.append(p("<b>Por que importa.</b> É bloco de informação, e informação sozinha não segura ninguém. "
           "O que segura são frases que abrem curiosidade <b>sem entregar nada</b> — a Luíza chama de "
           "pontas soltas e manda usar no mínimo duas. Essa é a única regra em que três leituras "
           "independentes bateram: ela ensinando em Reel, ela ensinando em carrossel, e a análise das "
           "referências que já estavam no Drive (Rony, Nigro, Benchimol).", CORPO))
h.append(p("<b>Como corrigir.</b> Duas frases, dois segundos cada:", CORPO))
h.append(tabela([
    ["Onde entra", "Frase"],
    ["Antes de explicar o esquema",
     "<i>&ldquo;E o jeito que eles faziam é o que me assusta de verdade.&rdquo;</i>"],
    ["Antes de falar do namorado",
     "<i>&ldquo;Só que tem uma parte dessa história que quase ninguém viu.&rdquo;</i>"],
], [58 * mm, LARGURA_UTIL - 58 * mm]))
h.append(Spacer(1, 9))
h.append(p("A segunda vale mais do que parece: o namorado com passagem anterior <b>é a prova da "
           "virada</b> — histórico vale mais que aparência. Anunciar antes de entregar transforma um "
           "fato solto em pagamento.", CORPO))
h.append(p("Se precisar de espaço, corta &ldquo;sétimo semestre&rdquo; e o nome da operação. É detalhe "
           "de jornal, não de retenção.", CORPO))

# --- achado 3
h.append(p("Achado 3 &nbsp;—&nbsp; O CTA pede uma confissão", H1))
h.append(bloco_destaque("O problema",
    "O roteiro fecha perguntando: <i>&ldquo;Você já contratou algum profissional só porque viu ele bem "
    "nas redes, sem nenhuma indicação de ninguém?&rdquo;</i>"))
h.append(Spacer(1, 8))
h.append(p("<b>Por que importa.</b> Isso pede que a pessoa admita em público que já contratou mal. "
           "Ninguém faz isso — o custo social é alto demais, e o comentário morre antes de nascer.", CORPO))
h.append(p("E há uma oportunidade sendo desperdiçada: a virada do vídeo <i>é</i> um recado que as "
           "pessoas querem dar a alguém. Todo mundo conhece alguém que fecha contrato por Instagram. "
           "O espectador não compartilha o vídeo — ele compartilha o recado que não quer dar na cara.", CORPO))
h.append(p("Os números do perfil reforçam: esse formato (história + indignação) é o de melhor interação "
           "orgânica da conta, e compartilhamento direcionado é o CTA que mais leva o conteúdo para fora "
           "da base de seguidores.", CORPO))
h.append(p("<b>Como corrigir.</b>", CORPO))
h.append(bloco_destaque(None,
    "<i>&ldquo;Manda esse vídeo pra pessoa que fecha contrato só porque o perfil é bonito.&rdquo;</i>",
    cor=colors.white, borda=VERDE))
h.append(Spacer(1, 8))
h.append(p("Se preferirem manter comentário, tira a confissão: <i>&ldquo;Você contrataria alguém que "
           "você só conhece pela internet? Responde sim ou não.&rdquo;</i>", CORPO))
h.append(p("<b>Um CTA só.</b> Não emenda &ldquo;e comenta aqui embaixo&rdquo; — pedir duas ações faz a "
           "pessoa não fazer nenhuma.", CORPO))

# --- travas
h.append(p("Antes de gravar: duas correções obrigatórias", H1))
h.append(p("1. Linguagem de presunção de inocência", H2))
h.append(p("O roteiro afirma a conduta como fato consumado: <i>&ldquo;ela e o namorado clonavam&rdquo;</i>, "
           "<i>&ldquo;os dois sumiam&rdquo;</i>. Um advogado afirmando autoria de crime antes do trânsito "
           "em julgado se expõe sem necessidade — e enfraquece a própria autoridade que o vídeo constrói.", CORPO))
h.append(tabela([
    ["Como está", "Como fica"],
    ["&ldquo;O esquema era esse: ela e o namorado clonavam…&rdquo;",
     "&ldquo;Segundo a Polícia Civil, o esquema funcionava assim…&rdquo;"],
    ["&ldquo;A vítima pagava no Pix. E os dois sumiam.&rdquo;",
     "&ldquo;A investigação aponta que a vítima pagava no Pix e os dois sumiam.&rdquo;"],
], [LARGURA_UTIL / 2, LARGURA_UTIL / 2]))
h.append(Spacer(1, 7))
h.append(p("Sem nome, rosto ou @ que permita identificar a pessoa.", CORPO))
h.append(p("2. Conferir as fontes", H2))
h.append(p("Operação Reflexo, a Polícia Civil do DF, a passagem anterior do namorado no Rio Grande do Sul "
           "e o &ldquo;sexta-feira passada&rdquo; precisam ser confirmados em veículo ou no site da PCDF "
           "antes de gravar, com o link guardado. Nenhuma afirmação factual sai de memória.", CORPO))
h.append(p("E &ldquo;sexta-feira passada&rdquo; vence rápido: se gravar depois de uma semana, troca pela "
           "data. <i>(Revisão de texto: &ldquo;somiam&rdquo; &rarr; &ldquo;sumiam&rdquo;.)</i>", CORPO))

# --- honestidade
h.append(p("O que eu defendo e o que é palpite", H1))
h.append(p("Vale separar, porque o objetivo do método é justamente parar de tratar tudo com o mesmo peso "
           "de certeza.", CORPO))
h.append(tabela([
    ["Correção", "Em que se apoia", "Quanto defendo"],
    ["Texto na tela", "Ela ensina <b>e</b> o número do perfil confirma",
     "<b>Alto.</b> A mais bem sustentada do método"],
    ["Pontas soltas", "Três leituras independentes no mesmo lugar", "<b>Alto</b>"],
    ["CTA de compartilhamento", "Regra dela tem fonte fraca; <b>o dado do perfil é que sustenta</b>",
     "<b>Médio-alto</b> — pelo dado, não por ela"],
    ["Reordenar a abertura", "Leitura de ritmo, sem lastro externo",
     "<b>Baixo.</b> Só depois das outras"],
], [40 * mm, 66 * mm, LARGURA_UTIL - 106 * mm]))
h.append(Spacer(1, 9))
h.append(p("Se for testar uma coisa por vez, faça as duas primeiras. São as que se defendem numa reunião "
           "sem hesitar.", CORPO))

# --- aposta
h.append(p("A aposta deste roteiro", H1))
h.append(p("Registrado <b>antes</b> de publicar — é isso que transforma a análise em teste, e não em "
           "explicação depois do fato. Se o roteiro for gravado como está hoje, a curva de retenção deve "
           "mostrar:", CORPO))
h.append(tabela([
    ["Trecho da curva", "Previsão", "Causa provável"],
    ["Primeiros segundos", "queda moderada a alta", "o gancho chega sozinho, sem texto na tela"],
    ["Meio", "queda contínua", "o bloco de sete fatos sem respiro"],
    ["Final", "queda acentuada", "o CTA que pede confissão"],
], [40 * mm, 42 * mm, LARGURA_UTIL - 82 * mm]))
h.append(Spacer(1, 9))
h.append(p("Se bater, essas três regras sobem de confiança e passam a valer como padrão da casa. Se o "
           "meio segurar mesmo sem ponta solta, a regra perde força neste formato — e isso é informação "
           "boa, não fracasso.", CORPO))


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(CINZA)
    canvas.drawString(22 * mm, 12 * mm, "Análise de roteiro — GOLPE")
    canvas.drawRightString(A4[0] - 22 * mm, 12 * mm, "%d" % doc.page)
    canvas.setStrokeColor(LINHA)
    canvas.setLineWidth(0.4)
    canvas.line(22 * mm, 15.5 * mm, A4[0] - 22 * mm, 15.5 * mm)
    canvas.restoreState()


doc = BaseDocTemplate(SAIDA, pagesize=A4,
                      leftMargin=22 * mm, rightMargin=22 * mm,
                      topMargin=18 * mm, bottomMargin=19 * mm,
                      title="Análise do roteiro GOLPE",
                      author="Método de roteiro — perfil @isaacbertolini")
quadro = Frame(doc.leftMargin, doc.bottomMargin, LARGURA_UTIL,
               A4[1] - doc.topMargin - doc.bottomMargin, id="normal")
doc.addPageTemplates([PageTemplate(id="pag", frames=[quadro], onPage=rodape)])
doc.build(h)
print("gerado:", SAIDA)
