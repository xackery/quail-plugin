import shlex
import io, os
from model.dmspritedef2 import dmspritedef2
from model.materialdef import materialdef
from model.simplespritedef import simplespritedef
from model.track import track
from model.trackdef import trackdef
from model.worlddef import worlddef
from model.materialpalette import materialpalette
from model.hierarchicalspritedef import hierarchicalspritedef
from model.actordef import actordef

class wce:
    dmspritedef2s:dict[str, dmspritedef2]
    materialdefs:dict[str, materialdef]
    simplespritedefs:dict[str, simplespritedef]
    trackdefs:dict[str, trackdef]
    tracks:dict[str, track]
    world:worlddef
    materialpalettes:dict[str, materialpalette]
    hierarchicalspritedefs:dict[str, hierarchicalspritedef]
    actordefs:dict[str, actordef]

    def __init__(self):
        self.dmspritedef2s = {}
        self.materialdefs = {}
        self.simplespritedefs = {}
        self.trackdefs = {}
        self.tracks = {}
        self.world = None
        self.materialpalettes = {}
        self.hierarchicalspritedefs = {}
        self.actordefs = {}

    def parse_definitions(self, current_path:str, r:io.TextIOWrapper):
        current_dir = os.path.dirname(current_path)

        line_number = 0
        for line in r:
            line_number += 1
            line = line.strip()
            records = shlex.split(line)
            if len(records) == 0:
                continue

            path_cursor = f"{current_path}:{line_number}"

            if line.startswith("//"):
                continue
            if line.startswith("INCLUDE"):
                if len(records) != 2:
                    raise Exception(f"{path_cursor} INCLUDE: expected 1 argument, got {len(records)-1}")
                new_path = f"{current_dir}/{records[1].lower()}"
                file_reader = open(new_path, "r")
                data = file_reader.read()
                r = io.StringIO(data)
                self.parse_definitions(new_path, r)
                continue

            tag = ""
            if len(records) > 1:
                tag = records[1]

            # if line.startswith("3DSPRITEDEF"):
            #     err = parse_3dspritedef(r)
            #     if err:
            #         return err
            #     continue
            if line.startswith("ACTORDEF"):
                try:
                    self.actordefs[tag] = actordef(tag, r)
                except Exception as e:
                    raise Exception(f"{path_cursor} actordef: {e}")
                continue
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
                    self.dmspritedef2s[tag] = dmspritedef2(records[1], r)
                except Exception as e:
                     raise Exception(f"{path_cursor} dmspritedef2: {e}")
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
            if line.startswith("HIERARCHICALSPRITEDEF"):
                try:
                    self.hierarchicalspritedefs[tag] = hierarchicalspritedef(tag, r)
                except Exception as e:
                     raise Exception(f"{path_cursor} hierarchicalspritedef: {e}")
                continue
            # if line.startswith("LIGHTDEFINITION"):
            #     parse_lightdefinition(r)
            #     if err:
            #         return err
            #     continue
            if line.startswith("MATERIALDEFINITION"):
                try:
                    self.materialdefs[tag] = materialdef(tag, r)
                except Exception as e:
                     raise Exception(f"{path_cursor} materialdef: {e}")
                continue
            if line.startswith("MATERIALPALETTE"):
                try:
                    self.materialpalettes[tag] = materialpalette(tag, r)
                except Exception as e:
                     raise Exception(f"{path_cursor} materialpalette: {e}")
                continue
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
            if line.startswith("SIMPLESPRITEDEF"):
                try:
                    self.simplespritedefs[tag] = simplespritedef(tag, r)
                except Exception as e:
                    raise Exception(f"{path_cursor} simplespritedef: {e}")
                continue
            # if line.startswith("SPRITE2DDEF"):
            #     parse_sprite2ddef(r)
            #     if err:
            #         return err
            #     continue
            if line.startswith("TRACKDEFINITION"):
                try:
                    tmp = trackdef(tag, r)
                    self.trackdefs[f"{tag}_{tmp.tag_index}"] = tmp
                except Exception as e:
                     raise Exception(f"{path_cursor} trackdef: {e}")
                continue
            if line.startswith("TRACKINSTANCE"):
                try:
                    tmp = track(tag, r)
                    self.tracks[f"{tag}_{tmp.definition}_{tmp.definition_index}"] = tmp
                except Exception as e:
                     raise Exception(f"{path_cursor} track: {e}")
                continue
            if line.startswith("WORLDDEF"):
                try:
                    self.world = worlddef(r)
                except Exception as e:
                    raise Exception(f"{path_cursor} worlddef: {e}")
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
            raise Exception(f"{path_cursor} unknown tag: {line}")

    def write_definitions(self, w:io.TextIOWrapper):
        for tag, dmspritedef2 in self.dmspritedef2s.items(): dmspritedef2.write(w)
        for tag, materialdef in self.materialdefs.items(): materialdef.write(w)
        for tag, simplespritedef in self.simplespritedefs.items(): simplespritedef.write(w)
        for tag, track in self.tracks.items(): track.write(w)
        for tag, trackdef in self.trackdefs.items(): trackdef.write(w)
        if self.world: self.world.write(w)
        for tag, materialpalette in self.materialpalettes.items(): materialpalette.write(w)
        for tag, hierarchicalspritedef in self.hierarchicalspritedefs.items(): hierarchicalspritedef.write(w)
        for tag, actordef in self.actordefs.items(): actordef.write(w)

