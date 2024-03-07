import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
import numpy as np

def draw_3d_model(texture_data):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, -5, 0, 0, 0, 0, 1, 0)

    glEnable(GL_TEXTURE_2D)
    texture_surface = pygame.image.fromstring(texture_data.tostring(), texture_data.shape[:2], "RGB")
    texture_data = pygame.image.tostring(texture_surface, 'RGB', 1)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, texture_surface.get_width(), texture_surface.get_height(), 0, GL_RGB,
                 GL_UNSIGNED_BYTE, texture_data)

    cube_vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
    )

    cube_edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7)
    )

    def draw_cube():
        glBegin(GL_LINES)
        for edge in cube_edges:
            for vertex in edge:
                glVertex3fv(cube_vertices[vertex])
        glEnd()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(1, 3, 1, 1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        draw_cube()
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

# 获取用户输入的图片
image_path = input("D:/pycharm/PyCharm 2021.3.1/pythonProject/__building.jpg")
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

draw_3d_model(image)
