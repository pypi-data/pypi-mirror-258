examples = """
    \033[1mWilcoxon Signed-Rank Test Example:\033[0m
    - \033[1mScenario:\033[0m Testing whether there's a significant difference in the median daily
    calorie intake before and after following a specific diet plan for a group of individuals.
    - \033[1mFormula:\033[0m The test statistic is W, which is the sum of the ranks of the positive
    differences between pairs. The calculation involves ranking the absolute differences, assigning
    signs based on the direction of the difference, and then summing the ranks for the positive differences.
    - \033[1mFormula Application:\033[0m Hypothetically, if the sum of ranks for the positive differences
    (after - before) is 120 and the number of pairs is 30, we would consult a Wilcoxon signed-rank
    table or use software to determine the significance based on W = 120.
    - \033[1mInterpretation:\033[0m Depending on the critical value for W from the Wilcoxon signed-rank
    table for n = 30 and a chosen significance level (e.g., α = 0.05), we determine if there's a
    significant difference in median calorie intake. If W is less than the critical value, we reject
    the null hypothesis, indicating a significant difference in medians before and after the diet.
"""
