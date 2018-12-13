import rospy
import smach
import math
import tf
from std_msgs.msg import Header
from geometry_msgs.msg import PoseArray, Pose, PoseStamped
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
threshold = 3


class moveTo(smach.State):
    def __init__(self):
        smach.State.__init__(
            self, outcomes=['succeeded', 'preempted', 'aborted'], input_keys=['goal'])
        self.mbp = rospy.Publisher("/waypoints", Path)

        self.tfListener = tf.TransformListener()
        # self.goalPub=rospy.Publisher("/move_base_simple/goal",PoseStamped)

    def execute(self, userdata):
        rospy.loginfo('Moving to location...')
        if isinstance(userdata.goal, PoseStamped):
            self.goals = [userdata.goal]
        else:
            self.goals = userdata.goal
        # recieve the current position
        r = rospy.Rate(10)
        cgoal = 0
        path_msg = Path()
        header = Header()
        header.stamp = rospy.Time.now()
        header.frame_id = "map"
        path_msg.header = header

        pose_list = []
        for g in self.goals:
            ps = PoseStamped()
            ps.header = header
            ps.pose = g.pose
            pose_list.append(ps)
        path_msg.poses = pose_list
        self.mbp.publish(path_msg)
        print(path_msg)
        while not rospy.is_shutdown():
            self.tfListener.waitForTransform(
                "map", "base_link", rospy.Time(0), rospy.Duration(4.0))
            (trans, rot) = self.tfListener.lookupTransform(
                "map", "base_link", rospy.Time(0))
            if (math.sqrt((trans[0]-self.goals[cgoal].pose.position.x)**2+(trans[1]-self.goals[cgoal].pose.position.y)**2) < threshold):
                cgoal = cgoal+1
                if cgoal > len(self.goals):
                    return 'succeeded'
            r.sleep()
