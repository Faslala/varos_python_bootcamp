# Projeto 1 - Relatório de fechamento de mercado por e-mail.

# Desafio: Construir um e-mail que chegue na caixa de entrada todos os dias com informações 
# de fechamento do Ibovespa e dólar. Passo a passo:

# Passo 1 - Importar os módulos e bibliotecas.

import datetime
import yfinance as yf
from matplotlib import pyplot as plt
import mplcyberpunk
import smtplib
from email.message import EmailMessage

import os
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())

# Passo 2 - Pegar dados do Ibovespa e do Dólar no Yahoo Finance.

ativos = ["^BVSP", "BRL=X", "MXRF11.SA"]

hoje = datetime.datetime.now()
um_ano_atras = hoje - datetime.timedelta(days=365)

dados_mercado = yf.download(ativos, um_ano_atras, hoje).round(2)

# print(dados_mercado.round(2))

# Passo 3 - Manipular os dados para deixá-los nos formatos necessários para fazer as contas.

dados_fechamento = dados_mercado['Adj Close']
dados_fechamento.columns = ['dolar', 'fii', 'ibovespa']
dados_fechamento = dados_fechamento.dropna()

dados_fechamento_mensal = dados_fechamento.resample("M").last()
dados_fechamento_anual = dados_fechamento.resample("Y").last()

# print(dados_fechamento.round(2))
# print(dados_fechamento_anual)
# print(dados_fechamento_mensal.round(2))

# Passo 4 - Calcular o retorno diário, mensal e anual.

retorno_no_ano = dados_fechamento_anual.pct_change().dropna()
retorno_no_mes = dados_fechamento_mensal.pct_change().dropna()
retorno_no_dia = dados_fechamento.pct_change().dropna()

# print(retorno_no_dia)

# Passo 5 - Localizar, dentro das tabelas de retornos, os valores de fechamento de mercado que 
# irão pro texto anexado no e-mail.

retorno_dia_dolar = retorno_no_dia.iloc[-1, 0]
retorno_dia_fii = retorno_no_dia.iloc[-1, 1]
retorno_dia_ibovespa = retorno_no_dia.iloc[-1, 2]

retorno_mes_dolar = retorno_no_mes.iloc[-1, 0]
retorno_mes_fii = retorno_no_mes.iloc[-1, 1]
retorno_mes_ibovespa = retorno_no_mes.iloc[-1, 2]

retorno_ano_dolar = retorno_no_ano.iloc[-1, 0]
retorno_ano_fii = retorno_no_ano.iloc[-1, 1]
retorno_ano_ibovespa = retorno_no_ano.iloc[-1, 2]

retorno_dia_dolar = round(retorno_dia_dolar * 100, 2)
retorno_dia_fii = round(retorno_dia_fii * 100, 2)
retorno_dia_ibovespa = round(retorno_dia_ibovespa * 100, 2)

retorno_mes_dolar = round(retorno_mes_dolar * 100, 2)
retorno_mes_fii = round(retorno_mes_fii * 100, 2)
retorno_mes_ibovespa = round(retorno_mes_ibovespa * 100, 2)

retorno_ano_dolar = round(retorno_ano_dolar * 100, 2)
retorno_ano_fii = round(retorno_ano_fii * 100, 2)
retorno_ano_ibovespa = round(retorno_ano_ibovespa * 100, 2)

# print(retorno_dia_dolar)
# print(retorno_mes_dolar)
# print(retorno_ano_dolar)

# Passo 6 - Fazer os gráficos dos ativos.

plt.style.use("cyberpunk")

dados_fechamento.plot(y='ibovespa', use_index=True, legend=False)
plt.title("Ibovespa")
plt.savefig('ibovespa.png', dpi=300)
mplcyberpunk.add_glow_effects(gradient_fill=True)

dados_fechamento.plot(y='fii', use_index=True, legend=False)
plt.title("FII")
plt.savefig('FII.png', dpi=300)
mplcyberpunk.add_glow_effects(gradient_fill=True)

dados_fechamento.plot(y='dolar', use_index=True, legend=False)
plt.title("Dolar")
plt.savefig('dolar.png', dpi=300)
mplcyberpunk.add_glow_effects(gradient_fill=True)

# plt.show()

# Passo 7 - Enviar o e-mail.

# senha = os.environ.get("SENHA")
senha = os.getenv('SENHA')
email = os.getenv('EMAIL')

msg = EmailMessage()
msg['Subject'] = "Fechamento Bolsa"
msg['From'] = email
msg['To'] = 'faslala1@gmail.com'
# 'brenno@varos.com.br'

msg.set_content(
    f'''Prezado diretor e associados, segue o relatório finaceiro diário:

Bolsa:

No ano o Ibovespa está tendo uma rentabilidade de {retorno_ano_ibovespa}%,
enquanto no mês a rentabilidade é de {retorno_mes_ibovespa}%.

No último dia útil, o fechamento do Ibovespa foi de {retorno_dia_ibovespa}%.

Dólar:

No ano o Dólar está tendo uma rentabilidade de {retorno_ano_dolar}%,
enquanto no mês a rentabilidade é de {retorno_mes_dolar}%.

No último dia útil, o fechamento do Dólar foi de {retorno_dia_dolar}%.

FII:

No ano o fii está tendo uma rentabilidade de {retorno_ano_fii}%,
enquanto no mês a rentabilidade é de {retorno_mes_fii}%.

No último dia útil, o fechamento do fii foi de {retorno_dia_fii}%.


Abs,

Faslala Assis
O melhor estagiário do mundo

''')

with open('dolar.png', 'rb') as content_file:
    content = content_file.read()
    msg.add_attachment(content, maintype='application', subtype='png', filename='dolar.png')

with open('ibovespa.png', 'rb') as content_file:
    content = content_file.read()
    msg.add_attachment(content, maintype='application', subtype='png', filename='ibovespa.png')

with open('FII.png', 'rb') as content_file:
    content = content_file.read()
    msg.add_attachment(content, maintype='application', subtype='png', filename='FII.png')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email, senha)
    smtp.send_message(msg)
