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

machine=smach.StateMachine(outcomes=['success', 'fail'])

with machine:
    # Add states to the container
    # waitForStart state
    #smach.StateMachine.add('waitForStart', waitForStart(), transitions={
    #                       'started': 'findGates', 'aborted': 'fail'})

    # Gate finding
    smach.StateMachine.add('findGates',
                            searchFor(
                                targets=['red buoy', 'red buoy', 'green buoy', 'green buoy']),
                            transitions={'found': 'find_start', 'partial_found': 'fail', 'timeout': 'fail'},
                            remapping={"objects":"data"})
    def midpointStart(data):
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
        # sort to give us closest items.
        items = sorted(items, key=lambda i: i[0])
        firstRed = None
        firstGreen = None
        for i in items:
            if firstRed is None and i[1].find("red"):
                firstRed = i
            if firstGreen is None and i[1].find("green"):
                firstGreen = i
        (rtrans, rot) = listener.lookupTransform(
            firstRed[2], '/map', rospy.Time(0))
        (gtrans, rot) = listener.lookupTransform(
            firstGreen[2], '/map', rospy.Time(0))
        midpoint = (-(rtrans[0]+gtrans[0])/2, -(rtrans[1]+gtrans[1])/2)
        angle = math.atan2((rtrans[0]-gtrans[0]),
                            (rtrans[1]-gtrans[1]))+math.pi/4
        mba = PoseStamped()
        mba.pose.position.x = midpoint[0]
        mba.pose.position.y = midpoint[1]
        mba.pose.position.z = 0.0
        # fix quarternion
        mba.pose.orientation.x = 0
        mba.pose.orientation.y = 0
        mba.pose.orientation.z = 0
        mba.pose.orientation.w = angle
        print(mba)
        print(rtrans)
        print(gtrans)
        return mba  # my code has a degree yay
    smach.StateMachine.add('find_start', executor(midpointStart),transitions={'done': 'navigate_to_start', 'error': 'fail'},remapping={"result":"goal"})
    smach.StateMachine.add('navigate_to_start', moveTo(),transitions={'succeeded': 'find_end', 'preempted': 'fail', 'aborted': 'fail'})

    def midpointEnd(data):
        # Extract IDs of start and end beacons
        items = []
        listener = tf.TransformListener()
        for i in data:
            # im assuming this is the relevant thing?
            listener.waitForTransform(
                '/'+i.frame_id, '/map', rospy.Time(0), rospy.Duration(4.0))
            (trans, rot) = listener.lookupTransform(
                '/'+i.frame_id, '/map', rospy.Time(0))
            dist = math.sqrt(trans[0] ** 2 + trans[1] ** 2)
            items.append((dist, i.best_guess, i.frame_id))
        # sort to give us closest items.
        items = sorted(items, key=lambda i: i[0],reverse=True)
        firstRed = None
        firstGreen = None
        for i in items:
            if firstRed is None and i[1].find("red"):
                firstRed = i
            if firstGreen is None and i[1].find("green"):
                firstGreen = i
        (rtrans, rot) = listener.lookupTransform(
            firstRed[2], '/map', rospy.Time(0))
        (gtrans, rot) = listener.lookupTransform(
            firstGreen[2], '/map', rospy.Time(0))
        midpoint = (-(rtrans[0]+gtrans[0])/2, -(rtrans[1]+gtrans[1])/2)
        angle = math.atan2((rtrans[0]-gtrans[0]),
                            (rtrans[1]-gtrans[1]))+math.pi/4
        mba = PoseStamped()
        mba.pose.position.x = midpoint[0]
        mba.pose.position.y = midpoint[1]
        mba.pose.position.z = 0.0
        # fix quarternion
        mba.pose.orientation.x = 0
        mba.pose.orientation.y = 0
        mba.pose.orientation.z = 0
        mba.pose.orientation.w = angle
        print(mba)
        print(rtrans)
        print(gtrans)
        return mba  # my code has a degree yay
    smach.StateMachine.add('find_end', executor(midpointEnd),transitions={'done': 'navigate_to_end', 'error': 'fail'},remapping={"result":"goal"})
    smach.StateMachine.add('navigate_to_end', moveTo(),transitions={'succeeded': 'success', 'preempted': 'fail', 'aborted': 'fail'})

if __name__ == '__main__':
    rospy.init_node('smach_demonav_state_machine')
    # start introspection server
    # Create and start the introspection server
    if rospy.get_param("machineDebug",False)==True:
        sis = smach_ros.IntrospectionServer('server_name', machine, '/SM_ROOT')
        sis.start()
    # Execute the state machine
    outcome = machine.execute()
    # Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()
