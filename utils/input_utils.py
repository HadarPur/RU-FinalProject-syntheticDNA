import getopt
import sys

from utils.output_utils import Logger
from utils.text_utils import format_text_bold_for_output


def get_terminal_usage():
    return f"{format_text_bold_for_output('Usage:')}\n"\
           "\t$ python ./app.py -s <seq_file_path> -p <pattern_file_path> -o <output_path_dir>\n\n"\
           "\tThis application is designed for the elimination of unwanted patterns from synthetic DNA sequences.\n\n"\
           f"{format_text_bold_for_output('Options:')}\n"\
           "\t-s --s_path\tSpecifies the sequence file path (mandatory)\n"\
           "\t-p --p_path\tSpecifies the patterns file path (mandatory)\n"\
           "\t-o --o_path\tSpecifies the output directory path (optional-default is the downloads directory)\n\n"\
           f"{format_text_bold_for_output('Info:')}\n"\
           "\tThe elimination program via terminal is designed to run automatically without any user intervention.\n"\
           "\tPlease be advised that the program makes the following decisions:\n"\
           "\t - The minimum length of a coding region is 5 codons (excluding start and stop codons).\n"\
           "\t - If a coding region contains another coding region, the longer region will be selected.\n"\
           "\t - If a coding region overlaps another coding region, the program will raise an error message and stop.\n"


class CommandLineParser:
    def __init__(self):
        """
        Initializes a CommandLineParser object with attributes for storing file paths.
        """
        self.p_path = None
        self.s_path = None
        self.o_path = None

    def parse_args(self, argv):
        """
        Parses command-line arguments and extracts file paths from them.

        Parameters:
            argv (list): List of command-line arguments.

        Returns:
            tuple: A tuple containing the paths to the patterns file and sequence file.
        """
        try:
            opts, args = getopt.getopt(argv, "hs:p:o:r:c:t", ["help", "s_path", "p_path=", "o_path"])
        except getopt.GetoptError as err:
            Logger.error(err)
            Logger.info(get_terminal_usage)
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                Logger.info(get_terminal_usage)
                sys.exit(1)
            elif opt in ("-s", "--s_path"):
                self.s_path = arg
            elif opt in ("-p", "--p_path"):
                self.p_path = arg
            elif opt in ("-o", "--o_path"):
                self.o_path = arg

        return self.s_path, self.p_path, self.o_path


