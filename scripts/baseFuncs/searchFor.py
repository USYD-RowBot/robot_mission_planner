import rospy
import smach

# initialise a single listener for all derivative classes to use - saving listener initialisation calls

class searchFor(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['found', 'timeout')
     self.times=0;
   def execute(self,userdata):
         rospy.loginfo('Waiting for start...')
         started=True;
         abort_condition=True; # to facilitate testing
         while not started:
            rospy.sleep(2)
            if abort_condition:
                return 'aborted'
        return 'started'
