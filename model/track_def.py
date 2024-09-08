import io
import wce.parse as parse

# TRACKDEFINITION "ELF_TRACKDEF"
# 	TAGINDEX 0
# 	SPRITE "ELF_DMSPRITEDEF"
# 	NUMFRAMES 1
# 		FRAME 256 0 0 0 -16384 0 0 0
# 	NUMLEGACYFRAMES 0

class track_frame:
    xyz_scale:int
    xyz:tuple[int,int,int]
    rot_scale:int
    rot:tuple[int,int,int]

class legacy_track_frame:
    xyz_scale:int
    xyz:tuple[int,int,int]
    rot:tuple[int,int,int,int]

class track_def:
    tag:str
    tag_index:int
    sprite:str
    frames: list[track_frame]
    legacy_frames:list[legacy_track_frame]

    def __init__(self, tag:str, r:io.TextIOWrapper):
        self.tag = tag
        records = parse.property(r, "TAGINDEX", 1)
        self.tag_index = int(records[1])
        records = parse.property(r, "SPRITE", 1)
        self.sprite = records[1]
        records = parse.property(r, "NUMFRAMES", 1)
        num_frames = int(records[1])
        self.frames = []
        for i in range(num_frames):
            frame = track_frame()
            records = parse.property(r, "FRAME", 8)
            frame.xyz_scale = int(records[1])
            frame.xyz = (int(records[2]), int(records[3]), int(records[4]))
            frame.rot_scale = int(records[5])
            frame.rot = (int(records[6]), int(records[7]), int(records[8]))
            self.frames.append(frame)
        records = parse.property(r, "NUMLEGACYFRAMES", 1)
        num_legacy_frames = int(records[1])
        self.legacy_frames = []
        for i in range(num_legacy_frames):
            frame = legacy_track_frame()
            records = parse.property(r, "LEGACYFRAME", 7)
            frame.xyz_scale = int(records[1])
            frame.xyz = (int(records[2]), int(records[3]), int(records[4]))
            frame.rot = (int(records[5]), int(records[6]), int(records[7]), int(records[8]))
            self.legacy_frames.append(frame)

    def write(self, w:io.TextIOWrapper):
        w.write(f"TRACKDEFINITION \"{self.tag}\"\n")
        w.write(f"\tTAGINDEX {self.tag_index}\n")
        w.write(f"\tSPRITE {self.sprite}\n")
        w.write(f"\tNUMFRAMES {len(self.frames)}\n")
        for frame in self.frames:
            w.write(f"\t\tFRAME {frame.xyz_scale} {frame.xyz[0]} {frame.xyz[1]} {frame.xyz[2]} {frame.rot_scale} {frame.rot[0]} {frame.rot[1]} {frame.rot[2]}\n")
        w.write(f"\tNUMLEGACYFRAMES {len(self.legacy_frames)}\n")
        for frame in self.legacy_frames:
            w.write(f"\t\tLEGACYFRAME {frame.xyz_scale} {frame.xyz[0]} {frame.xyz[1]} {frame.xyz[2]} {frame.rot[0]} {frame.rot[1]} {frame.rot[2]} {frame.rot[3]}\n")




