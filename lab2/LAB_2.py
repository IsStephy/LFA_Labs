import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions  
        self.start_state = start_state
        self.final_states = final_states
    
    def is_deterministic(self):
        for state, trans in self.transitions.items():
            for symbol, targets in trans.items():
                if len(targets) > 1:
                    return False
        return True
    
    def to_dfa(self):
        if self.is_deterministic():
            return self 
        
        new_states = {}
        queue = [frozenset([self.start_state])]
        new_transitions = {}
        new_final_states = set()
        
        while queue:
            current = queue.pop(0)
            state_name = ','.join(sorted(current))
            new_states[current] = state_name
            new_transitions[state_name] = {}
            
            for symbol in self.alphabet:
                next_states = set()
                for state in current:
                    next_states.update(self.transitions.get(state, {}).get(symbol, []))
                
                if next_states:
                    next_state_name = ','.join(sorted(next_states))
                    new_transitions[state_name][symbol] = next_state_name
                    if frozenset(next_states) not in new_states:
                        queue.append(frozenset(next_states))
                
                if any(s in self.final_states for s in next_states):
                    new_final_states.add(next_state_name)
        
        return FiniteAutomaton(set(new_states.values()), self.alphabet, new_transitions, new_states[frozenset([self.start_state])], new_final_states)
    
    def to_regular_grammar(self):
        grammar = defaultdict(list)
        for state, trans in self.transitions.items():
            for symbol, targets in trans.items():
                for target in targets:
                    grammar[state].append(symbol + target)
        
        for final in self.final_states:
            grammar[final].append('ε') 
        
        return grammar
    
    def classify_grammar(self, grammar):
        is_regular = True
        is_context_free = True
        is_context_sensitive = True
        
        for lhs, rhs_list in grammar.items():
            for rhs in rhs_list:
                if rhs == 'ε':
                    continue
                
                if len(lhs) > 1:
                    is_regular = True
                    is_context_free = False
                
                if not any(nonterm.isupper() for nonterm in lhs):
                    is_context_free = False
                    is_context_sensitive = False
                
        if is_regular:
            return "Type-3 (Regular Grammar)"
        elif is_context_free:
            return "Type-2 (Context-Free Grammar)"
        elif is_context_sensitive:
            return "Type-1 (Context-Sensitive Grammar)"
        else:
            return "Type-0 (Unrestricted Grammar)"
    
    def draw(self):
        G = nx.DiGraph()
        for state, trans in self.transitions.items():
            for symbol, targets in trans.items():
                for target in targets:
                    G.add_edge(state, target, label=symbol)
        
        pos = nx.spring_layout(G)
        labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()

states = {"q0", "q1", "q2", "q3"}
alphabet = {"a", "b"}
transitions = {
    "q0": {"a": ["q1"], "b": ["q0"]},
    "q1": {"b": ["q1", "q2"]},
    "q2": {"a": ["q2"], "b": ["q3"]},
}
start_state = "q0"
final_states = {"q3"}

fa = FiniteAutomaton(states, alphabet, transitions, start_state, final_states)
print("Deterministic?", fa.is_deterministic())
converted_dfa = fa.to_dfa()
print("DFA Transitions:", converted_dfa.transitions)
regular_grammar = fa.to_regular_grammar()
print("Regular Grammar:", regular_grammar)
print("Grammar Classification:", fa.classify_grammar(regular_grammar))
fa.draw()
x