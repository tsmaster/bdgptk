import random

# from https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html

# It asks whether, for a given set X and a collection Y of subsets of
# X, there exists a subcollection Y* of Y such that Y* forms a
# partition of X.

# So, for a puzzle piece placement puzzle, each element of X might be
# a set of slots that need to be occupied, and Y is a list of
# descriptions of placements of pieces, describing how they "cover"
# the slots from X.

# in this implementation, though, X is not a list, but a dictionary of
# sets of elements from Y, such that each slot "knows" what placements
# can be used to cover it.


def rand_solve(X, Y, solution=None):
    if solution is None:
        solution = []
    
    if not X:
        return list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))

        slot_list = list(X[c])
        random.shuffle(slot_list)
        
        for r in slot_list:
            solution.append(r)
            cols = select(X, Y, r)

            s = rand_solve(X, Y, solution)
            if s:
                return s

            deselect(X, Y, r, cols)
            solution.pop()
        return None



def solve(X, Y, solution=None):
    if solution is None:
        solution = []
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()

def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)
