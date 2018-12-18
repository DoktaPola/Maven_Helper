import os
import sys
import zipfile


def traverse_dir(file_path_in, file_path_out):
    my_array = []
    snapshot_file = open(file_path_out, 'w')
    for subdir, dirs, files in os.walk(file_path_in):
        for file in files:
            if file.endswith('.pom'):
                new_subdir = subdir.replace(file_path_in + os.sep, "")
                snapshot_file.write(new_subdir + '\n')
                my_array.append(os.path.join(subdir, file))
    snapshot_file.close()
    return my_array


def find_pom(file_path):
    pom_file = None
    for subdir, dirs, files in os.walk(file_path):
        for file in files:
            if file.endswith('.pom'):
                if pom_file:
                    raise ValueError('Found more then one .pom file')  ## где то тут проблема
                pom_file = os.path.join(subdir, file)
    if not pom_file:
        raise ValueError('Found no .pom file')
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
            # group_id_splits = a[9:-10]
            group_id_splits = a.replace('<groupId>', '')
            group_id_splits = group_id_splits.replace('</groupId>', '')
        if a.startswith('<artifactId>'):
            # artifact_id_splits = a[12:-13]
            artifact_id_splits = a.replace('<artifactId>', '')
            artifact_id_splits = artifact_id_splits.replace('</artifactId>', '')
        if a.startswith('<version>'):
            # version_splits = a[9:-10]
            version_splits = a.replace('<version>', '')
            version_splits = version_splits.replace('</version>', '')
        if group_id_splits and artifact_id_splits and version_splits:
            all += str(group_id_splits) + ":" + str(artifact_id_splits) + ":" + str(version_splits)
            all_versions.append(all)
    return all_versions


def depend_to_pom(deps):
    pom_paths = []
    for d in deps:
        parts = d.split(':')
        for i in range(0, len(parts) - 1):
            parts[i] = parts[i].replace('.', os.sep)
        s = os.sep.join(parts)
        pom_paths.append(s)
    return set(pom_paths)


def make_rec(artifact, set_of_poms, path_to_maven_folder):
    new_artifact = find_pom(artifact)
    if new_artifact:
        all_file = open_each_file(new_artifact)
        version = get_version(all_file)
        poms = depend_to_pom(version)
        for pom in poms:
            set_of_poms.add(pom)
            make_rec(pom, set_of_poms, path_to_maven_folder)


def read_snap_file(snapshot):
    snapshot_file = open(snapshot, 'r')
    set_pom = set()
    for line in snapshot_file:
        set_pom.add(line.strip())
    snapshot_file.close()
    return set_pom


def find_difference(local, deps):
    remote = depend_to_pom(deps)
    missed_in_local = remote.difference(local)
    if missed_in_local == 0:
        print('NO DEPENDENCES')
    return missed_in_local


def zipdir(path, zip_file_name):
    for root, dirs, files in os.walk(path):
        newzip = zipfile.ZipFile(zip_file_name, 'a')
        for file in files:
            newzip.write(root + os.sep + file)
        newzip.close()


def main():
    help_message = '''Please, enter a valid request!'
              If you want to use A LOCAL MODE, you should enter:
               (--snapshot-maven-local-repo, full path to your snapshot file,  full path to Maven folder.)
              Example: --snapshot-maven-local-repo .\\SNAPSHOT .\\local
              If you want to use A REMOTE MODE, you should enter:
              (--pack-missing-artifact-deps, missing library, full path to snapshot file, full path to Maven folder, 
                 full path where you want to your save finale archive.)'
              Example: --pack-missing-artifact-deps .\\remote\\org\\apache\\jena\\jena-tdb2\\3.8.0 .\\SNAPSHOT .\\remote .\\MY_AR.zip'''

    if len(sys.argv) < 2:
        print(help_message)
    else:
        if sys.argv[1] == '--snapshot-maven-local-repo':
            path_to_file = sys.argv[2]
            path_to_maven_folder = sys.argv[3]
            traverse_dir(path_to_maven_folder, path_to_file)
        elif sys.argv[1] == '--pack-missing-artifact-deps':
            artifact = sys.argv[2]
            path_to_maven_folder = sys.argv[4]
            snapshot_file = sys.argv[3]
            zip_file_name = sys.argv[5]
            zipdir(artifact, zip_file_name)
            set_of_poms = set()
            make_rec(artifact, set_of_poms, path_to_maven_folder)
            local_set = read_snap_file(snapshot_file)
            difference = find_difference(local_set, set_of_poms)
            for d in difference:
                zipdir(path_to_maven_folder + os.sep + d, zip_file_name)
        else:
            print(help_message)


if __name__ == "__main__":
    main()


# --pack-missing-artifact-deps C:\MAVEN_HELPER\remote\org\apache\jena\jena-tdb2\3.8.0 C:\Users\Полина\PycharmProjects\MavenHelper\SNAPSHOT C:\MAVEN_HELPER\remote C:\MAVEN_HELPER\MY_AR.zip