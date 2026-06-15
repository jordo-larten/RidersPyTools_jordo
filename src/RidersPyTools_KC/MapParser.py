# Created by Exortile for SRTE's recompilation workflow
# Repurposed to read in symbols and add it to the object database of an instantiated object in this package

import io, sys, os
# parse_map allow these to be fully read in the symbol entry section
allowed_sections = {
    ".init": True,
    ".text": True,
    ".fini": True,
    ".rodata": True,
    ".data": True,
    ".sdata": True,
    ".sdata2": True,
}

# .bss must be allowed to find the player list.
# condition: if '*(.bss)' in linelist[0] or line

# add known symbols we want to be able to modify with our py package
# or, just all symbols honestly
global lookingList_global, ptr_dict_list_global
lookingList_global = ["players"]
ptr_dict_list_global = {}
def parse_map(mapfile: io.TextIOWrapper, dolphinmapfile: io.TextIOWrapper, start_address: int):
    is_section_allowed = False
    memory_map_found = False
    global ptr_dict_list_global
    ptr_dict_list = {}
    line = mapfile.readline()

    while line:
        line = line.strip()
        if line == "Linker script and memory map":
            memory_map_found = True
            break

        line = mapfile.readline()

    if not memory_map_found:
        raise Exception("No memory map found.")

    line = mapfile.readline()

    while line:
        linelist = line.split()

        # change to new section
        if line[:1] == ".":
            is_section_allowed = allowed_sections.get(linelist[0], False)

            if is_section_allowed:
                # write out new section header
                section_header = "{} section layout\n".format(linelist[0])
                dolphinmapfile.write(section_header)

        elif is_section_allowed:
            if len(linelist) == 2:

                # symbol entry
                if linelist[0][:2] == "0x" and linelist[1][:2] != "0x":
                    address = int(linelist[0], 16)
                    address += start_address
                    address = hex(address)[2:]
                    symbol_entry = "{} {}\n".format(address, linelist[1])
                    dolphinmapfile.write(symbol_entry)
                    # print(symbol_entry)
                    # Here, it writes the symbols needed for the map file. We can intercept here and compare for known symbols.
                    # Text.s enters this, so we know this is an allowed section.
                    # Goes up to 0x80434af0

        # Here, we gather what symbols are.
        # in *(.bss) exists players. Get it from linelist[1]
        #if len(linelist) > 1 and linelist[1] == "players":
        if (len(linelist) > 1) and linelist[1] in lookingList_global :
            #print("Found TE ptr list:\n")
            # Store address and name it in our config/constants for TE
            #print(linelist[0] + " " + linelist[1])
            ptr_dict_list[linelist[1]] = int(linelist[0], 16)
            pass
        line = mapfile.readline()
    ptr_dict_list_global = ptr_dict_list


def parse_for_dol(parentdir, dolphinmapfile: io.TextIOWrapper):
    mapfile = open(parentdir + "/main.map")

    parse_map(mapfile, dolphinmapfile, 0)

    mapfile.close()


def parse_for_rel(parentdir, dolphinmapfile: io.TextIOWrapper):
    dolfile = open(parentdir + "/main.dol", "rb")
    relfile = open(parentdir + "/_Main.rel", "rb")
    mapfile = open(parentdir + "/_Main.map")

    dolfile.seek(0xD8)
    start_address = int.from_bytes(dolfile.read(4), 'big')
    bss_size = int.from_bytes(dolfile.read(4), 'big')

    relfile.seek(0x54)
    code_section_start = int.from_bytes(relfile.read(4), 'big')
    code_section_start &= ~1  # remove executable bit flag
    start_address += (bss_size + 0x1EED40 + code_section_start)

    relfile.close()
    dolfile.close()

    parse_map(mapfile, dolphinmapfile, start_address)

    mapfile.close()

# This is where parsing starts. Thing is, we have to set a directory for the map here
# I don't know how we'd do that for ALL instances when we make this a package.
# So, figure that out in the future, future me.

def read_for_list(buildDir, lookingList=["players"]):
    global lookingList_global,ptr_dict_list_global
    lookingList_global = lookingList
    buildDir = os.path.normpath(buildDir) #buildDir must be a folder that contains GXSRTE.map, main.dol, main.map

    dolphinMapFile = open("GXSRTE.map", "w")

    dolphinMapFile.write("-- main.dol memory map --\n\n")
    parse_for_dol(buildDir, dolphinMapFile)
    return ptr_dict_list_global


def read_for_files(pathToMap):
    # buildDir = "../build" # not needed anymore
    # if len(sys.argv) > 1:
    buildDir = pathToMap # User MUST send in a path to their map file. This might cause a problem with distribution... ugh.
    buildDir = os.path.normpath(buildDir)

    dolphinMapFile = open("GXSRTE.map", "w")

    dolphinMapFile.write("-- main.dol memory map --\n\n")
    parse_for_dol(buildDir, dolphinMapFile)

    # dolphinMapFile.write("\n-- _Main.rel memory map --\n\n")
    # parse_for_rel(buildDir, dolphinMapFile)

    dolphinMapFile.close()
    pass

