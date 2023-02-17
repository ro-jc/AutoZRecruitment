#!/usr/bin/env python

import sys
from math import sin,radians

import rospy
from turtlesim.srv import *


def draw_sine(amplitude):
    rospy.wait_for_service('/turtle1/set_pen')
    set_pen = rospy.ServiceProxy('/turtle1/set_pen', SetPen)
    set_pen(255, 255, 255, 3, 1)

    rospy.wait_for_service('/turtle1/teleport_absolute')
    teleport = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
    teleport(0, 5, 0)

    set_pen(255, 255, 255, 3, 0)
    
    scaling_factor = 11/360
    for d in range(360):
        x = scaling_factor*d
        y = amplitude*sin(radians(d))

        teleport(x, 5+y, 0)


if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            print("usage: node_turtle_sine.py amplitude")
        else:
            draw_sine(int(sys.argv[1]))
    except rospy.ROSInterruptException:
        pass
