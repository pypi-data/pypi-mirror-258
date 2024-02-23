code_snippet = """

    # before and after a training program on a group of employees

    before = [ 100, 105, 98, 87, 110, 103, 91, 95, 102, 106 ]
    after = [ 108, 110, 99, 89, 115, 105, 93, 97, 105, 108 ]

    diffs = [ n-m for (n,m) in zip(before, after) ]
    diffs

    scipy.stats.wilcoxon(diffs)

"""
