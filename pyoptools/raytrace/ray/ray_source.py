#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Module with functions to define ray sources"""

from __future__ import division
from numpy import sin,cos,pi,sqrt,floor,ceil
from numpy.random import normal

from pyoptools.raytrace.ray import Ray



def parallel_beam_c(origin=(0.,0.,0.),direction=(0.,0.,0.),size=(1.,1.),num_rays=(10,10),wavelength=0.58929, label=""):
    """Cartesian grid parallel beam

    This function creates a parallel beam, where the rays are organized in a
    cartesian grid.

    Parameters:


    *origin*
        Tuple with the coordinates of the central ray origin
    *direction*
        Tuple with the rotation of the beam arround the XYZ axes.
    *size*
        Tuple with the beam's width and the height.
    *num_rays*
        Tuple (nx,ny) containing the number of rays used to create the beam.
    *label*
        String used to identify the ray source
    """

    ret_val=[]

    nx,ny=num_rays
    dx,dy=size

    # note modify this to use traits
    dx=float(dx)
    dy=float(dy)

    for ix in range(nx):
        for iy in range(ny):
            x=-dx/2.+dx*ix/(nx-1)
            y=-dy/2.+dy*iy/(ny-1)
            ret_val.append(Ray(pos=(x,y,0),
                               dir=(0,0,1),
                               wavelength=wavelength, label=label).ch_coord_sys_inv(origin,direction))
    return ret_val

def parallel_beam_p(origin=(0.,0.,0.),direction=(0.,0.,0),radius=0.5, num_rays=(5,10),wavelength=0.58929, label=""):
    """Polar grid parallel beam

    This function creates a parallel beam, where the rays are organized in a
    polar grid.

    Parameters:


    *origin*
        Tuple with the coordinates of the central ray origin
    *direction*
        Tuple with the rotation of the beam arround the XYZ axes.
    *r*
        Beam radious
    *num_rays*
        Tuple (nr,na) containing the number of rays used to create the beam.
    *label*
        String used to identify the ray source
    """

    ret_val=[Ray(pos=(0,0,0),dir=(0,0,1),wavelength=wavelength, label=label).ch_coord_sys_inv(origin,direction)]
    nr,nt=num_rays
    for r_ in range(1,nr):
        r=radius*float(r_)/(nr-1)
        for t in range(nt):
            x_=r*sin(2*pi*t/nt)
            y_=r*cos(2*pi*t/nt)
            ret_val.append(Ray(pos=(x_,y_,0),
                               dir=(0,0,1),
                               wavelength=wavelength,label=label
                               ).ch_coord_sys_inv(origin,direction))
    return ret_val

def point_source_c(origin=(0.,0.,0.),direction=(0.,0.,0),span=(pi/8,pi/8)\
                     ,num_rays=(10,10),wavelength=0.58929, label=""):
    """Point source, with a cartesian beam distribution

    This function creates a point source, where the rays are organized in a
    cartesian grid.

    Parameters:


    *origin*
        Tuple with the coordinates of the central ray origin
    *direction*
        Tuple with the rotation of the beam arround the XYZ axes.
    *span*
        Tuple angular size of the ray pencil.
    *num_rays*
        Tuple (nx,ny) containing the number of rays used to create the beam.
    *label*
        String used to identify the ray source
    """
    ret_val=[]

    nx,ny=num_rays
    dx,dy=span

    for ix in range(nx):
        for iy in range(ny):
            if nx!=1: tx=-dx/2.+dx*ix/(nx-1)
            else: tx=0.

            if ny!=1: ty=-dy/2.+dy*iy/(ny-1)
            else: ty=0.
            temp_ray=Ray(pos=(0,0,0),
                         dir=(0,0,1),
                         wavelength=wavelength, label=label
                         ).ch_coord_sys_inv((0,0,0),(tx,ty,0))
            ret_val.append(temp_ray.ch_coord_sys_inv(origin,direction))
    return ret_val



def point_source_p(origin=(0.,0.,0.),direction=(0.,0.,0),span=pi/8,num_rays=(10,10),wavelength=0.58929, label=""):
    """Point source, with a polar beam distribution

    This function creates a point source, where the rays are organized in a
    polar grid.

    Parameters:


    *origin*
        Tuple with the coordinates of the central ray origin
    *direction*
        Tuple with the rotation of the beam arround the XYZ axes.
    *span*
        Tuple angular size of the ray pencil.
    *num_rays*
        Tuple (nr,na) containing the number of rays used to create the beam
    *label*
        String used to identify the ray source
    """

    ret_val=[Ray(pos=(0,0,0),dir=(0,0,1),wavelength=wavelength, label=label).ch_coord_sys_inv(origin,direction)]
    nr,nt=num_rays
    for r_ in range(1,nr):
        r=span*float(r_)/nr
        temp_ray=Ray(pos=(0,0,0),dir=(0,0,1),wavelength=wavelength, label=label).ch_coord_sys_inv((0,0,0),(r,0,0))
        for t in range(nt):
            tz=2*pi*t/nt
            temp_ray1=temp_ray.ch_coord_sys_inv((0,0,0),(0,0,tz))
            ret_val.append(temp_ray1.ch_coord_sys_inv(origin,direction))
    return ret_val


