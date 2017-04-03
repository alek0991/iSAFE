

def get_superpopulations():
    with open('super_populations.txt') as input:
        result = [population.strip() for population in input.readlines() if population.strip() != '']
    return result


def get_subpopulations():
    with open('subpopulations.txt') as input:
        result = [population.strip() for population in input.readlines() if population.strip() != '']
    return result
