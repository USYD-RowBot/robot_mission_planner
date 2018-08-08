import rospy
import smach
class waitForStart(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['started', 'aborted')
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
