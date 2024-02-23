content = """

\033[1m\033[94mCalculando Áreas sob Distribuições de Probabilidade com Python:\033[0m

\033[92m# Importamos as bibliotecas necessárias\033[0m
from scipy.stats import norm, expon, binom, poisson
import numpy as np

\033[1m\033[94m# Distribuição Normal\033[0m
\033[92m# Parâmetros: média (mu) e desvio padrão (sigma)\033[0m
mu, sigma = 0, 1  \033[93m# Normal padrão\033[0m
area_normal = norm.cdf(1, mu, sigma)  \033[93m# P(X < 1) para N(0,1)\033[0m
print(f"Área sob a curva normal padrão até Z=1: {area_normal:.4f}")

\033[1m\033[94m# Distribuição Exponencial\033[0m
\033[92m# Parâmetro: taxa (lambda), onde lambda = 1/escala\033[0m
lambda_exp = 1  \033[93m# Exponencial com taxa 1\033[0m
area_exponencial = expon.cdf(1, scale=1/lambda_exp)  \033[93m# P(X < 1) para Exp(1)\033[0m
print(f"Área sob a curva exponencial até X=1: {area_exponencial:.4f}")

\033[1m\033[94m# Distribuição Binomial\033[0m
\033[92m# Parâmetros: número de ensaios (n) e probabilidade de sucesso (p)\033[0m
n, p = 10, 0.5  \033[93m# Exemplo para 10 lançamentos de moeda\033[0m
area_binomial = binom.cdf(5, n, p)  \033[93m# P(X <= 5) para B(10,0.5)\033[0m
print(f"Área sob a curva binomial até X=5: {area_binomial:.4f}")

\033[1m\033[94m# Distribuição de Poisson\033[0m
\033[92m# Parâmetro: taxa média de ocorrência (lambda)\033[0m
lambda_poisson = 3  \033[93m# Exemplo para uma taxa de 3 eventos por intervalo\033[0m
area_poisson = poisson.cdf(2, lambda_poisson)  \033[93m# P(X <= 2) para Poisson(3)\033[0m
print(f"Área sob a curva de Poisson até X=2: {area_poisson:.4f}")

"""
