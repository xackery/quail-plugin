import shlex
import bpy
import os
import bmesh
from typing import Tuple

path = "/src/quail/test/crushbone/r/r.mod"

def message_box(message="", title="Message Box", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def parse(path=""): 
    r = open(path, "r")
    err = parse_definitions(r)
    if err:
        message_box(err, "Parsing Failed", 'ERROR')
        return
    


def parse_definitions(r=None) -> str:
    if r is None:
        return "reader is none"
    
    for line in r:
        line = line.strip()
        if line == "":
            continue
        if line.startswith("//"):
            continue
        # if line == "3DSPRITEDEF":
        #     err = parse_3dspritedef(r)
        #     if err:
        #         return err
        #     continue
        # if line == "ACTORDEF":
        #     parse_actordef(r)
        #     if err:
        #         return err
        #     continue
        # if line == "ACTORINST":
        #     parse_actorinst(r)
        #     if err:
        #         return err
        #     continue
        # if line == "AMBIENTLIGHT":
        #     parse_ambientlight(r)
        #     if err:
        #         return err
        #     continue
        # if line == "BLITSPRITEDEFINITION":
        #     parse_blitspritedefinition(r)
        #     if err:
        #         return err
        #     continue
        if line == "DMSPRITEDEF2":
            err = parse_dmspritedef2(r)
            if err:
                return "dmspritedef2: "+ err
            continue
        # if line == "DMSPRITEDEFINITION":
        #     parse_dmspritedefinition(r)
        #     if err:
        #         return err
        #     continue
        # if line == "GLOBALAMBIENTLIGHTDEF":
        #     parse_globalambientlightdef(r)
        #     if err:
        #         return err
        #     continue
        # if line == "HIERARCHICALSPRITEDEF":
        #     parse_hierarchicalspritedef(r)
        #     if err:
        #         return err
        #     continue
        # if line == "LIGHTDEFINITION":
        #     parse_lightdefinition(r)
        #     if err:
        #         return err
        #     continue
        # if line == "MATERIALDEFINITION":
        #     parse_materialdefinition(r)
        #     if err:
        #         return err
        #     continue
        # if line == "MATERIALPALETTE":
        #     parse_materialpalette(r)
        #     if err:
        #         return err
        #     continue
        # if line == "PARTICLECLOUDDEF":
        #     parse_particleclouddef(r)
        #     if err:
        #         return err
        #     continue
        # if line == "POINTLIGHT":
        #     parse_pointlight(r)
        #     if err:
        #         return err
        #     continue
        # if line == "POLYHEDRONDEFINITION":
        #     parse_polyhedrondefinition(r)
        #     if err:
        #         return err
        #     continue
        # if line == "REGION":
        #     parse_region(r)
        #     if err:
        #         return err
        #     continue
        # if line == "RGBDEFORMATIONTRACKDEF":
        #     parse_rgbdeformationtrackdef(r)
        #     if err:
        #         return err
        #     continue
        # if line == "SIMPLESPRITEDEF":
        #     parse_simplespritedef(r)
        #     if err:
        #         return err
        #     continue
        # if line == "SPRITE2DDEF":
        #     parse_sprite2ddef(r)
        #     if err:
        #         return err
        #     continue
        # if line == "TRACKDEFINITION":
        #     parse_trackdefinition(r)
        #     if err:
        #         return err
        #     continue
        # if line == "TRACKINSTANCE":
        #     parse_trackinstance(r)
        #     if err:
        #         return err
        #     continue
        # if line == "WORLDDEF":
        #     parse_worlddef(r)
        #     if err:
        #         return err
        #     continue
        # if line == "WORLDTREE":
        #     parse_worldtree(r)
        #     if err:
        #         return err
        #     continue
        # if line == "ZONE":
        #     parse_zone(r)
        #     if err:
        #         return err
        #     continue
        #return "Unknown definition: " + line
    return ""

def parse_property(r=None, property="", num_args=-1) -> Tuple[list[str], str]:
    if r is None:
        return None, "parse %s: reader is none" % property
    if property == "":
        return "empty property"
    for line in r:
        if line.find("//"):
            line = line.split("//")[0]
        line = line.strip()
        if line == "":
            continue
        records = shlex.split(line)
        if len(records) == 0:
            return None, "%s: empty records (%s)" % (property, line)    
        if records[0] != property:
            return None, "%s: expected property %s got %s" % (property, property, records[0])
        if num_args != -1 and len(records)-1 != num_args:
            return None, "%s: expected %d arguments, got %d" % (property, num_args, len(records)-1)
        
        return records, ""
        
    
def parse_dmspritedef2(r=None) -> str:
    if r is None:
        return "reader is none"
    
    records, err = parse_property(r, "TAG", 1)
    if err:
        return err
    
    tag = records[1]

    mesh = bpy.data.meshes.new(tag)
    
    records, err = parse_property(r, "CENTEROFFSET", 3)
    if err:
        return err
    
    mesh["centeroffset"] = (float(records[1]), float(records[2]), float(records[3]))

    records, err = parse_property(r, "NUMVERTICES", 1)
    if err:
        return err
    vert_count = int(records[1])
    mesh_verts = []
    for i in range(vert_count):
        records, err = parse_property(r, "XYZ", 3)
        if err:
            return err
        mesh_verts.append((float(records[1])+mesh["centeroffset"][0], float(records[2])+mesh["centeroffset"][1], float(records[3])+mesh["centeroffset"][2]))

    records, err = parse_property(r, "NUMUVS", 1)
    if err:
        return err
    uv_count = int(records[1])
    mesh_uvs = []
    for i in range(uv_count):
        records, err = parse_property(r, "UV", 2)
        if err:
            return err
        mesh_uvs.append((float(records[1]), float(records[2])))

    records, err = parse_property(r, "NUMVERTEXNORMALS", 1)
    if err:
        return err
    normal_count = int(records[1])
    mesh_normals = []
    for i in range(normal_count):
        records, err = parse_property(r, "XYZ", 3)
        if err:
            return err
        mesh_normals.append((float(records[1]), float(records[2]), float(records[3])))
    
    records, err = parse_property(r, "NUMVERTEXCOLORS", 1)
    if err:
        return err
    color_count = int(records[1])
    mesh_colors = []
    for i in range(color_count):
        records, err = parse_property(r, "RGBA", 4)
        if err:
            return err
        mesh_colors.append((float(records[1]), float(records[2]), float(records[3]), float(records[4])))

    records, err = parse_property(r, "SKINASSIGNMENTGROUPS", -1)
    if err:
        return err
    
    records, err = parse_property(r, "MATERIALPALETTE", 1)
    if err:
        return err
    mesh["materialpalette"] = records[1]

    records, err = parse_property(r, "POLYHEDRON", 0)
    if err:
        return err
    
    records, err = parse_property(r, "DEFINITION", 1)
    if err:
        return err
    mesh["definition"] = records[1]

    records, err = parse_property(r, "ENDPOLYHEDRON", 0)
    if err:
        return err
    
    records, err = parse_property(r, "NUMFACE2S", 1)
    if err:
        return err
    face_count = int(records[1])

    mesh_faces = []
    mesh_passable = []
    for i in range(face_count):
        records, err = parse_property(r, "DMFACE2", 0)
        if err:
            return err
        records, err = parse_property(r, "PASSABLE", 1)
        if err:
            return err
        mesh_passable.append(records[1])
        records, err = parse_property(r, "TRIANGLE", 3)
        if err:
            return err        
        mesh_faces.append((int(records[1]), int(records[2]), int(records[3])))
        _, err = parse_property(r, "ENDDMFACE2", 0)
        if err:
            return err

    records, err = parse_property(r, "FACEMATERIALGROUPS", -1)
    if err:
        return err
    if len(records) < 2:
        return "FACEMATERIALGROUPS: expected at least 2 records"
    face_material_count = int(records[1])
    mesh_face_materials = []
    for i in range(0, face_material_count*2, 2):
        mesh_face_materials.append(records[i+2])
        mesh_face_materials.append(records[i+3])
        
    records, err = parse_property(r, "VERTEXMATERIALGROUPS", -1)
    if err:
        return err
    if len(records) < 2:
        return "VERTEXMATERIALGROUPS: expected at least 2 records"
    vertex_material_count = int(records[1])
    mesh_vertex_materials = []
    for i in range(0, vertex_material_count*2,2):
        mesh_vertex_materials.append(records[i+2])
        mesh_vertex_materials.append(records[i+3])
        
    records, err = parse_property(r, "BOUNDINGBOXMIN", 3)
    if err:
        return err
    mesh["boundingboxmin"] = (float(records[1]), float(records[2]), float(records[3]))

    records, err = parse_property(r, "BOUNDINGBOXMAX", 3)
    if err:
        return err
    mesh["boundingboxmax"] = (float(records[1]), float(records[2]), float(records[3]))

    records, err = parse_property(r, "BOUNDINGRADIUS", 1)
    if err:
        return err
    
    mesh["boundingradius"] = float(records[1])

    records, err = parse_property(r, "FPSCALE", 1)
    if err:
        return err
    mesh["fpscale"] = float(records[1])

    records, err = parse_property(r, "HEXONEFLAG", 1)
    if err:
        return err
    mesh["hexoneflag"] = int(records[1])

    records, err = parse_property(r, "HEXTWOFLAG", 1)
    if err:
        return err
    mesh["hextwoflag"] = int(records[1])

    records, err = parse_property(r, "HEXFOURTOUSANDFLAG", 1)
    if err:
        return err
    mesh["hexfourthousandflag"] = int(records[1])

    records, err = parse_property(r, "HEXEIGHTTOUSANDFLAG", 1)
    if err:
        return err
    mesh["hexeightthousandflag"] = int(records[1])

    records, err = parse_property(r, "HEXTENTHOUSANDFLAG", 1)
    if err:
        return err
    mesh["hextenthousandflag"] = int(records[1])

    records, err = parse_property(r, "HEXTWENTYTHOUSANDFLAG", 1)
    if err:
        return err
    mesh["hextwentythousandflag"] = int(records[1])

    #print(mesh_verts)
    mesh.from_pydata(mesh_verts, [], mesh_faces)
    mesh.update(calc_edges=True)

    uvlayer = mesh.uv_layers.new(name="%s_uv" % tag)

    for triangle in mesh.polygons:
        vertices = list(triangle.vertices)
        i = 0
        for vertex in vertices:
            uvlayer.data[triangle.loop_indices[i]].uv = (mesh_uvs[vertex]                                                         [0], mesh_uvs[vertex][1]-1)
            i += 1

    # for i in range(len(mesh.polygons)):
    #     poly = mesh.polygons[i]
    #     if len(mesh_materials) > i:
    #         poly.material_index = mesh_materials[i]
   
    faces = {}
    mesh_obj = bpy.data.objects.new(tag.replace("_DMSPRITEDEF", ""), mesh)

    #collection = bpy.data.collections.new(tag)
    #collection.objects.link(mesh_obj)
    bpy.context.scene.collection.objects.link(mesh_obj)

    for i in range(len(mesh.polygons)):
        poly = mesh.polygons[i]
        #if len(mesh_materials) > i:
        #    poly.material_index = mesh_materials[i]
        new_map = "flag_%s" % mesh_passable[i]
        if new_map not in faces:
            faces[new_map] = []
        face_map = faces[new_map]
        face_map.append(i)

    for face in faces:
        if face not in mesh_obj.face_maps:
            face_map = mesh_obj.face_maps.new(name=face)
        face_map = mesh_obj.face_maps[face]
        face_map.add(faces[face])

    bm = bmesh.new()
    bm.from_mesh(mesh)

    return ""


for collection in bpy.data.collections:
                bpy.data.collections.remove(collection)

for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh)

# remove orphed objects
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj)

for bone in bpy.data.armatures:
    bpy.data.armatures.remove(bone)

for mat in bpy.data.materials:
    bpy.data.materials.remove(mat)

for img in bpy.data.images:
    bpy.data.images.remove(img)

for bone in bpy.data.armatures:
    bpy.data.armatures.remove(bone)

for action in bpy.data.actions:
    bpy.data.actions.remove(action)


if not os.path.exists(path):
    message_box("File does not exist", "Quail Error", 'ERROR')
    exit

ext = os.path.splitext(path)[1]
if ext != ".mod":
    message_box("Expected .mod, got extension " + ext, "Quail Error", 'ERROR')
    exit

parse(path)