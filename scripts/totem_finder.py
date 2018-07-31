#!/usr/bin/env python
import rospy
import smach
import smach_ros

class waitForStart(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['abort', 'start'])
   def execute(self,userdata):
         rospy.loginfo('Waiting for start...')
         rospy.sleep(2)
         if True:
             rospy.loginfo('Start aborted by controller.')
             return 'abort'
         if True:
             rospy.loginfo('Start signal recieved.')
             return 'start'

class getSequence(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['sequenceOK', 'sequenceMissing', 'criticalFail'])
   def execute(self,userdata):
         rospy.loginfo('Gathering sequence info...')
         rospy.sleep(2)
         if True:
             rospy.loginfo('Sequence detected.')
             return 'sequenceOK'
         if True:
             rospy.loginfo('Some sequence elements missing. Moving randomly...')
             return 'sequenceMissing'
         if True:
             rospy.loginfo('Something went badly wrong 3:')
             return 'criticalFail'

class findTotems(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['totemsFound', 'totemsFoundEnough', 'criticalFail'])
   def execute(self,userdata):
         rospy.loginfo('Identifying totems...')
         rospy.sleep(2)
         if True:
             rospy.loginfo('Totems found!')
             return 'totemsFound'
         if True:
             rospy.loginfo('Found enough totems to go ahead. Proceeding with caution')
             return 'totemsFoundEnough'
         if True:
             rospy.loginfo('Something went badly wrong 3:')
             return 'criticalFail'

class sequenceMoves(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['sequenceOK', 'criticalFail'])
   def execute(self,userdata):
         rospy.loginfo('Identifying sequence and planning moves...')
         rospy.sleep(2)
         if True:
             rospy.loginfo('Sequence planning ok.')
             return 'sequenceOK'
         if True:
             rospy.loginfo('Something went badly wrong 3:')
             return 'criticalFail'

class performSequence(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['sequenceExecutionOK', 'minorHindrance', 'criticalFail'])
   def execute(self,userdata):
         rospy.loginfo('Performing required sequence...')
         rospy.sleep(2)
         if True:
             rospy.loginfo('Sequence navigation complete. ')
             return 'sequenceExecutionOK'
         if True:
             rospy.loginfo('Something went wrong. Going to exit...')
             return 'minorHindrance'
         if True:
             rospy.loginfo('Something went badly wrong 3:')
             return 'criticalFail'

class gotoExit(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['arrivedAtExit', 'criticalFail'])
   def execute(self,userdata):
         rospy.loginfo('Going to exit..')
         rospy.sleep(2)
         if True:
             rospy.loginfo('Got to exit. Hooray!')
             return 'arrivedAtExit'
         if True:
             rospy.loginfo('Something went badly wrong 3:')
             return 'criticalFail'


if __name__ == '__main__':
    rospy.init_node(totem_finder)
    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['success', 'fail'])
    # Open the container
    with sm:
    # Add states to the container
        smach.StateMachine.add('waitForStart', waitForStart(), 
                              transitions={'abort': 'fail', 'start': 'getSequence'})
        smach.StateMachine.add('getSequence', getSequence(), 
                              transitions={'sequenceOK': 'findTotems', 'sequenceMissing': 'findTotems', 'criticalFail': 'fail'})
        smach.StateMachine.add('findTotems', findTotems(), 
                              transitions={'totemsFound': 'sequenceMoves', 'totemsFoundEnough': 'sequenceMoves', 'criticalFail': 'fail'})
        smach.StateMachine.add('sequenceMoves', sequenceMoves(), 
                              transitions={'sequenceOK': 'performSequence', 'criticalFail': 'fail'})
        smach.StateMachine.add('performSequence', performSequence(), 
                              transitions={'sequenceExecutionOK': 'gotoExit', 'minorHindrance': 'gotoExit', 'criticalFail': 'fail'})
        smach.StateMachine.add('gotoExit', gotoExit(), 
                              transitions={'arrivedAtExit': 'success', 'criticalFail': 'fail'})
    # Execute SMACH plan
    outcome = sm.execute()
