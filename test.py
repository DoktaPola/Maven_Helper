import os

rootdir = 'C:\\Users\\Полина\\Desktop\\MAVEN_HELPER\\org\\apache\\jena'


def traverse_dir(file_path):
    my_array = []
    for subdir, dirs, files in os.walk(file_path):
        for file in files:
            if file.endswith('.pom'):
                my_array.append(os.path.join(subdir, file))
    return my_array


var = traverse_dir(rootdir)


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


all_file = open_each_file(var)
# print(open_each_file(var))


def get_version(arr):
    all_versions = []

    for a in arr:
        if a.startswith('<version>'):
            version_splits = a[9:14]
            all_versions.append(version_splits)
            group_id = arr[a.find('<version>') + 2]
            print('group; ', group_id)
            artifact_id = arr[a.find('<version>') + 3]
            print('artifact: ', artifact_id)
            # all = line_folder + line_lib + splits
            # all_versions.append(all)
    return all_versions


version = get_version(all_file)
print(version)