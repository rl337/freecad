#!/Applications/FreeCAD.app/Contents/bin/FreeCADCmd

import Part
import FreeCAD

inch = 1.0
eighth = inch / 8
fiveeighth = 5 * eighth

# ranges taken from:
# http://specblockusa.com/downloads/gray-block/size-shape-2013.pdf
height_ranges = [ 4, 6, 8, 10, 12 ]
width_ranges = [ 16 ]
depth_ranges = [ 8 ]
thickness={
    3: 0.75,
    4: 1.0,
    6: 1.0,
    8: 1.25,
   10: 1.25,
   12: 1.25,
}

def round_rect(width, height, depth, radius=0.1, pnt=FreeCAD.Base.Vector(0,0,0)):
    #x1 = pnt.x + -width / 2
    #x2 = pnt.x + width / 2
    #y1 = pnt.y + -height / 2
    #y2 = pnt.y + height / 2
    #z1 = pnt.z + -depth / 2
    #z2 = pnt.z + depth / 2
    x1 = pnt.x 
    x2 = pnt.x + width
    y1 = pnt.y
    y2 = pnt.y + height
    z1 = pnt.z
    z2 = pnt.z + depth

    c1_pnt=FreeCAD.Base.Vector(
        x1 + radius,
        y1 + radius,
        z1,
    )
    c2_pnt=FreeCAD.Base.Vector(
        x2 - radius,
        y1 + radius,
        z1,
    )
    c3_pnt=FreeCAD.Base.Vector(
        x1 + radius,
        y2 - radius,
        z1,
    )
    c4_pnt=FreeCAD.Base.Vector(
        x2 - radius,
        y2 - radius,
        z1,
    )

    c1 = Part.makeCylinder(radius, depth, c1_pnt)
    c2 = Part.makeCylinder(radius, depth, c2_pnt)
    c3 = Part.makeCylinder(radius, depth, c3_pnt)
    c4 = Part.makeCylinder(radius, depth, c4_pnt)

    b1_pnt = FreeCAD.Base.Vector(
        x1 + radius,
        y1,
        z1,
    )
    box1 = Part.makeBox(
        width - radius*2,
        height,
        depth,
        b1_pnt,
        FreeCAD.Base.Vector(0,0,1)
    )
    b2_pnt = FreeCAD.Base.Vector(
        x1,
        y1 + radius,
        z1,
    )
    box2 = Part.makeBox(
        width,
        height - radius*2,
        depth,
        b2_pnt,
        FreeCAD.Base.Vector(0,0,1)
    )

    result = box1.fuse(box2)
    result = result.fuse(c1)
    result = result.fuse(c2)
    result = result.fuse(c3)
    result = result.fuse(c4)

    return result

def create_two_cavity_cmu(width, height, depth, thickness=1.0, radius=1.0):
    name = "TwoCavityCMU_%dx%dx%d" % (width, height, depth)

    x1 = 0
    x2 = width
    y1 = 0
    y2 = height
    z1 = 0
    z2 = depth

    #x1 = -width / 2
    #x2 = width / 2
    #y1 = -height / 2
    #y2 = height / 2
    #z1 = -depth / 2
    #z2 = depth / 2

    cavity_width = (width - 3*thickness) / 2
    cavity_height = (height - 2*thickness)

    cav1_x1 = x1 + thickness
    cav1_x2 = cav1_x1 + cavity_width
    cav1_y1 = y1 + thickness
    cav1_y2 = cav1_y1 + cavity_height

    cav2_x1 = cav1_x2 + thickness
    cav2_x2 = cav2_x1 + cavity_width
    cav2_y1 = y1 + thickness
    cav2_y2 = cav1_y1 + cavity_height

    cav1 = round_rect(cavity_width, cavity_height, depth, radius, FreeCAD.Base.Vector(cav1_x1, cav1_y1, z1))
    cav2 = round_rect(cavity_width, cavity_height, depth, radius, FreeCAD.Base.Vector(cav2_x1, cav2_y1, z1))

    result = Part.makeBox(
        width,
        height,
        depth,
        #FreeCAD.Base.Vector(x1,y1,z1)
        FreeCAD.Base.Vector(0,0,0)
    )
    result = result.cut(cav1)
    result = result.cut(cav2)

    print name

    result.exportStl("%s.stl" % name)

for width in width_ranges:
    for height in height_ranges:
        for depth in depth_ranges:
            #round_rect(width, height, depth, 1.0).exportStl('rrect_%d_%d_%d.stl' % (width, height, depth))

            create_two_cavity_cmu(width*inch, height*inch, depth, thickness[depth]*inch, fiveeighth*inch)

# print FreeCAD.listDocuments()
