#!/usr/bin/env python

import rospy
import smach
import smach_ros

from rowbot_mission_planner.msg import waitForStartAction, waitForStartGoal
from actionlib import *
from actionlib_msgs.msg import *


# Create the action server
class waitForStartServer:
    def __init__(self):
        self.server = SimpleActionServer('waitForStart',
                waitForStartGoal,
                self.execute)
        self.server.start();

    def execute(self,msg):
        #if found(msg.target):
        rospy.loginfo(msg.smachName+' is waiting for start.')
        if True:
            rospy.sleep(2);
            self.server.set_succeeded();
        #self.server.set_aborted();
        #self.server.set_preempted();