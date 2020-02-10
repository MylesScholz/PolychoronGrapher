# Graph Test
# Myles Scholz

import pyglet
from pyglet.gl import *
from pyglet.window import key
import math
from quaternion import *
import pentachoron
import tesseract
import polychoron

# Angle and axis increment for controls
INCREMENT = 0.05

class Window(pyglet.window.Window):
    
    # Initialize rotation axis and quaternion
    axis = Quaternion()
    axisX = axisY = axisZ = 1
    angle = math.pi / 4
    
    axis.set_sv_form((angle, [axisX, axisY, axisZ]))
        
    axis_v = axis.get_sv_form()[1]
    axisX = axis_v[0]
    axisY = axis_v[1]
    axisZ = axis_v[2]
    
    def __init__(self, width, height, title=''):
        super(Window, self).__init__(width, height, title)
        glClearColor(0, 0, 0, 1)
        glShadeModel(GL_SMOOTH)
        
        # Light parameter lists
        light_position = [0, 50, 100, 1]
        light_direction = [0, 0, 1, 0]
        light_diffuse = [1, 1, 1, 1]
        light_specular = [0, 0, -1, 1]
        gl_light_position = (GLfloat * len(light_position))(*light_position)
        gl_light_direction = (GLfloat * len(light_direction))(*light_direction)
        gl_light_diffuse = (GLfloat * len(light_diffuse))(*light_diffuse)
        gl_light_specular = (GLfloat * len(light_specular))(*light_specular)
        
        # Light position and attenuation settings
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.001)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.00001)
        glLightfv(GL_LIGHT0, GL_POSITION, gl_light_position)
        
        # Apply light parameters
        glLightfv(GL_LIGHT1, GL_DIFFUSE, gl_light_diffuse)
        glLightfv(GL_LIGHT1, GL_SPECULAR, gl_light_specular)
        glLightfv(GL_LIGHT1, GL_POSITION, gl_light_direction)
        
        glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
        
        # Enable OpenGL configurations
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        
    def on_draw(self):
        # Lighting parameter lists
        mat_specular = [1, 1, 1, 1]
        mat_shininess = [50]
        gl_mat_shininess = (GLfloat * len(mat_shininess))(*mat_shininess)
        gl_mat_specular = (GLfloat * len(mat_specular))(*mat_specular)
        
        self.clear()
        
        # Apply lighting parameters
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, gl_mat_shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, gl_mat_specular)
        
        glPushMatrix()
        
        # Convert the axis quaternion into a rotation matrix
        matrix = self.axis.get_rotation_matrix()
        
        # Convert the 3x3 rotation matrix into a linear, column-major 16 item list
        linear = []
        for i in range(3):
            for j in range(3):
                linear.append(matrix[j][i])
            linear.append(0)
        linear.extend([0, 0, 0, 1])
        
        # Apply the linearized rotation matrix
        gl_linear = (GLfloat * len(linear))(*linear)
        glMultMatrixf(gl_linear)
        
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Colored cube for testing
        """
        glBegin(GL_QUADS)
 
        # Top - Green
        glColor4ub(0, 255, 0, 127)
        glNormal3f(0, 1, 0)
        glVertex3f( 50, 50, -50)
        glVertex3f(-50, 50, -50)
        glVertex3f(-50, 50,  50)
        glVertex3f( 50, 50,  50)
        
        # Bottom - Orange
        glColor4ub(255, 127, 0, 127)
        glNormal3f(0, -1, 0)
        glVertex3f( 50, -50,  50)
        glVertex3f(-50, -50,  50)
        glVertex3f(-50, -50, -50)
        glVertex3f( 50, -50, -50)
        
        # Front - Red
        glColor4ub(255, 0, 0, 127)
        glNormal3f(0, 0, 1)
        glVertex3f( 50,  50, 50)
        glVertex3f(-50,  50, 50)
        glVertex3f(-50, -50, 50)
        glVertex3f( 50, -50, 50)
        
        # Back - Yellow
        glColor4ub(255, 255, 0, 127)
        glNormal3f(0, 0, -1)
        glVertex3f( 50, -50, -50)
        glVertex3f(-50, -50, -50)
        glVertex3f(-50,  50, -50)
        glVertex3f( 50,  50, -50)
        
        # Left - Blue
        glColor4ub(0, 0, 255, 127)
        glNormal3f(-1, 0, 0)
        glVertex3f(-50,  50,  50)
        glVertex3f(-50,  50, -50)
        glVertex3f(-50, -50, -50)
        glVertex3f(-50, -50,  50)
        
        # Right - Magenta
        glColor4ub(255, 0, 255, 127)
        glNormal3f(1, 0, 0)
        glVertex3f( 50,  50, -50)
        glVertex3f( 50,  50,  50)
        glVertex3f( 50, -50,  50)
        glVertex3f( 50, -50, -50)
        
        # Divider - Lime Green
        glColor4ub(127, 255, 0, 127)
        glNormal3f(-1, 0, 0)
        glVertex3f( 0,  75,  75)
        glVertex3f( 0,  75, -75)
        glVertex3f( 0, -75, -75)
        glVertex3f( 0, -75,  75)
        
        glEnd()
        # """
        
        # Pentachoron wireframe
        """
        obj = pentachoron.run()
        
        glLineWidth(3)
        glBegin(GL_LINES)
        glColor4ub(255, 255, 255, 255)
        
        for edge in obj.edges:
            vert_a = obj.vertices[edge[0]]*150
            gl_vert_a = (GLfloat * len(vert_a))(*vert_a)
            vert_b = obj.vertices[edge[1]]*150
            gl_vert_b = (GLfloat * len(vert_b))(*vert_b)
            
            glVertex3fv(gl_vert_a)
            glVertex3fv(gl_vert_b)
        
        glEnd()
        """
        
        # Translucent pentachoron
        """
        obj = pentachoron.run()
        vertices = polychoron.face_loops(obj.vertices, obj.edges, obj.faces)
        normals = calc_normals(obj)
        
        i = 0
        for face in vertices:
            glBegin(GL_POLYGON)
            glColor4ub(255, 127, 0, 127)
            gl_normal = (GLfloat * len(normals[i]))(*normals[i])
            glNormal3fv(gl_normal)
            
            for vertex in face:
                vertex = [x * 150 for x in vertex]
                gl_vert = (GLfloat * len(vertex))(*vertex)
                glVertex3fv(gl_vert)
            
            glEnd()
            i += 1
        # """
        
        # Translucent tesseract
        
        obj = tesseract.run()
        vertices = polychoron.face_loops(obj.vertices, obj.edges, obj.faces)
        normals = calc_normals(obj)
        
        i = 0
        for face in vertices:
            glBegin(GL_POLYGON)
            glColor4ub(255, 0, 255, 127)
            gl_normal = (GLfloat * len(normals[i]))(*normals[i])
            glNormal3fv(gl_normal)
            
            for vertex in face:
                vertex = [x * 150 for x in vertex]
                gl_vert = (GLfloat * len(vertex))(*vertex)
                glVertex3fv(gl_vert)
            
            glEnd()
            i += 1
        # """
        
        glPopMatrix()
        
        # Draw the rotation axis
        glPushMatrix()
        
        glLineWidth(5)
        glBegin(GL_LINES)
        
        # Rotation Axis - White
        glColor4ub(255, 255, 255, 127)
        glVertex3f(0, 0, 0)
        glVertex3f(self.axisX*100, self.axisY*100, self.axisZ*100)
        
        glEnd()
        
        glPopMatrix()
        
    def on_resize(self, width, height):
        aspectRatio = width / height
        
        glViewport(0, 0, width, height)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        gluPerspective(35, aspectRatio, 1, 1000)
        
        # Move model back into view
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -400)
        
    def on_key_press(self, symbol, modifiers):
        # Alter the rotation axis vector and angle
        if symbol == key.Q:
            self.axisX += INCREMENT
        elif symbol == key.A:
            self.axisX -= INCREMENT
        elif symbol == key.W:
            self.axisY += INCREMENT
        elif symbol == key.S:
            self.axisY -= INCREMENT
        elif symbol == key.E:
            self.axisZ += INCREMENT
        elif symbol == key.D:
            self.axisZ -= INCREMENT
        elif symbol == key.R:
            self.angle += INCREMENT
        elif symbol == key.F:
            self.angle -= INCREMENT
        
        # Loop the angle on [0, 2*pi]
        if self.angle > 2*math.pi:
            self.angle -= 2*math.pi
        elif self.angle < 0:
            self.angle += 2*math.pi
        
        # Update the quaternion to the new vector
        self.axis.set_sv_form((self.angle, [self.axisX, self.axisY, self.axisZ]))
        
        axis_v = self.axis.get_sv_form()[1]
        self.axisX = axis_v[0]
        self.axisY = axis_v[1]
        self.axisZ = axis_v[2]
        
    
def run():
    Window(640, 480, 'Graph Test')
    pyglet.app.run()

# Method to cross two 3-vectors u and v. Enter comma-separated 3-element lists.
def cross(u, v):
    result = [0, 0, 0]
    
    result[0] = u[1]*v[2] - u[2]*v[1]
    result[1] = u[2]*v[0] - u[0]*v[2]
    result[2] = u[0]*v[1] - u[1]*v[0]
    
    return result

# Method to normalize a vector. Enter a list of any length.
def normalize(vector):
    mag = 0
    for element in vector:
        mag += element**2
    mag = math.sqrt(mag)
    
    return [(i / mag) for i in vector]

# Method to calculate the normal vectors of a shape. Enter an initialized Polychoron.
# Edges must be arranged such that the first two elements of the edges list originate at the same vertex.
def calc_normals(obj):
    normals = []
    for face in obj.faces:
        arr = []
        for i in face:
            verts = []
            for j in obj.edges[i]:
                verts.append(obj.vertices[j])
            arr.append(verts)

        u = list(arr[0][1] - arr[0][0])
        v = list(arr[1][1] - arr[1][0])
        
        normals.append(normalize(cross(u, v)))
    
    return normals
