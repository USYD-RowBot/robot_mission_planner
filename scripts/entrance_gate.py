#!/usr/bin/env python
# http://wiki.ros.org/actionlib#Python_SimpleActionServer
import rospy
import smach
import smach_ros
from action_servers.searchFor import searchFor
from action_servers.moveToPos import moveToPos
from smach_ros import SimpleActionState
from action_servers.waitForStart import waitForStart
from rowbot_mission_planner.msg import searchForAction, searchForGoal
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


class chooseEntry(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['entryFound', 'entryRandomGuess', 'criticalFail'],output_keys=['chooseEntry_tfref'])
     self.times=0;
   def execute(self,userdata):
         rospy.loginfo('Choosing entry gate using sonar data.')
         rospy.sleep(2)
         userdata.chooseEntry_tfref="tf_reference_string"; ##  to edit - get from actual sensor data
         if self.times==0:
             rospy.loginfo('Chosen entry gate!')
             self.times++;
             return 'entryFound'
         elif self.times==1:
             rospy.loginfo('Chosen exit gate!')
             return 'exitFound'
         if True:
             rospy.loginfo('Not sure which gate to go through: aborting - better safe than sorry!')
             return 'criticalFail'


class chooseBuoy(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['buoyFoundConfident', 'buoyNoLock', 'criticalFail'],output_keys=['chooseBuoy_tfref'])
   def execute(self,userdata):
         rospy.loginfo('Choosing buoy...')
         rospy.sleep(2)
         if True:
             userdata.chooseBuoy_tfref="tf_reference_string"; ##  to edit - get from actual sensor data
             rospy.loginfo('Got a confident lock on the appropriate buoy.')
             return 'buoyFoundConfident'
         if True:
             rospy.loginfo('Not sure which buoy to go around. Just choosing a random one')
             return 'buoyNoLock'
         if True:
             rospy.loginfo('Aliens must have abducted the beacons or sth 3: what do .-.')
             return 'criticalFail'

thisName='entrance_gate';
if __name__ == '__main__':
    rospy.init_node(thisName)
    # Start required actionservers
    searchForServer=searchFor();
    
    
    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['success', 'fail'])
    # Open the container
    with sm:
    # Add states to the container
        smach.StateMachine.add('waitForStart',
                              smach_ros.SimpleActionState('waitForStart', waitForStartAction,
                                                       goal = waitForStartGoal(smachName=thisName)),
                              transitions={'succeeded':'chooseEntry'})
        smach.StateMachine.add('findGates',
                              smach_ros.SimpleActionState('searchFor', searchForAction, goal = searchForGoal(target=['gates'])), ### Or something.
                              transitions={'succeeded':'moveToStart'})
        smach.StateMachine.add('moveToStart',
                              smach_ros.SimpleActionState('move_base', MoveBaseAction, goal_cb=startMidpoint),
                              transitions={'succeeded':'moveToEnd'}
        )
        smach.StateMachine.add('moveToEnd',
                              smach_ros.SimpleActionState('moveToPos', moveToPosAction,
                                                       goal_slots = ['tfName']), ### Or something.
                              transitions={'succeeded':'findBuoys'},
                              remapping={'tfName':'chooseEntry_tfref'})
        smach.StateMachine.add('findBuoys',
                              smach_ros.SimpleActionState('searchFor', searchForAction,
                                                            goal = searchForGoal(target=['lightBuoy','markerBuoy'])), ### Or something.
                              transitions={'succeeded':'chooseBuoy'}))
        smach.StateMachine.add('chooseBuoy', chooseBuoy(), 
                              transitions={'buoyFoundConfident': 'navCircleBuoy', 'buoyNoLock': 'navCircleBuoy', 'criticalFail': 'fail'})
        def navCircleBuoy_goal_cb(userdata, goal):
            orbiter_goal = orbitPosGoal(radius=20,spinRadians=3.141); # should probably pick midpoint distance between buoys instead of a constant.
            orbiter_goal.tfName = userdata.chooseBuoy_tfref
            return gripper_goal
        smach.StateMachine.add('navCircleBuoy',
                              smach_ros.SimpleActionState('orbitPos', orbitPosAction,
                                                       goal_cb=navCircleBuoy_goal_cb,
                                                       input_keys=['chooseBuoy_tfref']),
                              transitions={'succeeded':'findGates'}, ## go back to find gates again.
                              )
        smach.StateMachine.add('navExit',
                              smach_ros.SimpleActionState('moveToPos', moveToPosAction,
                                                       goal_slots = ['tfName']),
                              transitions={'succeeded':'findBuoys'},
                              remapping={'tfName':'chooseEntry_tfref'})
    # Execute SMACH plan
    outcome = sm.execute()