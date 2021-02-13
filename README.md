# Second_assignment

## Introduction

In this repository it's implemented a simple user interface to permit to a genric robot to move in a definite map by avoiding the obstacles. In particular with this interface, user can ask to the robot to move in a random position between the six positions that are allowed, to move in a user defined position, to follow the external walls of the map and to stop in the last robot position.

To be executetd this interface needs other three packages (slam_gmapping, final_assignment and robot_description), without which is not posible to run this code, since some services that are required are contained in these packages.

Note: this code was developped for ROS melodic, but can be executed also in other ROS distributions by downloading the indicated slam_gmapping, final_assignment and robot_description packeges for the considered distribution.


In this repository there are four folders: 

* launch 
* scripts
* src
* srv

The first one contains a launch file who permits to execute the entire program, so the by launching the my_robot_controller.launch it's possible to run the robot user interface and other scripts, like move_base.py and wall_follower_switch.py, that are already implemented and  to permit the robot to move in a certain position and to follow the external walls.

In the "scripts" folder it's contained the robot_user_inteface.py script, that is the user interface of the program. Here the program asks to the user to give him the comamnds to decide wich operation should it execute and to do that it calls the services that are launched previously with the launch file.

The "src" folder contains the server_second_assignment.cpp code, that is a server that returns randomly one of the six allowed positions.

The "srv" folder contains a file to define the type of the data that are returned from the server.

## Comunication between nodes 

<br />
![rosgraph](https://user-images.githubusercontent.com/48511957/107848524-59255a00-6df4-11eb-8f9f-f9fe00d28803.png)

<br />

As it's possible to see in the picture, this is how the nodes comunicate to eachothers: what it's interesting to consider is that the robot_user_interface node get the odom data to obtain the position of the robot in the map (by subscribing to the odom service) and can set the velocity of the robot by publihing a cmd_vel message to the Twist pubblisher. 
The robot_user_interface also move the robot in a certain position by sending a message of type move_base_msgs/MoveBaseActionGoal. 

## Robot behaviors and software architecture 

First at the beginning of the execution the nodes /robot_user_interface and /server_second_assignment initialize the publishers and the subscibers with respect to the oter running nodes. After that the main part of the robot_user_interface has to ask in a innfinite time loop the commands to the user

1) To randomly move ina one of the allowed positions
2) Ask user to choose the target position for the robot
3) Let the robot following the external walls 
4) Stop the robot 

As previously mentioned, not all the positons are allowed, only positions: [-4, -3], [5, -3], [-4, 2], [-4, 7], [5, -7], [5, 1]

