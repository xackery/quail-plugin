import io
import wce.parse as parse

# WORLDDEF
# 	NEWWORLD 0
# 	ZONE 0
# 	EQGVERSION? NULL

class world_def:
    new_world:int
    zone:int
    eqg_version:tuple[int, None]

    def __init__(self, r:io.TextIOWrapper):
        records = parse.property(r, "NEWWORLD", 1)
        self.new_world = int(records[1])
        records = parse.property(r, "ZONE", 1)
        self.zone = int(records[1])
        records = parse.property(r, "EQGVERSION?", 1)
        self.eqg_version = (int(records[1]) if records[1] != "NULL" else None)

    def write(self, w:io.TextIOWrapper):
        w.write("WORLDDEF\n")
        w.write(f"\tNEWWORLD {self.new_world}\n")
        w.write(f"\tZONE {self.zone}\n")
        w.write(f"\tEQGVERSION? {self.eqg_version}\n")





