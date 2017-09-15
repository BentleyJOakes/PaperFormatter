
import os
from subprocess import Popen, PIPE, STDOUT
import shutil


class PaperFormatter:

    def __init__(self, main_filename, src_dir, dest_dir):
        self.main_filename = main_filename
        self.src_dir = os.path.expanduser(src_dir)
        self.dest_dir = os.path.expanduser(dest_dir)

        self.image_num = 0

    def make_paper(self):
        print(self.main_filename)
        print(self.src_dir)
        print(self.dest_dir)

        self.parse_main_file()

    def parse_main_file(self):
        full_main_filename = os.path.join(self.src_dir, self.main_filename)

        full_out_filename = os.path.join(self.dest_dir, self.main_filename)

        with open(full_main_filename) as f:

            with open(full_out_filename, 'w') as g:

                self.parse_file(f, g)



    def parse_file(self, input_file, output_file, only_packages = False):
        for line in input_file:

            line = line.strip()

            if line.startswith("%"):
                continue

            print(line)

            # if line.startswith(r"\usepackage"):
            #     self.copy_package(line, output_file)

            if only_packages:
                return


            if line.startswith(r"\input"):
                self.parse_input_file(line, output_file)

                if "&" in line:
                    and_index = line.index("&")
                    output_file.write(line[and_index:] + "\n")

                continue

            if r"\includegraphics" in line:
                self.parse_image(line, output_file)
                continue

            elif r"\documentclass" in line:
                self.parse_documentclass(line)

            elif r"\bibliography{" in line:
                self.parse_bib(line, output_file)
            #     continue

            output_file.write(line + "\n")


    def copy_package(self, package_line, output_file):


        package_name = package_line.replace("{", " ").replace("}"," ").split()[1]
        #print("Package detected: " + package_line + " Name: " + str(package_name))

        package_outfile = os.path.join(self.dest_dir, package_name + ".sty")
        exists = os.path.isfile(package_outfile)
        #print("Exists: " + str(exists))

        if not exists:
            cmd = "locate " + package_name + ".sty"

            p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            stdout, stderr = p.communicate()

            for line in stdout.decode("utf-8").split("\n"):
                #print(line)
                if line.split("/")[-1] == package_name + ".sty":
                    #print("Found the package")
                    shutil.copyfile(line, package_outfile)

                    package_file = open(package_outfile)
                    self.parse_file(package_file, output_file, only_packages = True)


    def parse_documentclass(self, class_line):

        #print("Document line: " + class_line)

        class_name = class_line.replace("{", " ").replace("}", " ").split()[1]

        class_file = os.path.join(self.src_dir, class_name)
        out_class_file = os.path.join(self.dest_dir, class_name)

        shutil.copyfile(class_file + ".sty", out_class_file + ".sty")
        shutil.copyfile(class_file + ".cls", out_class_file + ".cls")


    def parse_input_file(self, input_line, output_file):


        input_name = input_line.replace("{", " ").replace("}", " ").split()[1]

        #print("Input line: " + input_line + " Name: " + input_name)

        full_input_filename = os.path.join(self.src_dir, input_name + ".tex")

        #print("Full input: " + full_input_filename)

        with open(full_input_filename) as f:
            self.parse_file(f, output_file)



    def parse_image(self, image_line, output_line):
        print("Image line: " + image_line)

        image_name = image_line.replace("{", " ").replace("}", " ").split()[1]

        full_image_name = os.path.join(self.src_dir, image_name)

        print(full_image_name)

        #found_image = False
        endings = ["", ".png", ".pdf", ".eps"]

        for ending in endings:

            if os.path.exists(full_image_name + ending):
                print("Found image: " + full_image_name + ending)
                #found_image = True

                new_image_name = str(self.image_num) + "-" + image_name.split("/")[-1]
                self.image_num += 1
                
                shutil.copyfile(os.path.join(self.src_dir, image_name + ending), os.path.join(self.dest_dir, new_image_name + ending))

                output_line.write(image_line.replace(image_name, new_image_name) + "\n")

                break



    def parse_bib(self, line, out_file):

        bib_name = line.replace("{", " ").replace("}", " ").split()[1]


        bib_filename = os.path.join(self.src_dir, bib_name + ".bib")

        new_bib_filename = os.path.join(self.dest_dir, bib_name + ".bib")

        shutil.copyfile(bib_filename, new_bib_filename)


        # print("Bib name: " + bib_filename)
        #
        # with open(bib_filename) as bib:
        #     for line in bib:
        #         out_file.write(line + "\n")











