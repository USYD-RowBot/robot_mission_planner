import rospy
import smach
# initialise a single listener for all derivative classes to use - saving listener initialisation calls

class executor(smach.State):

    def __init__(self,function,timeout=None):
        rospy.loginfo('init Operator on function:' + str(function))
        smach.State.__init__(self, outcomes=['done','error'],input_keys=['data'], output_keys=['result'])
        self.toExecute=function
        self.timeout=-1
    def execute(self,userdata):
        rospy.loginfo('Executing function')
        userdata.result=self.toExecute(userdata.data)
        return 'done'
        """ try:
            
        except Exception,e:
            print(e)
            return 'error'
 """