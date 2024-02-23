wilcoxon = """

To calculate the Wilcoxon test, also known as the Wilcoxon Rank-Sum Test or Wilcoxon Mann-Whitney Test for independent samples, 
or the Wilcoxon Signed-Rank Test for paired samples, we'll go through both processes with applied examples. 
The choice of test depends on the study design.

### Wilcoxon Signed-Rank Test (Paired Samples)

The Wilcoxon Signed-Rank Test is used when you have two related samples, matched samples, or repeated measurements on a 
single sample to assess whether their population mean ranks differ (i.e., it's a non-parametric alternative to the paired t-test).

#### Example Problem:

Suppose we have data on 8 patients' blood pressure before and after a new medication. 
We want to test if the medication significantly affects blood pressure.

**Data:**

| Patient | Before | After |
|---------|--------|-------|
| 1       | 120    | 112   |
| 2       | 122    | 118   |
| 3       | 130    | 123   |
| 4       | 135    | 130   |
| 5       | 140    | 135   |
| 6       | 126    | 124   |
| 7       | 144    | 140   |
| 8       | 150    | 145   |

#### Steps:

1. **Calculate Differences**: Subtract the Before value from the After value for each pair.
2. **Rank the Differences**: Ignore the signs and rank the absolute differences from smallest to largest.
3. **Assign Signs to Ranks**: Give ranks their original signs (positive or negative based on whether the change was an 
increase or decrease).
4. **Sum Positive and Negative Ranks**: Calculate the sum of positive ranks (\(W^+\)) and the sum of negative ranks (\(W^-\)).
5. **Test Statistic**: The smaller of \(W^+\) and \(W^-\) is the test statistic.
6. **Critical Value or p-value**: Compare the test statistic to a Wilcoxon Signed-Rank table or calculate a p-value, 
depending on sample size and the significance level (\(\alpha\)) you are testing against.

#### Calculation:

Let's calculate the Wilcoxon Signed-Rank Test for our example.

**Step 1: Calculate Differences**

| Patient | Before | After | Difference |
|---------|--------|-------|------------|
| 1       | 120    | 112   | -8         |
| 2       | 122    | 118   | -4         |
| 3       | 130    | 123   | -7         |
| 4       | 135    | 130   | -5         |
| 5       | 140    | 135   | -5         |
| 6       | 126    | 124   | -2         |
| 7       | 144    | 140   | -4         |
| 8       | 150    | 145   | -5         |

**Step 2 to 5: Rank the Differences and Calculate Test Statistic**

Let's perform these steps using Python to rank the differences, assign signs, sum ranks, and find the test statistic.

Based on the calculations:

- The signed ranks for the differences are as follows: \([-8.0, -2.5, -7.0, -5.0, -5.0, -1.0, -2.5, -5.0]\).
- The sum of positive ranks (\(W^+\)) is \(0.0\), indicating no positive differences.
- The sum of negative ranks (\(W^-\)) is \(36.0\).

Since the test statistic is the smaller of \(W^+\) and \(W^-\), our test statistic is \(0.0\).

#### Step 6: Critical Value or p-value

To determine if the observed difference is statistically significant, we compare the test statistic to a critical value from the 
Wilcoxon Signed-Rank table or calculate a p-value. Given the small sample size, we would typically refer to a critical value table 
specific to the Wilcoxon Signed-Rank Test for a two-tailed test at a common significance level (e.g., \(\alpha = 0.05\)).

However, with modern statistical software, we can directly calculate the p-value:

Let's calculate the p-value for our test statistic.

The calculated test statistic \(W\) is \(0.0\) with a p-value of \(0.0078125\).

#### Conclusion:

Since the p-value (\(0.0078125\)) is less than the common alpha level of \(0.05\), we reject the null hypothesis. 
This suggests that there is a statistically significant difference in blood pressure before and after the medication, 
indicating that the medication has a significant effect on lowering blood pressure.

### Wilcoxon Rank-Sum Test (Independent Samples)

The Wilcoxon Rank-Sum Test is used for comparing two independent samples to assess whether their population mean ranks differ. 
It is the non-parametric alternative to the independent samples t-test.

If you're interested in a step-by-step example for the Wilcoxon Rank-Sum Test as well, let me know!

"""

mann_whitney = """
For the Wilcoxon Rank-Sum Test, which is also known as the Mann-Whitney U test when applied to independent samples, 
we'll work through an applied problem step by step. This test is used to compare two independent samples to determine if they
come from the same distribution. It's a non-parametric alternative to the independent samples t-test and is used when the
assumptions of the t-test are not met.

### Example Problem:

Suppose we have data from two different groups of plants, Group A and Group B, measuring some growth metric after applying different
 fertilizers. We want to test if there's a significant difference in the growth metric between the two groups.

**Data:**

- **Group A (Fertilizer 1):** 15, 12, 14, 11, 19, 13, 12
- **Group B (Fertilizer 2):** 14, 18, 17, 20, 16, 15, 18

### Steps to Perform Mann-Whitney U Test:

1. **Combine and Rank the Data**: Combine both groups into one dataset and rank the observations from smallest to largest, 
regardless of which group they belong to.

2. **Calculate U for Each Group**: The U statistic for each group is calculated by summing the ranks for that group and then 
subtracting the minimum possible rank sum for that group. The formula for U is:
   \[
   U = R - \frac{n(n+1)}{2}
   \]
   where \(R\) is the sum of ranks for the group, and \(n\) is the number of observations in the group.

3. **Determine the Test Statistic**: The smaller of the two U values is the test statistic used in the Mann-Whitney U test.

4. **Significance Testing**: Use tables or software to determine the significance of the observed U statistic, based on the 
sample sizes of the two groups. The null hypothesis \(H_0\) is that there is no difference between the two groups.

Let's calculate the Mann-Whitney U test for our example problem using Python to perform the calculations.

The Mann-Whitney U test statistic for our data is \(8.0\) with a p-value of \(0.04003\).

### Conclusion:

The p-value (\(0.04003\)) is less than the commonly used alpha level of \(0.05\), which suggests that we can reject the 
null hypothesis. This indicates that there is a statistically significant difference in the growth metrics between the two 
groups of plants treated with different fertilizers. Therefore, we conclude that the effect of the fertilizers on plant 
growth is significantly different between Group A and Group B.

"""

