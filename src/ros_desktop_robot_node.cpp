// Node file to create object and initialising the ROS node
#include "ros_desktop_robot.hpp" 

int main(int argc, char** argv)
{
    /* initialising the ROS node creating node handle
    for regestring it to the master and then private node handle to
    handle the parameters */
    ros::init(argc, argv, "ros_desktop_robot"); 
    ros::NodeHandle nh;
    ros::NodeHandle pnh("~"); 
    
    RosDesktopRobot node(nh,pnh); // Creating the object

    ros::Rate rate(1.0); // Defing the looping rate

    /* Looking for any interupt else it will continue looping */
    while (ros::ok())
    {   
        node.runOnce();
        ros::spinOnce();
        rate.sleep();
    }
    return 0;
}