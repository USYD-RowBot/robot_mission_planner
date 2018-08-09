import rospy
import smach
from copy import deepcopy
from rowbot_vision_msgs.msg import ObjectArray
# initialise a single listener for all derivative classes to use - saving listener initialisation calls

class searchFor(smach.State):
    def __init__(self,targets,timeout=None):
        smach.State.__init__(self, outcomes=['found', 'partial_found', 'timeout'], output_keys=['foundTargets'])
        self.findTargets=targets
        if not timeout is None:
            self.timeout=timeout
        else:
            self.timeout=-1;
        self.objectListener=rospy.Subscriber("objects",ObjectArray, updateInternal)
        self.storedObjects=[];
    def updateInternal(data):
        self.storedObjects=data;
    def execute(self,userdata):
        rospy.loginfo('Finding objects:' + self.findTargets)
        abort_condition=False
        while not self.timeout==0:
            rospy.sleep(2)
            tempTargets=deepcopy(self.findTargets)
            results=[];
            for found_obj in self.storedObjects:
                for target_obj in tempTargets:
                    if found_obj.best_guess==target_obj:
                        tempTargets.remove(target_obj);
                        results.append(found_obj)
                        pass
            if len(results)==len(self.findTargets):
                userdata.results=results
                break # exit the while loop once everything has been found
            if abort_condition:
                return 'aborted'
            self.timeout-=1;
        return 'started'
