code_snippet = """
    # samples have relations

    goals_first_tri = [ 3, 2, 4, 5, 2 ]
    goals_second_tri = [ 4, 6, 5, 7, 6 ]
    goals_third_tri = [ 5, 4, 6, 7, 8 ]

    scipy.stats.friedmanchisquare(
        goals_first_tri,
        goals_second_tri,
        goals_third_tri
    )

"""
