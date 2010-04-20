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

    window = glumpy.Window(800,600)
    trackball = glumpy.Trackball(60,30,1.1)
    mesh = Mesh(64)

    def func3(x,y):
        return numpy.sin(x*x+y*y)*numpy.cos(x+y*y)*numpy.sin(y) 
    #return (1-x/2+x**5+y**3)*numpy.exp(-x**2-y**2)
    dx, dy = .05, .05
    x = numpy.arange(-4.0, 4.0, dx, dtype=numpy.float32)
    y = numpy.arange(-4.0, 4.0, dy, dtype=numpy.float32)
    Z = func3(*numpy.meshgrid(x, y))
    I = glumpy.Image(Z, interpolation='bilinear',
                     cmap=glumpy.colormap.Hot, displace=True)
   
    @window.event
    def on_draw():
        gl.glClearColor(1,1,1,1)
        window.clear()
        trackball.push()

        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glPolygonOffset (1.0, 1.0)
        gl.glPolygonMode (gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        gl.glEnable (gl.GL_POLYGON_OFFSET_FILL)

        gl.glScalef(1,1,0.25)
        gl.glTranslatef(0,0,-0.5)
        gl.glColor4f(1,1,1,1)
        I.shader.bind(I.texture,I._lut)
        mesh.draw()
        gl.glPolygonMode (gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        gl.glDisable (gl.GL_POLYGON_OFFSET_FILL)
        gl.glColor4f(0,0,0,.25)
        mesh.draw()
        I.shader.unbind()

        trackball.pop()

    @window.event
    def on_mouse_drag(x, y, dx, dy, button):
        trackball.drag_to(x,y,dx,dy)
        window.draw()

    @window.event
    def on_mouse_scroll(x, y, dx, dy):
        trackball.zoom_to(x,y,dx,dy)
        window.draw()

    window.mainloop()
