from . import thorough_examples
from .code_snippets.t_test import code_snippet as t_test_code_snippets
from .code_snippets.z_test import code_snippet as z_test_code_snippets
from .code_snippets.friedman import code_snippet as friedman_code_snippets
from .code_snippets.wilcoxon import code_snippet as wilcoxon_code_snippets
from .code_snippets.mann_whitney import code_snippet as mann_whitney_code_snippets
from .code_snippets.kruskall import code_snippet as kruskall_code_snippets
from .code_snippets.kolmogorov import code_snippet as kolmogorov_code_snippets
from .code_snippets.confidence_intervals import code_snippet as confidence_intervals_code_snippets
from .summaries.mann_whitney import summary as mann_whitney_summary
from .summaries.z_test import summary as z_test_summary
from .summaries.t_test import summary as t_test_summary
from .summaries.f_test import summary as f_test_summary
from .summaries.wilcoxon import summary as wilcoxon_summary
from .summaries.anova import summary as anova_summary
from .summaries.kruskall import summary as kruskall_summary
from .summaries.friedman import summary as friedman_summary
from .summaries.correlation import summary as correlation_summary
from .summaries.regression import summary as regression_summary
from .summaries.time_series import summary as time_series_summary
from .summaries.chi_square import summary as chi_square_summary
from .examples.z_test import examples as z_test_examples
from .examples.t_test import examples as t_test_examples
from .examples.f_test import examples as f_test_examples
from .examples.wilcoxon import examples as wilcoxon_examples
from .examples.mann_whitney import examples as mann_whitney_examples

summaries = {
    "mann-whitney-test": mann_whitney_summary,
    "z-test": z_test_summary,
    "t-test": t_test_summary,
    "f-test": f_test_summary,
    "chi-square-test": chi_square_summary,
    "wilcoxon-test": wilcoxon_summary,
    "anova": anova_summary,
    "kruskal-wallis-test": kruskall_summary,
    "friedman-test": friedman_summary,
    "correlation": correlation_summary,
    "regression": regression_summary,
    "time-series": time_series_summary,
}

code_examples = {
    "mann-whitney-test": mann_whitney_code_snippets,
    "wilcoxon": wilcoxon_code_snippets,
    "kruskall-wallis": kruskall_code_snippets,
    "kolmogorov": kolmogorov_code_snippets,
    "friedman": friedman_code_snippets,
    "z-test": z_test_code_snippets,
    "t-test": t_test_code_snippets,
    "confidence-intervals": confidence_intervals_code_snippets
}

examples = {
    'z-test': z_test_examples,
    't-test': t_test_examples,
    'wilcoxon': wilcoxon_examples,
    'mann-whitney-test': mann_whitney_examples,
    'f-test': t_test_examples
}

