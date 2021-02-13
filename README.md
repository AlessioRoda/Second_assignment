# Second_assignment

## Introduction

In this repository it's implemented a simple user interface to permit to a genric robot to move in a definite map by avoiding the obstacles. In particular with this interface, user can ask to the robot to move in a random position between the six positions that are allowed, to move in a user defined position, to follow the external walls of the map and to stop in the last robot position.

To be executetd this interface needs other three packages (slam_gmapping, final_assignment and robot_description), without which is not posible to run this code, since some services that are required are contained in these packages.


In this repository there are four folders: 

* launch 
* scripts
* src
* srv

The first one contains a launch file who permits to execute the entire program, so the by lunching the my_robot_controller.launch it's possible to run the robot user interface and other scripts, like move_base.py and wall_follower_switch.py, that are already implemented and  to permit the robot to move in a certain position and to follow the external walls.

In the "scripts" folder it's contained the robot_user_inteface.py script, that is the user interface of the program. Here the program asks to te user to give him the comamnds to decide wich operation should it execute and to do that it calls the services that are launched previously with the launch file.

The "src" folder contains the server_second_assignment.cpp code, that is a server that teturns randomly one of the six allowed positions.

The "srv" folder contains a file to define the type of the data that are returned from the server.

## Comunication between nodes 


![rosgraph](https://user-images.githubusercontent.com/48511957/107848524-59255a00-6df4-11eb-8f9f-f9fe00d28803.png)


So, as it's possible to see in the picture, that is how the nodes comunicate to eachothers: what it's interesting to consider is that the robot_user_interface node get the odom data to obtain the position of the robot in the map (by subscribing to the odom service) and can set the velocity of the robot by publihing a cmd_vel message to the Twist pubblisher. 
The robot_user_interface also move the robot in a certain position by sending a message of type move_base_msgs/MoveBaseActionGoal. 

## Robot behaviors and software architecture 


