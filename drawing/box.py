import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Box:
    vertices = np.array([
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [0, 1, 1]
    ])
    edges = np.array([
        [0, 1],
        [0, 3],
        [0, 4],
        [2, 1],
        [2, 3],
        [2, 7],
        [6, 3],
        [6, 4],
        [6, 7],
        [5, 1],
        [5, 4],
        [5, 7]
    ])
    faces = np.array([
        [0, 1, 2, 3],
        [0, 1, 5, 4],
        [4, 5, 7, 6],
        [1, 2, 7, 5],
        [0, 3, 6, 4],
        [2, 3, 6, 7],
    ])

    @staticmethod
    def draw_box(position, size, face_color=(0.2470588235294118, 0.2823529411764706, 0.8), border_color=(0.8, 0.8, 0.8)):
        Box.draw_border(position, size, border_color)
        Box.draw_faces(position, size, face_color)


    @staticmethod
    def draw_faces(position, size, face_color):
        pos_x, pos_y = position
        size_x, size_y, size_z = size
        for i, face in enumerate(Box.faces):
            glBegin(GL_POLYGON)
            glColor(face_color)
            for vertex in face:
                glVertex3f(Box.vertices[vertex, 0] * size_x + pos_x,
                        -(Box.vertices[vertex, 1] * size_y + pos_y),
                        Box.vertices[vertex, 2] * size_z)
            glEnd()

    @staticmethod
    def draw_border(position, size, border_color):
        pos_x, pos_y = position
        size_x, size_y, size_z = size
        glBegin(GL_LINES)
        glColor(border_color)
        for edge in Box.edges:
            for vertex in edge:
                glVertex3f(
                        Box.vertices[vertex, 0] * size_x + pos_x,
                        -(Box.vertices[vertex, 1] * size_y + pos_y),
                        Box.vertices[vertex, 2] * size_z)
        glEnd()
        glLineWidth(2)
    
    @staticmethod
    def loadTexture():
        textureSurface = pygame.image.load('./drawing/images.jpg')
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()

        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)
        glEnable(GL_TEXTURE_2D)