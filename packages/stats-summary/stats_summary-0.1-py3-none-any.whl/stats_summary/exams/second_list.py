content = """

\033[1m\033[94m1. Encontrando l tal que P(−l < X − µ < l) = 0.9\033[0m
Usando o TLC, achamos que X segue aproximadamente uma Normal(0, 1). Para P(−l < X − µ < l) = 0.9, 
precisamos encontrar os quantis de uma Normal padrão que correspondam a essa probabilidade. Assumindo σ = 2 e n = 100, l é calculado como:

\033[92m# Código Python para encontrar l\033[0m
from scipy.stats import norm
l = norm.ppf(0.95) * 2 / (100**0.5)
print(f"l aproximado: {l:.3f}")

\033[1m\033[94m2. Tamanho da amostra para a média amostral não difira da média populacional por mais de 25% do desvio padrão\033[0m
Para garantir que a média amostral esteja dentro de 25% do desvio padrão da média populacional com 95% de probabilidade, 
calculamos o tamanho da amostra necessário usando o inverso da função de distribuição acumulada da Normal padrão:

\033[92m# Código Python para calcular o tamanho da amostra\033[0m
z = norm.ppf(0.975)
n = (2 * z / 0.25)**2
print(f"Tamanho da amostra necessário: {n:.0f}")

\033[1m\033[94m3. Probabilidade P(0.45 < X < 0.55) para uma amostra de tamanho 75\033[0m
Com X seguindo uma distribuição Uniforme(0, 1), e µ = 0.5, σ = 1/√12, a probabilidade é calculada aproximando X para uma Normal(0, 1) usando o TLC:

\033[92m# Código Python para calcular a probabilidade\033[0m
sigma = (1/12)**0.5
z_lower = (0.45 - 0.5) / (sigma / (75**0.5))
z_upper = (0.55 - 0.5) / (sigma / (75**0.5))
probabilidade = norm.cdf(z_upper) - norm.cdf(z_lower)
print(f"Probabilidade aproximada: {probabilidade:.4f}")

\033[1m\033[94m4. Aproximação para P(47.5 < Y < 52.5) usando o TLC para uma amostra Bernoulli(p)\033[0m
Com Y ∼ Binomial e transformando Y para uma distribuição aproximadamente Normal, calculamos a probabilidade desejada:

\033[92m# Código Python para calcular a probabilidade\033[0m
n, p = 100, 0.5
sigma_Y = (n * p * (1 - p))**0.5
z = (52.5 - n*p) / sigma_Y
probabilidade = norm.cdf(z) - norm.cdf(-z)
print(f"Probabilidade aproximada: {probabilidade:.4f}")

\033[1m\033[94m5. Probabilidade P(Y/n > 0.25) para Y ∼ Binomial(400, 1/5)\033[0m
Calculamos a probabilidade usando o TLC para aproximar a distribuição de Y/n para uma Normal:

\033[92m# Código Python para calcular a probabilidade\033[0m
n, p = 400, 1/5
sigma_Y_n = ((p * (1 - p)) / n)**0.5
z = (0.25 - p) / sigma_Y_n
probabilidade = 1 - norm.cdf(z)
print(f"Probabilidade de Y/n > 0.25: {probabilidade:.4f}")

\033[1m\033[94m6. Probabilidade de mais de 50 observações serem menores que 3\033[0m
Primeiro, encontramos P(X < 3) para uma distribuição com f(x) = 1/x², I(1,

∞)(x), e então calculamos a probabilidade desejada para a amostra:

\033[92m# Código Python para calcular P(X < 3)\033[0m
prob_X_less_3 = 1 - 1/3
\033[92m# Usando Binomial para calcular P(Y > 50)\033[0m
from scipy.stats import binom
prob_Y_more_50 = 1 - binom.cdf(50, 72, prob_X_less_3)
print(f"Probabilidade de mais de 50 observações < 3: {prob_Y_more_50:.4f}")

"""
