summary = """
    The Mann-Whitney U test is a non-parametric statistical test used to compare TWO INDEPENDENT samples to 
    determine whether there is a difference in their central tendency, specifically their MEDIANS. 
    It is particularly useful in the following contexts:

    * Non-Normal Distribution: When the data do not follow a normal distribution, which violates the assumption
    required for parametric tests like the t-test.

    * Ordinal Data: The test can be applied to ordinal data, where the data can be ranked but the intervals between 
    ranks are not necessarily equal.

    * Unequal Variances: It is also appropriate when the two groups have variances that are not assumed to be equal, 
    another assumption underlying many parametric tests.

    * Small Sample Sizes: The Mann-Whitney U test can be used for small sample sizes, where the central limit theorem might not apply, 
    and thus, normality cannot be assumed.

    The test works by ranking all the observations from both groups together and then comparing the sums of ranks between the groups. 
    The null hypothesis of the Mann-Whitney U test is that the distributions of both groups are equal. 
    If the test finds a significant difference in the sum of ranks, it suggests that one group tends to have higher or lower 
    values than the other, indicating a difference in their distributions.
"""
