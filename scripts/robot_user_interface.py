#! /usr/bin/env python

## import ros stuff
import rospy
from std_srvs.srv import *
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
from second_assignment import *
from move_base_msgs.msg import MoveBaseActionGoal

import math

# service callback

actual_position=Point()

## Variables to save the value of the target we want to receive
goal_x=0
goal_y=0

## Distance to the target
dist=0

yaw_ = 0


## Initialize a general publisher
pub=None
sub_odom=None

srv_client_go_to_point = None
srv_client_wall_follower = None
srv_client_user_interface = None


def positionCallback(msg):
    
    
    actual_position=msg.pose.pose.position
    
    quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
    euler = transformations.euler_from_quaternion(quaternion)
    yaw_ = euler[2]




## Function to get a new position from the user and check that it's one of the cathcable positions
def user_set_position():
	
    print("\nPlease insert a position")
    x = float(raw_input('x :'))
    y = float(raw_input('y :'))
    
    
    
    ## Now to choose the target we consider the only possible cases we have
    
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
            set_target_position(x,y)
            resp = srv_client_wall_follower_(False)

    else:
            print("\nThe position you insert is not correct")
	    
     
    
    
    
## Function to move in the direction received frome the server     
def move_randomly():
	
	
	## We have to ensure that the client wall_follower is disabled 
	resp = srv_client_wall_follower(False)
	resp = srv_pos()
	
	
	rospy.set_param("des_position_x", server_position.x)
	rospy.set_param("des_position_y", server_position.y)
	
	## I set the goal position as the one received from the server
	goal_x= rospy.get_param('des_position_x')
	goal_y= rospy.get_param('des_position_y')
	
	## Call the generic funtion to set the new target position
	set_target_position(goal_x, goal_y)
    
    

def follow_wall():
	
	resp = srv_client_wall_follower(True)
	

## To stop the robot I set my target goal in the position in wich the robot is
def stop_robot():
	
	move_goal = MoveBaseActionGoal()
	move_goal.goal.target_pose.header.frame_id="map"
	move_goal.goal.target_pose.pose.orientation.w=1

	move_goal.goal.target_pose.pose.position.x = actual_position.x
	move_goal.goal.target_pose.pose.position.y = actual_position.y
	pub.publish(move_goal)
	
	
	

def set_target_position(target_x, target_y):
	
	## Initialize a MoveActionGoal target to move my robot
	move_goal = MoveBaseActionGoal()
	move_goal.goal.target_pose.header.frame_id="map"
	move_goal.goal.target_pose.pose.orientation.w=1

	move_goal.goal.target_pose.pose.position.x = target_x
	move_goal.goal.target_pose.pose.position.y = target_y
	pub.publish(move_goal)
	
	print("\nLet's reach the position x: ", target_x, "y: ", target_y)
	
	response= srv_client_user_interface()
    
	

def distance():
	
	dist_x= actual_position.x-goal_x
	dist_y= actual_position.y-goal_y
	
	dist=math.sqrt(pow(dist_x, 2)+pow(dist_y, 2))
	
	print ("\nDistance to the target: ", dist)
	
	
	


def main():
	
    rospy.init_node('robot_user_interface')
    
    sub_odom=rospy.Subscriber("/odom", Odometry, positionCallback)
    sub_srv_positon=rospy.Service('/position', Empty, server_positionCallback)
    
   # rate = rospy.Rate(20)
   # while not rospy.is_shutdown():
   #     rate.sleep()
   
    srv_client_go_to_point_ = rospy.ServiceProxy(
        '/go_to_point_switch', SetBool)
    resp = srv_client_go_to_point(False)
    srv_client_wall_follower = rospy.ServiceProxy(
        '/wall_follower_switch', SetBool)
    srv_pos= rospy.ServiceProxy('/position', Server_second_assignment)
    srv_client_user_interface = rospy.ServiceProxy('/user_interface', Empty)
    
    
    while(-1):
		
		print("\nTarget to reach: x= ", goal_x, "y= ", goal_y)
		distance()
		
		print("Please give me a new command between the following\n")
		print("1- To move in a random position\n2- To move in a specific position\n3- Start to follow texternal walls\n4- Stop in last position")
		
		command=int(raw_input())
		
		if(command==1):
			move_randomly()
		
		elif(command==2):
			user_set_position()
		
		elif(command==3):
			follow_wall()
			
		elif(command==4):
			stop_robot()
			
		else:
			print("\nProbably you choose a command not allowed, please try again")
		
			
        
        

if __name__ == '__main__':
    main()
