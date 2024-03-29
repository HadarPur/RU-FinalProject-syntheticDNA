from Bio.Seq import Seq
import random


class DNAHighlighter:
    def __init__(self):
        """
        Initializes a DNAHighlighter object with a DNA sequence.
        """
        pass

    def highlight_coding_regions(self, seq, coding_regions):
        """
        Highlights coding regions within the DNA sequence using colored escape codes.

        Parameters:
            coding_regions (list of Seq): List of coding regions (Seq objects) to be highlighted.

        Returns:
            str: DNA sequence with highlighted coding regions using escape codes.
        """
        available_color_codes = [code for code in range(91, 98) if code not in [93, 97]]  # Define available color codes
        region_color_mapping = {}  # Create a dictionary to map coding regions to color codes

        # Assign colors to coding regions
        for region_seq in coding_regions:
            if not available_color_codes:
                break
            color_code = random.choice(available_color_codes)  # Randomly select a color code
            available_color_codes.remove(color_code)  # Remove the used color code from the available list
            region_color_mapping[str(region_seq)] = f'\033[{color_code}m'  # Map the region sequence to the color code

        highlighted_seq = str(seq)  # Convert the DNA sequence to a string for highlighting

        # Highlight coding regions in the DNA sequence
        for region_seq in coding_regions:
            region_str = str(region_seq)
            region_start = highlighted_seq.find(region_str)  # Find the start position of the region

            while region_start >= 0:
                region_end = region_start + len(region_str)
                color_code = region_color_mapping[region_str]

                # Highlight the region with the assigned color code
                highlighted_seq = (
                    highlighted_seq[:region_start] +
                    color_code + highlighted_seq[region_start:region_end] + '\033[0m' +  # Reset color code
                    highlighted_seq[region_end:]
                )

                region_start = highlighted_seq.find(region_str, region_end)  # Find the next occurrence

        return highlighted_seq  # Return the DNA sequence with highlighted coding regions

    def get_coding_and_non_coding_regions(self, seq):
        """
        Identifies and returns coding regions within the DNA sequence.

        Returns:
            list of dict: List of dictionaries containing "seq" (Seq object) and "is_coding_region" (bool) keys.
        """
        start_codon = Seq("ATG")  # Define the start codon
        stop_codons = [Seq("TAA"), Seq("TAG"), Seq("TGA")]  # Define the stop codons
        coding_regions = []  # Create a list to store coding regions

        i = 0
        non_coding_region = ""  # Initialize a variable to store non-coding sequences
        in_coding_region = True

        # Traverse the DNA sequence to identify coding regions
        while i < len(seq):
            found_stop_codons = any(seq[j:j + 3] in stop_codons for j in range(i + 3, len(seq), 3))
            if seq[i:i + 3] == start_codon and found_stop_codons:  # Check for the start codon
                if in_coding_region is False:
                    coding_regions.append({
                        "seq": non_coding_region,
                        "is_coding_region": False
                    })
                    non_coding_region = ""

                start_idx = i
                in_coding_region = True
                for j in range(i + 3, len(seq), 3):
                    if seq[j:j + 3] in stop_codons:  # Check for stop codons
                        coding_regions.append({
                            "seq": seq[start_idx:j + 3],
                            "is_coding_region": True
                        })
                        i = j + 3
                        in_coding_region = False
                        break
                if in_coding_region:
                    i += 3
            else:
                in_coding_region = False
                non_coding_region += seq[i]
                i += 1

        if non_coding_region == seq and len(coding_regions) == 0:
            coding_regions.append({
                "seq": non_coding_region,
                "is_coding_region": False
            })

        return coding_regions  # Return a list of dictionaries containing coding and non-coding regions

    def extract_coding_regions_with_indexes(self, region_list):
        """
        Extracts coding regions and their indexes from a list of dictionaries.

        Args:
            region_list (list of dict): List of dictionaries containing "seq" (Seq object) and "is_coding_region" (bool) keys.

        Returns:
            tuple: A tuple containing two lists:
                - List of Seq objects representing coding regions.
                - List of indexes (int) corresponding to the coding regions.
        """

        coding_regions = []  # Create a list to store coding regions
        coding_indexes = []  # Create a list to store indexes of coding regions

        for index, region in enumerate(region_list):
            if region["is_coding_region"]:
                coding_regions.append(region["seq"])  # Add coding region to the list
                coding_indexes.append(index)  # Add index to the list

        return coding_regions, coding_indexes  # Return coding regions and their corresponding indexes

    def update_coding_regions(self, region_list, coding_indexes, coding_regions_to_exclude):
        """
        Update the 'is_coding_region' values in a list of dictionaries at specified indices.

        Args:
            region_list (list of dict): List of dictionaries containing "seq" (Seq object) and " is_coding_region" (bool) keys.
            coding_regions_to_exclude (dict of str): Dictionary of sequences to exclude.

        Returns:
            region_list: Updated list of dictionaries with modified 'is_coding_region' values.
        """

        for key, value in coding_regions_to_exclude.items():
            coding_region_index = coding_indexes[key]
            region = region_list[coding_region_index]
            if region['seq'] == value:
                region['is_coding_region'] = False
                region_list[coding_region_index] = region  # Update the 'is_coding_region' value

        return region_list  # Return the updated list of dictionaries

