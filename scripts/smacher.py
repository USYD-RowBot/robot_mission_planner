stateMachineName="entrance_gate"

states=[
#	{name:'name',
#	 transitions:{
#	 	('pathName','toStateName','Relevant output message')
#	 }
	
	
	
]



with open(stateMachineName+".py",'w') as f:
	f.write('#!/usr/bin/env python\n'+
			'import rospy\n'+
			'import smach\n'+
			'import smach_ros\n')
	for i in states:
		f.write('class '+i['name']+'(smach.State):
				'def __init__(self):
				'	smach.State.__init__(self, outcomes=['start','abort'])
				'
				'def execute(self,userdata):
				'	rospy.loginfo("Waiting for start.")
				'	rospy.sleep(2)
				'	if True:
				'		rospy.loginfo("Starting...")
				'		return 'start'
				'	else:
				'		rospy.loginfo("Mission aborted.")
				'		return 'abort'
