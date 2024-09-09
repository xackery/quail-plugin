import io
import wce.parse as parse

# HIERARCHICALSPRITEDEF "ELF_HS_DEF"
# 	NUMDAGS 109
# 		DAG // 0
# 			TAG "ELF_DAG"
# 			SPRITE ""
# 			TRACK "ELF_TRACK"
# 			TRACKINDEX 0
# 			SUBDAGLIST 1 1

# 	NUMATTACHEDSKINS 3
# 		ATTACHEDSKIN
# 			DMSPRITE "ELFEYE_R_DMSPRITEDEF"
# 			LINKSKINUPDATESTODAGINDEX 0

# 	POLYHEDRON
# 		DEFINITION "" // refer to polyhedron tag, or SPECIAL_COLLISION = 4294967293
# 	CENTEROFFSET? NULL NULL NULL
# 	BOUNDINGRADIUS? 5.10975647e+00
# 	HEXTWOHUNDREDFLAG 1
# 	HEXTWENTYTHOUSANDFLAG 0

class dag:
    tag:str
    sprite:str
    track:str
    track_index:int
    subdags:list[int]

    def __init__(self, r:io.TextIOWrapper):
        parse.property(r, "DAG", 0)
        records = parse.property(r, "TAG", 1)
        self.tag = records[1]
        records = parse.property(r, "SPRITE", 1)
        self.sprite = records[1]
        records = parse.property(r, "TRACK", 1)
        self.track = records[1]
        records = parse.property(r, "TRACKINDEX", 1)
        self.track_index = int(records[1])
        records = parse.property(r, "SUBDAGLIST", -1)
        if len(records) < 2:
            raise ValueError("SUBDAGLIST must have at least 2 arguments")
        num_subdags = int(records[1])
        self.subdags = []
        for i in range(num_subdags):
            self.subdags.append(int(records[i+2]))

    def write(self, w:io.TextIOWrapper):
        w.write(f"\tDAG\n")
        w.write(f"\t\tTAG \"{self.tag}\"\n")
        w.write(f"\t\tSPRITE \"{self.sprite}\"\n")
        w.write(f"\t\tTRACK \"{self.track}\"\n")
        w.write(f"\t\tTRACKINDEX {self.track_index}\n")
        w.write(f"\t\tSUBDAGLIST {len(self.subdags)}")
        for subdag in self.subdags:
            w.write(f" {subdag}")
        w.write("\n")


class hierarchicalspritedef:
    tag:str
    dags:dag
    attached_skins:list[tuple[str, int]]
    polyhedron_definition:str
    center_offset:tuple[tuple[int, None], tuple[int, None], tuple[int, None]]
    bounding_radius:tuple[float, None]
    hex_two_hundred_flag:int
    hex_twenty_thousand_flag:int


    def __init__(self, tag:str, r:io.TextIOWrapper):
        self.tag = tag
        records = parse.property(r, "NUMDAGS", 1)
        num_dags = int(records[1])
        self.dags = []
        for i in range(num_dags):
            self.dags.append(dag(r))
        records = parse.property(r, "NUMATTACHEDSKINS", 1)
        num_attached_skins = int(records[1])
        self.attached_skins = []
        for i in range(num_attached_skins):
            parse.property(r, "ATTACHEDSKIN", 0)
            records = parse.property(r, "DMSPRITE", 1)
            skin_sprite = records[1]
            records = parse.property(r, "LINKSKINUPDATESTODAGINDEX", 1)
            self.attached_skins.append((skin_sprite, int(records[1])))
        parse.property(r, "POLYHEDRON", 0)
        records = parse.property(r, "DEFINITION", 1)
        self.polyhedron_definition = records[1]
        records = parse.property(r, "CENTEROFFSET?", 3)
        self.center_offset = ((int(records[1]) if records[1] != "NULL" else None), (int(records[2]) if records[2] != "NULL" else None), (int(records[3]) if records[3] != "NULL" else None))
        records = parse.property(r, "BOUNDINGRADIUS?", 1)
        self.bounding_radius = (float(records[1]) if records[1] != "NULL" else None)
        records = parse.property(r, "HEXTWOHUNDREDFLAG", 1)
        self.hex_two_hundred_flag = int(records[1])
        records = parse.property(r, "HEXTWENTYTHOUSANDFLAG", 1)
        self.hex_twenty_thousand_flag = int(records[1])

    def write(self, w:io.TextIOWrapper):
        w.write(f"HIERARCHICALSPRITEDEF \"{self.tag}\"\n")
        w.write(f"\tNUMDAGS {len(self.dags)}\n")
        for dag in self.dags:
            dag.write(w)
        w.write(f"\tNUMATTACHEDSKINS {len(self.attached_skins)}\n")
        for attached_skin in self.attached_skins:
            w.write(f"\t\tATTACHEDSKIN\n")
            w.write(f"\t\t\tDMSPRITE \"{attached_skin[0]}\"\n")
            w.write(f"\t\t\tLINKSKINUPDATESTODAGINDEX {attached_skin[1]}\n")
        w.write(f"\tPOLYHEDRON\n")
        w.write(f"\t\tDEFINITION \"{self.polyhedron_definition}\"\n")
        w.write(f"\tCENTEROFFSET? {self.center_offset[0]} {self.center_offset[1]} {self.center_offset[2]}\n")
        if self.bounding_radius != None:
            w.write(f"\tBOUNDINGRADIUS? {self.bounding_radius}\n")
        w.write(f"\tHEXTWOHUNDREDFLAG {self.hex_two_hundred_flag}\n")
        w.write(f"\tHEXTWENTYTHOUSANDFLAG {self.hex_twenty_thousand_flag}\n")