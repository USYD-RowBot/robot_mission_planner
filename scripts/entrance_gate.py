#!/usr/bin/env python
import rospy
import smach
import smach_ros

class waitForStart(smach.State):
   def __init__(self):
	 smach.State.__init__(self, outcomes=['abort'])
   def execute(self,userdata):
	     rospy.loginfo('Waiting for start...')
	     rospy.sleep(2)
	    if True:
	    	rospy.loginfo('Start aborted by controller.')
	    	return 'abort'


 if __name__ == '__main__':
    rospy.init_node(entrance_gate)
    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['success', 'fail'])
    # Open the container
    with sm:
    # Add states to the container
        smach.StateMachine.add('waitForStart', waitForStart(), 
                              transitions={'abort': 'fail'})
    # Execute SMACH plan
    outcome = sm.execute()
