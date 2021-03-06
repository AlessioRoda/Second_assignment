#! /usr/bin/env python

## import ros stuff
import rospy
import time
from std_srvs.srv import *
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
from second_assignment.srv import *
from move_base_msgs.msg import MoveBaseActionGoal
from geometry_msgs.msg import Twist

import math

actual_position=Point()

## Variables to save the value of the target robot has to reach
goal_x=0
goal_y=0

## Variable to generate a message of reached position in the positionCallback
notify=False

set_target=False

## Initialize the distance to the target
dist=0


## Initialize the publishers
pub_move_base=None
pub_twist=None

## Initialize the odom subscriber
sub_odom=None

## Initialize the wall_follower client
srv_client_wall_follower = None


## Callback to constantly get the robot position
def positionCallback(msg):
	
    global actual_position, goal_x, goal_y, notify
    actual_position=msg.pose.pose.position
    
    if (distance()<=0.4 and notify==True):
		print("\nTarget reached!")
		notify=False
    
    
    
## Function to get a new position from the user and check that it's one of the catchable positions
def user_set_position():
	
    global srv_client_wall_follower
    
    ## Initialize the variable to decide if the position can be gotten or not
    catchable_position=False
    
    x=0
    y=0
    
    while(catchable_position==False):
		
		print("\n Please insert a position between {[-4, -3], [5, -3], [-4, 2], [-4, 7], [5, -7], [5, 1]}")
		
		## Check if the input that user gives is a number or not
		try:
			x = float(raw_input('x :'))
			y = float(raw_input('y :'))
			
		## If the input is not a number come back to the main user interface (this can also be a way to exit from this functon without giving an input)	
		except:
			print("Char characters are not allowed, let's exit \n")
			break
    
		## Now to choose the target are considered the only possible cases we have
		
		if (y==-3 and x==-4 or x==5):
				catchable_position=True
		
		elif (y==2 and x==-4):
				catchable_position=True
			  
		elif(y==7 and x==-4):
				catchable_position=True
				
		elif(y==-7 and x==5):
				catchable_position=True
				
		elif(y==1 and x==5):
				catchable_position=True
				
		else:
				catchable_position=False
					

		if (catchable_position==True):
				## Make sure that the robot can't follow the wall
				resp = srv_client_wall_follower(False)
				## Send the values to the general function to reach a target
				set_target_position(x,y)

		else:
				print("\nThe position you insert is not correct, try again, otherwise digit a string to exit")
	    
     
    
    
    
## Function to move in the direction received from the server     
def move_randomly():
	global srv_client_wall_follower, srv_pos, actual_position
	
	## I's necessary to ensure that the client wall_follower is disabled 
	srv_client_wall_follower(False)
	
	print("\nActual robot position: "+str(actual_position))

	resp=srv_pos()
	
	## Call the generic funtion to set the new target position
	set_target_position(resp.x, resp.y)
	
	return
    
    
## Function to make the robot follow the external walls
def follow_wall():
	
	global srv_client_wall_follower
	
	print("\n Let's follow the external walls")
	srv_client_wall_follower(True)
	
	return
	

## To stop the robot the linear velocity values are set to 0, evenmore the target to reach is set to the position in wich robot is, so that to make sure it won't try to reach another position
def stop_robot():
	
	global set_target, pub_move_base, srv_client_wall_follower, pub_twist
	global goal_x, goal_y, notify
	
	## Check that the robot doesn't follow the wall
	resp = srv_client_wall_follower(False)
	
	## Set the value of velocity to 0	
	velocity=Twist()
	velocity.linear.x=0
	velocity.linear.y=0
	
	move_goal = MoveBaseActionGoal()
	move_goal.goal.target_pose.header.frame_id="map"
	move_goal.goal.target_pose.pose.orientation.w=1

	move_goal.goal.target_pose.pose.position.x = actual_position.x
	move_goal.goal.target_pose.pose.position.y = actual_position.y
	pub_move_base.publish(move_goal)
		
	
	pub_twist.publish(velocity)
	
	print("Robot has been stoped in position x="+str(actual_position.x)+", y="+str(actual_position.y))
	
	## To not generate a message to reached position
	notify=False
	
	## Set the goal position as the last position in wich robot is
	goal_x=actual_position.x
	goal_y=actual_position.y
	
	
	return
	
	
	
## This function get two parameters, target_x and target_y and set the target position in wich robot has to go
def set_target_position(target_x, target_y):
	
	global resp, srv_client_user_interface, set_target, pub_move_base
	global goal_x, goal_y, notify
	
	## Initialize a MoveBaseActionGoal target to move my robot
	move_goal = MoveBaseActionGoal()
	move_goal.goal.target_pose.header.frame_id="map"
	move_goal.goal.target_pose.pose.orientation.w=1

	move_goal.goal.target_pose.pose.position.x = target_x
	move_goal.goal.target_pose.pose.position.y = target_y
	
	pub_move_base.publish(move_goal)
	
	print("\n Let's reach the position x="+str(target_x)+" y="+str(target_y))
	
	## Set the goal position as the one I received 
	goal_x=target_x
	goal_y=target_y
	
	## Set the variable notify to true to be allerted when the robot reaches the target
	notify=True
	
	## Print the distance beteen the robot and the target
	print ("\n Distance to the target: "+str(distance()))
	
	
	return
    
	
## Function to estimate the value of the distance between the robot positon and the target it has to reach
def distance():
	
	global goal_x, goal_y, actual_position
	
	dist_x= actual_position.x-goal_x
	dist_y= actual_position.y-goal_y
	
	## To estimate the distance it's used the vector distance from the coordinate of the position to the actual robot position
	dist=math.sqrt(pow(dist_x, 2)+pow(dist_y, 2))
	
	return dist
	
		


def main():
	
    global srv_client_wall_follower, srv_pos, pub_move_base, pub_twist, set_target
	
    rospy.init_node('robot_user_interface')
    
    
    ## Subscribe to Odom service to get the robot position
    sub_odom=rospy.Subscriber("/odom", Odometry, positionCallback)
    
   
   #Pubblisher to pubblsh the poition in wich the robot has to go and the velocity to set
    pub_move_base=rospy.Publisher('move_base/goal', MoveBaseActionGoal, queue_size=1)
    pub_twist = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
   
    ## To make the robot follows the wall it's utilized the already implemented wall_follower service
    srv_client_wall_follower = rospy.ServiceProxy(
        '/wall_follower_switch', SetBool)
    ## Connect to the server_second_assignment node, the server that provides to give the random position
    srv_pos= rospy.ServiceProxy('/position', Server_second_assignment)
    
    
    rate = rospy.Rate(20)
    
    ## For the entire execution of the program it's shown an user interface to obtain the command the robot has to execute:
    ## robot can move in a random position, move in a specific position, follow the walls or stop in the last position.
    while not rospy.is_shutdown():

		print("\nPlease give me a new command between the following\n")
		print("1- To move in a random position\n2- To move in a specific position\n3- Start to follow external walls\n4- Stop in last position")
		
        ## Initialize variable command to 0
		command=0

		command=int(raw_input())

		if(command==1):
			move_randomly()

		elif(command==2):
			user_set_position()

		elif(command==3):
			follow_wall()
			
		elif(command==4):
			stop_robot()
			
		## If there's a not allowed command user has to digit the command again	
		else:
			print("\n Probably you choose a command not allowed, please try again")
		

    
		
			

if __name__ == '__main__':
	## Since there are other scripts to be launched at the beginning this program waits 2 seconds, so the logs of the scripts aren't printed together
    time.sleep(2)
    main()
