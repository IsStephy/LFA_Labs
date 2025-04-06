import itertools
from collections import defaultdict

class CFG:
    def __init__(self, variables, terminals, start_symbol, productions):
        self.V = set(variables)
        self.T = set(terminals)
        self.S = start_symbol
        self.P = defaultdict(list)
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                self.P[lhs].append(tuple(rhs) if isinstance(rhs, str) else tuple(rhs))

    def eliminate_epsilon(self):
        nullable = set()
        changed = True
        while changed:
            changed = False
            for A in self.V:
                if A not in nullable:
                    for prod in self.P[A]:
                        if all(sym in nullable or sym == '' for sym in prod):
                            nullable.add(A)
                            changed = True

        new_P = defaultdict(list)
        for A in self.P:
            for prod in self.P[A]:
                subsets = list(itertools.product(*[[s, ''] if s in nullable else [s] for s in prod]))
                for alt in subsets:
                    new_rhs = tuple(s for s in alt if s != '')
                    if new_rhs != () or A == self.S:
                        if new_rhs not in new_P[A]:
                            new_P[A].append(new_rhs)
        self.P = new_P

    def eliminate_renaming(self):
        unit_pairs = set()
        for A in self.V:
            unit_pairs.add((A, A))

        changed = True
        while changed:
            changed = False
            for A in self.V:
                for prod in self.P[A]:
                    if len(prod) == 1 and prod[0] in self.V:
                        B = prod[0]
                        for C in self.V:
                            if (B, C) in unit_pairs and (A, C) not in unit_pairs:
                                unit_pairs.add((A, C))
                                changed = True

        new_P = defaultdict(list)
        for A in self.V:
            for (X, Y) in unit_pairs:
                if X == A:
                    for prod in self.P[Y]:
                        if len(prod) != 1 or prod[0] not in self.V:
                            if prod not in new_P[A]:
                                new_P[A].append(prod)
        self.P = new_P

    def eliminate_inaccessible(self):
        reachable = {self.S}
        changed = True
        while changed:
            changed = False
            for A in list(reachable):
                for prod in self.P[A]:
                    for sym in prod:
                        if sym in self.V and sym not in reachable:
                            reachable.add(sym)
                            changed = True
        self.V = reachable
        self.P = {A: self.P[A] for A in self.V}

    def eliminate_non_productive(self):
        productive = set()
        changed = True
        while changed:
            changed = False
            for A in self.V:
                for prod in self.P[A]:
                    if all(sym in self.T or sym in productive for sym in prod):
                        if A not in productive:
                            productive.add(A)
                            changed = True
        self.V = self.V & productive
        new_P = defaultdict(list)
        for A in self.V:
            for prod in self.P[A]:
                if all(sym in self.T or sym in self.V for sym in prod):
                    new_P[A].append(prod)
        self.P = new_P

    def to_cnf(self):
        new_P = defaultdict(list)
        new_vars = {}
        counter = 1

        def get_var_for_terminal(t):
            if t not in new_vars:
                new_var = f"T{counter + len(new_vars)}"
                while new_var in self.V:
                    new_var = f"T{counter + len(new_vars)}"
                new_vars[t] = new_var
                self.V.add(new_var)
                new_P[new_var].append((t,))
            return new_vars[t]

        for A in self.P:
            for prod in self.P[A]:
                if len(prod) == 1 and prod[0] in self.T:
                    new_P[A].append(prod)
                else:
                    new_rhs = []
                    for sym in prod:
                        if sym in self.T:
                            new_rhs.append(get_var_for_terminal(sym))
                        else:
                            new_rhs.append(sym)

                    while len(new_rhs) > 2:
                        B = f"X{counter}"
                        counter += 1
                        self.V.add(B)
                        new_P[B].append((new_rhs[0], new_rhs[1]))
                        new_rhs = [B] + new_rhs[2:]
                    new_P[A].append(tuple(new_rhs))

        for t, v in new_vars.items():
            new_P[v] = [(t,)]

        self.P = new_P

    def normalize(self):
        self.eliminate_epsilon()
        self.eliminate_renaming()
        self.eliminate_inaccessible()
        self.eliminate_non_productive()
        self.to_cnf()

    def print_grammar(self):
        print(f"Variables: {sorted(self.V)}")
        print(f"Terminals: {sorted(self.T)}")
        print(f"Start symbol: {self.S}")
        print("Productions:")
        for A in sorted(self.P):
            for prod in self.P[A]:
                print(f"  {A} -> {''.join(prod)}")

variables = {'S', 'A', 'B', 'C', 'D'}
terminals = {'a', 'b'}
start_symbol = 'S'
productions = {
    'S': ['abAB'],
    'A': ['aSab', 'BS', 'aA', 'b'],
    'B': ['BA', 'ababB', 'b', ''],
    'C': ['AS']
}

cfg = CFG(variables, terminals, start_symbol, productions)
print("Before normalization:")
cfg.print_grammar()

cfg.normalize()

print("\nAfter normalization to CNF:")
cfg.print_grammar()
