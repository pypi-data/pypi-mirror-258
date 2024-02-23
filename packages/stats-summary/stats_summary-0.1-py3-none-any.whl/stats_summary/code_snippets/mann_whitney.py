code_snippet = """
    # two different teaching methods on two different student groups (traditional x interactive)

    group_a = np.array([ 75, 85, 80, 70, 90, 95, 65, 80 ])
    group_b = np.array([ 85, 90, 75, 88, 80, 84, 82, 95 ])

    full_array = [n for n in group_a] + [n for n in group_b]
    full_array

    ranked_array = scipy.stats.rankdata(full_array)

    ranked_a = ranked_array[:len(group_a)]
    ranked_b = ranked_array[len(group_a):]

    U, p = scipy.stats.mannwhitneyu(group_a, group_b, alternative='two-sided') # use the samples, not the RANKED samples here
    U, p

"""
