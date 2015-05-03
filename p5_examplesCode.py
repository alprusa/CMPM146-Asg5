import json

#how to load the json rules

with open('Crafting.json') as f:
    Crafting = json.load(f)
    
# List of items that can be in your inventory:
print Crafting['Items']

# example: ['bench', 'cart', ..., 'wood', 'wooden_axe', 'wooden_pickaxe']
# List of items in your initial inventory with amounts:
print Crafting['Initial']

# {'coal': 4, 'plank': 1}
# List of items needed to be in your inventory at the end of the plan:
# (okay to have more than this; some might be satisfied by initial inventory)
print Crafting['Goal']

# {'stone_pickaxe': 2}
# Dictionary of crafting recipes:
print Crafting['Recipes']['craft stone_pickaxe at bench']

# example:
# { 'Produces': {'stone_pickaxe': 1},
# 'Requires': {'bench': True},
# 'Consumes': {'cobble': 3, 'stick': 2},
# 'Time': 1
# }

#Container Class to hold comipled recipes

from collections import namedtuple
Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []

for name, rule in Crafting['Recipes'].items:
    checker = make_checker(rule)
    effector = make_effector(rule)
    recipe = Recipe(name, checker, effector, rule['Time'])
    all_recipes.append(recipe)

#Funtcions for making a checker and effector
def make_checker(rule):
    … # this code runs once
    # do something with rule['Consumes'] and rule['Requires']

    def check(state):
        … # this code runs millions of times
        return True # or False
    return check
    
def make_effector(rule):
    … # this code runs once
    # do something with rule['Produces'] and rule['Consumes']
    def effect(state):
        … # this code runs millions of times
        return next_state
    return check

#A* search
def search(graph, initial, is_goal, limit, heuristic):
    ...
    return total_cost, plan
    
#Get adjacent nodes
def graph(state):
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost

#Run/Test A* algorithm
t_initial = 'a'
t_limit = 20
edges = {'a': {'b':1,'c':10}, 'b':{'c':1}}

def t_graph(state):
    for action, next_state, cost in graph(current_state):
        ... # do something with action, next_state, and cost
        #yield ((state,next_state), next_state, cost)

def t_is_goal(state):
    return state == 'c'

def t_heuristic(state):
    return 0

print search(t_graph, t_initial, t_is_goal, t_limit, t_heuristic)

#Building Blocks State
def make_initial_state(inventory):
    ...
    return state

initial_state = make_initial_state(Crafting['Initial'])

def make_goal_checker(goal):
    ... # this code runs once  
    def is_goal(state):
        ... # this code runs millions of times
        return True # or False
    return is_goal

is_goal = make_goal_checker(Crafting['Goal'])

def make_checker(rule):
    ...
    def check(state):
        ...
        return True # or False
        
def make_effector(rule):
    ...
    def effect(state):
        ...
        return next_state
        
def graph(state):
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)
            
def heuristic(state):
    ...
    return 0 # or something more accurate

#Caveats Hashable objects
dist = {}
state_dict = {'coal': 5}
dist[state_dict] = 6
    TypeError: unhashable type: 'dict'
Items = Crafting['Items']

def inventory_to_tuple(d):
    return tuple(d.get(name,0) for i,name in enumerate(Items))

h = inventory_to_tuple(state_dict) # >(0,0,0,0,5,0,0,0)

def inventory_to_set(d):
    return frozenset(d.items()

h = inventory_to_frozenset(state_dict) # > frozenset({('coal':5)})

dist[h] = 6
    No error
