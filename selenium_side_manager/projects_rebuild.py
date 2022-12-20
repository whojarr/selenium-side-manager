import json
import os
import argparse
import uuid


class ProjectsRebuld():

    def __init__(self, project_definitions_folder="./project_definitions", project_tests_folder="./tests"):

        self.project_definitions_folder = project_definitions_folder
        self.project_tests_folder = project_tests_folder

    def project_list(self):
        project_files = os.listdir(self.project_definitions_folder)
        return project_files

    def project_definition(self, project_file):
        with open(os.path.join(self.project_definitions_folder, project_file)) as json_file:
            project_definition = json.load(json_file)
        return project_definition

    def project_definition_from_file(self, project_file):
        return self.project_definition(project_file)

    def project_definition_from_name(self, project_name):
        project_files = self.project_list()
        for project_file in project_files:
            if project_name in project_file:
                return self.project_definition(project_file)
        return None

    def project_definition_from_id(self, project_id):
        project_files = self.project_list()
        for project_file in project_files:
            if project_id in project_file:
                return self.project_definition(project_file)
        return None

    def project_rebuild(self, project_filename):

        open_path = os.path.join(
            self.project_definitions_folder, project_filename)

        with open(open_path) as file:
            project_raw = file.read()
            project_data = json.loads(project_raw)

        name = project_data['name']
        print(f'\nProject: {name}')
        output_filename = project_data['output_filename']
        import_filename = project_data.get('import_side', '')
        import_tests = project_data.get('import_tests', [])
        combine_tests = project_data.get('combine_tests', [])

        if not import_filename == '':

            with open(import_filename, 'r') as import_side_file:
                import_side_raw = import_side_file.read()

            with open(output_filename, 'w') as output_file:
                output_file.write(import_side_raw)

        if len(import_tests) > 0:

            if not os.path.isfile(output_filename):
                empty = self.side_file_blank(name)
                with open(output_filename, 'w') as newfile:
                    newfile.write(json.dumps(empty, indent=2))

            with open(output_filename, 'r') as output_file_original:
                output_file_original_raw = output_file_original.read()
                output_file_data = json.loads(output_file_original_raw)

            for test_filename in import_tests:

                if os.path.isfile(test_filename):

                    with open(test_filename, 'r') as filename:
                        test_file_raw = filename.read()
                        test_file_data = json.loads(test_file_raw)

                    test_name = test_file_data['name']
                    print(f'processing test {test_name}')

                    test_found = False
                    for index in range(len(output_file_data['tests'])):
                        if test_name == output_file_data['tests'][index]['name']:
                            print(f'replacing {test_name} with imported test')
                            output_file_data['tests'][index] = test_file_data
                            test_found = True
                    if not test_found:
                        output_file_data['tests'].append(test_file_data)

            with open(output_filename, 'w') as newfile:
                newfile.write(json.dumps(output_file_data, indent=2))

        if len(combine_tests) > 0:
            for combine in combine_tests:
                self.side_tests_combine(
                    combine['from'], combine['to'], combine['where'], combine['replace'], output_filename)


    def side_file_blank(self, name):
        sideid = uuid.uuid4()
        return {
            "name": name,
            "id": str(sideid),
            "version": "2.0",
            "description": "",
            "url": "http://localhost/",
            "tests": []
        }

    def side_tests_combine(self, test_from, test_to, combine_where, test_replace, output_filename):

        if combine_where in ['before', 'prepend']:

            print(
                f'add {test_from} to the start of {test_to} and replace {test_replace}')

            test_from_data = None
            if os.path.isfile(test_from):
                with open(test_from) as file:
                    test_from_data = file.read()

            test_to_data = None
            if os.path.isfile(test_to):
                with open(test_to) as file:
                    test_to_data = file.read()

            if test_from_data and test_to_data:
                from_json = json.loads(test_from_data)
                to_json = json.loads(test_to_data)

                if combine_where in ['before', 'prepend']:
                    # add each dict from from_json to the beginning of to_json['commands']
                    to_json['commands'] = from_json['commands'] + \
                        to_json['commands']
                else:
                    to_json['commands'] = to_json['commands'] + \
                        from_json['commands']

                combined_output_file_data = None
                with open(output_filename, 'r') as output_file_original:
                    output_file_original_raw = output_file_original.read()
                    combined_output_file_data = json.loads(
                        output_file_original_raw)

                # replace the record in combined_output_file_data where id = test_to with to_json
                for index in range(len(combined_output_file_data['tests'])):
                    if combined_output_file_data['tests'][index]['id'] == test_replace:
                        combined_output_file_data['tests'][index] = to_json
                        break

                print(f'writing output to {output_filename}')
                with open(output_filename, 'w') as newfile:
                    newfile.write(json.dumps(
                        combined_output_file_data, indent=2))


def run():

    parser = argparse.ArgumentParser(
        description='rebuilds .side files with tests split from other side files based on json specs usually in ./project_definitions')
    parser.add_argument(
        '--project-definitions-folder', dest='project_definitions_folder', default='./project_definitions', help='folder where project definitions are stored')

    args = parser.parse_args()

    rebuild = ProjectsRebuld(
        project_definitions_folder=args.project_definitions_folder)
    for project in rebuild.project_list():
        rebuild.project_rebuild(project)
