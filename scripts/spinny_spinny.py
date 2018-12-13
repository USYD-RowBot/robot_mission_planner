#!/usr/bin/env python

import rospy
import smach
import smach_ros
import math

import baseFuncs.searchFor as sf
from baseFuncs.waitForStart import waitForStart
from baseFuncs.searchFor import searchFor
from baseFuncs.moveTo import moveTo
from baseFuncs.executor import executor
from smach_ros import SimpleActionState
# from rowbot_mission_planner.msg import searchForAction, searchForGoal, waitForStartAction
from geometry_msgs.msg import PoseStamped
import tf

if __name__ == '__main__':
    rospy.init_node('smach_spinnypsinny_state_machine')
    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['success', 'fail'])
    # Open the container
    with sm:
        # Add states to the container
        # waitForStart state
        #smach.StateMachine.add('waitForStart', waitForStart(), transitions={
        #                       'started': 'findGates', 'aborted': 'fail'})

        # Gate finding
        smach.StateMachine.add('findBuoy',
                               searchFor(
                                   targets=['white buoy']),
                               transitions={'found': 'plot_course', 'partial_found': 'fail', 'timeout': 'fail'},
                               remapping={"objects":"data"})

        def coursePlotter(data):
            # Extract IDs of start and end beacons
            items = []
            listener = tf.TransformListener()
            for i in data:
                # im assuming this is the relevant thing?
                listener.waitForTransform(
                    '/'+i.frame_id, '/base_link', rospy.Time(0), rospy.Duration(4.0))
                (trans, rot) = listener.lookupTransform(
                    '/'+i.frame_id, '/base_link', rospy.Time(0))
                dist = math.sqrt(trans[0] ** 2 + trans[1] ** 2)
                items.append((dist, i.best_guess, i.frame_id))
            # sort to give us closest items... unnecessary tbh
            #items = sorted(items, key=lambda i: i[0])
            i=items[0]
            (reltrans, rot) = listener.lookupTransform(
                i[2], '/base_link', rospy.Time(0))
            (maptrans, rot) = listener.lookupTransform(
                i[2], '/map', rospy.Time(0))
            #currentDist=math.sqrt(trans[0] ** 2 + trans[1] ** 2)
            currentDist=5
            currentAngle = math.atan2(reltrans[0],reltrans[1])
            plist=[]
            for i in range(1,16):
                mba = PoseStamped()
                mba.pose.position.x = -maptrans[0]+currentDist*math.cos(currentAngle+i*math.pi/8)
                mba.pose.position.y = -maptrans[1]+currentDist*math.sin(currentAngle+i*math.pi/8)
                mba.pose.position.z = 0.0
                # fix quarternion
                mba.pose.orientation.x = 0
                mba.pose.orientation.y = 0
                mba.pose.orientation.z = 0
                mba.pose.orientation.w = 1
                plist.append(mba)
            return plist
        smach.StateMachine.add('plot_course', executor(coursePlotter),transitions={'done': 'navigate_to_start', 'error': 'fail'},remapping={"result":"goal"})
        smach.StateMachine.add('navigate_to_start', moveTo(),transitions={'succeeded': 'success', 'preempted': 'fail', 'aborted': 'fail'})

    # Execute SMACH plan
    # Create and start the introspection server
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    # Execute the state machine
    outcome = sm.execute()

    # Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()