def point_source_r(origin=(0.,0.,0.),direction=(0.,0.,0),span=pi/8,num_rays=100,wavelength=0.58929, label=""):
    """Point source, with a ranrom beam distribution

    This function creates a point source, where the rays are organized in a
    random grid.

    Parameters:


    *origin*
        Tuple with the coordinates of the central ray origin
    *direction*
        Tuple with the rotation of the beam arround the XYZ axes.
    *span*
        Tuple angular size of the ray pencil.
    *num_rays*
        Number of rays used to create the beam
    *label*
        String used to identify the ray source
    """

    ret_val=[]

    for n_ in range(num_rays):
        rx=normal(0,span)
        ry=normal(0,span)
        temp_ray=Ray(pos=(0,0,0),dir=(0,0,1),wavelength=wavelength, label=label).ch_coord_sys_inv((0,0,0),(rx,ry,0))
        ret_val.append(temp_ray.ch_coord_sys_inv(origin,direction))
    return ret_val


def parallel_beam_list(x, y, origin=(0.,0.,0.), direction=(0.,0.,0), wavelength=0.58929, label=""):
    """Custom grid parallel beam

    This function creates a parallel beam, where the rays are located in
    coordinates specified in a list.

    Parameters:


    *x*
        X coordinate(s) of the rays
    *y*
        Y coordinate(s) of the rays
    *origin*
        Tuple with the coordinates of the (0, 0, 0) point
    *direction*
        Tuple with the rotation of the beam arround the XYZ axes.
    *wavelength*
        Wavelength of the rays
    *label*
        String used to identify the ray source
    """
    from itertools import repeat
    islist_x = hasattr(x, '__len__')
    islist_y = hasattr(y, '__len__')
    if not islist_x and not islist_y:
        x, y = (x, ), (y, )
    elif not islist_x:
        x, y = repeat(x, len(y)), y
    elif not islist_y:
        x, y = x, repeat(y, len(x))
    else:
        assert(len(x)==len(y))
    ret_val = []
    for _x, _y in zip(x, y):
        ret_val.append(Ray(pos=(_x,_y,0), dir=(0,0,1), wavelength=wavelength,
            label=label).ch_coord_sys_inv(origin,direction))
    return ret_val


def parallel_beam_h(origin=(0.,0.,0.), direction=(0.,0.,0), radius=0.5, num_rays=41, wavelength=0.58929, label=""):
    """Hexagonal grid parallel beam

    This function creates a parallel beam, where the rays are organized in an
    hexagonal grid.

    Parameters:


    *origin*
        Tuple with the coordinates of the central ray origin
    *direction*
        Tuple with the rotation of the beam arround the XYZ axes.
    *r*
        Beam radious
    *num_rays*
        approximate number of rays used to create the beam.
    *label*
        String used to identify the ray source
    """
    radius_sq = radius**2
    area = pi*radius_sq/num_rays
    l = sqrt(2./3/sqrt(3) * area) * 0.97
    h = sqrt(3.)/2*l
    r3l = radius/3./l
    r2h = radius/2./h
    ray_list = []
    for kx in xrange(int(floor(-r3l)), int(ceil(r3l))):
        for ky in xrange(int(floor(-r2h)), int(ceil(r2h))):
            x_ = 3 * kx * l
            y_ = 2 * ky * h
            if x_**2 + y_**2 <= radius_sq:
                ray = Ray(pos=(x_,y_,0), dir=(0,0,1), wavelength=wavelength,
                    label=label).ch_coord_sys_inv(origin,direction)
                ray_list.append(ray)
    for kx in xrange(int(floor(-r3l-0.5)), int(ceil(r3l-0.5))):
        for ky in xrange(int(floor(-r2h-0.5)), int(ceil(r2h-0.5))):
            x_ = (3 * kx + 1.5) * l
            y_ = (2 * ky + 1.0) * h
            if x_**2 + y_**2 <= radius_sq:
                ray = Ray(pos=(x_,y_,0), dir=(0,0,1), wavelength=wavelength,
                        label=label).ch_coord_sys_inv(origin,direction)
                ray_list.append(ray)
    return ray_list

