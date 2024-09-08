import io
import wce.parse as parse

# DMSPRITEDEF2 "ELFEYE_R_DMSPRITEDEF"
# 	CENTEROFFSET 0.00000000e+00 0.00000000e+00 0.00000000e+00
# 	NUMVERTICES 19
# 	XYZ 5.85937500e-03 -2.42919922e-02 -4.47998047e-02
# 	NUMUVS 19
# 	UV 2.50000000e-01 0.00000000e+00
# 	NUMVERTEXNORMALS 19
# 	XYZ 5.46875000e-02 -5.23437500e-01 -8.35937500e-01
# 	NUMVERTEXCOLORS 0
# 	SKINASSIGNMENTGROUPS 1 19 9
# 	MATERIALPALETTE "ELF_MP"
# 	POLYHEDRON
# 		DEFINITION ""
# 	NUMFACE2S 30
# 		DMFACE2 //0
# 			PASSABLE 0
# 			TRIANGLE 2 1 0
# 	NUMMESHOPS 0
# 	FACEMATERIALGROUPS 1 30 0
# 	VERTEXMATERIALGROUPS 1 19 0
# 	BOUNDINGBOXMIN 0.00000000e+00 0.00000000e+00 0.00000000e+00
# 	BOUNDINGBOXMAX 0.00000000e+00 0.00000000e+00 0.00000000e+00
# 	BOUNDINGRADIUS 1.02222003e-01
# 	FPSCALE 13
# 	HEXONEFLAG 1
# 	HEXTWOFLAG 1
# 	HEXFOURTHOUSANDFLAG 0
# 	HEXEIGHTHOUSANDFLAG 0
# 	HEXTENTHOUSANDFLAG 0
# 	HEXTWENTYTHOUSANDFLAG 0

class face2:
    passable:int
    triangle:tuple[int,int,int]

    def __init__(self, r:io.TextIOWrapper):
        records = parse.property(r, "PASSABLE", 1)
        self.passable = int(records[1])
        records = parse.property(r, "TRIANGLE", 3)
        self.triangle = (int(records[1]), int(records[2]), int(records[3]))


