#! /usr/bin/env python

# import ros stuff
import rospy
from std_srvs.srv import *
from nav_msgs.msg import Odometry

# service callback

server_position_x=0
server_position_y=0

actual_position_x=0
actual_position_y=0


def positionCallback(msg):
    
    actual_position_x=msg->pose.pose.position.x
    actual_position_y=msg->pose.pose.position.y



def set_new_pos(req):
    print("Target reached! Please insert a new position")
    x = float(raw_input('x :'))
    y = float(raw_input('y :'))
    rospy.set_param("des_pos_x", x)
    rospy.set_param("des_pos_y", y)
    print("Thanks! Let's reach the next position")
    return []
    
    
    
    
def move_randomly():
	rospy.Subscriber("/position", Odometry, positionCallback)
	
	server_position_x=rec_pos.response.x
    server_position_y=rec_pos.response.y
	
	
	
	


def main():
    rospy.init_node('robot_user_interface')

    x = rospy.get_param("des_pos_x")
    y = rospy.get_param("des_pos_y")
    print("Hi! We are reaching the first position: x = " +
          str(x) + ", y = " + str(y))
    srv = rospy.Service('user_interface', Empty, set_new_pos)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        rate.sleep()
        
        
        
	while(-1)
	    //I give a general commands for the user interface
        print("Please give me a new command between the following\n")
        print("1- To move in a random position\n2- To move in a specific position\n
               3- Start following the external walls\n4- Stop in last position")
               
	    command=int(raw_input())
	    
	    switch(command):
			
			case(1):
				move_randomly();
				break
		
		    case(2):
				set_new_pos();
				break
				
			case(3):
				
				break
				
			case(4):
				
				break
				
			default:
				print("Probably you choose a command not allowed, please try again")
				break		
        

        


if __name__ == '__main__':
    main()
