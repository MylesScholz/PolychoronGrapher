# Pentachoron / 5-Cell script
# Myles Scholz

from polychoron import *
import math

def run():
    obj = Polychoron()
    
    a = 1 / math.sqrt(10)
    b = 1 / math.sqrt(6)
    c = 1 / math.sqrt(3)
    d = -math.sqrt(3 / 2)
    e = -2*math.sqrt(2 / 5)
    
    obj.set_vertices([a,b,c,1],[a,b,c,-1],[a,b,-2*c,0],[a,d,0,0],[e,0,0,0])
    obj.set_edges([0,1],[0,2],[0,3],[0,4],[1,2],[1,3],[1,4],[2,3],[2,4],[3,4])
    obj.set_faces([0,1,4],[0,2,5],[0,3,6],[1,2,7],[1,3,8],[2,3,9],[4,5,7],[4,6,8],[5,6,9],[7,8,9])
    obj.set_cells([0,1,3,6],[0,2,3,7],[1,2,5,8],[3,4,5,9],[6,7,8,9])
    
    obj.convert_to_eye([0,0,0,4],[0,0,0,0],[0,0,1,0],[0,1,0,0])
    obj.perspective_project((math.pi / 2),[0,0,0],[4,4,4])
    
    # print(obj.vertices)
    return obj
