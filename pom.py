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
    buffer = []
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
                    buffer.append(line)
            elif line == start:
                Flag = True
    return buffer


print(open_each_file(var))
