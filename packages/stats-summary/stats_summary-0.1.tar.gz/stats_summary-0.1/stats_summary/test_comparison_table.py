comparison_table = """
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Test Name               | When to Use                                      | Use Cases                                          | Paired/Not-Paired | Known Variance | Parametric/Non-Parametric |
|-------------------------|--------------------------------------------------|----------------------------------------------------|-------------------|----------------|---------------------------|
| z-Test                  | Large sample sizes, known population variance.   | Proportions, mean comparison to a population mean. | Not-paired        | Yes            | Parametric                |
|                         |                                                  |                                                    |                   |                |                           |
| t-Test                  | Unknown population variance, small sample sizes. | Comparing means between two groups.                | Both              | No             | Parametric                |
|                         |                                                  |                                                    |                   |                |                           |
| Paired t-Test           | Comparing means of related samples.              | Before and after measurements, matched subjects.   | Paired            | No             | Parametric                |
|                         |                                                  |                                                    |                   |                |                           |
| ANOVA                   | Comparing means across three or more groups.     | Effect of a categ. variable on a contin. outcome.  | Not-paired        | No             | Parametric                |
|                         |                                                  |                                                    |                   |                |                           |
| Kruskal-Wallis Test     | Non-normal data, comparing three or more groups. | Non-parametric alternative to ANOVA.               | Not-paired        | N/A            | Non-Parametric            |
|                         |                                                  |                                                    |                   |                |                           |
| Mann-Whitney U Test     | Non-normal data, comparing 2 independent samples.| Non-parametric alternative to ind. samples t-test. | Not-paired        | N/A            | Non-Parametric            |
|                         |                                                  |                                                    |                   |                |                           |
| Wilcoxon Signed-Rank    | Non-normal data, comparing two related samples.  | Non-parametric alternative to paired t-test.       | Paired            | N/A            | Non-Parametric            |
|                         |                                                  |                                                    |                   |                |                           |
| Friedman Test           | Repeated measures over three or more conditions. | Non-param. alternative to repeated measures ANOVA. | Paired            | N/A            | Non-Parametric            |
|                         |                                                  |                                                    |                   |                |                           |
| Chi-Square Test         | Categorical data.                                | Testing independence, goodness-of-fit.             | Not-paired        | N/A            | Non-Parametric            |
|                         |                                                  |                                                    |                   |                |                           |
| F-test                  | Comparing variances, regression analysis signif. | Variance equality across groups, model significan. | Not-paired        | Yes            | Parametric                |
|                         |                                                  |                                                    |                   |                |                           |
| Kolmogorov-Smirnov Test | Comparing a sample with a ref distr. or 2 sampl. | Goodness-of-fit, two-sample comparison.            | Not-paired        | N/A            | Non-Parametric            |
|                         |                                                  |                                                    |                   |                |                           |
| Correlation             | Assessing the relationship between two variables | Direction and strength of association.             | N/A               | N/A            | Both (depends on method)  |
| (Pearson, Spearman,     |                                                  |                                                    |                   |                |                           |
| Kendall)                |                                                  |                                                    |                   |                |                           |
|                         |                                                  |                                                    |                   |                |                           |
| Regression              | Predicting a dep. variable from ind. variables.  | Modeling relationships, forecasting.               | N/A               | N/A            | Parametric                |
| (Linear, Logistic, etc.)|                                                  |                                                    |                   |                |                           |
|                         |                                                  |                                                    |                   |                |                           |
| Time Series Analysis    | Data collected over time.                        | Trend analysis, seasonal effect measurement, forec | N/A               | N/A            | Both (depends on method)  |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

"""