# Projeto 3 - Fazendo um modelo de investimento com Python - Factor Investing no Ibovespa.

# Desafio: Construir um código que faça um backtesting dos últimos 6 anos, escolhendo as 8 melhores ações do índice
# ibovespa e utilizando como critério o fator momento 7 meses.

# Passo a passo da estratégia:
# Passo 1 - Definir um universo investível.
# Passo 2 - Escolher o fator que servirá como critério para criação dos rankings.
# Passo 3 - Escolher o período de teste.
# Passo 4 - Escolher o número de ações na carteira.
# Passo 5 - Definir o período de balanceamento. De quanto em quanto tempo a carteira muda?

# Passo a passo do código?
# Passo 1 - Ler a composição histórica do Ibovespa e os tickers que já passaram pelo índice.

import yfinance as yf
import pandas as pd
import quantstats as qs

comp_historica = pd.read_excel('composicao_ibov.xlsx')
tickers = pd.read_excel('composicao_ibov.xlsx', sheet_name='lista_acoes')

# print(comp_historica)
# print(tickers)
#
# Passo 2 - Puxar as cotações de todas as empresas que farão parte do backtest.

dados_cotacoes = yf.download(tickers=tickers['tickers'].to_list(), start="2015-05-29", end="2022-12-31")['Adj Close']

# print(dados_cotacoes)

# Passo 3 - Transformar o índice em data e ordenar a série de tempo.
dados_cotacoes.index = pd.to_datetime(dados_cotacoes.index)
dados_cotacoes = dados_cotacoes.sort_index()

# print(dados_cotacoes.index)


# Passo 4 - Calcular a média dos retornos 7 meses e ajustar a tabela com o fator.

retorno_7meses = (dados_cotacoes.resample("M").last().pct_change().rolling(7).mean().
                  dropna(axis=0, how="all").drop('2022-12-31'))

# print(retorno_7meses)

# Passo 5 - Classificar e retirar empresas que não participaram do Ibovespa no período de tempo selecionado.

for data in retorno_7meses.index:
    for empresa in retorno_7meses.columns:

        if empresa.replace(".SA", "") not in comp_historica.loc[:, data].to_list():
            retorno_7meses.loc[data, empresa] = pd.NA

# print(retorno_7meses)

# Passo 6 - Criar as carteiras de investimento em uma matriz de 0 ou 1.

carteiras = retorno_7meses.rank(axis=1, ascending=False)

for data in carteiras.index:
    for empresa in carteiras.columns:

        if carteiras.loc[data, empresa] < 9:

            carteiras.loc[data, empresa] = 1

        else:

            carteiras.loc[data, empresa] = 0
# print(carteiras)

# Passo 7 - Calcular o retorno mensal das empresas no período de backtest.

retorno_mensal = dados_cotacoes.resample("M").last().pct_change()
retorno_mensal = retorno_mensal.drop(retorno_mensal.index[:8], axis=0)
carteiras.index = retorno_mensal.index

# print(carteiras)
# print(retorno_mensal)

# Passo 8 - Cruzar a matriz de retorno mensal com a matriz das carteiras para chegar na rentabilidade do modelo.

comp_historica = pd.read_excel('composicao_ibov.xlsx')
tickers = pd.read_excel('composicao_ibov.xlsx', sheet_name='lista_acoes')

dados_cotacoes = yf.download(tickers=tickers['tickers'].to_list(),
                             start="2015-05-29", end="2022-12-31")['Adj Close']

dados_cotacoes.index = pd.to_datetime(dados_cotacoes.index)
dados_cotacoes = dados_cotacoes.sort_index()

r7 = (dados_cotacoes.resample("M").last().pct_change().rolling(7).mean().
      dropna(axis=0, how="all").drop('2022-12-31'))

for data in r7.index:
    for empresa in r7.columns:

        if empresa.replace(".SA", "") not in comp_historica.loc[:, data].to_list():
            r7.loc[data, empresa] = pd.NA

carteiras = r7.rank(axis=1, ascending=False)

for data in carteiras.index:
    for empresa in carteiras.columns:

        if carteiras.loc[data, empresa] < 9:

            carteiras.loc[data, empresa] = 1

        else:

            carteiras.loc[data, empresa] = 0

retorno_mensal = dados_cotacoes.resample("M").last().pct_change()
retorno_mensal = retorno_mensal.drop(retorno_mensal.index[:8], axis=0)
carteiras.index = retorno_mensal.index

retorno_modelo = (carteiras * retorno_mensal).sum(axis=1) / 8

# print(retorno_modelo)

# qs.extend_pandas()
# print(retorno_modelo.plot_monthly_heatmap())

# Passo 9 - Puxar e calcular a rentabilidade do Ibovespa no período.

ibovespa = yf.download("^BVSP", start="2015-12-30", end="2022-12-31")['Adj Close']

retornos_ibovespa = ibovespa.resample("M").last().pct_change().dropna()

# print(retornos_ibovespa)


# Passo 10 - Calcular e visualizar as rentabilidades do modelo contra o Ibovespa.
retorno_acum_modelo = (1 + retorno_modelo).cumprod() - 1
retorno_acum_ibov = (1 + retornos_ibovespa).cumprod() - 1

retorno_acum_modelo.plot_monthly_heatmap()
retorno_acum_ibov.plot_monthly_heatmap()

# Passo 11 - Calcular e visualizar as rentabilidades do modelo contra o Ibovespa.

overperfom_modelo_menos_ibov = retorno_modelo - retornos_ibovespa
overperfom_modelo_menos_ibov.plot_monthly_heatmap()
