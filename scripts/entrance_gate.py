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

class findGates(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['gatesFound', 'gateTimeout', 'criticalFail'])
   def execute(self,userdata):
         rospy.loginfo('Finding Gates...')
         rospy.sleep(2)
         if True:
             rospy.loginfo('Found Gates!')
             return 'gatesFound'
         if True:
             rospy.loginfo('Not all gates could be found in allocated time period. Proceed with caution!')
             return 'gateTimeout'
         if True:
             rospy.loginfo('No gates could be found. Critical error! Aborting...')
             return 'criticalFail'

class chooseEntry(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['entryFound', 'entryRandomGuess', 'criticalFail'])
   def execute(self,userdata):
         rospy.loginfo('Choosing entry gate...')
         rospy.sleep(2)
         if True:
             rospy.loginfo('Chosen entry gate!')
             return 'entryFound'
         if True:
             rospy.loginfo('Not sure which gate to go through; making random guess :/')
             return 'entryRandomGuess'
         if True:
             rospy.loginfo('Not sure which gate to go through: aborting - better safe than sorry!')
             return 'criticalFail'

class navEntry(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['gatePassthroughOK', 'minorHindrance', 'criticalFail'])
   def execute(self,userdata):
         rospy.loginfo('Navigating to entry...')
         rospy.sleep(2)
         if True:
             rospy.loginfo('Passed through entry gate!')
             return 'gatePassthroughOK'
         if True:
             rospy.loginfo('Something went wrong, but we are still alive... Moving on.')
             return 'minorHindrance'
         if True:
             rospy.loginfo('Something went pretty badly wrong. hlep pls')
             return 'criticalFail'

class findBuoys(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['2buoysFound', '1buoyFound', 'criticalFail'])
   def execute(self,userdata):
         rospy.loginfo('Identifying buoys...')
         rospy.sleep(2)
         if True:
             rospy.loginfo('Got both buoys.')
             return '2buoysFound'
         if True:
             rospy.loginfo('Got one buoy. Lets just use that one :3')
             return '1buoyFound'
         if True:
             rospy.loginfo('No buoys could be found. what do .-.')
             return 'criticalFail'

class chooseBuoy(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['buoyFoundConfident', 'buoyNoLock', 'criticalFail'])
   def execute(self,userdata):
         rospy.loginfo('Choosing buoy...')
         rospy.sleep(2)
         if True:
             rospy.loginfo('Got a confident lock on the appropriate buoy.')
             return 'buoyFoundConfident'
         if True:
             rospy.loginfo('Not sure which buoy to go around. Just choosing a random one')
             return 'buoyNoLock'
         if True:
             rospy.loginfo('Aliens must have abducted the beacons or sth 3: what do .-.')
             return 'criticalFail'

class navCircleBuoy(smach.State):
   def __init__(self):
     smach.State.__init__(self, outcomes=['orbitDone', 'whereRWe', 'criticalFail'])
   def execute(self,userdata):
         rospy.loginfo('Orbiting buoys.')
         rospy.sleep(2)
         if True:
             rospy.loginfo('Orbit done.')
             return 'orbitDone'
         if True:
             rospy.loginfo('wh-- what happened? ah well im alive lets keep going')
             return 'whereRWe'
         if True:
             rospy.loginfo('X-X')
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


if __name__ == '__main__':
    rospy.init_node(entrance_gate)
    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['success', 'fail'])
    # Open the container
    with sm:
    # Add states to the container
        smach.StateMachine.add('waitForStart', waitForStart(), 
                              transitions={'abort': 'fail', 'start': 'findGates'})
        smach.StateMachine.add('findGates', findGates(), 
                              transitions={'gatesFound': 'chooseEntry', 'gateTimeout': 'findGates', 'criticalFail': 'fail'})
        smach.StateMachine.add('chooseEntry', chooseEntry(), 
                              transitions={'entryFound': 'navEntry', 'entryRandomGuess': 'navEntry', 'criticalFail': 'fail'})
        smach.StateMachine.add('navEntry', navEntry(), 
                              transitions={'gatePassthroughOK': 'findBuoys', 'minorHindrance': 'findBuoys', 'criticalFail': 'fail'})
        smach.StateMachine.add('findBuoys', findBuoys(), 
                              transitions={'2buoysFound': 'chooseBuoy', '1buoyFound': 'chooseBuoy', 'criticalFail': 'fail'})
        smach.StateMachine.add('chooseBuoy', chooseBuoy(), 
                              transitions={'buoyFoundConfident': 'navCircleBuoy', 'buoyNoLock': 'navCircleBuoy', 'criticalFail': 'fail'})
        smach.StateMachine.add('navCircleBuoy', navCircleBuoy(), 
                              transitions={'orbitDone': 'chooseExit', 'whereRWe': 'chooseExit', 'criticalFail': 'fail'})
        smach.StateMachine.add('chooseExit', chooseExit(), 
                              transitions={'choiceOK': 'choiceOK', 'choiceUnsure': 'chooseBuoy', 'criticalFail': 'fail'})
        smach.StateMachine.add('navigateThroughExit', navigateThroughExit(), 
                              transitions={'navOK': 'success', 'navError': 'success', 'criticalFail': 'fail'})
    # Execute SMACH plan
    outcome = sm.execute()
