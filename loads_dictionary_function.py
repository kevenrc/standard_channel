#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 13:12:23 2020

@author: jacobzamora
"""
#UNSET = 0
from abaqus import *
from abaqusConstants import *

def loads_dict(r_loads = [], s_loads = [], t_loads = [], l_loads = [], loads = {}):

    # find number of different loads scenarios to create
    if len(r_loads) != 0:
        num_loads = len(r_loads)
    elif len(s_loads) != 0:
        num_loads = len(s_loads)
    elif len(t_loads) != 0:
        num_loads = len(t_loads)
    elif len(l_loads) != 0:
        num_loads = len(l_loads)
    else:
        return loads

    # create list of UNSET for empty loads
    if len(r_loads) == 0:
        r_loads = [UNSET] * num_loads
    if len(s_loads) == 0:
        s_loads = [UNSET] * num_loads
    if len(t_loads) == 0:
        t_loads = [UNSET] * num_loads
    if len(l_loads) == 0:
        l_loads = [UNSET] * num_loads

    # set loads of 0 to UNSET?????
    for i in range(0, num_loads):
        if r_loads[i] == 0:
            r_loads[i] = UNSET
        if s_loads[i] == 0:
            s_loads[i] = UNSET
        if t_loads[i] == 0:
            t_loads[i] = UNSET
        if l_loads[i] == 0:
            l_loads[i] = UNSET

    # create load scenarios and update loads dictionary
    for i in range(0, num_loads):
        load = [('NS6', UNSET, UNSET, r_loads[i]), ('NS60', UNSET, UNSET, r_loads[i]), ('NS3', s_loads[i], 0., UNSET), ('NS4', l_loads[i], t_loads[i], UNSET), ('NS40', UNSET, t_loads[i], UNSET)]
        update_name = str()
        if r_loads[i] != UNSET:
            r_name = ('r'+str(r_loads[i]))
            update_name = (update_name + r_name)
        if s_loads[i] != UNSET:
            s_name = ('s'+str(s_loads[i]))
            update_name = (update_name + s_name)
        if t_loads[i] != UNSET:
            t_name = ('t'+str(t_loads[i]))
            update_name = (update_name + t_name)
        if l_loads[i] != UNSET:
            l_name = ('l'+str(l_loads[i]))
            update_name = (update_name + l_name)
        loads.update({(update_name).replace('.',''): load})
        #loads.update({('r'+str(r_loads[i]) + 's'+str(s_loads[i]) + 't'+str(t_loads[i]) + 'l'+str(l_loads[i])).replace('.',''): load})
    return loads
