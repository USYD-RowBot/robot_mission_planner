#!/usr/bin/env python

import rospy
import smach
import smach_ros
import math

from baseFuncs import waitForStart
from baseFuncs import searchFor
from smach_ros import SimpleActionState
from rowbot_mission_planner.msg import searchForAction, searchForGoal, waitForStartAction
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import tf

if __name__ == '__main__':
    rospy.init_node('smach_example_state_machine')
    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['success','fail'])

    # Open the container
    with sm:
        # Add states to the container
        # waitForStart state
        smach.StateMachine.add('waitForStart',waitForStart(),transitions={'started':'navigate_to_start','aborted':'fail'});

        #Gate finding
        smach.StateMachine.add('findGates',searchFor(targets=['*-navbuoy]),
                              transitions={'found':'navigate_to_start','timeout':'fail'});
        def midpointStart(userdata, goal):
            # Extract IDs of start and end beacons
            items=[];
            listener = tf.TransformListener()
            for i in userdata.objects:
                (trans,rot) = listener.lookupTransform(i.frame_id, '/pose', rospy.Time(0)) # im assuming this is the relevant thing?
                dist=math.sqrt(trans[0] ** 2 + trans[1] ** 2)
                items.append((dist,i.best_guess,i.frame_id))
            items=sorted(items, key=lambda i: i[0]); # sort to give us closest items.
            firstRed=None;
            firstGreen=None;
            for i in items:
                if firstRed is None and i[1].find("red-"):
                    firstRed=i;
                if firstGreen is None and i[1].find("green-"):
                    firstGreen=i;
            (rtrans,rot) = listener.lookupTransform(firstRed[2], '/map', rospy.Time(0))
            (gtrans,rot) = listener.lookupTransform(firstGreen[2], '/map', rospy.Time(0))
            midpoint=((rtrans[0]+gtrans[0])/2,(rtrans[1]+gtrans[1])/2)
            angle=math.atan2((rtrans[1]-gtrans[0]),(rtrans[1]-gtrans[1]))+math.pi/4;
            mba = MoveBaseGoal()
            mba.target_pose.header.frame_id = 'map'
            mba.target_pose.pose.position.x = position[0]
            mba.target_pose.pose.position.y = position[1]
            mba.target_pose.pose.position.z = 0.0
            mba.target_pose.pose.orientation.x = 0
            mba.target_pose.pose.orientation.y = 0
            mba.target_pose.pose.orientation.z = 0
            mba.target_pose.pose.orientation.w = angle;
            return mba; # my code has a degree yay

        smach.StateMachine.add('navigate_to_start', smach_ros.SimpleActionState(
                                                'move_base',
                                                MoveBaseAction,
                                                goal_cb = midpointStart, input_keys=['objects']), ### Or something.
                               transitions={'succeeded':'navigate_to_end','preempted':'fail','aborted':'fail'})

        def midpointEnd(userdata, goal):
        # Extract IDs of start and end beacons
            items=[];
            listener = tf.TransformListener()
            for i in userdata.objects:
                (trans,rot) = listener.lookupTransform(i.frame_id, '/pose', rospy.Time(0)) # im assuming this is the relevant thing?
                dist=math.sqrt(trans[0] ** 2 + trans[1] ** 2)
                items.append((dist,i.best_guess,i.frame_id))
            items=sorted(items, key=lambda i: i[0], reverse=True); # sort to give us closest items.
            firstRed=None;
            firstGreen=None;
            for i in items:
                if firstRed is None and i[1].find("red-"):
                    firstRed=i;
                if firstGreen is None and i[1].find("green-"):
                    firstGreen=i;
            (rtrans,rot) = listener.lookupTransform(firstRed[2], '/map', rospy.Time(0))
            (gtrans,rot) = listener.lookupTransform(firstGreen[2], '/map', rospy.Time(0))
            midpoint=((rtrans[0]+gtrans[0])/2,(rtrans[1]+gtrans[1])/2)
            angle=math.atan2((rtrans[1]-gtrans[0]),(rtrans[1]-gtrans[1]))+math.pi/4;
            mba = MoveBaseGoal()
            mba.target_pose.header.frame_id = 'map'
            mba.target_pose.pose.position.x = position[0]
            mba.target_pose.pose.position.y = position[1]
            mba.target_pose.pose.position.z = 0.0
            mba.target_pose.pose.orientation.x = 0
            mba.target_pose.pose.orientation.y = 0
            mba.target_pose.pose.orientation.z = 0
            mba.target_pose.pose.orientation.w = angle;
            return mba; # my code has a degree yay

        smach.StateMachine.add('navigate_to_end', smach_ros.SimpleActionState(
                                                'move_base',
                                                MoveBaseAction,
                                                goal_cb = midpointEnd, input_keys=['objects']), ### Or something.
                               transitions={'succeeded':'exit','preempted':'fail','aborted':'fail'})

        def midpointEnd(userdata, goal):
        # Move forward
            listener = tf.TransformListener()
            (trans,rot) = listener.lookupTransform('/pose', '/map', rospy.Time(0)) # im assuming this is the relevant thing?
            dx=Math.cos(rot[4])*10;
            dy=Math.sin(rot[4])*10; # 10 units forward, or whatever
            mba = MoveBaseGoal()
            mba.target_pose.header.frame_id = 'pose'
            mba.target_pose.pose.position.x = dx
            mba.target_pose.pose.position.y = dy
            mba.target_pose.pose.position.z = 0.0
            mba.target_pose.pose.orientation=rot;
            return mba; # my code has a degree yay

        smach.StateMachine.add('exit', smach_ros.SimpleActionState(
                                                'move_base',
                                                MoveBaseAction,
                                                goal_cb = midpointEnd, input_keys=['objects']), ### Or something.
                               transitions={'succeeded':'success','preempted':'fail','aborted':'fail'})
    # Execute SMACH plan
    outcome = sm.execute()
