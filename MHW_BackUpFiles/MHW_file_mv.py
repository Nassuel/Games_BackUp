import os
import shutil
import argparse
from datetime import datetime
from variables import file_location

class BackUpper:
    _master_rank = ''
    _hunter_rank = ''
    _dict_from_file = {}

    def __init__(self, master_rank, hunter_rank, dict_from_file):
        self._master_rank = master_rank
        self._hunter_rank = hunter_rank
        self._dict_from_file = dict_from_file

    def copy_save_data(self, f_origin_path, f_dest_path):
        try:
            shutil.copytree(f_origin_path, f_dest_path)
            print("File copied successfully.")

        # If there is any permission issue
        except PermissionError:
            print("Permission denied.")

        # For other errors
        except:
            print("Error occurred while copying file.")

        return

    def clean_up_old_files(self, dest_path):
        cleanup_path = self._dict_from_file['in_dest_path']
        cleanup_dst_path = self._dict_from_file['in_cleanup_dest_path']
        file_to_not_move = dest_path.split('/')[-1]
        files_in_dir = os.listdir(cleanup_path)

        for file in files_in_dir:
            files_to_move = cleanup_path + file
            if file_to_not_move != file:
                # print(file_to_not_move)
                shutil.move(files_to_move, cleanup_dst_path)

        print('Files have been cleaned up successfully.')
        return

    def run(self):
        today_dt = datetime.now()
        full_dest_path = self._dict_from_file['in_dest_path'] + '{0}({1},{2})'.format(
            today_dt.strftime('%d%m%Y_%H,%M,%S'), self._master_rank, self._hunter_rank)

        self.copy_save_data(self._dict_from_file['in_origin'], full_dest_path)
        self.clean_up_old_files(full_dest_path)


def main(dictionary):
    current_master_rnk = dictionary['mr']
    current_hunter_rnk = dictionary['hr']
    # print(dictionary)
    backupper_obj = BackUpper(
        current_master_rnk, current_hunter_rnk, dictionary['file_location'])

    backupper_obj.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse command line argument')
    parser.add_argument('-hr', type=int, required=True)
    parser.add_argument('-mr', type=int, required=True)
    args = parser.parse_args()
    input_to_main = dict(file_location=file_location,hr=args.hr,mr=args.mr)

    # print(input_to_main)

    main(input_to_main)
