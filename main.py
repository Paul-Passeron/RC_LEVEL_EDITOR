import sys

"""Structure of .rcmap files:

#HEADBEGIN
This is a comment describing the map
#HEADEND

#WBEGIN #:Walls
<float p1x> <float p1y> <float p2x> <float p2y> <int textureIdentifier>
#WEND

#IBEGIN #:Items
<flaot px> <float py> <float size> <int textureIdentifire>
#IEND

#PBEGIN #: Player
<float px> <float py>
#PEND
"""

def parse_list(list):
    buffer = ""
    for w in list:
        for token in w:
            buffer = str(token) + " "
        buffer += "\n"
    return buffer

def create_rcmap_from_lists(filename, head, wall_list, item_list, player):
    with open(filename, 'w') as f:
        sys.stdout = f
        print("#HEADBEGIN")
        print(head)
        print("#HEADEND")
        print("\n")
        print("#WBEGIN")
        print(parse_list(wall_list))
        print("#WEND")
        print("\n")
        print("#IBEGIN")
        print(parse_list(wall_list))
        print("#IEND")
        print("\n")
        print("#PBEGIN")
        print(str(player[0]) + " " + str(player[1]))
        print("#PEND")


create_rcmap_from_lists("test.rcmap", "This is a head", [], [], (0, 0))

