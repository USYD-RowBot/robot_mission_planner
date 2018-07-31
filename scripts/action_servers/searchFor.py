#!/usr/bin/env python

import rospy
import smach
import smach_ros

from rowbot_mission_planner.msg import searchForAction, searchForGoal
from actionlib import *
from actionlib_msgs.msg import *


# Create the action server
class searchForServer:
    def __init__(self):
        self.server = SimpleActionServer('searchFor',
                searchForGoal,
                self.execute)
        self.server.start();

    def execute(self,msg):
        rospy.loginfo('Searching for: '+''.join(ms.targets))
        #if found(msg.target):
        if True:
            rospy.sleep(2);
            self.server.set_succeeded();
        #self.server.set_aborted();
        #self.server.set_preempted();