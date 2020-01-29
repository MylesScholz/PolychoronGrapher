# Polychoron
# Myles Scholz
import numpy as np
import math

class Polychoron:
    
    def __init__(self, vert_num=5, edge_num=10, edges_per_face=3, face_num=10, faces_per_cell=4, cell_num=5):
        self.vertices = np.empty([vert_num, 4]) # An empty array for coordinates of the vertices (5 minimum for 4D).
        self.edges = np.empty([edge_num, 2], dtype=int) # An empty array for the indices of the vertices that form the edges (10 minimum for 4D).
        self.faces = np.empty([face_num, edges_per_face], dtype=int) # An empty array for the indices of the edges that form the faces (10 minimum for 4D).
        self.cells = np.empty([cell_num, faces_per_cell], dtype=int) # An empty array for the indices of the faces that for the cells (5 minimum for 4D).
        
    # Set the value of the vertices. Enter as comma-separated 4-element lists.
    def set_vertices(self, *args):
        for i, vert in enumerate(args):
            self.vertices[i] = vert
    
    # Set the indices of the vertices that form the edges. Enter as comma-separated 2-element lists.
    def set_edges(self, *args):
        for i, edge in enumerate(args):
            self.edges[i] = edge
    
    # Set the indices of the edges that form the faces. Enter as comma-separated lists of length equal to edges_per_face.
    def set_faces(self, *args):
        for i, face in enumerate(args):
            self.faces[i] = face
    
    # Set the indices of the faces that form the cells. Enter as comma-separated lists of length equal to faces_per_cell.
    def set_cells(self, *args):
        for i, cell in enumerate(args):
            self.cells[i] = cell
    
    # Convert all of the vertices to eye coordinates. Enter comma-separated 4-element lists.
    def convert_to_eye(self, eye_coord, view_point, up, over):
        # Convert lists to Numpy arrays for math
        eye_coord = np.array(eye_coord)
        view_point = np.array(view_point)
        up = np.array(up)
        over = np.array(over)
        
        # Create columns of transformation matrix
        d_col = normalize(view_point - eye_coord)
        a_col = normalize(cross(up, over, d_col))
        b_col = normalize(cross(over, d_col, a_col))
        c_col = cross(d_col, a_col, b_col)
        
        # Define transformation matrix
        matrix = np.empty([4, 4])
        matrix[:, 0] = a_col
        matrix[:, 1] = b_col
        matrix[:, 2] = c_col
        matrix[:, 3] = d_col
        
        # Convert the vertices to eye coordinates with the transformation matrix.
        for i in range(len(self.vertices)):
            diff = self.vertices[i] - eye_coord
            self.vertices[i] = np.dot(diff, matrix)
        
    # Project the polychoron to a 3D view box after converting to eye coordinates. Enter a number in radians and comma-separated 3-element lists.
    def perspective_project(self, view_angle, center, sides):
        # Convert lists to Numpy arrays for math
        center = np.array(center)
        sides = np.array(sides)
        
        # Intermediate math value
        t = math.tan(view_angle / 2)
        
        # Convert each vertex to 3D coordinates with a perspective projection
        for i in range(len(self.vertices)):
            vert = self.vertices[i]
            q = np.empty([3,])
            
            for j in range(3):
                q[j] = vert[j] / (vert[3]*t)
                vert[j] = (sides[j] / 2)*q[j] + center[j]
            
            vert[3] = 0
        
        self.vertices = self.vertices[:,:3]
    

# Method to normalize a vector. Enter an nD Numpy array.
def normalize(vector):
    mag = 0
    for element in vector:
        mag += element**2
    mag = math.sqrt(mag)
    
    return vector / mag

# Method to cross three 4-vectors u, v, w. Enter comma-separated 4-element Numpy arrays.
def cross(u, v, w):
    result = np.empty([4,])
    
    # Define intermediate values
    a = v[0]*w[1] - v[1]*w[0]
    b = v[0]*w[2] - v[2]*w[0]
    c = v[0]*w[3] - v[3]*w[0]
    d = v[1]*w[2] - v[2]*w[1]
    e = v[1]*w[3] - v[3]*w[1]
    f = v[2]*w[3] - v[3]*w[2]
    
    # Define resulting vector
    result[0] =  u[1]*f - u[2]*e + u[3]*d
    result[1] = -u[0]*f + u[2]*c - u[3]*b
    result[2] =  u[0]*e - u[1]*c + u[3]*a
    result[3] = -u[0]*d + u[1]*b - u[2]*a
    
    return result

def face_loops(vertices, edges, faces):
    face_loops = []
    for face in faces:
        a = []
        for i in face:
            a.append(list(edges[i]))
    
        prev_vert = a[0][0]
        curr_vert = a[0][1]
        edge_loop = [prev_vert, curr_vert]
    
        for i in range(len(a) - 2):
            next_vert = 0
            for edge in a:
                if curr_vert in edge and prev_vert not in edge:
                    if edge[1] == curr_vert:
                        next_vert = edge[0]
                    else:
                        next_vert = edge[1]
            prev_vert = curr_vert
            curr_vert = next_vert
            edge_loop.append(curr_vert)
        
        edge_loop = [list(vertices[i]) for i in edge_loop]
        
        face_loops.append(edge_loop)
    
    return face_loops
