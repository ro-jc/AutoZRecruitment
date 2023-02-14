#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys
from math import pi

def node_turtle_revolve(radius):
    pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=1)
    rospy.init_node('node_turtle_revolve', anonymous=True)
    rate = rospy.Rate(10000)
    
    # Creating the Twist message to move the turtle
    command = Twist()
    command.linear.x = radius
    command.angular.z = 1
    
    # Keep track of distance
    distance = 0

    t0 = rospy.Time.now()
    while distance < 2*pi*radius:
        pub.publish(command)
        rate.sleep()

        distance += (rospy.Time.now() - t0).to_sec()*radius
        t0 = rospy.Time.now()
    else:
        command.linear.x = 0
        command.angular.z = 0
        pub.publish(command)


if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            print("usage: node_turtle_revolve.py radius")
        else:
            node_turtle_revolve(float(sys.argv[1]))
    except rospy.ROSInterruptException:
        pass
