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

import os
import itertools as it
import json
import scraperwiki
import mechanize

#%%

## Consts
JOGADORES_URL = 'http://cartolafc.globo.com/mercado/filtrar.json?page='
LOGIN_URL = 'https://loginfree.globo.com/login/438'
LOGIN_EMAIL = os.environ['MORPH_LOGIN_EMAIL']
LOGIN_SENHA = os.environ['MORPH_LOGIN_SENHA']

#%%

## Download dados
print '[LOG] Download Iniciado'

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

print '[LOG] Download Terminado'

#%%

## Minera Scouts
## e concatena em um DataFrame

print '[LOG] Processando dados'

# Concatena lista de atletas dos arquivos
atletasJSON = [j['atleta'] for j in jsonRaw]
atletasJSON = list(it.chain(*atletasJSON))

## Minera Rodada
rodada = jsonRaw[0]['rodada_id'] - 1

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

print '[LOG] Processamento de dados terminado'

#%%

## Salva dados para SQLite

print '[LOG] Salvando dados'

scraperwiki.sqlite.save(unique_keys = ['Atleta', 'Rodada'],
                        data = ScoutsDict)

