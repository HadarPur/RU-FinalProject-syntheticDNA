import numpy as np
from utils.amino_acid_utils import AminoAcidConfig


def calculate_cost(target_sequence, coding_positions, codon_usage, i, v, sigma, alpha, beta, w):
    """
    Calculate the substitution cost for a given position in a nucleotide sequence.

    Parameters:
    ----------
    target_sequence : str
        The nucleotide sequence in which substitutions are analyzed.
    coding_positions : list[int]
        A list indicating the coding status of each position in the sequence:
        - Non-coding: 0
        - Coding: 1, 2, or 3 (indicating the codon phase).
    codon_usage : dict
        A dictionary mapping codons to their frequency of use in synonymous substitutions.
    i : int
        The position in the sequence being analyzed.
    v : str
        The sequence fragment being tested or modified (e.g., a codon or part of a codon).
    sigma : str
        The proposed nucleotide substitution at position `i`.
    alpha : float
        The cost for a transition substitution in a non-coding region.
    beta : float
        The cost for a transversion substitution in a non-coding region.
    w : float
        The cost for non-synonymous substitutions in coding regions.

    Returns:
    -------
    float
        The substitution cost based on the position type and mutation type.
        - Returns infinity (`float('inf')`) for stop codon formation.
        - Returns a logarithmic penalty for rare synonymous substitutions.
        - Returns `0.0` for no substitution or synonymous substitutions of high codon usage.

    Raises:
    ------
    IndexError:
        If `i` is out of bounds for `target_sequence` or `coding_positions`.
    ValueError:
        If codon usage contains invalid or non-normalized probabilities.

    Notes:
    ------
    - Positions 1 and 2 within a codon are assumed to have no substitution cost.
    - Stop codon formation is heavily penalized as biologically deleterious.
    """

    # Determine coding position of the current index.
    codon_pos = coding_positions[i]  # Non-coding: 0; Coding: ((i - \text{coding\_start}) \mod 3) + 1.

    # Non-coding region logic
    if codon_pos == 0:
        if target_sequence[i] == sigma:
            # No substitution
            return 0.0
        if AminoAcidConfig.is_transition(target_sequence[i], sigma):
            # Transition substitution
            return alpha
        else:
            # Transversion substitution
            return beta

    # Coding region positions 1 and 2
    elif codon_pos in {1, 2}:
        # Cost is always 0 for positions 1 and 2
        return 0.0

    # Coding region, position 3
    elif codon_pos == 3:  # At 3rd position of codon
        # Retrieve the current codon and construct the proposed codon
        current_codon = AminoAcidConfig.get_last3(target_sequence, i)
        last2_bases = AminoAcidConfig.get_last2(v)
        proposed_codon = f'{last2_bases}{sigma}'

        # Evaluate substitution costs
        if proposed_codon == current_codon:
            # No substitution
            return 0.0
        elif AminoAcidConfig.encodes_same_amino_acid(proposed_codon, current_codon):
            # Synonymous substitution with a logarithmic penalty based on codon usage
            return -np.log(codon_usage[proposed_codon])
        elif AminoAcidConfig.is_stop_codon(proposed_codon):
            # Penalize stop codon formation
            return float('inf')
        else:
            # Non-synonymous substitution
            return w

    # Fallback (should not be reached under correct conditions)
    raise ValueError(f"Unexpected codon position value: {codon_pos}")


class EliminationScorerConfig:
    def __init__(self):
        """
        Initializes a DNASequenceAnalyzer object.
        Sets up the DNA alphabet containing the characters 'A', 'G', 'T', and 'C'.
        """
        self.alphabet = {'A', 'G', 'T', 'C'}

    @staticmethod
    def cost_function(target_sequence, coding_positions, codon_usage, alpha, beta, w):
        """
        Creates a dynamic cost function based on the given sequence properties and scoring parameters.

        Args:
            target_sequence (str): The DNA sequence being analyzed.
            coding_positions (list): Array where each index indicates coding or non-coding regions.
            codon_usage (dict): Dictionary of codon frequencies for synonymous substitutions.
            alpha (float): Cost for transition substitution in non-coding regions.
            beta (float): Cost for transversion substitution in non-coding regions.
            w (float): Cost for non-synonymous substitution in coding regions.

        Returns:
            function: A cost function that takes index i, current state v, and proposed symbol σ
                      as arguments, and returns the dynamic cost.
        """
        def cost(i, v, sigma):
            return calculate_cost(target_sequence, coding_positions, codon_usage, i, v, sigma, alpha, beta, w)

        return cost
