from utils.amino_acid_utils import AminoAcidScheme
from settings.costs_settings import s_coding_region, o_coding_region, w_coding_region, x_coding_region
from settings.costs_settings import o_non_coding_region, w_non_coding_region, x_non_coding_region


# Define a class called CodonScorer
class CodonScorer:
    def __init__(self):
        """
        Initializes a CodonScorer object with a codon scoring scheme.
        """

        # Initialize the object with codon scoring schemes for coding and non-coding regions
        self.coding_region_scheme = AminoAcidScheme(w_coding_region, o_coding_region, x_coding_region, s_coding_region).get_cost_table_coding_region()
        self.non_coding_region_scheme = AminoAcidScheme(w_non_coding_region, o_non_coding_region, x_non_coding_region).get_cost_table_none_coding_region()

    def get_codon_scores(self, codon, codon_scores):
        """
        Retrieves the scoring information for a given codon.

        Parameters:
            codon (str): Codon sequence for which scoring information is needed.

        Returns:
            list or None: List of scoring information for the codon, or None if codon is not found.
            :param codon:
            :param codon_scores:
        """
        # Iterate through codon scores
        for amino_acid_dict in codon_scores:
            for codon_key, scoring_dicts in amino_acid_dict.items():
                if codon_key == codon:
                    return scoring_dicts
        return None  # Codon not found

    def calculate_scores(self, sequences):
        """
        Calculates scores for each codon in a list of sequences using the provided scoring schemes based on 'is_coding_region'.

        Parameters:
            sequences (list of dict): List of dictionaries, each containing a 'seq' key and an 'is_coding_region' key.

        Returns:
            list: List of scores for each codon in the sequences.
        """
        scores_array = []  # To store scores for each codon

        for seq_info in sequences:
            sequence = seq_info['seq']
            is_coding_region = seq_info['is_coding_region']

            # Select the appropriate scoring scheme based on 'is_coding_region'
            if is_coding_region:
                # Iterate through the sequence in steps of 3 (codons)
                for i in range(0, len(sequence), 3):
                    codon = sequence[i:i + 3]
                    score = self.get_codon_scores(codon, self.coding_region_scheme)
                    if score:
                        scores_array = scores_array + score
                    else:
                        print(f"Warning: Codon {codon} not found in the scoring scheme.")
            else:
                # Iterate through the sequence in steps of 1
                for i in range(0, len(sequence)):
                    codon = sequence[i]
                    score = self.get_codon_scores(codon, self.non_coding_region_scheme)
                    if score:
                        scores_array = scores_array + score
                    else:
                        print(f"Warning: Codon {codon} not found in the scoring scheme.")

        return scores_array
