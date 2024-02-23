content = """

\033[1m\033[94mQuestão 1.\033[0m\033[1m Qual a diferença entre estatística paramétrica e não paramétrica?

\033[0mA estatística paramétrica busca estimar parâmetros populacionais, como a média e a variância. Além
disso, nesse tipo de inferência, a distribuição dos estimadores é conhecida, assim como as suposições
necessárias para que o estimador convirja ou possua determinadas propriedades. Como no TCL, que
supondo variância finita e uma amostra suficientemente grande, garante que a distribuição da média
amostral converge para uma distribuição conhecida, a normal, de média µ e variância σ²/n. Na inferência
não paramétrica, não se busca estimar parâmetros desconhecidos, além disso, não são feitas suposições
com relação à população, são métodos mais flexíveis.

\033[1m\033[94mQuestão 2.\033[0m\033[1m Em um teste de hipóteses para comparação de um vetor de médias (H0 : µ1 = µ2) foi
observado um p-valor de 0,029. O pesquisador do estudo escreveu a seguinte conclusão:\033[0m "há 2,9% de
probabilidade de do vetor de médias serem iguais e 97,1% de probabilidade de serem diferentes". 
A conclusão do pesquisador está correta?

Está incorreta, o p-valor não é a probabilidade de H0 ser verdade. A interpretação correta é: Dado
que H0 é verdade (não há diferença entre as médias), 0,029 de probabilidade de ocorrer a diferença de
média observada ou uma diferença mais extrema.

\033[1m\033[94mQuestão 3.\033[0m\033[1m Os testes paramétricos são mais poderosos que os testes não paramétricos? Justifique a sua
resposta?
\033[0mSim, eles são mais poderosos, pois fazem mais suposições. Os testes não paramétricos são mais flexíveis
e não precisam respeitar os mesmos pressupostos dos testes paramétricos que dependem de algum tipo
de parâmetro. Logo, é mais difícil captar diferenças significativas, isto é, a probabilidade de rejeitar H0
dado que ele é falso nos testes paramétricos é maior que nos testes não paramétricos.

\033[1m\033[94mQuestão 4.\033[0m\033[1m Suponha que você é um cientista de dados trabalhando em uma empresa de transporte de
mercadorias. A empresa está interessada em analisar o tempo que leva para os motoristas entregarem os
produtos em diferentes regiões. Você coletou uma amostra de 15 observações sobre o tempo de entrega
de motoristas em uma rota específica.

\033[0mAmostra: 3 8 21 6 10 0.5 45 1 9 25 3 8 2 7 25 4

Teste a hipótese de que o tempo de entrega segue uma distribuição exponencial de parâmetro λ = 1/10.

1) F0 = Exp(1/10) vs F0 ≠ Exp(1/10)
2) Teste de Kolmogorov Smirnov
3) α = 0,03
4) Estatística de teste (nesse exercício, como eu não defini o tipo de parametrização da exponencial
se f(x) = exp−λx ou f(x) = 1/λ exp−1/λx considerei as duas respostas como certas)
D = 0.99326, p-value = 3.897e-14 ou D = 0.12754, p-value = 0.9571
5) Aceita H0
6) Há evidências que os dados seguem uma distribuição exponencial.

\033[1m\033[94mQuestão 5.\033[0m\033[1m Um estudo comparativo foi conduzido entre dois grupos de adolescentes que jogam videogames
regularmente. Um grupo dedicou horas extras à prática, enquanto o outro grupo utilizou técnicas de relaxamento, como meditação ou exercícios de respiração, antes de jogar. Após um período de tempo definido,
os participantes foram avaliados quanto ao seu desempenho em uma série de jogos. 
Considerando que as duas variáveis possuem distribuição aproximadamente simétrica, avalie se há diferença entre os métodos, utilize um α = 0,02.\033[0m

1) µextra = µrelaxamento vs µextra ≠ µrelaxamento
2) Teste para comparação de média de duas populações com variâncias iguais.
3) α = 0,02 RC = -2,36 e 2,36

\033[92mTable 1: Estatísticas do desempenho dos jogadores\033[0m
Grupo horas extras 1 n=50 x = 80 s² = 20
Grupo técnicas de relaxamento n=40 x = 70 s² = 20
4) t = 13 p-valor ≈ 0
5) Rejeito H0, pvalor < α
6) Deve haver diferença entre os métodos, há evidências de que as horas extras possuem um desempenho médio superior às técnicas de relaxamento.

\033[1m\033[94mQuestão 6.\033[0m\033[1m Suponha que você está conduzindo um estudo para avaliar o impacto de um novo algoritmo
de recomendação de amigos em uma plataforma. 

O objetivo é determinar se o novo algoritmo aumenta
o número médio de novos amigos adicionados por usuário.\033[0m

Você coletou dados de 10 usuários e contabilizou o número de novos amigos que eles adicionaram um
mês antes da implementação do algoritmo e um mês depois da implementação do novo algoritmo.

\033[92mTable 2: Dados de Novos Amigos Adicionados em Redes Sociais\033[0m
Usuário Novos Amigos antes Novos Amigos depois
    1    5    8
    2    7    9
    3    6    8
    4    8    10
    5    6    8
    6    5    7
    7    9    12
    8    10   13
    9    7    9
    10   6    8

Sabendo que as variáveis possuem distribuição normal, calcule um intervalo de confiança de 95%,
interprete o intervalo. O novo algoritmo funciona?

Intervalo de confiança para a média de amostras pareadas
xd = −2, 3 s²d = 0, 233
n = 10
α = 0, 05
tα/2 = −2, 26 e gl = 9
xd ± tα/2 √sd/n
−2, 3 ± 2, 26 0,48 √10 = −2, 3 ± 0, 34
IC com 95% é [−2, 64; −1, 96]

Com 95% de confiança o intervalo [−2, 64; −1, 96] contem a média da diferença entre a quantidade de
novos amigos dos dois algoritmos. Como o intervalo não contém o valor zero e a diferença é negativa,
há evidências de que o novo algoritmo funciona, visto que aumenta o número de amigos novos de um
usuário.

\033[1m\033[94mQuestão 7.\033[0m\033[1m Suponha que você está conduzindo um estudo para comparar duas plataformas de produção
musical online, a BeatMaster e a MelodiaFlow, em termos de tempo médio gasto pelos usuários na criação
de uma faixa musical completa. A plataforma BeatMaster oferece uma interface tradicional de produção
musical, enquanto a plataforma MelodiaFlow oferece recursos avançados de inteligência artificial para
acelerar o processo de criação.\033[0m

Você coletou dados de 10 usuários de cada plataforma sobre o tempo gasto na produção de uma faixa
musical completa, os dados estão indicados na tabela abaixo:

Avalie se o método utilizando inteligência artificial é mais eficiente que o tradicional, para isso faça
um teste de hipóteses e utilize α = 0, 03.

\033[92mTable 3: Minutos gastos pelo usuário\033[0m
Usuários MelodiaFlow 66 62 52 63 62 70 52 20 40 30
Usuários BeatMaster 72 80 63 65 80 80 80 40 30 25

1) as duas amostras vêm da mesma população vs a mediana do MelodiaFlow é inferior a mediana do BeatMaster
2) Teste não paramétrico para comparação de duas populações independentes Wilcoxon, teste de Mann-Whitney ou teste U de Mann-Whitney
3) α = 0, 03
4) wilcox.test(melodia, beat, alternative = c("less"), paired = FALSE, exact = TRUE)
W = 29.5, p-value = 0.0642
5) Aceito H0, pvalor < α
6) Não há evidências de que o método de inteligência artificial (MelodiaFlow) seja mais eficiente que
o método tradicional (BeatMaster).

\033[1mPASSOS PARA CONSTRUÇÃO DOS TESTE DE HIPÓTESES\033[0m
1) Defina as hipóteses
2) Indique o teste que deve ser utilizado
3) Dado o nível de significância indique a região crítica
4) Calcule a estatística de teste e o p-valor
5) Aceite ou Rejeite a hipótese nula
6) Conclusão experimental
"""
