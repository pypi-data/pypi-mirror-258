from .TreeNodes import Power, Product, Sum, Constant, Variable
from .randomNumber import randomNumber
from .Tree import Tree


def variableTreeBuild(power: int, name: str) -> Tree:
    if power == 1:
        return Product(Constant(randomNumber()),
                       Power(Variable(name),
                             Constant(power)))

    return Sum(Product(Constant(randomNumber()),
                       Power(Variable(name),
                             Constant(power))),
               variableTreeBuild(power - 1, name))


def baseTreeBuild(powers: list[int], i: int = 0) -> Tree:
    if i == len(powers) - 1:
        return variableTreeBuild(powers[i], f'x{i}')

    return Sum(variableTreeBuild(powers[i], f'x{i}'),
               baseTreeBuild(powers, i + 1))


def treeBuild(powers: list[int]) -> Tree:
    return Sum(Constant(randomNumber()),
               baseTreeBuild(powers))
