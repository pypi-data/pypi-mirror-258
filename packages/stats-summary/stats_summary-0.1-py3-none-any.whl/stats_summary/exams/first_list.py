content = """

\033[1m\033[94m1. Bolas são sorteadas com reposição de uma urna contendo 1 bola branca e 2 bolas pretas.\033[0m

a) A distribuição conjunta é i.i.d. e dada por p(X1, ..., X9) = (2/3)^sum(Xi) * (1/3)^(9-sum(Xi)).

b) A soma das variáveis segue uma distribuição Binomial(9, 2/3).

c) O valor esperado da média amostral é E[X] = 2/3.

d) O valor esperado da variância amostral S² é σ² = p(1 - p) = 2/9.

\033[1m\033[94mCalculando com Python:\033[0m
\033[92m# Importando a biblioteca necessária\033[0m
from scipy.stats import binom

\033[92m# Definindo os parâmetros para a distribuição binomial\033[0m
n, p = 9, 2/3

\033[92m# Calculando a probabilidade acumulada (exemplo para k sucessos)\033[0m
k = 5
probabilidade = binom.cdf(k, n, p)
print(f"Probabilidade de até {k} sucessos: {probabilidade:.4f}")

\033[92m# Calculando o valor esperado e a variância da distribuição binomial\033[0m
valor_esperado = n * p
variancia = n * p * (1 - p)
print(f"Valor esperado: {valor_esperado}")
print(f"Variância: {variancia}")

\033[1m\033[94me) Para uma amostra aleatória de uma população exponencial(λ):\033[0m

a) A distribuição conjunta é dada por f(x1, ..., xn) = λ^n * exp(-λ * sum(xi)), para xi >= 0.

b) A probabilidade de todos os equipamentos durarem mais de 2 anos é (1 - FX(2))^n = exp(-2λn).

\033[92m# Calculando a probabilidade para a distribuição exponencial com Python\033[0m
from scipy.stats import expon

\033[92m# Definindo o parâmetro λ\033[0m
lambda_exp = 1/10  # Exemplo com λ = 1/10

\033[92m# Calculando a probabilidade de durar mais de 2 anos\033[0m
probabilidade_exp = expon.sf(2, scale=1/lambda_exp)
print(f"Probabilidade de durar mais de 2 anos: {probabilidade_exp:.4f}")

"""