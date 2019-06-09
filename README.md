# System Integration Project
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

This is the final project for the Udacity Self-Driving Car Engineer Nanodegree.  In this project, I created several ROS nodes to implement the core functionality of an autonomous vehicle.  For more information about the project, see the project introduction [here](https://classroom.udacity.com/nanodegrees/nd013/parts/30260907-68c1-4f24-b793-89c0c2a0ad32/modules/702b3c5a-b896-4cca-8a64-dfe0daf09449/lessons/e43b2e6d-6def-4d3a-b332-7a58b847bfa4/concepts/1f6c617c-c8f2-4b44-9906-d192ba7ff924).

[//]: # (Image References)
[image1]: ./imgs/carla_architecture.png
[image2]: ./imgs/final-project-ros-graph-v2.jpg
[image3]: ./imgs/system_architecture.png
[video1]: https://www.youtube.com/watch?time_continue=124&v=PzIRniXv0z0

![][video1]

## Setup

Please use **one** of the two installation options, either native **or** docker installation.
Please use **one** of the two installation options, either native **or** docker installation.

### Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros)
  * Use this option to install the SDK on a workstation that already has ROS installed: [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)
* Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases).

### Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```

### Port Forwarding
To set up port forwarding, please refer to the [instructions from term 2](https://classroom.udacity.com/nanodegrees/nd013/parts/40f38239-66b6-46ec-ae68-03afd8a601c8/modules/0949fca6-b379-42af-a919-ee50aa304e6a/lessons/f758c44c-5e40-4e01-93b5-1a82aa4e044f/concepts/16cf4a78-4fc7-49e1-8621-3450ca938b77)

### Usage

1. Clone the project repository
```bash
git clone https://github.com/udacity/CarND-Capstone.git
```

2. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```
3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
4. Run the simulator

### Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```
3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND-Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images

## Project Overview

### System Architecture Diagram
For this project, I wrote ROS nodes to implement the core functionality of the autonomous vehicle system, including traffic light detection, control, and waypoint following! I have done this project individually and tested my code using a simulator.
![][image1]


The following is the system architecture diagram showing the ROS nodes and topics used in the project. The ROS nodes and topics shown in the diagram are described briefly in the Code Structure section below.

#### Sensors
Includes all measurement devices such as **cameras**, **lidar**, **GPS**, **radar**, and **IMU** is used to identify and map the surrounding objects and location including 
#### Perception
Abstracts sensor inputs into object **detection** and **localization**
##### Detection
* Includes software solution to detect other vehicles, pedestrians, traffic lights, obstacles
##### Localization
To idetfy where the car is located in the map with an accuracy of 10cm or less
#### Planning
Based on localization, destination, and obstacles, it generates the Path for the car. 
##### Prediction
The prediction component estimates other cars and people actions and trajectory in the future. 
##### Behavioral Planning
High-level behavior of the vehicle at any point in time such as stopping a traffic light or intersection, changing lanes, accelerating, or making a left turn onto a new street are all maneuvers that may be issued by this component.
##### Trajectory Planning
Based on the high-level behavior, the trajectory planning component determines the optimized trajectory to achieve this behavior.
### Control
The low-level component that ensures car follows the chosen trajectory and adjust the control inputs for the smooth operation of the vehicle. 


### ROS Architecture

The ROS Architecture consists of different nodes that are in communication via ROS messages. The nodes and their communication with each other are explained in details in project descriptions[here](https://classroom.udacity.com/nanodegrees/nd013/parts/30260907-68c1-4f24-b793-89c0c2a0ad32/modules/702b3c5a-b896-4cca-8a64-dfe0daf09449/lessons/e43b2e6d-6def-4d3a-b332-7a58b847bfa4/concepts/455f33f0-2c2d-489d-9ab2-201698fbf21a). 

The central node is the styx_server that links the simulator and ROS by providing information about the car's state such as its position, velocity, and the front camera and receiving control input such as steering angle, braking, and throttle. 

The images are processed with the traffic light classifier by a trained neural network in order to detect traffic lights. The perception state of a potential upcoming traffic light is passed to the traffic light detector as well as the car's current pose and a set of base waypoints coming from the waypoint loader. With this frequently incoming information, the traffic light detector is able to publish a waypoint close to the next traffic light where the car should stop in case the light is red. 

With the subscriber information of the traffic light detector and the subscriptions to base waypoints, the waypoint updater node is able to plan acceleration/deceleration and publish it to the waypoint follower node. This node publishes to the DBW (Drive by wire) node that satisfies the task of steering the car autonomously. It also takes as input the car's current velocity (coming directly from the car/simulator) and outputs steering, braking, and throttle commands. 

### Node Structures

![][image1]

Ros nodes structures are shown in this image. The main nodes that we update in this projects are the waypoint updater(waypoint_updater.py), the traffic light detector (tl_detector.py) and the drive by wire node (dbw_node.py). 

#### Waypoint Updater
The waypoint updater node specifies the required waypoints the car follows. The node is structured into different parts: In the initialization of the node, it defines some constants that including the number of waypoints and rate of the publications. The most important function is the decelerate_waypoints-function which incorporates a square-root shaped deceleration at stop line location in case of red traffic lights. 

#### Traffic Light Detection
The purpose of the traffic light detector is to receive the image from Car Camera and detect the traffic light. This node subscribes to the current position base waypoints, the traffic light array with the ground-truth coordinates of the traffic lights, along with the identified color of the traffic light. The color of the traffic light is the output of the traffic light classifier, a trained neural network. 

#### Drive-By-Wire (DBW) Node
The third node written by us is the dbw_node which is responsible for controlling the car. It subscribes to a twist controller which outputs throttle, brake and steering values with the help of a PID-controller and Lowpass filter. The dbw node directly publishes throttle, brake and steering commands for the car/simulator, in case dbw_enabled is set to true.

### Neural Network Design

#### Model
The traffic light classification model is based on the pre-trained on the COCO dataset model "rfcn_resnet101_coco_2018_01_28" from [Tensorflow detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md). Using the [Tensorflow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection), the simulator data model and real data model were trained. 

The models are available in the `ros/src/tl_detector/light_classification/fine_tuned_model` directory or [here](https://drive.google.com/drive/folders/1uXxvwPW907UJXw-0wscE8hEZ7ySvEUYb). 

#### Dataset
Step-by-step [Tensorflow Object Detection API tutorial](https://medium.com/@WuStangDan/step-by-step-tensorflow-object-detection-api-tutorial-part-1-selecting-a-model-a02b6aabe39e) was a good great source of using the Tensorflow object detection API for traffic light classification.

The simulator dataset was from [here](https://github.com/masih84/CarND-Capstone/tree/master/Object_detection/training_data). Traffic light boxes are labeled [here](https://github.com/masih84/CarND-Capstone/blob/master/Object_detection/training_data/labeld_data.csv) using [Developing Traffic Light Labels .ipynb](https://github.com/masih84/CarND-Capstone/blob/master/Object_detection/Developing%20Traffic%20Light%20Labels%20.ipynb) . Then, they converted to data.tfrecords [here](https://github.com/masih84/CarND-Capstone/tree/master/Object_detection/data) by [GenerateLabelModel2](https://github.com/masih84/CarND-Capstone/blob/master/Object_detection/GenerateLabelModel2.ipynb).


#### Classification
The classification output has four categories: Red, Green, Yellow and off. To simplify, the final output will be Red, yellow, Green or Unknown. The logic is modified such that if the traffic light is unknown, it assumes the previous state is correct. Also, both yellow and red color would lead to stopping the car at the stop line.


#### Examples of Simulator Testing Results:

![sim_red](https://github.com/masih84/CarND-Capstone/blob/master/Object_detection/training_data/processed2/image1.jpg)
![sim_green](https://github.com/masih84/CarND-Capstone/blob/master/Object_detection/training_data/processed2/image2.jpg)
![sim-yellow](https://github.com/masih84/CarND-Capstone/blob/master/Object_detection/training_data/processed2/image3.jpg)
![sim_none](https://github.com/masih84/CarND-Capstone/blob/master/Object_detection/training_data/processed2/image4.jpg)

## Results

I started by following the walkthrough videos and wrote the program to work. Then, I spent most of my time on making object detection working and installing all required environments. One of the hardest tasks for this project was getting the environment setup. 

Also running the Ros on Virtual machine with no GPU support made the object detection very slow. Also, running the simulation in the Windows was becoming very slow when turning on the Camera. I saw some suggestion such as processing image every 10 cycles and only near traffic lights. These suggestions have improved the speed but still, it was far from perfect.

Overall, this was the most challenging project in this program, and I learned a lot but finishing this. Unfortunately, I could not do this project as a team since I was busy with my day job and could spend time working the project on weekends. However, doing all parts by myself give the opportunity of understanding the details in depth.  


