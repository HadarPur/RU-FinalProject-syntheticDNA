# DNA sequence
# S = "ATGTACATACAGTAA"     # Y, I, Q
# S = "TATAATGTACATACAGTAA"     # one coding
# S = "ATGTACATACAGTAAB"     # not valid
# S = "TACAGTAA"     # no coding
# S = "TACATACAGTAA"     # no coding
# S = "ATGTACATACAG"     # Y, I, Q
# S = "TACATACAGATG"     # Y, I, Q
# S = "ATG"     # start codon
# S = "TAA"     # stop codon
# S = "ATGTAA"     # no coding region
# S = ''     # empty string
# S = "TACATACAGATACAGATGATGTACATACAGTAA"     # one coding
# S = "TTACATACAGATGTACATACAGTAATACATACAGTAATACATACAGATGTACATACAGTAA"  # two coding
# S = "TTACATACAGATGTACATACAGTAATACATACAGTAATACATACAGATGTACATACAGTAAATGTAA"  # tree coding
# S = "TATAATGTACATACAGTAAATGTACATACAGATGATGTACATACAGTAA"
# S = "TATAATGTACATACAGTAAATGATGTACATACAGATGATGTACATACAGATGTAATACATACAGATGATGTACATACAGATGTAATAA"  # contained
S = "ATGCATGCGTAGCTAGCTGATCGTAGCTAGTCGATCGATCGTAGCTAG"