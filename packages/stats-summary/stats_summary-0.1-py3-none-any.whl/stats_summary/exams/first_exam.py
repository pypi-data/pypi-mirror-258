content = """

\033[1m\033[94mQuestão 1.\033[0m\033[1m Calcule:\033[0m

(a) A esperança de X é a média da distribuição de X. Se X é uma variável aleatória com distribuição conhecida, 
a esperança é o valor médio esperado conforme essa distribuição.

(b) A variância de X mede o grau de dispersão dos valores de X em torno da sua média. 
Se X é uma variável aleatória com distribuição conhecida, a variância é a média dos quadrados das diferenças entre os valores de X e a média de X.

(c) Um estimador é dito viciado se sua esperança (ou média) não é igual ao parâmetro que ele estima. 
Sem mais informações sobre como X está sendo usado para estimar um parâmetro, não podemos determinar se é viciado ou não.


\033[1m\033[94mQuestão 2.\033[0m\033[1m Por que o Teorema Central do Limite é tão importante para a estatística?\033[0m

O Teorema Central do Limite é importante porque garante que, sob condições bastante gerais, 
a distribuição da média amostral se aproxima de uma distribuição normal à medida que o tamanho da amostra aumenta, 
independente da forma da distribuição da população. Isso facilita a inferência estatística para médias amostrais e outras estatísticas relacionadas.


\033[1m\033[94mQuestão 3.\033[0m\033[1m Seja X a média de uma amostra aleatória de tamanho 100 de uma distribuição Normal com média µ = 10 e σ² = 4. 
Calcule um valor aproximado para a seguinte probabilidade P(6.2 < X < 12.6).\033[0m

1) Definimos a variável aleatória X como sendo a média da amostra de tamanho n=100 da população normalmente distribuída com média µ=10 e variância σ²=4.

2) A distribuição da média amostral X pode ser aproximada por uma distribuição normal devido ao tamanho da amostra (n=100) ser grande.

3) A variável padronizada Z para a média amostral X é dada por Z = (X - µ) / (σ/√n). 
Usamos esta transformação para calcular as probabilidades com a distribuição normal padrão.

4) Calculamos Z para os limites dados: Z_6.2 para X=6.2 e Z_12.6 para X=12.6.

5) Usamos a distribuição normal padrão para calcular P(Z_6.2 < Z < Z_12.6), que é a mesma que P(6.2 < X < 12.6).

6) A probabilidade encontrada nos dá uma aproximação da chance de a média amostral X estar entre 6.2 e 12.6.

\033[93m# Exemplo de cálculo hipotético (os valores de Z devem ser determinados a partir dos dados ou tabelas da distribuição normal padrão):\033[0m
# Z_6.2 = (6.2 - 10) / (2/√100) = (6.2 - 10) / 0.2 = -19
# Z_12.6 = (12.6 - 10) / (2/√100) = (12.6 - 10) / 0.2 = 13
# Portanto, P(6.2 < X < 12.6) = P(-19 < Z < 13) = P(Z < 13) - P(Z < -19), o que pode ser encontrado usando uma tabela Z ou software estatístico.

\033[93m# Cálculo com Python:\033[0m
\033[92m# Importamos as bibliotecas necessárias\033[0m
from scipy.stats import norm
import numpy as np

\033[92m# Definimos a média (mu) e a variância (sigma^2) da população\033[0m
mu = 10
sigma_squared = 4
n = 100
sigma = np.sqrt(sigma_squared)

\033[92m# Calculamos o desvio padrão da média amostral\033[0m
std_error = sigma / np.sqrt(n)

\033[92m# Calculamos os valores Z para 6.2 e 12.6\033[0m
z_6_2 = (6.2 - mu) / std_error
z_12_6 = (12.6 - mu) / std_error

\033[92m# Calculamos a probabilidade usando a distribuição normal cumulativa\033[0m
prob_lower = norm.cdf(z_6_2, 0, 1)  \033[93m# P(Z < z_6_2)\033[0m
prob_upper = norm.cdf(z_12_6, 0, 1)  \033[93m# P(Z < z_12_6)\033[0m

\033[92m# A probabilidade desejada é P(6.2 < X < 12.6)\033[0m
probability = prob_upper - prob_lower


\033[1m\033[94mQuestão 4.\033[0m\033[1m Quais os tipos de erros de um teste de hipóteses?\033[0m

Em um teste de hipóteses, podemos cometer dois tipos de erros. 
O Erro Tipo I ocorre quando rejeitamos a hipótese nula sendo ela verdadeira. 
O Erro Tipo II acontece quando aceitamos a hipótese nula sendo ela falsa. 

Por exemplo, se um pesquisador rejeita a hipótese de que uma moeda é justa baseando-se em um resultado de amostra, mas a moeda é realmente justa, 
ele cometeu um Erro Tipo I.


\033[1m\033[94mQuestão 5.\033[0m\033[1m Explique com suas palavras o que é o estimador de máxima verossimilhança.\033[0m

O estimador de máxima verossimilhança é um método estatístico que encontra o valor do parâmetro de um modelo estatístico que torna a 
amostra observada mais provável. Ele maximiza a função de verossimilhança, que é a probabilidade de obter os dados observados dado um conjunto de parâmetros.


\033[1m\033[94mQuestão 6.\033[0m\033[1m Suponha que o tempo médio de terapia tradicional em pacientes com depressão seja de
pelo menos 2 anos. Admita ainda que se pretenda testar um tipo de terapia alternativa cujo tempo
de recuperação esperado seja menor que o tradicional. Realizou-se um experimento com 20 pacientes
submetidos à nova terapia e obteve-se os seguintes resultados: x = 1.7 e s² = 1. Com base nestas
informações e considerando que o tempo médio de terapia é uma variável aproximadamente simétrica,
utilize um teste de hipóteses com α = 0.1 para testar a hipótese que a nova terapia funciona.\033[0m

Resposta: Aplicamos um teste t unicaudal para a média com o nível de significância α = 0.1. 
A hipótese nula é que o tempo médio de terapia com o novo método é pelo menos 2 anos. 
A estatística de teste é calculada e, se o p-valor for menor que 0.1, rejeitamos a hipótese nula, indicando que a nova terapia pode ser mais eficaz.


\033[1m\033[94mQuestão 7.\033[0m\033[1m Deseja-se verificar a proporção de agentes penitenciários que sofrem de problemas psicológicos. 
Em uma amostra de 50 agentes verificou-se que 35 sofriam de depressão. Através de um intervalo de confiança de 98% podemos afirmar que 
a maioria dos agentes penitenciários sofre de depressão? Interprete o resultado do intervalo.\033[0m

Resposta: Calculamos o intervalo de confiança para a proporção usando a fórmula para proporção de amostras grandes com zα/2 correspondente a 98% de confiança. 
Se o intervalo de confiança não incluir 50%, podemos afirmar com 98% de confiança que a maioria dos agentes sofre de depressão. 
A interpretação do intervalo de confiança nos dirá se a afirmação é suportada estatisticamente.

\033[1mPASSOS PARA CONSTRUÇÃO DOS TESTE DE HIPÓTESES\033[0m
1) Defina as hipóteses nula e alternativa.
2) Escolha o teste estatístico apropriado.
3) Estabeleça o nível de significância e determine a região crítica.
4) Calcule a estatística de teste e o p-valor.
5) Aceite ou rejeite a hipótese nula baseando-se na região crítica e no p-valor.
6) Apresente a conclusão experimental baseando-se nos resultados.

\033[1mINTERVALO DE CONFIANÇA\033[0m
Para a média: x ± zα/2 (σ/√n)
Para a média com desvio padrão amostral: x ± tα/2 (s/√n)

"""