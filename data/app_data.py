from pathlib import Path


class InputData:
    # Input Data
    dna_sequence = None
    unwanted_patterns = None

    coding_indexes = None
    coding_positions = None
    coding_regions_list = None

    excluded_coding_indexes = None
    excluded_coding_positions = None
    excluded_regions_list = None


class CostData:
    codon_usage = None

    alpha = 1.0
    beta = 2.0
    w = 100.
    stop_codon = float('inf')


class EliminationData:
    info = None
    detailed_changes = None
    min_cost = None


class OutputData:
    output_path = Path.home() / 'Downloads'
    optimized_sequence = None