class dmspritedef2:
    tag:str
    center_offset:tuple[float,float,float]
    vertices:list[tuple[float,float,float]]
    uvs:list[tuple[float,float]]
    normals:list[tuple[float,float,float]]
    vertex_colors:list[tuple[float,float,float]]
    skin_assignment_groups:list[tuple[int,int]]
    material_palette:str
    polyhedron_definition:str
    face2s:list[face2]
    # num_mesh_ops:int

    face_material_groups:list[tuple[int,int]]
    vertex_material_groups:list[tuple[int,int]]
    bounding_box_min:tuple[float,float,float]
    bounding_box_max:tuple[float,float,float]
    bounding_radius:float
    fp_scale:int
    hex_one_flag:int
    hex_two_flag:int
    hex_four_thousand_flag:int
    hex_eight_thousand_flag:int
    hex_ten_thousand_flag:int
    hex_twenty_thousand_flag:int


    def __init__(self, tag:str, r:io.TextIOWrapper):
        self.tag = tag
        records = parse.property(r, "CENTEROFFSET", 3)
        self.center_offset = (float(records[1]), float(records[2]), float(records[3]))
        records = parse.property(r, "NUMVERTICES", 1)
        num_vertices = int(records[1])
        self.vertices = []
        for i in range(num_vertices):
            records = parse.property(r, "XYZ", 3)
            self.vertices.append((float(records[1]), float(records[2]), float(records[3])))
        records = parse.property(r, "NUMUVS", 1)
        num_uvs = int(records[1])
        self.uvs = []
        for i in range(num_uvs):
            records = parse.property(r, "UV", 2)
            self.uvs.append((float(records[1]), float(records[2])))
        records = parse.property(r, "NUMVERTEXNORMALS", 1)
        num_normals = int(records[1])
        self.normals = []

        for i in range(num_normals):
            records = parse.property(r, "XYZ", 3)
            self.normals.append((float(records[1]), float(records[2]), float(records[3])))
        records = parse.property(r, "NUMVERTEXCOLORS", 1)
        num_vertex_colors = int(records[1])
        self.vertex_colors = []
        for i in range(num_vertex_colors):
            records = parse.property(r, "XYZ", 3)
            self.vertex_colors.append((float(records[1]), float(records[2]), float(records[3])))
        records = parse.property(r, "SKINASSIGNMENTGROUPS", -1)
        self.skin_assignment_groups = []
        for i in range(int(records[1])):
            self.skin_assignment_groups.append((int(records[2 + i]), int(records[3 + i])))
        records = parse.property(r, "MATERIALPALETTE", 1)
        self.material_palette = records[1]
        parse.property(r, "POLYHEDRON", 0)
        records = parse.property(r, "DEFINITION", 1)
        self.polyhedron_definition = records[1]
        records = parse.property(r, "NUMFACE2S", 1)
        num_face2s = int(records[1])
        self.face2s = []
        for i in range(num_face2s):
            records = parse.property(r, "DMFACE2", 0)
            self.face2s.append(face2(r))
        records = parse.property(r, "NUMMESHOPS", 1)
        self.num_mesh_ops = int(records[1])

        records = parse.property(r, "FACEMATERIALGROUPS", -1)
        self.face_material_groups = []
        for i in range(int(records[1])):
            self.face_material_groups.append((int(records[2 + i]), int(records[3 + i])))
        records = parse.property(r, "VERTEXMATERIALGROUPS", -1)
        self.vertex_material_groups = []
        for i in range(int(records[1])):
            self.vertex_material_groups.append((int(records[2 + i]), int(records[3 + i])))

        records = parse.property(r, "BOUNDINGBOXMIN", 3)
        self.bounding_box_min = (float(records[1]), float(records[2]), float(records[3]))
        records = parse.property(r, "BOUNDINGBOXMAX", 3)
        self.bounding_box_max = (float(records[1]), float(records[2]), float(records[3]))
        records = parse.property(r, "BOUNDINGRADIUS", 1)
        self.bounding_radius = float(records[1])
        records = parse.property(r, "FPSCALE", 1)
        self.fp_scale = int(records[1])
        records = parse.property(r, "HEXONEFLAG", 1)
        self.hex_one_flag = int(records[1])
        records = parse.property(r, "HEXTWOFLAG", 1)
        self.hex_two_flag = int(records[1])
        records = parse.property(r, "HEXFOURTHOUSANDFLAG", 1)
        self.hex_four_thousand_flag = int(records[1])
        records = parse.property(r, "HEXEIGHTTHOUSANDFLAG", 1)
        self.hex_eight_thousand_flag = int(records[1])
        records = parse.property(r, "HEXTENTHOUSANDFLAG", 1)
        self.hex_ten_thousand_flag = int(records[1])
        records = parse.property(r, "HEXTWENTYTHOUSANDFLAG", 1)
        self.hex_twenty_thousand_flag = int(records[1])

    def write(self, w:io.TextIOWrapper):
        w.write(f"DMSPRITEDEF2 \"{self.tag}\"\n")
        w.write(f"\tCENTEROFFSET {self.center_offset[0]} {self.center_offset[1]} {self.center_offset[2]}\n")
        w.write(f"\tNUMVERTICES {len(self.vertices)}\n")
        for vertex in self.vertices:
            w.write(f"\tXYZ {vertex[0]} {vertex[1]} {vertex[2]}\n")
        w.write(f"\tNUMUVS {len(self.uvs)}\n")
        for uv in self.uvs:
            w.write(f"\tUV {uv[0]} {uv[1]}\n")
        w.write(f"\tNUMVERTEXNORMALS {len(self.normals)}\n")
        for normal in self.normals:
            w.write(f"\tXYZ {normal[0]} {normal[1]} {normal[2]}\n")
        w.write(f"\tNUMVERTEXCOLORS {len(self.vertex_colors)}\n")
        for vertex_color in self.vertex_colors:
            w.write(f"\tXYZ {vertex_color[0]} {vertex_color[1]} {vertex_color[2]}\n")
        w.write(f"\tSKINASSIGNMENTGROUPS {len(self.skin_assignment_groups)}")
        for skin_assignment_group in self.skin_assignment_groups:
            w.write(f" {skin_assignment_group[0]} {skin_assignment_group[1]}")
        w.write("\n")
        w.write(f"\tMATERIALPALETTE \"{self.material_palette}\"\n")
        w.write(f"\tPOLYHEDRON\n")
        w.write(f"\t\tDEFINITION \"{self.polyhedron_definition}\"\n")
        w.write(f"\tNUMFACE2S {len(self.face2s)}\n")
        for face2 in self.face2s:
            w.write("\t\tDMFACE2\n")
            w.write(f"\t\t\tPASSABLE {face2.passable}\n")
            w.write(f"\t\t\tTRIANGLE {face2.triangle[0]} {face2.triangle[1]} {face2.triangle[2]}\n")
        w.write(f"\tNUMMESHOPS {self.num_mesh_ops}\n")
        w.write(f"\tFACEMATERIALGROUPS {len(self.face_material_groups)}")
        for face in self.face_material_groups:
            w.write(f" {face[0]} {face[1]}")
        w.write("\n")
        w.write(f"\tVERTEXMATERIALGROUPS {len(self.vertex_material_groups)}")
        for vertex in self.vertex_material_groups:
            w.write(f" {vertex[0]} {vertex[1]}")
        w.write("\n")
        w.write(f"\tBOUNDINGBOXMIN {self.bounding_box_min[0]} {self.bounding_box_min[1]} {self.bounding_box_min[2]}\n")
        w.write(f"\tBOUNDINGBOXMAX {self.bounding_box_max[0]} {self.bounding_box_max[1]} {self.bounding_box_max[2]}\n")
        w.write(f"\tBOUNDINGRADIUS {self.bounding_radius}\n")
        w.write(f"\tFPSCALE {self.fp_scale}\n")
        w.write(f"\tHEXONEFLAG {self.hex_one_flag}\n")
        w.write(f"\tHEXTWOFLAG {self.hex_two_flag}\n")
        w.write(f"\tHEXFOURTHOUSANDFLAG {self.hex_four_thousand_flag}\n")
        w.write(f"\tHEXEIGHTTHOUSANDFLAG {self.hex_eight_thousand_flag}\n")
        w.write(f"\tHEXTENTHOUSANDFLAG {self.hex_ten_thousand_flag}\n")
        w.write(f"\tHEXTWENTYTHOUSANDFLAG {self.hex_twenty_thousand_flag}\n")

