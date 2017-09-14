
import os

class PaperFormatter:

    def __init__(self, main_filename, src_dir, dest_dir):
        self.main_filename = main_filename
        self.src_dest = src_dir
        self.dest_dir = dest_dir

    def make_paper(self):
        print(self.main_filename)
        print(self.src_dest)
        print(self.dest_dir)

        self.parse_main_file()

    def parse_main_file(self):
        full_main_filename = os.path.join(self.src_dest, self.main_filename)

        with open(full_main_filename) as f:

            for line in f:
                print(line)

