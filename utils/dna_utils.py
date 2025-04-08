from Bio.Seq import Seq

min_coding_region_length = 7 * 3  # start_codon_length + stop_codon_length + 5 codons length in the coding area


class DNAUtils:
    @staticmethod
    def find_overlapping_regions(dna_sequence):
        start_codon = 'ATG'
        stop_codons = {'TAA', 'TAG', 'TGA'}
        coding_regions = []
        sequence_length = len(dna_sequence)

        # Check all three reading frames
        for frame in range(3):
            i = frame
            while i < sequence_length - 2:
                if dna_sequence[i:i + 3] == start_codon:
                    # Found a start codon, now look for a stop codon
                    for j in range(i + 3, sequence_length - 2, 3):
                        if dna_sequence[j:j + 3] in stop_codons:
                            if len(dna_sequence[i:j + 3]) > min_coding_region_length:
                                coding_regions.append((i, j + 2))
                                i = j + 3  # Move to the next possible start codon
                                break
                i += 3  # Move to the next codon in this reading frame

        overlaps = []

        # Compare each pair of coding regions for overlap
        for i, (start1, end1) in enumerate(coding_regions):
            for j, (start2, end2) in enumerate(coding_regions):
                if i < j:  # Ensure we only check each pair once
                    # Check if the regions overlap
                    if (start1 <= start2 <= end1) or (start2 <= start1 <= end2):
                        overlaps.append(((start1+1, end1+1), (start2+1, end2+1)))

        return len(overlaps) > 0, overlaps

    @staticmethod
    def get_overlapping_regions(dna_sequence, overlaps):
        info = f"Target Sequence:\n{dna_sequence}\n"
        for (start1, end1), (start2, end2) in overlaps:
            start1 -= 1
            end1 -= 1
            start2 -= 1
            end2 -= 1

            overlap_start = max(start1, start2)
            overlap_end = min(end1, end2)
            overlap_region = dna_sequence[overlap_start:overlap_end + 1]

            info += f"\nOverlap between regions ({start1}, {end1}) and ({start2}, {end2}):\n\n"
            info += " " * start1 + dna_sequence[start1:end1 + 1] + "\n"
            info += " " * overlap_start + '|' * len(overlap_region) + "\n"
            info += " " * start2 + dna_sequence[start2:end2 + 1] + "\n"
            info += f"\nOverlapping region: {overlap_region}\n"

        return info

    @staticmethod
    def get_coding_regions_list(coding_indexes, seq):
        """
        Constructs a dictionary of coding regions from coding index ranges.

        Parameters:
            coding_indexes (list of tuples): List of (start, end) tuples representing coding regions.
            seq (str): The full DNA sequence.

        Returns:
            dict: A dictionary where keys are coding region numbers (as strings) and values are the corresponding sequences.
        """
        coding_regions_list = {}

        for region_counter, (start, end) in enumerate(coding_indexes, start=1):
            # Extract the sequence for the current coding region
            coding_regions_list[str(region_counter)] = seq[start:end]

        return coding_regions_list

    @staticmethod
    def get_coding_and_non_coding_regions_positions(seq):
        """
        Identifies coding regions in the DNA sequence and precomputes an array of codon positions.

        Args:
            seq (str): The DNA sequence to analyze.

        Returns:
            list: An array where each index represents the codon position (1, 2, 3) for coding regions,
                  and 0 for non-coding regions.
        """
        start_codon = "ATG"
        stop_codons = {"TAA", "TAG", "TGA"}

        N = len(seq)
        codon_positions = [0] * N  # Initialize all positions as non-coding (0)
        coding_region_indexes = []

        i = 0  # Pointer to traverse the sequence

        while i < len(seq) - 2:
            if seq[i:i + 3] == start_codon:
                # Search for the nearest stop codon in the same reading frame
                for j in range(i + 3, len(seq) - 2, 3):
                    if seq[j:j + 3] in stop_codons:
                        start_idx = i
                        end_idx = j + 3  # Include the stop codon

                        # Check if this is a valid coding region
                        if end_idx - start_idx >= min_coding_region_length:
                            # Assign codon positions for this coding region
                            for k in range(start_idx, end_idx):
                                codon_positions[k] = ((k - start_idx) % 3) + 1

                            coding_region_indexes.append((start_idx, end_idx))
                        i = end_idx  # Move the pointer past the coding region
                        break
                else:
                    # No valid stop codon; treat the rest as non-coding
                    break
            else:
                i += 1

        return codon_positions, coding_region_indexes
