import json
import os
import argparse


class ProjectSplit():

    def __init__(self, source_file, destination_folder="./tests"):

        self.source_file = source_file
        self.destination_folder = destination_folder

    def split(self):

        with open(self.source_file) as file:
            side_raw = file.read()
            side_json = json.loads(side_raw)

        project_name = side_json['name']

        destination_sub_folder = os.path.join(
            self.destination_folder, project_name)

        # suites = side_json['suites']
        tests = side_json['tests']
        # url = side_json['url']
        # urls = side_json['urls']

        if not os.path.isdir(self.destination_folder):
            os.mkdir(self.destination_folder)

        if not os.path.isdir(destination_sub_folder):
            os.mkdir(destination_sub_folder)

        destination_filename = os.path.join(
            destination_sub_folder, self.source_file)

        with open(destination_filename, 'w') as side_filename:
            side_filename.write(side_raw)

        for test in tests:
            test_id = test['id']
            # test_name = test['name']

            test_filename = os.path.join(
                destination_sub_folder, test_id + '.test')
            with open(test_filename, 'w') as test_file:
                test_file.write(json.dumps(test, indent=2))


def run():

    parser = argparse.ArgumentParser(description='Splits a .side file into .test files')
    parser.add_argument(
        'sidefile', type = str, help = 'the path to the .side file to split')
    parser.add_argument(
        '--destination-folder', dest = 'destination_folder', type = str, default = "./tests", help = 'the path to the destination folder')

    args=parser.parse_args()

    prj=ProjectSplit(source_file = args.sidefile,
                     destination_folder = args.destination_folder)
    prj.split()
