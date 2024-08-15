from io import TextIOWrapper
import bpy
import os
import mathutils
import bmesh
from typing import Tuple

path = "/src/quail/test/crushbone.quail/r/r2.mod"

def message_box(message="", title="Message Box", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def write(path=""):
    w = open(path, "w")
    err = write_definitions(w)
    if err:
        message_box(err, "Parsing Failed", 'ERROR')
        return

def write_definitions(w) -> str:
    # type: (TextIOWrapper) -> str
    for i in range(1, len(bpy.data.meshes)+2):
        name = "R%d" % i
        for object in bpy.data.objects:
            if object.name != name:
                continue
            err = write_dmspritedef2(w, object)
            if err:
                return err


def write_dmspritedef2(w=None, object=None) -> str:
    # type: (TextIOWrapper, bpy.types.Object) -> str
    if w is None:
        return "writer is none"
    if object is None:
        return "object is none"

    mesh = object.data
    center = object.location

    bm = bmesh.new()
    if bpy.context.mode == 'EDIT_MESH':
        bm.from_edit_mesh(mesh)
    else:
        bm.from_mesh(mesh)
    bm.faces.ensure_lookup_table()


    w.write("DMSPRITEDEF2\n")
    w.write("\tTAG \"%s_DMSPRITEDEF\"\n" % object.name)

    # center = mathutils.Vector((0.0, 0.0, 0.0))
    # for vertex in mesh.vertices:
    #     center += vertex.co
    # center /= len(mesh.vertices)



    w.write("\tCENTEROFFSET %0.8e %0.8e %0.8e\n" % (center[0], center[1], center[2]))
    w.write("\n")
    w.write("\tNUMVERTICES %d\n" % len(mesh.vertices))
    for vertex in mesh.vertices:
        w.write("\tXYZ %0.8e %0.8e %0.8e\n" % (vertex.co.x, vertex.co.y, vertex.co.z))
    w.write("\n")
    w.write("\tNUMUVS %d\n" % len(mesh.vertices))
    for vertex in mesh.vertices:
        uv = mesh.uv_layers[0].data[vertex.index]
        w.write("\tUV %0.8e %0.8e\n" % (uv.uv.x, uv.uv.y))
    w.write("\n")
    w.write("\tNUMVERTEXNORMALS %d\n" % len(mesh.vertices))
    for vertex in mesh.vertices:
        w.write("\tXYZ %0.8e %0.8e %0.8e\n" % (vertex.normal.x, vertex.normal.y, vertex.normal.z))
    w.write("\n")

    color_layer = mesh.vertex_colors[0].data
    w.write("\tNUMVERTEXCOLORS %d\n" % len(mesh.vertices))
    for vertex in mesh.vertices:
        color = color_layer[vertex.index]
        r = int(color.color[0] * 255)
        g = int(color.color[1] * 255)
        b = int(color.color[2] * 255)
        a = int(color.color[3] * 255)
        w.write("\tRGBA %d %d %d %d\n" % (r, g, b, a))
    w.write("\n")
    w.write("\n")
    w.write("\tSKINASSIGNMENTGROUPS 0\n")
    w.write("\tMATERIALPALETTE \"%s\"\n" % mesh["materialpalette"])
    w.write("\n")
    w.write("\tPOLYHEDRON\n")
    w.write("\t\tDEFINITION \"%s\"\n" % mesh["definition"])
    w.write("\tENDPOLYHEDRON\n\n")
    w.write("\tNUMFACE2S %d\n" % len(mesh.polygons))
    w.write("\n")
    passable_layer = bm.faces.layers.int.get("passable")
    for i, face in enumerate(mesh.polygons):
        w.write("\tDMFACE2 //%d\n" % i)
        w.write("\t\tPASSABLE %d\n" % bm.faces[i][passable_layer])
        # w.write("\t\tPASSABLE %d\n" %  face["passable"])
        w.write("\t\tTRIANGLE %d %d %d\n" % (face.vertices[0], face.vertices[1], face.vertices[2]))
        w.write("\tENDDMFACE2 //%d\n\n" % i)
    w.write("\n")
    w.write("\t// meshops are not supported\n")
    w.write("\t// NUMMESHOPS 0\n")
    w.write("\n")
    w.write("\tFACEMATERIALGROUPS %s" % mesh["facematerialgroups"])
    w.write("\n")
    w.write("\tVERTEXMATERIALGROUPS %s" % mesh["vertexmaterialgroups"])
    w.write("\n")
    w.write("\tBOUNDINGBOXMIN %0.8e %0.8e %0.8e\n" % (mesh["boundingboxmin"][0], mesh["boundingboxmin"][1], mesh["boundingboxmin"][2]))
    w.write("\tBOUNDINGBOXMAX %0.8e %0.8e %0.8e\n" % (mesh["boundingboxmax"][0], mesh["boundingboxmax"][1], mesh["boundingboxmax"][2]))

    w.write("\tBOUNDINGRADIUS %0.8e\n" % mesh["boundingradius"])
    w.write("\n")
    w.write("\tFPSCALE %d\n" % mesh["fpscale"])
    w.write("\tHEXONEFLAG %d\n" % mesh["hexoneflag"])
    w.write("\tHEXTWOFLAG %d\n" % mesh["hextwoflag"])
    w.write("\tHEXFOURTOUSANDFLAG %d\n" % mesh["hexfourthousandflag"])
    w.write("\tHEXEIGHTTOUSANDFLAG %d\n" % mesh["hexeightthousandflag"])
    w.write("\tHEXTENTHOUSANDFLAG %d\n" % mesh["hextenthousandflag"])
    w.write("\tHEXTWENTYTHOUSANDFLAG %d\n" % mesh["hextwentythousandflag"])

    w.write("ENDDMSPRITEDEF2\n\n")

    bm.free()
    return ""

err = write(path)
if err:
    message_box(err, "Writing Failed", 'ERROR')
    exit
print("Writing Successful")