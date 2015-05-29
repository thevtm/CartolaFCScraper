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

import re
import itertools as it
import json
from lxml import html
import scraperwiki
from LancesScrapers import Substituicoes
from LancesScrapers import Cartoes

def ScrapeLances(USER_AGENT):

    # Consts
    PARTIDAS_RODADA_URL = 'http://globoesporte.globo.com/servico/esportes_campeonato/responsivo/widget-uuid/09021843-e53d-4020-80f7-302a15756585/fases/fase-unica-brasileiro-2015/rodada/{0}/jogos.html'
    LANCES_URL = 'mensagens.json'
    TOTAL_RODADA = 38


    # Fetch links das Partidas

    print '[LOG] Obtendo os links dos Lances'

    PartidasRodadaLinks = [PARTIDAS_RODADA_URL.format(i) for i in range(1, TOTAL_RODADA + 1)]
    PartidasRodadaLinksData = [scraperwiki.scrape(u, user_agent=USER_AGENT) for u in PartidasRodadaLinks]
    PartidasLinks = [html.fromstring(d).xpath('//a/@href') for d in PartidasRodadaLinksData]
    PartidasLinks = list(it.chain.from_iterable(PartidasLinks))

    print '[LOG] Links das Lances obtidos'


    # Download dados dos lances

    print '[LOG] Download Lances Iniciado'

    LancesJSON = []
    for i, l in enumerate(PartidasLinks):
        url = l + '/' + LANCES_URL
        print '[LOG] Baixando ', i + 1, '/', len(PartidasLinks)
        data = scraperwiki.scrape(url)
        jData = json.loads(data)
        ## Adiciona PartidaID em cada lance
        PartidaID = int(re.search('"jogo_id": (\d+),', data).groups()[0])
        for j in jData:
            j['PartidaID'] = PartidaID
        LancesJSON.append(jData)

    # Concatena Lances
    LancesJSON = list(it.chain.from_iterable(LancesJSON))

    print '[LOG] Download Substituições Terminado'


    # Minera dados
    print '[LOG] Processamento de Lances Iniciado'

    # Minera Substituicoes
    Substituicoes.ScrapeSubstituicoes(LancesJSON)

    # Minera Cartões
    Cartoes.ScrapeCartoes(LancesJSON)

    print '[LOG] Processamento de Lances Terminado'

