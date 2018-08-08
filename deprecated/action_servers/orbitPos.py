#!/usr/bin/env python

import rospy
import smach
import smach_ros

from rowbot_mission_planner.msg import orbitPosAction, orbitPosGoal
from actionlib import *
from actionlib_msgs.msg import *


# Create the action server
class moveToPosServer:
    def __init__(self):
        self.server = SimpleActionServer('orbitPos',
                orbitPosGoal,
                self.execute)
        self.server.start();

    def execute(self,msg):
        #if found(msg.target):
        rospy.loginfo('Orbiting tf: '+msg.tfName)
        if True:
            rospy.sleep(2);
            self.server.set_succeeded();
        #self.server.set_aborted();
        #self.server.set_preempted();