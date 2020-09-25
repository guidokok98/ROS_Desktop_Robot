// Declaration file 

#pragma once //designed to include the current source file only once in a single compilation.
#ifndef ROS_DESKTOP_ROBOT //usd for conditional compiling.
#define ROS_DESKTOP_ROBOT
#include <ros/ros.h> // including the ros header file

/* defining the class */
class RosDesktopRobot
{
    public:
        RosDesktopRobot(ros::NodeHandle &nh, ros::NodeHandle &pnh); //constructor method
        ~RosDesktopRobot(); // distructor method
        void runOnce(); // runOnce method to control the flow of program
    private:
        ros::NodeHandle nh_; // Defining the ros NodeHandle variable for registrating the same with the master
};
#endif  