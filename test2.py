import os
import sys


# rootdir = 'C:\\Users\\Полина\\Desktop\\MAVEN_HELPER\\org\\apache\\jena'


def traverse_dir(file_path_in, file_path_out):
    my_array = []
    snapshot_file = open(file_path_out, 'w')
    for subdir, dirs, files in os.walk(file_path_in):
        for file in files:
            if file.endswith('.pom'):
                snapshot_file.write(file + '\n')
                my_array.append(os.path.join(subdir, file))
    snapshot_file.close()
    return my_array


# var = traverse_dir(rootdir, path_to_file)


def open_each_file(var):
    all_depend = []
    for file in var:
        f = open(file, 'r')
        lines = f.readlines()
        f.close()
        start, end = '<dependencies>', '</dependencies>'
        Flag = False
        for line in lines:
            line = line.strip()
            if Flag:
                if line == end:
                    Flag = False
                else:
                    all_depend.append(line)
            elif line == start:
                Flag = True
    return all_depend


# all_file = open_each_file(var)


def get_version(arr):
    all_versions = []
    for a in arr:
        if a.startswith('<version>'):
            version_splits = a[9:-10]
            group_id = arr[a.find('<version>') + 2]
            group_id_splits = group_id[9:-10]
            artifact_id = arr[a.find('<version>') + 3]
            artifact_id_splits = artifact_id[12:-13]
            all = group_id_splits + ":" + artifact_id_splits + ":" + version_splits
            all_versions.append(all)
    return all_versions


# version = get_version(all_file)


def make_dict(path, values):
    dependency = dict(zip(path, values))
    print(dependency)


# make_dict(var, version)


# stop_words = ('<', '/', '${ver')
#
#
# def filter_stop_words(freq_arr: list, stop_words: tuple):
#     # stop_words = ('<', '/', '${ver')
#     frequencies = freq_arr.copy()
#     for word in stop_words:
#         if word in frequencies:
#             del frequencies[word]
#     return frequencies
#
#
# filter = filter_stop_words(version, stop_words)
# print(filter)

def main():
    # print('This is the name of the script: ', sys.argv[0])
    # print("This is first argument: ", sys.argv[1])
    # print("Number of arguments: ", len(sys.argv))
    # print("The arguments are: ", str(sys.argv))

    user_mode = sys.argv[1]  # локально или удаленно
    path_to_maven_folder = sys.argv[3]
    path_to_file = sys.argv[2]
    artifact = sys.argv[2]
    if user_mode == '--snapshot-maven-local-repo':
        traverse_dir(path_to_maven_folder, path_to_file)
    elif user_mode == '--pack-missing-artifact-deps':
        path_to_maven_folder = sys.argv[2]
        path_to_file = sys.argv[3]
        var = traverse_dir(path_to_maven_folder, path_to_file)
        all_file = open_each_file(var)
        version = get_version(all_file)
        var = traverse_dir(path_to_maven_folder, path_to_file)
        make_dict(var, version)


# elif execute_as_pack_missings_artifacts_mode:
#         pack_missings_artifacts(artifact, snapshot_file, path_to_maven_folder)


if __name__ == "__main__":
    main()
