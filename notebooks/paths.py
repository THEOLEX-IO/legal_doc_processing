import os


# ### 1.5 - paths

one_file = "data/order-vision-financial-markets-llc.txt"
one_file_path = os.getcwd() + "/" + one_file
assert os.path.isfile(one_file_path)

test_dataset_folder = "tests/dataset/features"
_files_path = os.getcwd() + "/" + test_dataset_folder
files_test_path_list = [
    _files_path + "/" + filename for filename in os.listdir(_files_path)
]