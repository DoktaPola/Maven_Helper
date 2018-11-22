import os
import sys


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


def find_pom(file_path):
    for subdir, dirs, files in os.walk(file_path):
        for file in files:
            if file.endswith('.pom'):
                pom_file = os.path.join(subdir, file)
    return pom_file


def open_each_file(art):
    all_depend = []
    f = open(art, 'r')
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


def make_dict(path, values):
    # deps = []
    dependency = dict([(path, values)])
    # deps.append(dependency)
    return dependency
    pass


def depend_to_pom(deps, path_to_maven):
    pom_paths = []
    for d in deps:
        parts = d.split(':')
        for i in range(0, len(parts) - 1):
            parts[i] = parts[i].replace('.', '\\')
        s = path_to_maven + '\\' + '\\'.join(parts)
        pom_paths.append(s)
    return pom_paths


def main():
    user_mode = sys.argv[1]
    path_to_file = sys.argv[2]
    artifact = sys.argv[2]
    if user_mode == '--snapshot-maven-local-repo':
        path_to_maven_folder = sys.argv[3]
        traverse_dir(path_to_maven_folder, path_to_file)
    elif user_mode == '--pack-missing-artifact-deps':
        path_to_maven_folder = sys.argv[4]
        pom = find_pom(artifact)
        all_file = open_each_file(pom)
        version = get_version(all_file)
        # deps_dict = make_dict(path_to_maven_folder, version)
        depend_to_pom(version, path_to_maven_folder)


if __name__ == "__main__":
    main()