tests = {
    #CIs are not technically tests, but they are included here for the sake of completeness
    "confidence-intervals": {
        "use-cases": ["Estimating the population mean from a sample mean", "Determining the difference between two independent sample means"],
        "description": "A statistical technique used to estimate the range in which a population parameter (mean, proportion, etc.) is likely to fall based on a sample statistic.",
        "code_snippets": code_examples.get('confidence-intervals'),
    },
    "z-test": {
        "use-cases": ["Comparing proportions between two large independent samples", "Testing the difference between a sample mean and a population mean when the population standard deviation is known"],
        "description": "Used for testing hypotheses about proportions or means in large samples when the population standard deviation is known.",
        "examples": examples.get('z-test'),
        "calculation-process": ["Calculate the test statistic based on sample and population parameters", "Determine the p-value from the z-distribution"],
        "formulas": ["Z = (X̄ - μ) / (σ / √n) for means", "Z = (p̂1 - p̂2) / √P(1-P)(1/n1 + 1/n2) for proportions"],
        "parametric": True,
        "summary": summaries.get('z-test'),
        "code_snippets": code_examples.get('z-test')
    },
    "t-test": {
        "use-cases": ["Comparing the means of two independent samples", "Comparing the mean of a single sample against a known mean", "Comparing the means of two paired samples"],
        "description": "Used to compare the means of two groups or a single group against a standard when the population standard deviation is unknown.",
        "examples": examples.get('z-test'),
        "calculation-process": ["Calculate the t-score", "Determine the degrees of freedom", "Find the p-value from the t-distribution"],
        "formulas": ["t = (X̄ - μ) / (s / √n) for one-sample", "t = (X̄1 - X̄2) / √((s1²/n1) + (s2²/n2)) for independent samples"],
        "parametric": True,
        "summary": summaries.get('t-test'),
        "code_snippets": code_examples.get('t-test')
    },
    "f-test": {
        "use-cases": ["Comparing the variances of two populations", "Testing overall significance in regression analysis"],
        "description": "Used to compare the variances between two populations or to test the significance of predictors in a regression model.",
        "examples": examples.get('f-test'),
        "calculation-process": ["Calculate the variance of each group", "Divide the larger variance by the smaller variance to find the F-statistic", "Compare the F-statistic to the F-distribution"],
        "formulas": ["F = s1² / s2²"],
        "parametric": True,
        "summary": summaries.get('f-test')
    },
    "chi-square-test": {
        "use-cases": ["Testing independence between two categorical variables", "Goodness-of-fit testing against a known distribution"],
        "description": "Used to assess whether observed frequencies differ from expected frequencies in categorical data.",
        "examples": ["Analyzing the relationship between gender and voting preference", "Comparing observed dice rolls to a uniform distribution"],
        "calculation-process": ["Calculate the expected frequencies", "Compute the chi-square statistic using observed and expected frequencies", "Find the p-value from the chi-square distribution"],
        "formulas": ["χ² = Σ((O-E)² / E) where O is observed frequency and E is expected frequency"],
        "parametric": False,
        "summary": summaries.get('chi-square-test')
    },
    "wilcoxon": {
        "use-cases": ["Comparing two related samples", "Non-parametric alternative to the paired t-test"],
        "description": "A non-parametric test for assessing whether two paired samples come from the same distribution.",
        "examples": examples.get('wilcoxon'),
        "calculation-process": ["Rank the differences between pairs", "Sum the ranks for positive and negative differences", "Calculate the test statistic from the smaller of the two sums"],
        "formulas": ["W = min(W+, W-) where W+ is the sum of positive ranks and W- is the sum of negative ranks"],
        "parametric": False,
        "summary": summaries.get('wilcoxon-test'),
        "code_snippets": code_examples.get('wilcoxon'),
        "thorough_examples": thorough_examples.examples.get('wilcoxon')
    },
    "mann-whitney": {
        "use-cases": ["Comparing ranks between two independent samples", "Non-parametric alternative to the independent samples t-test"],
        "description": "A non-parametric test used to determine if there is a statistically significant difference between the medians of two independent samples.",
        "examples": examples.get('mann-whitney-test'),
        "calculation-process": ["Rank all observations across both groups", "Sum the ranks for each group", "Calculate the U statistic based on ranks"],
        "formulas": ["U = n1*n2 + (n1*(n1+1)/2) - R1", "where n1 and n2 are the sample sizes, and R1 is the sum of ranks for sample 1"],
        "parametric": False,
        "summary": summaries.get('mann-whitney-test'),
        "code_snippets": code_examples.get("mann-whitney-test"),
        "thorough_examples": thorough_examples.examples.get('mann_whitney')
    },
    "anova": {
        "use-cases": ["Comparing means across three or more groups", "Testing the effect of a categorical variable on a continuous outcome"],
        "description": "Used to determine whether there are any statistically significant differences between the means of three or more independent (or related) groups.",
        "examples": ["Analyzing the impact of diet type (vegan, vegetarian, omnivore) on cholesterol levels", "Evaluating the performance of students across different education methods"],
        "calculation-process": ["Calculate group means and the overall mean", "Compute the between-group and within-group variances", "Calculate the F-statistic and find the p-value"],
        "formulas": ["F = (Between-group variance) / (Within-group variance)"],
        "parametric": True,
        "summary": summaries.get('anova')
    },
    "kruskal-wallis": {
        "use-cases": ["Comparing medians across three or more independent groups", "Non-parametric alternative to one-way ANOVA"],
        "description": "A non-parametric method for testing whether samples originate from the same distribution. It is used for comparing two or more independent samples of equal or different sample sizes.",
        "examples": ["Comparing customer satisfaction ratings across multiple store locations", "Assessing the effectiveness of different types of pain relief medication"],
        "calculation-process": ["Rank all data from all groups together", "Calculate the sum of ranks for each group", "Compute the test statistic using ranks"],
        "formulas": ["H = (12 / N(N+1)) * Σ(Ri²/ni) - 3(N+1)", "where N is the total number of observations, Ri is the sum of ranks for group i, and ni is the number of observations in group i"],
        "parametric": False,
        "summary": summaries.get('kruskal-wallis-test'),
        "code_snippets": code_examples.get("kruskall-wallis")
    },
    "friedman": {
        "use-cases": ["Comparing three or more paired groups", "Non-parametric alternative to repeated measures ANOVA"],
        "description": "Used for analyzing and comparing matched or paired samples across multiple test conditions. It assesses the differences in treatments across multiple test attempts.",
        "examples": ["Evaluating the performance of algorithms on different datasets", "Assessing the taste preference of a food product across different recipes"],
        "calculation-process": ["Rank each block (or subject) across all conditions", "Sum the ranks for each condition", "Compute the Friedman statistic"],
        "formulas": ["χ² = (12 / k(n+1)) ΣRi² - 3n(k+1)", "where k is the number of conditions, n is the number of blocks, and Ri is the sum of ranks for condition i"],
        "parametric": False,
        "summary": summaries.get('friedman-test'),
        "code_snippets": code_examples.get("friedman"),
        "thorough_examples": thorough_examples.examples.get('friedman')
    },
    "correlation": {
        "use-cases": ["Measuring the strength and direction of association between two continuous variables"],
        "description": "Statistical technique to determine how strongly two variables are related to each other. Includes Pearson (linear relationship) and Spearman/Kendall (monotonic relationship) methods.",
        "examples": ["Exploring the relationship between height and weight", "Studying the association between education level and income"],
        "calculation-process": ["Calculate the covariance between variables", "Normalize by the product of the standard deviations", "Determine the correlation coefficient"],
        "formulas": ["Pearson's r = Σ((xi - x̄)(yi - ȳ)) / (nσxσy)", "Spearman's ρ = 1 - (6 Σd²) / (n(n² - 1))", "where d is the difference between ranks of each observation, n is the number of observations"],
        "parametric": True,
        "summary": summaries.get('correlation')
    },
    "regression": {
        "use-cases": ["Modeling the relationship between a dependent variable and one/more independent variables", "Predicting outcomes based on predictors"],
        "description": "A statistical approach to model and analyze the relationships between dependent and independent variables. It identifies the equation that best predicts the dependent variable.",
        "examples": ["Predicting house prices based on their size, location, and age", "Estimating future sales based on advertising spend"],
        "calculation-process": ["Estimate the model parameters (slopes, intercept) minimizing the error", "Calculate the coefficient of determination (R²)", "Assess the significance of predictors"],
        "formulas": ["y = β0 + β1x1 + ... + βnxn + ε", "where y is the dependent variable, x1,...,xn are independent variables, β0 is the intercept, β1,...,βn are the slopes, and ε is the error term"],
        "parametric": True,
        "summary": summaries.get('regression')
    },
    "time-series": {
        "use-cases": ["Analyzing trends, seasonal patterns, and cyclical fluctuations in data collected over time", "Forecasting future values based on past observations"],
        "description": "Statistical techniques for analyzing time-ordered data points to understand the underlying structure and function for forecasting.",
        "examples": ["Forecasting stock market prices", "Analyzing the trend of monthly sales data"],
        "calculation-process": ["Identify trend, seasonality, and residuals", "Model the time series using appropriate methods (ARIMA, Exponential Smoothing)", "Validate the model with diagnostics checks"],
        "formulas": ["Depends on the specific model: ARIMA(p,d,q), ETS, etc.", "where ARIMA is AutoRegressive Integrated Moving Average, ETS is Exponential Smoothing State Space model"],
        "parametric": True,
        "summary": summaries.get('time-series')
    },
    "kolmogorov-smirnov": {
        "use-cases": ["Comparing a sample distribution to a reference probability distribution (one-sample KS test)", "Comparing two sample distributions to determine if they are from the same distribution (two-sample KS test)"],
        "description": "The Kolmogorov-Smirnov (KS) test is a non-parametric test used to determine whether a sample comes from a specific distribution or to compare two samples. It is valuable for testing the goodness-of-fit between observed data and a known distribution or for comparing two empirical distributions without assuming them to follow a specific distribution.",
        "examples": ["Testing if reaction times in a cognitive psychology experiment follow a normal distribution", "Comparing the distribution of daily returns of two different stocks"],
        "calculation-process": ["Calculate the cumulative distribution function (CDF) for the reference distribution or for both samples in the case of the two-sample KS test", "Compute the maximum distance (D-statistic) between the CDFs", "Use the D-statistic to assess the hypothesis through the KS distribution"],
        "formulas": ["D = max|F1(x) - F2(x)| for the two-sample KS test", "D = max|Fn(x) - F(x)| for the one-sample KS test", "where F1(x) and F2(x) are the empirical distribution functions of the two samples, Fn(x) is the empirical distribution function of the sample, and F(x) is the CDF of the reference distribution"],
        "code_snippets": code_examples.get('kolmogorov'),
        "parametric": False,
        "summary": summaries.get('kolmogorov-smirnov-test'),
        "thorough_examples": thorough_examples.examples.get('kolmogorov')
    }
}

