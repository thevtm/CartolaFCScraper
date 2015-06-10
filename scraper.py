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


import os
import json
import scraperwiki
from Scrapers import Scouts
from Scrapers import Partidas
from Scrapers import Lances

# Consts
LOGIN_EMAIL = os.environ['MORPH_LOGIN_EMAIL'] ## CartolaFC Login
LOGIN_SENHA = os.environ['MORPH_LOGIN_SENHA'] ## CartolaFC Senha
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
PARTIDAS_DATA = 'Data/Partidas.json'

# Functions
def FetchUltimaRodadaDosScouts():
    try:
        Rodada = scraperwiki.sqlite.select("max(Rodada) as Rodada from data")[0]['Rodada']
    except Exception, e:
        DEFAULT_RODADA_ERROR = 0
        print '[ERROR] Nao foi possivel obter a ultima rodada da tabela Scouts, usando rodada:', DEFAULT_RODADA_ERROR
        Rodada = DEFAULT_RODADA_ERROR
    else:
        print '[LOG] Ultima rodada na tabela Scouts:', Rodada
    finally:
        return Rodada
    

# Carrega ids das partidas
with open(PARTIDAS_DATA) as f:
    PartidasData = json.load(f)

# Scrape Scouts
Scouts.ScrapeScouts(LOGIN_EMAIL, LOGIN_SENHA, USER_AGENT)

# Obtem a ultima rodada da tabela Scouts
ultimaRodada = FetchUltimaRodadaDosScouts()

# Scrape Partidas
PartidasID = [p['ID'] for p in PartidasData if p['Rodada'] == ultimaRodada]
Partidas.ScrapePartidas(PartidasID, USER_AGENT)

# Scrape Lances
Lances.ScrapeLances(USER_AGENT)
