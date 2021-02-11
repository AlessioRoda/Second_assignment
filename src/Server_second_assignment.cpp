#include "ros/ros.h"
#include "second_assignment/Server_second_assignment.h"
#include <ctime>


bool myrandom (second_assignment::Server_second_assignment::Request &req, second_assignment::Server_second_assignment::Response &res){
	
    float x_values[]={-4, -4, -4, 5, 5, 5};
	float y_values[]={-3, 2, 7, -7, -3, 1};
	
	srand((unsigned) time(0));
	
	int index=rand()%6;  
	
	    res.x = x_values[index];
        res.y = y_values[index];
        ROS_INFO("\nServer position: x[%f] y[%f]", res.x, res.y);
    return true;
}



int main(int argc, char **argv)
{
   ros::init(argc, argv, "server_second_assignment");
   ros::NodeHandle n;
   ros::ServiceServer service= n.advertiseService("/position", myrandom);
   ROS_INFO("Server activated \n");
   ros::spin();

   return 0;
}
