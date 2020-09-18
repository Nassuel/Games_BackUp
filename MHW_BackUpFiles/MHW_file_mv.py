import os
import shutil
import zipfile as zipf
import argparse
from datetime import datetime
from variables import file_location


class BackUpper:
    # Varibles for archive name
    _master_rank = ''
    _hunter_rank = ''

    # File paths
    _in_origin = ''
    _in_dest_path = ''
    _in_cleanup_dest_path = ''

    def __init__(self, master_rank, hunter_rank, dict_from_file, dry_run):
        self._master_rank = master_rank
        self._hunter_rank = hunter_rank

        self.dry_run = dry_run

        self._in_origin = dict_from_file['in_origin']
        self._in_dest_path = dict_from_file['in_dest_path']
        self._in_cleanup_dest_path = dict_from_file['in_cleanup_dest_path']

        self.full_dest_path = self._in_dest_path + '{0}({1},{2})'.format(
            datetime.now().strftime('%d%m%Y_%H,%M,%S'), self._master_rank, self._hunter_rank
        )

    def _copy_save_data(self):
        shutil.make_archive(self.full_dest_path, 'zip', self._in_origin)
        return

    def _clean_up_old_files(self):
        cleanup_path = self._in_dest_path
        cleanup_dst_path = self._in_cleanup_dest_path
        file_to_not_move = self.full_dest_path.split('/')[-1]
        files_in_dir = os.listdir(cleanup_path)

        for file in files_in_dir:
            file_to_move_path = cleanup_path + file
            if file_to_not_move != file:
                # print(file_to_not_move)
                # shutil.move(file_to_move_path, cleanup_dst_path)
                shutil.make_archive(cleanup_dst_path, 'zip', file_to_move_path)

        print('Files have been cleaned up successfully.')
        return

    def run(self):
        if not self.dry_run:
            self._copy_save_data()
            self._clean_up_old_files()
        else:
            print('You\'re currently doing a dry run!')

# def main(dictionary):
#     # print(dictionary)
#     backupper_obj = BackUpper(
#         dictionary['mr'], dictionary['hr'], dictionary['file_location'], dictionary['dryrun']
#     )

#     backupper_obj.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse command line argument for BackUpper program')
    parser.add_argument('-hr', type=int)
    parser.add_argument('-mr', type=int)
    parser.add_argument('-dryrun', type=str, required=False, default=0)
    args = parser.parse_args()
    input_to_main = dict(
        file_location=file_location['file_locations'], hr=args.hr, mr=args.mr, dryrun=args.dryrun
    )

    # print(input_to_main)
    # main(input_to_main)

    backupper_obj = BackUpper(
        args.mr, args.hr, file_location['file_locations'], args.dryrun
    )

    backupper_obj.run()
