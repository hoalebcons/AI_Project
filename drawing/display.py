import pygame
import time
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


flashLightPos = [ 0.1, 0.1, 0.1];
flashLightDir = [ 0.1, 0.1, 0.1 ];
flashLightColor = [ 0.1, 0.1, 0.1 ];

class Display:
    
    def __init__(self, title='', size=(800, 600), map_size = (10,6)):
        self.width, self.height = map_size
        self.title = title
        self.size = size
        self.delta = 0
        self.currentFrame = self.get_time()
        self.lastFrame = self.get_time()
        self.surface = pygame.display.set_mode(self.size, DOUBLEBUF | OPENGL)

        pygame.display.set_caption(self.title)

        glClearColor(0.1, 0.1, 0.1, 0)

        gluPerspective(60, (size[0] / size[1]), 0.1, 80.0)
        gluLookAt(-3, -7, 5, 0, 0, 0, 0, 0, 1)

        glTranslatef(-self.width / 2, self.height / 2, 0)
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_BLEND)
        glLineWidth(2)
        glDepthFunc(GL_LESS)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)

    def update(self):
        self.delta = self.currentFrame - self.lastFrame
        pygame.display.flip()
        self.lastFrame = self.get_time()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glViewport(0, 0, self.surface.get_width(), self.surface.get_height())

    @staticmethod
    def quit(event):
        ESCAPE = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        QUIT = event.type == pygame.QUIT
        SPACE = event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
        return ESCAPE or QUIT or SPACE

    @staticmethod
    def get_time():
        return time.time() * 1000
    
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