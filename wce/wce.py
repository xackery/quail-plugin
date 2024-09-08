import shlex
import io, os
from model.track_def import track_def
from model.track import track
from model.world_def import world_def
from model.dmspritedef2 import dmspritedef2

class wce:
    track_defs:list[track_def]
    tracks:list[track]
    world:world_def
    dmspritedef2s:list[dmspritedef2]

    def __init__(self):
        self.track_defs = []
        self.tracks = []
        self.world = None
        self.dmspritedef2s = []

    def parse_definitions(self, current_path:str, r:io.TextIOWrapper):
        current_dir = os.path.dirname(current_path)

        for line in r:
            line = line.strip()
            records = shlex.split(line)
            if len(records) == 0:
                continue

            if line.startswith("//"):
                continue
            if line.startswith("INCLUDE"):
                if len(records) != 2:
                    raise Exception(f"INCLUDE: expected 1 argument, got {len(records)-1}")
                new_path = f"{current_dir}/{records[1].lower()}"
                file_reader = open(new_path, "r")
                data = file_reader.read()
                r = io.StringIO(data)
                self.parse_definitions(new_path, r)


            # if line.startswith("3DSPRITEDEF"):
            #     err = parse_3dspritedef(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("ACTORDEF"):
            #     parse_actordef(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("ACTORINST"):
            #     parse_actorinst(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("AMBIENTLIGHT"):
            #     parse_ambientlight(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("BLITSPRITEDEFINITION"):
            #     parse_blitspritedefinition(r)
            #     if err:
            #         return err
            #     continue
            if line.startswith("DMSPRITEDEF2"):
                try:
                    self.track_defs.append(dmspritedef2(records[1], r))
                except Exception as e:
                     raise Exception(f"dmspritedef2: {e}")
                continue
            # if line.startswith("DMSPRITEDEFINITION"):
            #     parse_dmspritedefinition(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("GLOBALAMBIENTLIGHTDEF"):
            #     parse_globalambientlightdef(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("HIERARCHICALSPRITEDEF"):
            #     parse_hierarchicalspritedef(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("LIGHTDEFINITION"):
            #     parse_lightdefinition(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("MATERIALDEFINITION"):
            #     parse_materialdefinition(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("MATERIALPALETTE"):
            #     parse_materialpalette(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("PARTICLECLOUDDEF"):
            #     parse_particleclouddef(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("POINTLIGHT"):
            #     parse_pointlight(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("POLYHEDRONDEFINITION"):
            #     parse_polyhedrondefinition(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("REGION"):
            #     parse_region(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("RGBDEFORMATIONTRACKDEF"):
            #     parse_rgbdeformationtrackdef(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("SIMPLESPRITEDEF"):
            #     parse_simplespritedef(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("SPRITE2DDEF"):
            #     parse_sprite2ddef(r)
            #     if err:
            #         return err
            #     continue
            if line.startswith("TRACKDEFINITION"):
                try:
                    self.track_defs.append(track_def(records[1], r))
                except Exception as e:
                     raise Exception(f"track_def: {e}")
                continue
            if line.startswith("TRACKINSTANCE"):
                try:
                    self.tracks.append(track(records[1], r))
                except Exception as e:
                     raise Exception(f"track: {e}")
                continue
            if line.startswith("WORLDDEF"):
                try:
                    self.world = world_def(r)
                except Exception as e:
                    raise Exception(f"world_def: {e}")
                continue
            # if line.startswith("WORLDTREE"):
            #     parse_worldtree(r)
            #     if err:
            #         return err
            #     continue
            # if line.startswith("ZONE"):
            #     parse_zone(r)
            #     if err:
            #         return err
            #     continue
            #return "Unknown definition: " + line
        return ""


    def write_definitions(self, w:io.TextIOWrapper):
        for track_def in self.track_defs:
            track_def.write(w)
        for track in self.tracks:
            track.write(w)
        if self.world:
            self.world.write(w)
        for dmspritedef2 in self.dmspritedef2s:
            dmspritedef2.write(w)