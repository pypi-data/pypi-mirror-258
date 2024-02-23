examples = """
    \033[1mOne-sample z-test Example:\033[0m
    - \033[1mScenario:\033[0m Testing if light bulbs last 1200 hours on average. A sample of 50 bulbs
    has an average lifespan of 1180 hours.
    - \033[1mFormula:\033[0m z = (x̄ - μ) / (σ / √n)
    - \033[1mFormula Application:\033[0m z = (1180 - 1200) / (100 / sqrt(50)) = -1.41
    - \033[1mInterpretation:\033[0m Since z = -1.41, which is within the critical value of ±1.96,
    there's insufficient evidence to reject the claim that the bulbs last 1200 hours
    on average.

    \033[1mTwo-sample z-test Example:\033[0m
    - \033[1mScenario:\033[0m Comparing average test scores between two classes. Class A: avg=78, n=35.
    Class B: avg=82, n=40.
    - \033[1mFormula:\033[0m z = (x̄1 - x̄2) / √(σ1²/n1 + σ2²/n2)
    - \033[1mFormula Application:\033[0m z = (78 - 82) / sqrt(10^2/35 + 12^2/40) = -1.57
    - \033[1mInterpretation:\033[0m With z = -1.57, there's insufficient evidence to conclude a
    significant difference between the class scores.

    \033[1mProportion z-test Example:\033[0m
    - \033[1mScenario:\033[0m Testing if a website redesign increased the purchase rate from 15% to
    20% (40 out of 200 visitors).
    - \033[1mFormula:\033[0m z = (p̂ - p₀) / √(p₀(1-p₀)/n)
    - \033[1mFormula Application:\033[0m z = (0.20 - 0.15) / sqrt(0.15(1-0.15)/200) = 1.98
    - \033[1mInterpretation:\033[0m Since z = 1.98, which is slightly above 1.96, there's evidence
    suggesting a significant increase in the purchase rate after the website redesign.
"""