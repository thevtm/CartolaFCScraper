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

import scraperwiki


def ScrapeCartoes(LancesJSON):
    print '[LOG] Processamento de Lances.Cartões Iniciado'

    def isCartao(x):
        try:
            return (x['tipo'] == 'LANCE_CARTAO' and 'cartao' in x)
        except:
            return False

    # Filtra Cartões
    CartoesJSON = filter(isCartao, LancesJSON)

    CartoesDict = []
    for c in CartoesJSON:
        cDict = {}
        cDict['ID'] = c['id']
        cDict['PartidaID'] = c['PartidaID']
        cDict['Periodo'] = c['periodo_sigla']
        cDict['Momento'] = c['momento']
        cDict['Time'] = c['nome_time']
        cDict['Apelido'] = c['cartao']['nome_jogador']
        cDict['AtletaID'] = c['cartao']['jogador_id']
        cDict['Cartao'] = c['cartao']['tipo']
        CartoesDict.append(cDict)

    print '[LOG] Processamento de Lances.Cartões Terminado'


    # Save DataFrame to SQLite

    print '[LOG] Transferindo Lances.Cartões para SQLite'

    scraperwiki.sqlite.save(unique_keys=['ID'],
                            data=CartoesDict,
                            table_name='Cartoes')

    print '[LOG] Lances.Cartões Salvas'
