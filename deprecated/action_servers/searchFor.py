#!/usr/bin/env python

import rospy
import smach
import smach_ros

from rowbot_mission_planner.msg import searchForAction, searchForGoal
from rowbot_vision.msg import ObjectArray
from actionlib import *
from actionlib_msgs.msg import *


# Create the action server
class searchForServer:
    def __init__(self):
        self.server = SimpleActionServer('searchFor',
                searchForGoal,
                self.execute)
        self.server.start();
        self.objectListener=rospy.Subscriber("objects",ObjectArray, callback)
        self.storedObjects=[];
        
    def updateInternal(data):
        self.storedObjects=data;
    
    def execute(self,msg): # Single target only.
        rospy.loginfo('Searching for: '+''.join(msg.target))
        tt=msg.timeout;
        while tt>0:
            tt-=1;
            for i in self.storedObjects:
                if msg.target==i['best_guess']:
                    self._result.tfframe=i.frame_id;
                    self.server.set_succeeded();
                    return;
            else:
                rospy.sleep(2)
        