# TASK - 2
# Problem Statement 1:

Now that you are familiar with ROS and linux commands (Hopefully; If not, please familiarize yourself with the same), try making the turtle in turtlesim follow a path that resembles a sine wave. Take feedback from the odometry topic which gives the current position of the turtle. This is called a closed control loop, and is a very important part of control systems.

---

Now that you have completed problem statement 1, we will get into spawning gazebo entities in this world and control it using cmd vel.
Use the internet, and explore gazebo to complete this task

The World :
![image](https://user-images.githubusercontent.com/40001795/201526417-7f5b88ac-169e-44af-9d30-b0182904f454.png)

The ebot :

![image](https://user-images.githubusercontent.com/40001795/201526427-42e96412-af7f-4c46-920e-d6e6b8095fd5.png)

# Problem Statement 2:
Your task is to spawn the ebot in the gazebo world and control it through teleop


1. Git clone the following rep in src directory and catkin make in workspace and source it

2. Execute the following statement
```sh
roslaunch ebot_description ebot_gazebo.launch
```

3. The gazebo world is the racetrack world.
4. You need to spawn on the start line on the race track , not 0 , 0 , 0 coordinates 
4. Add a gazebo plugin (skidsteer drive) to control the ebot.
5. Control your bot using cmd vel commands 

Hints:
1. Use [Teleop](http://wiki.ros.org/teleop_twist_keyboard):
2. Refrence [Turtlbot3](https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/)


---


