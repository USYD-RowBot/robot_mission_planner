#!/usr/bin/env python

import rospy
import smach
import smach_ros

class wait_for_start(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['start','abort'])

    def execute(self,userdata):
        rospy.loginfo("Waiting for start.")
        rospy.sleep(2)
        if True:
            rospy.loginfo("Starting...")
            return 'start'
        else:
            rospy.loginfo("Mission aborted.")
            return 'abort'

class find_gates(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['found','not_found','fail'])

    def execute(self,userdata):
        rospy.loginfo("Finding entrance gates")
        rospy.sleep(2)
        if True:
            rospy.loginfo("Successfully found gates")
            return 'found'
        elif True:
            rospy.loginfo("Some gates could not be found within the time limit. Proceeding with caution.")
            return 'not_found'
        elif True:
            rospy.loginfo("Critical error!")
            return 'fail'

class navigate_to_start(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['fail','success'])
    def execute(sleep,userdata):
        rospy.loginfo("Executing navigate to start")
        rospy.sleep(5)
        if True: 
            rospy.loginfo("Successfully Navigated to start")
            return'success'
        else:
            return 'fail'
class navigate_to_end(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['fail','success'])
    def execute(sleep,userdata):
        rospy.loginfo("Executing navigate to end")
        rospy.sleep(5)
        if True: 
            rospy.loginfo("Successfully Navigated to End")
            return'success'
        else:
            return 'fail'


if __name__ == '__main__':
    rospy.init_node('smach_entrance_gates_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['success','fail'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('waitForStart', waitForStart(), 
                               transitions={'start':'find_gates', 'abort':'fail'})
        smach.StateMachine.add('find_gates', find_gates(), 
                               transitions={'start':'find_gates', 'abort':'fail'})
        smach.StateMachine.add('navigate_to_start', navigate_to_start(), 
                               transitions={'success':'navigate_to_end','fail':'fail'})
        smach.StateMachine.add('navigate_to_end',navigate_to_end(), transitions={'success':'success','fail':'fail'})

    # Execute SMACH plan
    outcome = sm.execute()
