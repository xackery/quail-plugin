import io
import wce.parse as parse

# TRACKINSTANCE "C01AELFC01A_ELF_TRACK"
# 	TAGINDEX 0
# 	SPRITE "ELF_DMSPRITEDEF"
# 	DEFINITION "C01AELFC01A_ELF_TRACKDEF"
# 	DEFINITIONINDEX 0
# 	INTERPOLATE 0
# 	REVERSE 0
# 	SLEEP? NULL

class track:
    tag:str
    tag_index:int
    sprite:str
    definition:str
    definition_index:int
    interpolate:int
    reverse:int
    sleep: tuple[str, None]

    def __init__(self, tag:str, r:io.TextIOWrapper):
        self.tag = tag
        records = parse.property(r, "TAGINDEX", 1)
        self.tag_index = int(records[1])
        records = parse.property(r, "SPRITE", 1)
        self.sprite = records[1]
        records = parse.property(r, "DEFINITION", 1)
        self.definition = records[1]
        records = parse.property(r, "DEFINITIONINDEX", 1)
        self.definition_index = int(records[1])
        records = parse.property(r, "INTERPOLATE", 1)
        self.interpolate = int(records[1])
        records = parse.property(r, "REVERSE", 1)
        self.reverse = int(records[1])
        records = parse.property(r, "SLEEP?", 1)
        self.sleep = (records[1] if records[1] != "NULL" else None)

    def write(self, w:io.TextIOWrapper):
        w.write(f"TRACKINSTANCE \"{self.tag}\"\n")
        w.write(f"\tTAGINDEX {self.tag_index}\n")
        w.write(f"\tSPRITE {self.sprite}\n")
        w.write(f"\tDEFINITION {self.definition}\n")
        w.write(f"\tDEFINITIONINDEX {self.definition_index}\n")
        w.write(f"\tINTERPOLATE {self.interpolate}\n")
        w.write(f"\tREVERSE {self.reverse}\n")
        w.write(f"\tSLEEP? {self.sleep}\n")

