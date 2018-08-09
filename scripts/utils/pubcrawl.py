#!/usr/bin/env python

## An object publisher.

 # license removed for brevity
 import rospy
 from rowbot_vision.msg import Object, ObjectArray

 

 def talker():
     pub = rospy.Publisher('objects', ObjectArray, queue_size=10)
     rospy.init_node('pubcrawl', anonymous=True)
     rate = rospy.Rate(10) # 10hz
     while not rospy.is_shutdown():
        pub.publish(objects)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
