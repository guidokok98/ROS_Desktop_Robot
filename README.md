# Installs
Gebruik Ubuntu 18.04.5 LTS

Voer de volgende commands uit: 
- sudo apt install python
		
installeer ROS Melodic -> volg de volgende pagina http://wiki.ros.org/melodic/Installation/Ubuntu
- sudo apt install ros-melodic-joint-state-publisher
- sudo apt install ros-melodic-joint-state-publisher-gui

- sudo apt-get git (github)
interface om github niet in terminal te gebruiken -> https://www.syntevo.com/downloads/smartgit/smartgit-20_1_4.deb
voeg de git toe op locatie catkin_ws/src
- source /opt/ros/melodic/setup.bash
- mkdir -p ~/catkin_ws/src
- cd ~/catkin_ws
- catkin_make
- cd ~/catkin_ws/src
- git clone https://github.com/guidokok98/ros_desktop_robot.git
- cd ~/catkin_ws 
- catkin_make
- sudo apt-get install ros-melodic-moveit

Eventueel:
- sudo apt install tree (typ in terminal tree en je ziet wat het doet)
- sudo apt-get install terminator (handige terminal om in meerdere windows ter gelijk te werken)



# Start commands
roslaunch ros_desktop_robot ros_desktop_robot.launch

#useful URDF links
http://wiki.ros.org/urdf/Tutorials/Building%20a%20Visual%20Robot%20Model%20with%20URDF%20from%20Scratch

#useful move_it links
https://www.theconstructsim.com/ros-movelt/
