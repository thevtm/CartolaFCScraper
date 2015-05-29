# -*- coding: utf-8 -*-

# The MIT License (MIT)
##
# Copyright (c) 2015 Vinícius Tabille Manjabosco
##
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
##
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
##
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import itertools as it
import json
from lxml import html
import scrapewiki
import requests


# Consts
PARTIDAS_RODADA_URL = 'http://globoesporte.globo.com/servico/esportes_campeonato/responsivo/widget-uuid/09021843-e53d-4020-80f7-302a15756585/fases/fase-unica-brasileiro-2015/rodada/{0}/jogos.html'
SUBSTITUICOES_URL = 'mensagens.json'
TOTAL_RODADA = 38
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

#%%

# Fetch links das Partidas

print '[LOG] Obtendo os links das Substituições'

PartidasRodadaLinks = [PARTIDAS_RODADA_URL.format(i) for i in range(1, TOTAL_RODADA + 1)]
PartidasRodadaLinksData = [requests.get(u, timeout=(1.0, 5)) for u in PartidasRodadaLinks]
PartidasLinks = [html.fromstring(d).xpath('//a/@href') for d in PartidasRodadaLinksData]
PartidasLinks = list(it.chain.from_iterable(PartidasLinks))

print '[LOG] Links das Substituições obtidos'

# Download dados substituições

print '[LOG] Download Substituições Iniciado'

SubstituicoesJSON = []
for i, l in enumerate(PartidasLinks):
	url = l + '/' + SUBSTITUICOES_URL
	print '[LOG] Baixando ', i + 1, '/', len(PartidasLinks)
	req = requests.get(url, timeout=(1.0, 5))
	SubstituicoesJSON.append(json.loads(req.content))

print '[LOG] Download Substituições Terminado'

# Minera dados

print '[LOG] Processamento de Substituições Iniciado'

def isSubstituicao(x):
    try:
        return (x['tipo'] == 'LANCE_SUBSTITUICAO')
    except:
        return False

SubstituicoesJSON = filter(isSubstituicao, SubstituicoesJSON)

PartidasDict = []
for p in PartidasJSON:
    pDict = {}
    pDict['ID'] = p['jogo_id']
    pDict['Rodada'] = p['rodada']
    pDict['EquipeMandante'] = p['equipe_mandante']['slug']
    pDict['EquipeVisitante'] = p['equipe_visitante']['slug']
    pDict['PlacarMandante'] = p['placar_mandante']
    pDict['PlacarVisitante'] = p['placar_visitante']

    PartidasDict.append(pDict)

print '[LOG] Processamento de Partidas Terminado'


