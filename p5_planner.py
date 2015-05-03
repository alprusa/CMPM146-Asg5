from collections import namedtuple
from heapq import heappop, heappush
import json

def make_checker(rule, items):
    consumes = ()
    requirements = ()

    if rule.get('Consumes') != None:
        consumes = ruleToTuple(rule['Consumes'], items)

    if rule.get('Requires') != None:
        requirements = ruleToTuple(rule['Requires'], items)

    def check(state):
        if requirements != () and state != ():
            for i, amount in enumerate(requirements):
                if state[i] < amount:
                    return False

        if consumes != () and state != ():
            for i, amount in enumerate(consumes):
                if state[i] < amount:
                    return False

        return True

    return check

def make_effector(rule, items):
    consumes = ()
    produces = ()

    if rule.get('Consumes') != None:
        consumes = ruleToTuple(rule['Consumes'], items)

    if rule.get('Produces') != None:
        produces = ruleToTuple(rule['Produces'], items)

    def effect(state):
        nextState = state;

        if consumes != () and nextState != ():
            nextState = tuple(nextState[i] - amount for i, amount in enumerate(consumes))

        if produces != () and nextState != ():
            nextState = tuple(nextState[i] + amount for i, amount in enumerate(produces))

        return nextState

    return effect

def heuristic(node, nextNode, goal):
    # wooden_pickaxe: 1 took 0.147 seconds
    # stone_pickaxe: 1 took 0.229 seconds
    # furnace: 1 took 0.283 seconds
    # iron_pickaxe: 1 took 16.551 seconds
    # cart: 1 took  seconds 17.623
    # cart: 1, rail: 10 took 19.787 seconds
    # cart: 1, rail: 20 took 22.343 seconds
    # ingot: 1 took 2.261 seconds
    # rail: 1 took 17.814 seconds

    cost = 0

    for i in xrange(len(node[1])):
        # something new could've been crafted
        if node[1][i] >= nextNode[1][i] and node[1][i] != 0 and nextNode[1][i] != 0:
           cost += 10

        # something we didn't have was crafted
        if node[1][i] == 0 and nextNode[1][i] > 0:
           cost -= 10

    # more than one tool not needed
    if nextNode[1][0] > 1 or nextNode[1][4] > 1 or nextNode[1][6] > 1 or nextNode[1][7] > 1 or nextNode[1][12] > 1 or nextNode[1][13] > 1 or nextNode[1][15] > 1 or nextNode[1][16] > 1:
        cost += float("inf")

    # replace this with something that analyzes
    # goal and produces a limit on consumables

    # coal
    if nextNode[1][2] > 8:
        cost += float("inf")

    # cobble
    elif nextNode[1][3] > 8:
        cost += float("inf")

    # ingot
    elif nextNode[1][5] > 17:
        cost += float("inf")

    # ore
    elif nextNode[1][8] > 8:
        cost += float("inf")

    # plank
    elif nextNode[1][9] > 4:
        cost += float("inf")

    # stick
    elif nextNode[1][11] > 8:
        cost += float("inf")

    # wood
    elif nextNode[1][14] > 8:
        cost += float("inf")

    return cost

def reachedGoal(state, goals):
    satisfied = False

    for i, amount in enumerate(goals):
        if state[i] >= amount and amount != 0:
            satisfied = True
        elif state[i] <= amount and amount != 0:
            satisfied = False
            break

    return satisfied

def graph(state, recipes):
    adjacent = []

    for recipe in recipes:
        if recipe.check(state[1]):
            adjacent.append((recipe.cost, recipe.effect(state[1]), recipe.name))

    return adjacent


def plan(graph, state, items, goals, recipes):
    dist = {}
    prev = {}
    initial = inventoryToTuple(state, items)
    goal = inventoryToTuple(goals, items)
    dist[initial] = 0
    prev[initial] = None
    heap = [(dist[initial], initial, "initial")]

    while heap:
        node = heappop(heap)
        print(node)

        if reachedGoal(node[1], goal):
            break

        for nextNode in graph(node, recipes):
            if nextNode[1] not in dist or nextNode[0] < dist[nextNode[1]]:
                dist[nextNode[1]] = nextNode[0]
                prev[nextNode[1]] = node[1]
                cost = nextNode[0] + dist[node[1]] + heuristic(node, nextNode, goal)
                heappush(heap, (cost, nextNode[1], nextNode[2]))

    path = []

    if reachedGoal(node[1], goal):
        node = node[1]

        while node:
            path.append(node)
            node = prev[node]

        path.reverse()

    print(str(len(path) - 1))

def ruleToTuple(rules, items):
    rule = []

    for i, name in enumerate(items):
        rule.append(rules.get(name, 0))

        if rules.get(name, 0) == True:
            rule[i] = 1

    return tuple(rule)

def inventoryToTuple(inventory, items):
    return tuple(inventory.get(name, 0) for i, name in enumerate(items))

def make_recipes(recipes, items):
    Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])
    allRecipes = []

    for name, rule in recipes.items():
        checker = make_checker(rule, items)
        effector = make_effector(rule, items)
        recipe = Recipe(name, checker, effector, rule['Time'])
        allRecipes.append(recipe)

    return allRecipes

def planner(inputFile):
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    inventory = Crafting['Initial']
    items = Crafting['Items']
    goals = Crafting['Goal']
    recipes = make_recipes(Crafting['Recipes'], items)

    plan(graph, inventory, items, goals, recipes)

if __name__ ==  '__main__':
    import sys
    _, filename  = sys.argv
    planner(filename)
