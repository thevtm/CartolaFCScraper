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


import json
import scraperwiki


def ScrapePartidas(PartidasID, USER_AGENT):

    # Consts
    FICHA_URL = 'http://globoesporte.globo.com/dynamo/confronto/jogo/{0}/ficha.json'

    # Download dados das partidas

    print '[LOG] Downloading Partidas Iniciado'

    PartidasJSON = []
    for i, p, in enumerate(PartidasID):
        url = FICHA_URL.format(p)

        print '[LOG] Baixando Partida', i + 1, '/', len(PartidasID)
        PartidasJSON.append(scraperwiki.scrape(url, user_agent=USER_AGENT))

    print '[LOG] Downloading Partidas Terminado'

    # Minera dados

    print '[LOG] Processamento de Partidas Iniciado'

    PartidasJSON = [json.loads(j) for j in PartidasJSON]
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

    # Save DataFrame to SQLite

    print '[LOG] Transferindo Partidas para SQLite'

    scraperwiki.sqlite.save(unique_keys=['ID'],
                            data=PartidasDict,
                            table_name='Partidas')

    print '[LOG] Partidas Salvas'
