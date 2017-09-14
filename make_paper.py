

from PaperFormatter import PaperFormatter

import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

src_paper_dir = config.get('PaperFormatter', 'src_paper_dir')
dest_paper_dir = config.get('PaperFormatter', 'dest_paper_dir')

main_filename = config.get('PaperFormatter', 'main_filename')

pf = PaperFormatter(main_filename, src_paper_dir, dest_paper_dir)
pf.make_paper()


