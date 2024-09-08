import io

from wce.wce import wce

def test_wce_reader():
    e = wce()
    path = "../quail/test/globalelf_chr/_root.wce"
    file_reader = open(path, "r")
    data = file_reader.read()
    r = io.StringIO(data)
    e.parse_definitions(path, r)
    print("Done")

def test_wce_writer():
    e = wce()
    path = "../quail/test/globalelf_chr/_root.wce"
    file_reader = open(path, "r")
    data = file_reader.read()
    r = io.StringIO(data)
    e.parse_definitions(path, r)

    file_writer = open("test/_root.wce", "w")
    w = io.StringIO()
    e.write_definitions(file_writer)
    print("Done")