import io
import wce.parse as parse

# MATERIALDEFINITION "ELFCH0101_MDF"
# 	VARIATION 1
# 	RENDERMETHOD "USERDEFINED_21"
# 	RGBPEN 178 178 178 0
# 	BRIGHTNESS 1.00000001e-01
# 	SCALEDAMBIENT 7.50000000e-01
# 	SIMPLESPRITEINST
# 		TAG "ELFCH0101_SPRITE"
# 		HEXFIFTYFLAG 0
# 	PAIRS? 0 0.00000000e+00
# 	HEXONEFLAG 0

class materialdef:
    tag:str
    variation:int
    render_method:str
    rgbpen:tuple[int,int,int,int]
    brightness:float
    scaled_ambient:float
    simple_sprite_inst_tag:str
    simple_sprite_hex_fifty_flag:int
    pairs:tuple[int,float]
    hex_one_flag:int


    def __init__(self, tag:str, r:io.TextIOWrapper):
        self.tag = tag
        records = parse.property(r, "VARIATION", 1)
        self.tag_index = int(records[1])
        records = parse.property(r, "RENDERMETHOD", 1)
        self.render_method = records[1]
        records = parse.property(r, "RGBPEN", 4)
        self.rgbpen = (int(records[1]), int(records[2]), int(records[3]), int(records[4]))
        records = parse.property(r, "BRIGHTNESS", 1)
        self.brightness = float(records[1])
        records = parse.property(r, "SCALEDAMBIENT", 1)
        self.scaled_ambient = float(records[1])
        records = parse.property(r, "SIMPLESPRITEINST", 0)
        records = parse.property(r, "TAG", 1)
        self.simple_sprite_inst_tag = records[1]
        records = parse.property(r, "HEXFIFTYFLAG", 1)
        self.simple_sprite_hex_fifty_flag = int(records[1])
        records = parse.property(r, "PAIRS?", 2)
        self.pairs = (int(records[1]), float(records[2]))
        records = parse.property(r, "HEXONEFLAG", 1)
        self.hex_one_flag = int(records[1])



    def write(self, w:io.TextIOWrapper):
        w.write(f'MATERIALDEFINITION "{self.tag}"\n')
        w.write(f'\tVARIATION {self.tag_index}\n')
        w.write(f'\tRENDERMETHOD "{self.render_method}"\n')
        w.write(f'\tRGBPEN {self.rgbpen[0]} {self.rgbpen[1]} {self.rgbpen[2]} {self.rgbpen[3]}\n')
        w.write(f'\tBRIGHTNESS {self.brightness}\n')
        w.write(f'\tSCALEDAMBIENT {self.scaled_ambient}\n')
        w.write(f'\tSIMPLESPRITEINST\n')
        w.write(f'\t\tTAG "{self.simple_sprite_inst_tag}"\n')
        w.write(f'\t\tHEXFIFTYFLAG {self.simple_sprite_hex_fifty_flag}\n')
        w.write(f'\tPAIRS? {self.pairs[0]} {self.pairs[1]}\n')
        w.write(f'\tHEXONEFLAG {self.hex_one_flag}\n')
        w.write('\n')