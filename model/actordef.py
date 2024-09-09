import io
import wce.parse as parse

# ACTORDEF "ELF_ACTORDEF"
# 	CALLBACK "SPRITECALLBACK"
# 	BOUNDSREF 0
# 	CURRENTACTION? NULL
# 	LOCATION? NULL NULL NULL NULL NULL NULL
# 	ACTIVEGEOMETRY? NULL
# 	NUMACTIONS 1
# 		ACTION
# 			UNK1 0
# 			NUMLEVELSOFDETAIL 1
# 				LEVELOFDETAIL
# 					SPRITE "ELF_HS_DEF"
# 					SPRITEINDEX 0
# 					MINDISTANCE 1.00000002e+30
# 	UNK2 0
# 	HASEIGHTYFLAG 0

class lod:
    sprite:str
    sprite_index:int
    min_distance:float

    def __init__(self, r:io.TextIOWrapper):
        parse.property(r, "LEVELOFDETAIL", 0)
        records = parse.property(r, "SPRITE", 1)
        self.sprite = records[1]
        records = parse.property(r, "SPRITEINDEX", 1)
        self.sprite_index = int(records[1])
        records = parse.property(r, "MINDISTANCE", 1)
        self.min_distance = float(records[1])

class action:
    unk1:int
    level_of_details:list[lod]

    def __init__(self, r:io.TextIOWrapper):
        parse.property(r, "ACTION", 0)
        records = parse.property(r, "UNK1", 1)
        self.unk1 = int(records[1])
        records = parse.property(r, "NUMLEVELSOFDETAIL", 1)
        num_levels_of_detail = int(records[1])
        self.level_of_details = []
        for i in range(num_levels_of_detail):
            self.level_of_details.append(lod(r))


class actordef:
    tag:str
    callback:str
    boundsref:int
    current_action:tuple[int, None]
    location:tuple[tuple[float, None], tuple[float, None], tuple[float, None], tuple[float, None], tuple[float, None], tuple[float, None]]
    active_geometry:tuple[int, None]
    actions:list[action]
    unk2:int
    has_eighty_flag:int




    def __init__(self, tag:str, r:io.TextIOWrapper):
        self.tag = tag

        records = parse.property(r, "CALLBACK", 1)
        self.callback = records[1]
        records = parse.property(r, "BOUNDSREF", 1)
        self.boundsref = int(records[1])
        records = parse.property(r, "CURRENTACTION?", 1)
        self.current_action = (int(records[1]) if records[1] != "NULL" else None)
        records = parse.property(r, "LOCATION?", 6)
        self.location = ((float(records[1]) if records[1] != "NULL" else None), (float(records[2]) if records[2] != "NULL" else None), (float(records[3]) if records[3] != "NULL" else None), (float(records[4]) if records[4] != "NULL" else None), (float(records[5]) if records[5] != "NULL" else None), (float(records[6]) if records[6] != "NULL" else None))
        records = parse.property(r, "ACTIVEGEOMETRY?", 1)
        self.active_geometry = (int(records[1]) if records[1] != "NULL" else None)
        records = parse.property(r, "NUMACTIONS", 1)
        num_actions = int(records[1])
        self.actions = []
        for i in range(num_actions):
            self.actions.append(action(r))
        records = parse.property(r, "UNK2", 1)
        self.unk2 = int(records[1])
        records = parse.property(r, "HASEIGHTYFLAG", 1)
        self.has_eighty_flag = int(records[1])




    def write(self, w:io.TextIOWrapper):
        w.write(f"ACTORDEF \"{self.tag}\"\n")
        w.write(f"\tCALLBACK {self.callback}\n")
        w.write(f"\tBOUNDSREF {self.boundsref}\n")
        if self.current_action != None:
            w.write(f"\tCURRENTACTION? {self.current_action}\n")
        if self.location != None:
            w.write(f"\tLOCATION? {self.location[0]} {self.location[1]} {self.location[2]} {self.location[3]} {self.location[4]} {self.location[5]}\n")
        if self.active_geometry != None:
            w.write(f"\tACTIVEGEOMETRY? {self.active_geometry}\n")
        w.write(f"\tNUMACTIONS {len(self.actions)}\n")
        for action in self.actions:
            w.write(f"\t\tACTION\n")
            w.write(f"\t\t\tUNK1 {action.unk1}\n")
            w.write(f"\t\t\tNUMLEVELSOFDETAIL {len(action.level_of_details)}\n")
            for lod in action.level_of_details:
                w.write(f"\t\t\t\tLEVELOFDETAIL\n")
                w.write(f"\t\t\t\t\tSPRITE {lod.sprite}\n")
                w.write(f"\t\t\t\t\tSPRITEINDEX {lod.sprite_index}\n")
                w.write(f"\t\t\t\t\tMINDISTANCE {lod.min_distance}\n")
        w.write(f"\tUNK2 {self.unk2}\n")
        w.write(f"\tHASEIGHTYFLAG {self.has_eighty_flag}\n")