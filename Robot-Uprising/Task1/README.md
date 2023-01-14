# TASK - 1 

## Introduction 

Today, robots are used to assist humans or to reduce human efforts rather than just
mimicking humans. With the massive development of AI and machine learning, robots
are now capable of making their own decisions. Robots are leaving the comforts of a
controlled factory environment and moving to the unpredictable environment we inhabit.
This ‘real-world environment’ holds many interesting and complex challenges for us
engineers to explore and resolve.

Assistance robots are being massively used around the globe be it in the medical
industry or the food business. Although significant progress has been made there is so
much more to explore in a variety of fields. Assistance robots are presently seen in
applications such as cleaning, manufacturing, and entertainment. What if we could build
a robot that can truly assist in your tasks just like a human partner would. The
applications for such a robot are limitless and are constrained only by the limits of our
imagination.


**Challenges in this theme include installing UBUNTU-20.04 and ROS-Noetic, learning
basics of ROS, and performing basic node operations**

---

# Prerequisite

We need the following software for completing TASK -1 and further tasks!
1. [Ubuntu 20.04 OS](https://releases.ubuntu.com/focal/)
    - It may be in virtual machine , or the host itself
    - RAM : 4GB +
    - Storage : 50GB+
2.  [ROS Noetic](http://wiki.ros.org/noetic/Installation/Ubuntu)


---

# Getting Started 

### Introduction [ROS](https://www.ros.org/)
	Robot operating system is software that has tools , algorithms and drivers.
	It help us to reduce the redundant code for diifrent robots/ its applications.
Watch this [video](https://vimeo.com/639236696?embedded=true&source=vimeo_logo&owner=15710607)  to get better understanding 


# Catkin Workspace
1. **Catkin** is the official build system for ros1
2. **Catkin** combines CMake macros and python scripts to provide functionality on top of CMake's normal workflow 
Check out this [link](https://wiki.ros.org/catkin#Installing_catkin) to get started 

# ROS WIKI
The ROS1 documentation is maintained in [ROS wiki](http://wiki.ros.org/ROS/Tutorials)
Follow the tutorials for 1.1 to 1.8 to get better understanding of the ROS.

---


# Robotic Simulation Overview
	NOTE: This is only to give a quick overview of what these terms are. 
	There is a lot
	to explore and learn in each of the following subparts, and we strongly
	recommend you to explore these further as you do the tasks.

## Rviz
- Visualizing sensor information is an important part of developing and debugging
controllers.
- Rviz is a powerful 3D visualization tool in ROS that will help you do exactly that.
- It allows the user to view the simulated robot model, log sensor information from
the robot's sensors, and replay the logged sensor information.
- Read rviz - ROS Wiki Gazebo : Tutorial : Visualization and logging

## Gazebo
- Robot simulation is an essential tool in every roboticist's toolbox.
- A robust physics engine, high-quality graphics, and convenient programmatic
and graphical interfaces make Gazebo a top Choice for 3D Simulator.
- .World File: The file used to describe a collection of objects (such as buildings,
tables, and lights), and global parameters including the sky, ambient light, and
physics properties.
- Read Gazebo : Tutorials (gazebosim.org)

## URDF
- The Unified Robot Description Format (URDF) contains a number of XML
specifications for robot models, sensors, scenes, etc.
- It describes the position of all the joints, sensors, type of joints, structure of the
robot base, arm, etc.
- Read urdf - ROS Wiki urdf/Tutorials - ROS Wiki

## XACRO
- Xacro (XML Macros) Xacro is an XML macro language.
- With xacro, you can construct shorter and more readable XML files by using
macros that expand to larger XML expressions.
- Xacro is useful when the structure of the robot is complex so instead of
describing the whole structure in an urdf we can divide the structure into small
parts and call those macro files in the main xacro file.
- Xacros also make it easier to define common structures. For example, let's say
the robot has 2 wheels, we just need to make macros of a cylindrical
structure(wheels), call it in the main xacro file, and then define 2 different joints
using the same structure but giving different joint locations.
- Read urdf/Tutorials/Using Xacro to Clean Up a URDF File - ROS Wiki xacro -
ROS Wiki


## ROS & Gazebo
- ROS and Gazebo together are a great combination to simulate how your
algorithm would work in real-time scenarios.
- Transmission Tags
	1. Transmission tags are used to link actuators to joints.
	2. If the transmission tags the joints won't move in Gazebo and they will be
	considered as stationary objects.
	3. We need to define transmission for every dynamic(moving) joint.
- Gazebo Plugins
	1. In addition to the transmission tags, a Gazebo plugin needs to be added to
	your URDF that actually parses the transmission tags and loads the
	appropriate hardware interfaces and controller manager.
	2. Plugins basically replicate the exact architecture of the sensors in use or
	the control system used to control the movement of the robot.
Read Gazebo : Tutorial : [ROS control](gazebosim.org)

---

# Problem Statement - 1

- The objective of the task is to move the turtle inside the turtlesim window
in a circle and stop at its initial location.
- The second objective is to move the turtle in a sin wave.
- Individuals are supposed to do this by creating a node name,
/node_turtle_revolve within a python script, node_turtle_revolve.py


## Hints

The turtle needs to move in a circular motion with a certain radius. This
radius should be sufficient to fit within the turtlesim window. But making it
rotate in a circular manner, with only velocities to control is something to
think about.

- Use linear velocity as well as angular velocity with some combination to
get this done.
- Keep tracking the distance traveled so as to know when to stop.
- ROS/Tutorials/UnderstandingTopics - ROS Wiki

![image](https://user-images.githubusercontent.com/40001795/201526354-d185d296-2604-433c-8c1d-9cc560cbccb6.png)

![image](https://user-images.githubusercontent.com/40001795/201526363-954fcb25-10c9-4f8e-aac3-b613abb67a18.png)

![image](https://user-images.githubusercontent.com/40001795/201526377-13e2ba74-3685-4e53-98e9-44d4e5ba6bb1.png)

---



