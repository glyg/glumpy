#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (C) 2009-2010  Nicolas P. Rougier
#
# Distributed under the terms of the BSD License. The full license is in
# the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------
import numpy, glumpy
import OpenGL.GL as gl
import OpenGL.GLUT as glut

class Mesh(object):
    def __init__(self, n=64):
        self.indices  = numpy.zeros((n-1,n-1,4), dtype=numpy.float32)
        self.vertices = numpy.zeros((n,n,3), dtype=numpy.float32)
        self.texcoords= numpy.zeros((n,n,2), dtype=numpy.float32)
        for xi in range(n):
            for yi in range(n):
                x,y,z = xi/float(n-1), yi/float(n-1), 0
                self.vertices[xi,yi] =  x-0.5,y-0.5,z
                self.texcoords[xi,yi] = x,y
        for yi in range(n-1):
            for xi in range(n-1):
                i = yi*n + xi
                self.indices[xi,yi] = i,i+1,i+n+1,i+n
    def draw(self):
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY);
        gl.glVertexPointerf(self.vertices)
        gl.glTexCoordPointerf(self.texcoords)
        gl.glDrawElementsus(gl.GL_QUADS, self.indices)
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY);


if __name__ == '__main__':

    window = glumpy.Window(900,600)
    trackball = glumpy.Trackball(60,30,0.85)
    mesh = Mesh(64)

    def func3(x,y):
        return (1-x/2+x**5+y**3)*numpy.exp(-x**2-y**2)
    dx, dy = .05, .05
    x = numpy.arange(-3.0, 3.0, dx, dtype=numpy.float32)
    y = numpy.arange(-3.0, 3.0, dy, dtype=numpy.float32)
    Z = func3(*numpy.meshgrid(x, y))
    I = glumpy.Image(Z, interpolation='bicubic',
                     cmap=glumpy.colormap.Hot,
                     lighted=True, gridsize=(31.0,31.0,0.0), elevation = 0.5)

    def draw_background():
        viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        gl.glDisable (gl.GL_LIGHTING)
        gl.glDisable (gl.GL_DEPTH_TEST)
        gl.glPolygonMode (gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        gl.glBegin(gl.GL_QUADS)
        #gl.glColor(0.75,0.75,1.0)
        gl.glColor(1.0,1.0,0.75)
        gl.glVertex(0,0,-1)
        gl.glVertex(viewport[2],0,-1)
        gl.glColor(1.0,1.0,1.0)
        gl.glVertex(viewport[2],viewport[3],0)
        gl.glVertex(0,viewport[3],0)
        gl.glEnd()

    @window.event
    def on_draw():
        gl.glClearColor(1,1,1,1)
        window.clear()
        draw_background()
        trackball.push()
        gl.glEnable(gl.GL_DEPTH_TEST)
#        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc (gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glTranslatef(0,0,-.25)
        gl.glColor4f(1,1,1,1)
        I.shader.bind(I.texture,I._lut)
        mesh.draw()
        I.shader.unbind()
        trackball.pop()

    @window.event
    def on_init():
       gl.glLightfv (gl.GL_LIGHT0, gl.GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
       gl.glLightfv (gl.GL_LIGHT0, gl.GL_AMBIENT, (0.3, 0.3, 0.3, 1.0))
       gl.glLightfv (gl.GL_LIGHT0, gl.GL_SPECULAR,(0.0, 0.0, 0.0, 0.0))
       gl.glLightfv (gl.GL_LIGHT0, gl.GL_POSITION,(2.0, 2.0, 2.0, 0.0))

    @window.event
    def on_mouse_drag(x, y, dx, dy, button):
        trackball.drag_to(x,y,dx,dy)
        window.draw()

    @window.event
    def on_mouse_scroll(x, y, dx, dy):
        trackball.zoom_to(x,y,dx,dy)
        window.draw()

    window.mainloop()
