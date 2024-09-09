import io
import wce.parse as parse

# SIMPLESPRITEDEF "ELFCH0102_SPRITE"
# 	VARIATION 1
# 	SKIPFRAMES? NULL
# 	ANIMATED? NULL
# 	SLEEP? 0
# 	CURRENTFRAME? NULL
# 	NUMFRAMES 2
# 	FRAME "ELFCHSK02.DDS" "ELFCHSK02"

class simplespritedef:
    variation:int
    skip_frames:tuple[int, None]
    animated:tuple[int, None]
    sleep:tuple[int, None]
    current_frame:tuple[int, None]
    frames:list[tuple[str, str]]

    def __init__(self, tag:str, r:io.TextIOWrapper):
        self.tag = tag
        records = parse.property(r, "VARIATION", 1)
        self.variation = int(records[1])
        records = parse.property(r, "SKIPFRAMES?", 1)
        self.skip_frames = (int(records[1]) if records[1] != "NULL" else None)
        records = parse.property(r, "ANIMATED?", 1)
        self.animated = (int(records[1]) if records[1] != "NULL" else None)
        records = parse.property(r, "SLEEP?", 1)
        self.sleep = (int(records[1]) if records[1] != "NULL" else None)
        records = parse.property(r, "CURRENTFRAME?", 1)
        self.current_frame = (int(records[1]) if records[1] != "NULL" else None)
        records = parse.property(r, "NUMFRAMES", 1)
        num_frames = int(records[1])
        self.frames = []
        for i in range(num_frames):
            records = parse.property(r, "FRAME", 2)
            self.frames.append((records[1], records[2]))

    def write(self, w:io.TextIOWrapper):
        w.write(f"SIMPLESPRITEDEF \"{self.tag}\"\n")
        w.write(f"\tVARIATION {self.variation}\n")
        if self.skip_frames != None:
            w.write(f"\tSKIPFRAMES? {self.skip_frames}\n")
        if self.animated != None:
            w.write(f"\tANIMATED? {self.animated}\n")
        if self.sleep != None:
            w.write(f"\tSLEEP? {self.sleep}\n")
        if self.current_frame != None:
            w.write(f"\tCURRENTFRAME? {self.current_frame}\n")
        w.write(f"\tNUMFRAMES {len(self.frames)}\n")
        for frame in self.frames:
            w.write(f"\tFRAME \"{frame[0]}\" \"{frame[1]}\"\n")

