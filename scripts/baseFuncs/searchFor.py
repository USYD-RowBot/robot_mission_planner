import rospy
import smach
from copy import deepcopy
from rowbot_vision.msg import ObjectArray
# initialise a single listener for all derivative classes to use - saving listener initialisation calls

class searchFor(smach.State):

    def updateInternal(data):
        self.storedObjects=data;

    def __init__(self,targets,timeout=None):
        rospy.loginfo('init Finding objects:' + str(targets))
        smach.State.__init__(self, outcomes=['found', 'partial_found', 'timeout'], output_keys=['foundTargets'])
        self.findTargets=targets
        if not timeout is None:
            self.timeout=timeout
        else:
            self.timeout=-1;
        self.objectListener=rospy.Subscriber("objects",ObjectArray, self.updateInternal)
        self.storedObjects=[];

    def execute(self,userdata):
        rospy.loginfo('Finding objects:' + str(self.findTargets))
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
                # return 'started' ## STRICTLY FOR DEBUGGING ONLY - Replace with above line for production
            self.timeout-=1;
        return 'started'
