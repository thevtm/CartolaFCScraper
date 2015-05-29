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

def ScrapeSubstituicoes(LancesJSON):
    print '[LOG] Processamento de Lances.Substituições Iniciado'

    def isSubstituicao(x):
        try:
            return (x['tipo'] == 'LANCE_SUBSTITUICAO' and 'substituicao' in x)
        except:
            return False


    # Filtra Substituições
    SubstituicoesJSON = filter(isSubstituicao, LancesJSON)

    SubstituicoesDict = []
    for s in SubstituicoesJSON:
        sDict = {}
        sDict['ID'] = s['id']
        sDict['PartidaID'] = s['PartidaID']
        sDict['Periodo'] = s['periodo_sigla']
        sDict['Momento'] = s['momento']
        sDict['Time'] = s['nome_time']
        sDict['TimeID'] = s['substituicao']['time_id']
        sDict['SaiuApelido'] =  s['substituicao']['nome']
        sDict['SaiuAtletaID'] =  s['substituicao']['pessoa_id']
        sDict['SaiuTitular'] =  s['substituicao']['titular']
        sDict['SaiuPosicao'] =  s['substituicao']['posicao']
        sDict['EntrouApelido'] =  s['substituicao']['substituido_por']['nome']
        sDict['EntrouAtletaID'] =  s['substituicao']['substituido_por']['pessoa_id']
        sDict['EntrouTitular'] =  s['substituicao']['substituido_por']['titular']
        sDict['EntrouPosicao'] =  s['substituicao']['substituido_por']['posicao']


        SubstituicoesDict.append(sDict)

    print '[LOG] Processamento de Lances.Substituições Terminado'

    # Save DataFrame to SQLite

    print '[LOG] Transferindo Lances.Substituições para SQLite'

    scraperwiki.sqlite.save(unique_keys=['ID'],
                            data=SubstituicoesDict,
                            table_name='Substituicoes')

    print '[LOG] Lances.Substituições Salvas'

