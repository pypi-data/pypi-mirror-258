examples = """
    \033[1mOne-sample t-test Example:\033[0m
    - \033[1mScenario:\033[0m Testing if the average height of a sample of students is different from the national average height of 170 cm.
    - \033[1mFormula:\033[0m t = (x̄ - μ) / (s / √n)
    - \033[1mFormula Application:\033[0m Hypothetically, t = (168 - 170) / (10 / sqrt(30)) = -1.09
    - \033[1mInterpretation:\033[0m Since t is within the critical value range, there's insufficient evidence to reject the null hypothesis that the sample mean is the same as the national average.

    \033[1mTwo-sample (independent) t-test Example:\033[0m
    - \033[1mScenario:\033[0m Comparing the average test scores of students from two different schools.
    - \033[1mFormula:\033[0m t = (x̄1 - x̄2) / √(s1²/n1 + s2²/n2)
    - \033[1mFormula Application:\033[0m Hypothetically, t = (75 - 80) / sqrt((15^2/50) + (20^2/50)) = -1.89
    - \033[1mInterpretation:\033[0m With t = -1.89, there's insufficient evidence to conclude a significant difference in average test scores.

    \033[1mPaired-sample t-test Example:\033[0m
    - \033[1mScenario:\033[0m Testing the effect of a study app on the scores of students by comparing their scores before and after using the app.
    - \033[1mFormula:\033[0m t = (d̄ - μd) / (sd / √n), where d̄ is the mean difference, and μd is the hypothesized mean difference (often 0).
    - \033[1mFormula Application:\033[0m Hypothetically, t = (5 - 0) / (10 / sqrt(30)) = 3.16
    - \033[1mInterpretation:\033[0m Since t = 3.16, which is beyond the critical value, there's evidence suggesting a significant effect of the study app on scores.
"""
