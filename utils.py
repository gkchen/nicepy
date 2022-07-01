def get_latex(formula):
    formula = list(formula)
    for i, char in enumerate(formula):
        if char.isnumeric():
            formula[i] = "$_{" + char + "}$"
    return "".join(formula)


def time_to_mass(time, factor, offset):
    pass