kolmogorv = """

The Kolmogorov-Smirnov (K-S) test is a non-parametric test used to determine whether two samples come from the same 
distribution, or to compare a sample with a reference probability distribution (one-sample K-S test). It compares the 
cumulative distributions of the two samples or a sample and a reference distribution. The test is useful for comparing 
theoretical distributions with empirical data or for comparing two empirical data sets without making assumptions about 
the distribution of data.

### Example Problem: Comparing Two Empirical Data Sets

Let's say we have two groups of data representing two different treatments applied to plants, and we want to test if 
the growth rate distributions of these two treatments are significantly different.

**Data:**

- **Treatment 1:** 20, 22, 19, 20, 21, 20, 22
- **Treatment 2:** 23, 25, 24, 22, 26, 24, 23

We will perform a two-sample K-S test on these data sets.

### Steps to Perform Kolmogorov-Smirnov Test:

1. **Sort the Data**: Each dataset should be sorted in ascending order.

2. **Calculate the Cumulative Distribution Function (CDF)** for each dataset. The CDF at a point \(x\) is the proportion 
of values less than or equal to \(x\).

3. **Compute the K-S Statistic**: This is the maximum absolute difference between the CDFs of the two datasets. 
The K-S statistic, \(D\), is given by:
   \[
   D = \max_{x} |F_1(x) - F_2(x)|
   \]
   where \(F_1(x)\) and \(F_2(x)\) are the empirical distribution functions of the first and second datasets, respectively.

4. **Significance Testing**: Determine the critical value of \(D\) for the sample sizes of the two groups at a chosen 
significance level (\(\alpha\)). Alternatively, calculate a p-value to determine the significance of the observed \(D\). 
If the calculated or observed \(D\) is greater than the critical value, or if the p-value is less than \(\alpha\), 
reject the null hypothesis that the two samples come from the same distribution.

Let's calculate the two-sample Kolmogorov-Smirnov test for our example using Python.

The Kolmogorov-Smirnov test statistic for comparing the two treatments is \(0.8571\) with a p-value of \(0.00816\).

### Conclusion:

The p-value (\(0.00816\)) is less than the commonly used alpha level of \(0.05\), suggesting that we can reject the
null hypothesis. This indicates that there is a statistically significant difference between the growth rate distributions 
of the two treatments. Therefore, we conclude that the effects of the treatments on plant growth rates are 
significantly different.

"""

friedman = """

The Friedman test is a non-parametric statistical test used to detect differences in treatments across multiple test attempts. 
It's essentially the non-parametric version of the one-way ANOVA with repeated measures. This test is applicable 
when you have two or more dependent samples with measurements made on the same subjects. It's particularly useful 
when the data do not meet the assumptions necessary for ANOVA, such as normally distributed residuals or homogeneity of variances.

### Example Problem:

Imagine we conducted an experiment to evaluate the effectiveness of three different teaching methods on the same group
of students. Each student was taught with each method, and their performance was scored. We want to test if there is a 
statistically significant difference in the median performance scores across the three teaching methods.

**Data:**

Here are the performance scores of 5 students across the three teaching methods:

- **Method 1:** 85, 80, 70, 90, 95
- **Method 2:** 88, 77, 78, 95, 92
- **Method 3:** 75, 85, 80, 80, 90

### Steps to Perform the Friedman Test:

1. **Rank the Scores for Each Student**: Within each row (representing each student), rank the scores from 1 to the 
number of methods (in this case, 1 to 3), with 1 being the lowest score.

2. **Calculate the Sum of Ranks for Each Method**: Sum the ranks for each teaching method across all students.

3. **Calculate the Friedman Test Statistic**: The test statistic is calculated using the formula:
   \[
   \chi^2_F = \frac{12N}{k(k+1)}\left[\sum R^2_j - \frac{k(k+1)^2}{4}\right]
   \]
   where \(N\) is the number of subjects (students), \(k\) is the number of groups (teaching methods), \(R_j\) is the sum 
   of ranks for the \(j^{th}\) group, and \(\chi^2_F\) is the Friedman statistic.

4. **Determine Significance**: Compare the calculated \(\chi^2_F\) value to the critical value from the \(\chi^2\) 
distribution with \(k-1\) degrees of freedom at the chosen significance level (\(\alpha\)). 
Alternatively, compute a p-value to assess significance.

Let's calculate the Friedman test for our example problem using Python.

The Friedman test statistic for comparing the three teaching methods is \(0.40\) with a p-value of \(0.8187\).

### Conclusion:

The p-value (\(0.8187\)) is much greater than the commonly used alpha level of \(0.05\), suggesting that we fail to 
reject the null hypothesis. This indicates that there is no statistically significant difference in the median performance 
scores across the three teaching methods based on our sample data. Therefore, we conclude that the effects of the teaching 
methods on student performance are not significantly different from each other within this group of students.

"""

examples = {
    'wilcoxon': wilcoxon,
    'mann_whitney': mann_whitney,
    'kolmogorv': kolmogorv,
    'friedman': friedman
}

