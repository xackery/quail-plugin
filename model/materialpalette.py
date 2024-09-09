import io
import wce.parse as parse

# MATERIALPALETTE "ELF_MP"
# 	NUMMATERIALS 27
# 	MATERIAL "ELFR_EYE_MDF"

class materialpalette:
    tag:str
    materials:list[str]

    def __init__(self, tag:str, r:io.TextIOWrapper):
        self.tag = tag
        records = parse.property(r, "NUMMATERIALS", 1)
        num_materials = int(records[1])
        self.materials = []
        for i in range(num_materials):
            records = parse.property(r, "MATERIAL", 1)
            self.materials.append(records[1])

    def write(self, w:io.TextIOWrapper):
        w.write(f"MATERIALPALETTE \"{self.tag}\"\n")
        w.write(f"\tNUMMATERIALS {len(self.materials)}\n")
        for material in self.materials:
            w.write(f"\tMATERIAL \"{material}\"\n")