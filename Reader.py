import os
import os.path
import json


class Reader:
    # init the Reader class with a base_folder name

    # call get_next_file() to get a tuple (doc_id, the actual JSON file)
    # call get_num_of_file_processed() to get the number of files that are already processed
    # call self.doc_id_dict.items() to get a list of tuples (doc_id : path_to_file)

    # ** all other functions and variables are internal or for testing purposes **

    def __init__(self, base_folder):

        if not os.path.isdir(base_folder):
            raise NoMoreFilesToReadException(f'{base_folder} is not a valid path!')

        # Store the name/path of the base folder
        self.base_folder = base_folder

        # Get a list of files/directories under the base folder
        sub_folder_name_list = os.listdir(base_folder)

        # Filter out paths that is not a directory (e.g. filter out .DS_Store files)
        self.sub_folder_file_path_list = [os.path.join(self.base_folder, sub) for sub in sub_folder_name_list if
                                          os.path.isdir(os.path.join(self.base_folder, sub))]

        # A list of files under the current sub folder
        self.current_sub_folder_file_path_list = list()
        self.get_next_sub_folder()

        # Track the next doc id to be assigned (this also tracks the total number of files processed)
        self.next_doc_id_to_be_assigned = 1

        # Track the path that the doc id is assigned to
        self.doc_id_dict = dict()  # doc_id : path_to_file

    def get_next_sub_folder(self) -> None:
        if len(self.current_sub_folder_file_path_list) == 0:
            sub_folder_path = self.sub_folder_file_path_list.pop()

            sub_folder_file_name_list = os.listdir(sub_folder_path)

            self.current_sub_folder_file_path_list = [os.path.join(sub_folder_path, file_name) for file_name in
                                                      sub_folder_file_name_list if
                                                      file_name.endswith('.json') and os.path.isfile(
                                                          os.path.join(sub_folder_path, file_name))]

    def print_not_processed_sub_folders(self) -> None:
        for f in self.sub_folder_file_path_list:
            print(f)

    def print_not_processed_files_in_current_sub_folder(self) -> None:
        for f in self.current_sub_folder_file_path_list:
            print(f)

    def print_process_doc_id_and_file(self) -> None:
        print('doc_id : file_path')

        for doc_id, file_path in self.doc_id_dict.items():
            print(f'{doc_id} : {file_path}')

    def get_num_of_file_processed(self) -> int:
        return self.next_doc_id_to_be_assigned - 1

    def get_next_file(self) -> (int, dict):  # returns (doc_id, processed_json_as_dict)
        if len(self.sub_folder_file_path_list) > 0 or len(self.current_sub_folder_file_path_list) > 0:
            # There are stuff left to be processed!

            # If the sub folder is empty, get the next sub folder
            if len(self.current_sub_folder_file_path_list) == 0:
                self.get_next_sub_folder()

            # Get the file path of the next file to be processed
            file_path = self.current_sub_folder_file_path_list.pop()

            # Log the doc id dict
            self.doc_id_dict[self.next_doc_id_to_be_assigned] = file_path

            # Move doc id one digit forward
            self.next_doc_id_to_be_assigned += 1

            # Open the file, and process it with json.load().
            # processed_file is the json dict to be returned
            with open(file_path, "r") as file:
                processed_file = json.load(file)

            return self.next_doc_id_to_be_assigned - 1, processed_file

        else:
            # If there's no more files to be processed, raise exception
            raise NoMoreFilesToReadException(f'Reader has processed all files under folder {self.base_folder}. '
                                             f'An exception has been raised to notify the main function to stop the loop.')


# Custom Exception
class NoMoreFilesToReadException(Exception):
    pass


# ** This part is just for testing the Reader class **
# Use the main function in Indexer.py to build the indexer with this class
if __name__ == '__main__':
    reader = Reader('DEV')

    # reader.print_not_processed_sub_folders()
    # reader.print_not_processed_files_in_current_sub_folder()

    try:
        while True:
            print(reader.get_next_file())

    except NoMoreFilesToReadException as e:
        print(e)

    # reader.print_process_doc_id_and_file()
    # print('Total number of files processed: ' + str(reader.get_num_of_file_processed()))
