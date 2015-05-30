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


def ScrapeGols(LancesJSON):
    print '[LOG] Processamento de Lances.Gols Iniciado'

    def isGol(x):
        try:
            return (x['tipo'] == 'LANCE_GOL' and 'gol' in x  and 'momento' in x)
        except:
            return False

    # Filtra Gols
    GolsJSON = filter(isGol, LancesJSON)

    GolsDict = []
    for g in GolsJSON:
        gDict = {}
        gDict['ID'] = g['id']
        gDict['PartidaID'] = g['PartidaID']
        gDict['Periodo'] = g['periodo_sigla']
        gDict['Momento'] = g['momento']
        gDict['Time'] = g['nome_time']
        gDict['Apelido'] = g['gol']['autor']
        gDict['AtletaID'] = g['gol']['autor_id']
        gDict['Contra'] = g['gol']['contra']
        GolsDict.append(gDict)

    print '[LOG] Processamento de Lances.Gols Terminado'

    # Save DataFrame to SQLite

    print '[LOG] Transferindo Lances.Gols para SQLite'

    scraperwiki.sqlite.save(unique_keys=['ID'],
                            data=GolsDict,
                            table_name='Gols')

    print '[LOG] Lances.Gols Salvas'
