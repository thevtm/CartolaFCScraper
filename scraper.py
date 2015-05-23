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
import cookielib

#%%

## Consts
SCOUTS_URL = 'http://cartolafc.globo.com/mercado/filtrar.json?page='
LOGIN_URL = 'https://loginfree.globo.com/login/438'
LOGIN_EMAIL = os.environ['MORPH_LOGIN_EMAIL'] ## CartolaFC Login
LOGIN_SENHA = os.environ['MORPH_LOGIN_SENHA'] ## CartolaFC Senha
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

#%%

## Cria o mechanize browser
print '[LOG] Downloading Data Started'

# Inicialisa browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Define user-agent
br.addheaders = [('User-agent', USER_AGENT)]


#%%

## Loga no CartolaFC

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

#%%

## Download Scouts

jsonRaw = []
for i in it.count(1):    
    url = SCOUTS_URL + str(i)
    
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

print '[LOG] Processing Data Started'

rodada = jsonRaw[0]['rodada_id'] - 1

#%%

# Concatena lista de atletas dos arquivos
atletasJSON = [j['atleta'] for j in jsonRaw]
atletasJSON = list(it.chain(*atletasJSON))

#%%

## Minera Scouts
## e concatena em um DataFrame

# Scouts
ScoutsDict = []

for atleta in atletasJSON:
    scoutDict = {s['nome']:s['quantidade'] for s in atleta['scout']} # Add Scouts
    scoutDict['Rodada'] = rodada
    scoutDict['Atleta'] = atleta['id']
    scoutDict['Apelido'] = atleta['apelido']
    scoutDict['Clube'] = atleta['clube']['slug']
    scoutDict['Posicao'] = atleta['posicao']['abreviacao']
    scoutDict['Status'] = atleta['status']
    scoutDict['Pontos'] = float(atleta['pontos'])
    scoutDict['PontosMedia'] = float(atleta['media'])
    scoutDict['Preco'] = float(atleta['preco'])
    scoutDict['PrecoVariacao'] = float(atleta['variacao'])
    scoutDict['Mando'] = atleta['clube']['id'] == atleta['partida_clube_casa']['id']
    scoutDict['Jogos'] = atleta['jogos']
    scoutDict['PartidaCasa'] = atleta['partida_clube_casa']['slug']
    scoutDict['PartidaVisitante'] = atleta['partida_clube_visitante']['slug']
    scoutDict['PartidaData'] = atleta['partida_data']

    ScoutsDict.append(scoutDict)

print '[LOG] Processing Data Ended'

#%%

## Save DataFrame to SQLite

print '[LOG] Transferindo dados para SQLite'

scraperwiki.sqlite.save(unique_keys = ['Atleta', 'Rodada'],
                        data = ScoutsDict,
                        table_name = 'data')

print '[LOG] Dados Salvos'
