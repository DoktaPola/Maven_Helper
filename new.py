import os
import sys
import shutil
import zipfile


def traverse_dir(file_path_in, file_path_out):
    my_array = []
    snapshot_file = open(file_path_out, 'w')
    for subdir, dirs, files in os.walk(file_path_in):
        for file in files:
            if file.endswith('.pom'):
                new_subdir = subdir.replace("C:\\MAVEN_HELPER\\local\\", "")   # убрала C:\MAVEN_HELPER
                # new_subdir = new_subdir[0:new_subdir.rfind('\\')]
                snapshot_file.write(new_subdir + '\n')
                my_array.append(os.path.join(subdir, file))
    snapshot_file.close()
    return my_array


def find_pom(file_path):
    pom_file = None
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
    group_id_splits = None
    artifact_id_splits = None
    version_splits = None
    for a in arr:
        all = ''
        if a.startswith('<groupId>'):
            group_id_splits = a[9:-10]
        if a.startswith('<artifactId>'):
            artifact_id_splits = a[12:-13]
        if a.startswith('<version>'):
            version_splits = a[9:-10]
        if group_id_splits and artifact_id_splits and version_splits:
            all += str(group_id_splits) + ":" + str(artifact_id_splits) + ":" + str(version_splits)
            all_versions.append(all)
    return all_versions


def depend_to_pom(deps, path_to_maven): # убрала C:\MAVEN_HELPER
    pom_paths = []
    for d in deps:
        parts = d.split(':')
        for i in range(0, len(parts) - 1):
            parts[i] = parts[i].replace('.', '\\')
        s = '\\'.join(parts)
        pom_paths.append(s)
    return set(pom_paths)


def make_rec(artifact, set_of_poms):
    path_to_maven_folder = sys.argv[4]   # стоит ли это сюда включать?
    new_artifact = find_pom(artifact)  # добавлять тут библиотеку потерянную

    if new_artifact:
        all_file = open_each_file(new_artifact)
        version = get_version(all_file)
        poms = depend_to_pom(version, path_to_maven_folder)
        for pom in poms:
            set_of_poms.add(pom)
            make_rec(pom, set_of_poms)


def read_snap_file(snapshot):
    snapshot_file = open(snapshot, 'r')
    set_pom = set()
    for line in snapshot_file:
        set_pom.add(line.strip())
    snapshot_file.close()
    return set_pom


def find_difference(file_path_in, local, deps):
    remote = depend_to_pom(deps, file_path_in)
    missed_in_local = remote.difference(local)
    if missed_in_local == 0:
        print('NO DEPENDENCES')
    return missed_in_local


def zipdir(path):
    for root, dirs, files in os.walk(path):
        zname = r'C:\MAVEN_HELPER\MY_AR.zip'
        newzip = zipfile.ZipFile(zname, 'a')
        for file in files:
            newzip.write(root + '\\' + file)  # добавляем файл в архив
        newzip.close()


def main():
    user_mode = sys.argv[1]
    path_to_file = sys.argv[2]

    if user_mode == '--snapshot-maven-local-repo':
        path_to_maven_folder = sys.argv[3]
        traverse_dir(path_to_maven_folder, path_to_file)
    elif user_mode == '--pack-missing-artifact-deps':
        artifact = sys.argv[2]
        path_to_maven_folder = sys.argv[4]
        snapshot_file = sys.argv[3]
        zipdir(artifact)
        set_of_poms = set()
        make_rec(artifact, set_of_poms)
        local_set = read_snap_file(snapshot_file)
        difference = find_difference(path_to_maven_folder, local_set, set_of_poms)
        for d in difference:
            zipdir(path_to_maven_folder + "\\" + d)
    else:
        print('Please, enter a valid request! If you want to use A LOCAL MODE, you should enter:'
              ' (--snapshot-maven-local-repo, full path to your snapshot file,  full path to Maven folder.)'
              'If you want to use A REMOTE MODE, you should enter:'
              '(--pack-missing-artifact-deps, missing library, full path to snapshot file, full path to Maven folder.)')


if __name__ == "__main__":
    main()
