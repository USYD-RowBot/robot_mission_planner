stateMachineName="entrance_gate"
finalOutcomes=['success','fail']
states=[
#	{'name':'name',
#    'mymessage':'Something to say at the start',
#	 'transitions':[
#	 	('pathName','toStateName','Relevant output message')
#	 ]},
	{'name':'waitForStart',
    'mymessage':'Waiting for start...',
    'transitions':[
	 	('abort','fail','Start aborted by controller.')
	 ]}
]



with open(stateMachineName+".py",'w+') as f:
    f.write("#!/usr/bin/env python\n"
    "import rospy\n"
    "import smach\n"
    "import smach_ros\n")
    stateString=""
    for i in states:
        transitNames=[it[0] for it in i['transitions']]
        stateString+="\nclass "+i['name']+"(smach.State):\n"
        stateString+="   def __init__(self):\n"
        stateString+="	 smach.State.__init__(self, outcomes={0})\n".format(transitNames)
        stateString+="   def execute(self,userdata):\n"
        stateString+="	     rospy.loginfo('{0}')\n".format(i['mymessage'])
        stateString+="	     rospy.sleep(2)\n";
        for c,j in enumerate(i['transitions']):
            stateString+="	    if True:\n"
            stateString+="	    	rospy.loginfo('{0}')\n".format(j[2])
            stateString+="	    	return '{0}'\n".format(j[0]);
    f.write(stateString);
    f.write("\n\n if __name__ == '__main__':\n"
    "    rospy.init_node({0})\n".format(stateMachineName)+
    "    # Create a SMACH state machine\n"
    "    sm = smach.StateMachine(outcomes={0})\n".format(finalOutcomes)+
    "    # Open the container\n"
    "    with sm:\n"
    "    # Add states to the container\n");
    stateString="";
    for i in states:
        transitDict=[(j[0],j[1]) for j in i['transitions']]
        transitDict=dict(transitDict)
        stateString+="        smach.StateMachine.add('{0}', ".format(i['name'])+i['name']+"(), \n"
        stateString+="                              transitions={0})\n".format(transitDict);
    f.write(stateString);
    f.write("    # Execute SMACH plan\n"
    "    outcome = sm.execute()\n");