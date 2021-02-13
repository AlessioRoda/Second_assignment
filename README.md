# Second_assignment

## Introduction

In this repository it's implemented a simple user interface to permit to a generic robot to move in a definite map by avoiding the obstacles. In particular with this interface, user can ask to the robot to move in a random position between the six positions that are allowed, to move in a user defined position, to follow the external walls of the map and to stop in the last robot position.

To be executed this interface needs other three packages (slam_gmapping, final_assignment and robot_description), without which is not possible to run this code, since some services that are required are contained in these packages.

Note: this code was developed for ROS melodic, but can be executed also in other ROS distributions by downloading the indicated slam_gmapping, final_assignment and robot_description packages for the considered distribution.


In this repository there are four folders:

* launch
* scripts
* src
* srv

The first one contains a launch file who permits to execute the entire program, so by launching the my_robot_controller.launch it's possible to run the robot user interface and other nodes, like move_base and wall_follower, that are already implemented and permit the robot to move in a certain position and to follow the external walls.

In the "scripts" folder it's contained the robot_user_interface.py script, that is the user interface of the program. Here the program asks the user to give him the commands to decide wich operation should it execute and to do that it calls the services that are launched previously with the launch file.

The "src" folder contains the server_second_assignment.cpp code, that is a server that returns randomly one of the six allowed positions.

The "srv" folder contains a file to define the type of the data that are returned from the server.

## Comunication between nodes

![rosgraph](https://user-images.githubusercontent.com/48511957/107848524-59255a00-6df4-11eb-8f9f-f9fe00d28803.png)

<br />


As it's possible to see in the picture, this is how the nodes communicate to each others: what it's interesting to consider is that the robot_user_interface node gets the odom data to obtain the position of the robot in the map (by subscribing to the odom service) and can set the velocity of the robot by publishing a cmd_vel message to the Twist publisher.
The robot_user_interface also moves the robot in a certain position by sending a message of type move_base_msgs/MoveBaseActionGoal.

## Robot behaviors and software architecture

### Software architecture

First, at the beginning of the execution the nodes /robot_user_interface and /server_second_assignment initialize the publishers and the subscribers with respect to the other running nodes. After that the main part of the robot_user_interface has to ask in an infinite loop the commands to the user

1) To randomly move in one of the allowed positions
2) Ask user to choose the target position for the robot
3) Let the robot following the external walls
4) Stop the robot

As previously mentioned, not all the positons are allowed, the only target position that robot is allowed to reach are [-4, -3], [5, -3], [-4, 2], [-4, 7], [5, -7], [5, 1], so if user chooses another position the program asks him to digit it agin.

When the position is randomly chosen the robot_user_interface node sends a request to server_second_assignment node, which will return one of the allowed positions.
After having received the position either from the server or from the user, to move the robot it's set a field goal with the x and y coordinates of the target to reach

To let the robot follow the external walls, the program only has to call the wall_follower service while to stop the robot the linear velocity is set to 0 and to make sure that the robot won't go to another position, user asks him before, the program sets a field goal with the coordinates of the position of the robot when it was ordered him to stop.

### Behaviors

As it's possible to notice by having a look to the RVIZ simulation, at the beginning the robot doesn't completely know the entire map, so to move in a certain position it will learn the map by scanning it while it is moving. This means that sometimes when the robot has to reach a position it doesn't know, it goes in a wrong direction at the beginning and when robot understands it, it comes back and searches for another path to follow. At the end, when the robot has seen the entire map, it doesn't fail the optimal path to reach a certain position anymore.

## Considerations

The robot can successfully reach the positions and in general move avoiding the obstacles. The algorithm that is implemented to understand the map in which it moves is optimal in this case, since the dimension of the entire map is limited, maybe in a bigger and more complicate map it's possible that robot can get lost more time before it can learn the entire map.

In the code to move in a certain position is adopted the move_base algorithm, it could also be possible to do it by implementing the bug0 algorithm and even ask to user to decide which kind of algorithm robot should use.

## How to run the code

To run the code it's necessary to have the slam_gmapping, final_assignment and robot_description packages inside its own workspace, then clone also this repository inside it and then, after having gone in your workspace folder in the terminal, execute the following commands:

* roscore &
* catkin_make
* roslaunch final_assignment simulation_gmapping.launch
* roslaunch second_assignment my_robot_controller.launch

Then you should see the RVIZ and Gazeebo simulation of the robot and of the map, then by digiting the commands on the terminal and by following the instructions on the user interface you can send commands to the robot. 
