from naive_approach.algorithms.elimination_manager import Reducer
from naive_approach.algorithms.fsm import FSM
from naive_approach.utils.table_cost_utils import DNASequenceAnalyzer
from typing import Set
from collections import defaultdict
from naive_approach.utils.display_utils import DNASequencePrinter


class EliminateSequence:
    @staticmethod
    def _eliminate(S: str, P: Set[str], C: list[dict[str, float]], reducer_class: type[Reducer]) -> str:
        """Computing a min-cost P-clean sequence of length n

        A valid sequence is defined by the given mitigator.

        Args:
            S (str):                                DNA sequence
            P (set[str]):                           set of unwanted patterns
            C (list[dict[str, float]]):             cost
            mitigator_class (type[DNAMitigator]):  mitigator implementation

        Returns:
            str | None: target DNA sequence
        """
        print('\n' + 100*'*')
        print(f"Eliminating {P} from the sequence...")

        n = len(S)
        dna_analyzer = DNASequenceAnalyzer()
        cost = dna_analyzer.cost_function(C)
        reducer = reducer_class(P)

        # Compute an FSM(V(f) over alphabet {'A', 'G', 'T', 'C'} that generates all and only P-clean sequences.
        fsm = FSM[reducer.state_type](dna_analyzer.alphabet, reducer.initial_state, reducer.states, reducer.transition_function)
        valid_set, vs_by_seq_len, transition_back_tracker = fsm.generate_valid_sequences(n)
        # print(f"{len(valid_set)} valid sequences were found.")

        """A[i, v] holds the minimum cost 
            of a sequence of length i that is generated by the FSM 
            with a generating path that ends with state v.
        """
        # Initialize: A[0, v]
        inf = float('inf')
        A_0 = defaultdict(lambda: inf)
        A_0[fsm.initial_state] = 0
        A = [A_0]

        # for tracking
        A_star = []

        # for i=1...n do and v in V:
        for i in range(1, n + 1):
            A_i = defaultdict(lambda: inf)
            A_star_i = dict()
            V_i = vs_by_seq_len[i]

            for v in V_i:
                u_star = ''
                sigma_star = ''
                cost_star = inf

                for (u, sigma) in transition_back_tracker[v]:
                    current_cost = A[i - 1][u] + cost(i, sigma)
                    if current_cost < cost_star:
                        cost_star = current_cost
                        u_star, sigma_star = u, sigma

                A_star_i[v] = (u_star, sigma_star)
                A_i[v] = cost_star

            A_star.append(A_star_i)
            A.append(A_i)

        # argmin
        min_cost = inf
        v_curr = ''
        for v, c in A[n].items():
            if c < min_cost:
                min_cost = c
                v_curr = v

        if min_cost == inf:
            print("No solution!")
            print(100*'*' + '\n')
            return None

        print(f"min_cost={min_cost}")

        print(f"Constructing target sequence using A*...")
        target_seq = []

        # Final update
        for i in range(n - 1, -1, -1):
            v_curr, s_i = A_star[i][v_curr]
            target_seq.insert(0, s_i)

        print(100*'*' + '\n')
        return ''.join(target_seq)

    @staticmethod
    def eliminate(S: str, P: Set[str], C: list[dict[str, float]]) -> str:
        """Computing a min-cost valid sequence of length n

        Args:
            S (str):                                DNA sequence
            P (set[str]):                           set of unwanted patterns
            C (list[dict[str, float]]):             cost

        Returns:
            str | None: target DNA sequence
        """

        reducer: type[Reducer] = Reducer
        target_seq = EliminateSequence._eliminate(S, P, C, reducer)
        if target_seq is not None:
            DNASequencePrinter.print_target_sequence(target_seq)
        else:
            print("No valid sequence matches the unwanted pattern list.")