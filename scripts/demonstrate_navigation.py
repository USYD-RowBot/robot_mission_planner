#!/usr/bin/env python
from states import waitForStart
from states import searchFor
import rospy
import smach
import smach_ros
from smach_ros import SimpleActionState


class nav_controller(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success','fail'])

    def execute(self,userdata):
        rospy.loginfo("Executing find buoys")
        rospy.sleep(2)
        if True:
            rospy.loginfo("Successfully found Buoys")
            return 'found'
        else:
            return 'not_found'
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
    rospy.init_node('smach_example_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['success','fail'])

    # Open the container
    with sm:
        # Add states to the container
        # waitForStart state
        smach.StateMachine.add('waitForStart', waitForStart(), 
                               transitions={'start':'find_buoys', 'abort':'fail'})
                               
                               
        # SearchFor state which finds the gate buoys
        def search_goal_cb(userdata, goal):
            search_goal = {};
            search_goal.target = 'gateBuoys'
            return search_goal
        smach.StateMachine.add('find_buoys',
                                SimpleActionState('',searchFor,search_goal_cb,input_keys=['target'],remapping='derp')
                    )
        
        smach.StateMachine.add('find_buoys', find_buoys(), 
                               transitions={'found':'navigate_to_start', 'not_found':'fail'})
        smach.StateMachine.add('navigate_to_start', navigate_to_start(), 
                               transitions={'success':'navigate_to_end','fail':'fail'})
        smach.StateMachine.add('navigate_to_end',navigate_to_end(), transitions={'success':'success','fail':'fail'})

    # Execute SMACH plan
    outcome = sm.execute()
