#!/usr/bin/env python
# http://wiki.ros.org/actionlib#Python_SimpleActionServer
import rospy
import smach
import smach_ros
from action_servers.searchFor import searchFor
from rowbot_mission_planner.msg import searchForAction, searchForGoal



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

class chooseExit(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['choiceOK', 'choiceUnsure', 'criticalFail'])
   def execute(self,userdata):
         rospy.loginfo('Choosing exit gate...')
         rospy.sleep(2)
         if True:
             rospy.loginfo('Chose the exit buoy. Allg.')
             return 'choiceOK'
         if True:
             rospy.loginfo('Not sure which buoy to go through. Choosing a random one...')
             return 'choiceUnsure'
         if True:
             rospy.loginfo('No buoys could be found. what do .-.')
             return 'criticalFail'

class navigateThroughExit(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['navOK', 'navError', 'criticalFail'])
   def execute(self,userdata):
         rospy.loginfo('Heading through exit...')
         rospy.sleep(2)
         if True:
             rospy.loginfo('All done!')
             return 'navOK'
         if True:
             rospy.loginfo('Something went wrong but i think i am ok...')
             return 'navError'
         if True:
             rospy.loginfo('Nooo! So close!')
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
                                                       goal = waitForStartAction(smachName=thisName)),
                              transitions={'succeeded':'chooseEntry'})
        smach.StateMachine.add('findGates',
                              smach_ros.SimpleActionState('searchFor', searchForAction,
                                                       goal = searchForGoal(target=['gates'])), ### Or something.
                              transitions={'succeeded':'chooseEntry'})
        smach.StateMachine.add('chooseEntry', chooseEntry(), ## this state is reused for choosing exit
                              transitions={'entryFound': 'navEntry', 'exitFound': 'navExit', 'criticalFail': 'fail'})
        smach.StateMachine.add('navEntry',
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
        # smach.StateMachine.add('chooseExit', chooseExit(), #Superceded by chooseEntry
                              # transitions={'choiceOK': 'choiceOK', 'choiceUnsure': 'chooseBuoy', 'criticalFail': 'fail'})
        smach.StateMachine.add('navExit',
                              smach_ros.SimpleActionState('moveToPos', moveToPosAction,
                                                       goal_slots = ['tfName']),
                              transitions={'succeeded':'findBuoys'},
                              remapping={'tfName':'chooseEntry_tfref'})
    # Execute SMACH plan
    outcome = sm.execute()