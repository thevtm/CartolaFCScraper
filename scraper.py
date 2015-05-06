# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

#%%

## The MIT License (MIT)
##
## Copyright (c) 2015 Vinícius Tabille Manjabosco
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.

#%%

import itertools as it
import json
import scraperwiki
import mechanize

#%%

## Consts
JOGADORES_URL = 'http://cartolafc.globo.com/mercado/filtrar.json?page='
LOGIN_URL = 'https://loginfree.globo.com/login/438'
LOGIN_EMAIL = MORPH_LOGIN_EMAIL
LOGIN_SENHA = MORPH_LOGIN_SENHA

#%%

def ExtractPlayerDF(Data):
    colNames = ['Date', 'Round', 'Opponent', 'MP', 'GS', 'A', 'CS', 'GC', 'OG', 'PS',
                'PM', 'YC', 'RC', 'S', 'B', 'ESP', 'BPS', 'NT', 'Value', 'Points']
    fixtures = Data['fixture_history']['all']
    playerDF = pandas.DataFrame(fixtures, columns = colNames)

    playerDF['ID'] = Data['id']
    playerDF['Code'] = Data['code']
    playerDF['WebName'] = Data['web_name']
    playerDF['FirstName'] = Data['first_name']
    playerDF['SecondName'] = Data['second_name']
    playerDF['Position'] = Data['type_name']
    playerDF['Team'] = Data['team_name']

    colOrder = ['ID', 'Code', 'Round', 'WebName', 'FirstName', 'SecondName', 'Position', 'Team',
                'Date', 'Opponent', 'MP', 'GS', 'A', 'CS', 'GC', 'OG', 'PS', 'PM', 'YC',
                'RC', 'S', 'B', 'ESP', 'BPS', 'NT', 'Value', 'Points']

    return playerDF[colOrder]

#%%

## Download dados
print '[LOG] Downloading Data Started'

# Inicialisa browser
br = mechanize.Browser()

# Abre a página de login Cartola através do mechanize
br.open(LOGIN_URL)

# Na página, selecionamos o primeiro form presente. 'nr=0' indica que estamos
# selecionando o form de índice 0 dentre os encontrados.
# Analisando a página, vemos que realmente só há um form.
# Após selecionarmos o form, preenchemos os campos com username e
# senha que permitam fazer o login.
 
br.select_form(nr=0)
br.form['login-passaporte'] = LOGIN_EMAIL
br.form['senha-passaporte'] = LOGIN_SENHA
br.submit()

jsonRaw = []
for i in it.count(1):    
    url = JOGADORES_URL + str(i)
    
    r = br.open(url)
    j = json.loads(r.read())
    jsonRaw.append(j)
    
    pgAtual = int(j['page']['atual'])
    pgTotal = int(j['page']['total'])
    
    print '[LOG] Baixando ', i, '/', pgTotal
    
    if pgAtual == pgTotal:
        break

print '[LOG] Downloading Data Ended'

#%%

## Minera Rodada
rodada = jsonRaw[0]['rodada_id'] - 1

#%%

# Concatena lista de atletas dos arquivos
atletasJSON = [j['atleta'] for j in jsonRaw]
atletasJSON = list(it.chain(*atletasJSON))

#%%

## Minera Scouts
## e concatena em um DataFrame

print '[LOG] Processing Data Started'

# Scouts
ScoutsDict = []

for atleta in atletasJSON:
    scoutDict = {s['nome']:s['quantidade'] for s in atleta['scout']} # Add Scouts
    scoutDict['Rodada'] = rodada
    scoutDict['Atleta'] = atleta['id']
    scoutDict['Apelido'] = atleta['apelido']
    scoutDict['Clube'] = atleta['clube']['abreviacao']
    scoutDict['Posicao'] = atleta['posicao']['abreviacao']
    scoutDict['Status'] = atleta['status']
    scoutDict['Pontos'] = float(atleta['pontos'])
    scoutDict['PontosMedia'] = float(atleta['media'])
    scoutDict['Preco'] = float(atleta['preco'])
    scoutDict['PrecoVariacao'] = float(atleta['variacao'])
    scoutDict['Mando'] = atleta['clube']['id'] == atleta['partida_clube_visitante']['id']
    scoutDict['PartidaCasa'] = atleta['partida_clube_casa']['abreviacao']
    scoutDict['PartidaVisitante'] = atleta['partida_clube_visitante']['abreviacao']
    scoutDict['PartidaData'] = atleta['partida_data']

    ScoutsDict.append(scoutDict)
    
#ScoutsDFColOrder = ['Rodada', 'Atleta', 'Apelido', 'Clube', 'Posicao', 'Status', 'Pontos', 'PontosMedia', 'Preco',
#                    'PrecoVariacao', 'Mando', 'PartidaCasa', 'PartidaVisitante', 'PartidaData', 'FS', 'PE', 'A', 'FT',
#                    'FD', 'FF', 'G', 'I', 'PP', 'RB', 'FC', 'GC', 'CA', 'CV', 'SG', 'DD', 'DP', 'GS']
#ScoutsDF = pd.DataFrame(ScoutsDict, columns = ScoutsDFColOrder)

print '[LOG] Processing Data Ended'

#%%

## Save DataFrame to SQLite

print '[LOG] Transfering data to SQLite format'

scraperwiki.sqlite.save(unique_keys = ['Atleta', 'Rodada'],
                        data = ScoutsDict)

