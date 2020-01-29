# Quaternion
# Myles Scholz
import numpy as np
from numpy import linalg as la
import math

class Quaternion:
    
    def __init__(self, x=1, y=0, z=0, w=0):
        self.q = np.array([x, y, z, w])
        # Real part
        self.x = self.q[0]
        # Vector part
        self.y = self.q[1]
        self.z = self.q[2]
        self.w = self.q[3]
        self.get_conjugate()
    
    # Returns the vector of quaternion values
    def get_v_form(self):
        return self.q
    
    # Sets quaternion values to a given list
    def set_v_form(self, arr):
        self.q = np.array(arr)
        self.x = arr[0]
        self.y = arr[1]
        self.z = arr[2]
        self.w = arr[3]
        self.get_conjugate()
        
    # Returns the scalar/vector form as a tuple
    # Scalar is the angle of rotation in radians
    # Vector is the axis of rotation
    # Rotation calculated as if quaternion were normalized
    def get_sv_form(self):
        r = Quaternion(self.q[0], self.q[1], self.q[2], self.q[3])
        r = r.normalize()
        scalar = 2*math.acos(r[0])
        vector = r[1:] / math.sin(scalar / 2)
        return (scalar, vector)
    
    # Converts a given scalar/vector tuple to vector form and sets the quaternion values to it
    # Accepts a tuple
    # The first element is the rotation angle in radians
    # The second element is the rotation axis as a three element list
    def set_sv_form(self, sv_form):
        scalar = math.cos(sv_form[0] / 2)
        u = Quaternion(0, sv_form[1][0], sv_form[1][1], sv_form[1][2])
        u = u.normalize()
        vector = u[1:]*math.sin(sv_form[0] / 2)
        arr = [scalar]
        arr.extend(vector)
        self.set_v_form(arr)
    
    # Sets and returns the conjugate quaternion for rotation
    def get_conjugate(self):
        self.conj = np.array([self.x, -self.y, -self.z, -self.w])
        return self.conj    
    
    # Returns the equivalent rotation matrix to the quaternion
    # Rotation calculated as if quaternion were normalized
    def get_rotation_matrix(self):
        r = Quaternion(self.q[0], self.q[1], self.q[2], self.q[3])
        r.normalize()
        rot = np.ndarray((3,3))
        rot[0, 0] = 1 - 2*(r.q[2]**2 + r.q[3]**2)
        rot[0, 1] = 2*(r.q[1]*r.q[2] - r.q[3]*r.q[0])
        rot[0, 2] = 2*(r.q[1]*r.q[3] + r.q[2]*r.q[0])
        rot[1, 0] = 2*(r.q[1]*r.q[2] + r.q[3]*r.q[0])
        rot[1, 1] = 1 - 2*(r.q[1]**2+ r.q[3]**2)
        rot[1, 2] = 2*(r.q[2]*r.q[3] - r.q[1]*r.q[0])
        rot[2, 0] = 2*(r.q[1]*r.q[3] - r.q[2]*r.q[0])
        rot[2, 1] = 2*(r.q[2]*r.q[3] + r.q[1]*r.q[0])
        rot[2, 2] = 1 - 2*(r.q[1]**2 + r.q[2]**2)
        
        return rot
    
    # Returns the normalization of the quaternion
    def normalize(self):
        mag = la.norm(self.q)
        self.set_v_form(self.q / mag)
        return self.q
        
    # Multiplies the quaternion by another Quaternion object from the right
    def multiply(self, q2):
        q2 = q2.get_v_form()
        a = self.q[0]*q2[0] - self.q[1]*q2[1] - self.q[2]*q2[2] - self.q[3]*q2[3]
        b = self.q[0]*q2[1] + self.q[1]*q2[0] + self.q[2]*q2[3] - self.q[3]*q2[2]
        c = self.q[0]*q2[2] - self.q[1]*q2[3] + self.q[2]*q2[0] + self.q[3]*q2[1]
        d = self.q[0]*q2[3] + self.q[1]*q2[2] - self.q[2]*q2[1] + self.q[3]*q2[0]
        
        self.set_v_form([a, b, c, d])

    # Returns the rotation of a Quaternion object with real part 0 (vector) by the quaternion
    def rotate(self, p):
        r = Quaternion(self.q[0], self.q[1], self.q[2], self.q[3])
        r.normalize()
        print(r.q)
        r.multiply(p)
        print(r.q)
        r_conj = Quaternion(self.conj[0], self.conj[1], self.conj[2], self.conj[3])
        print(r_conj.q)
        r.multiply(r_conj)
        return r.get_v_form()
