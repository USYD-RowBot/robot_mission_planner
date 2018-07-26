stateMachineName="entrance_gate"
finalOutcomes=['success','fail']
states=[
#   {'name':'name',
#    'mymessage':'Something to say at the start',
#    'transitions':[
#       ('pathName','toStateName','Relevant output message')
#     ]},
    {'name':'waitForStart',
    'mymessage':'Waiting for start...',
    'transitions':[
         ('abort','Start aborted by controller.','fail'),
        ('start','Start signal recieved.','findGates'),
     ]},
     {'name':'findGates',
    'mymessage':'Finding Gates...',
    'transitions':[
         ('gatesFound','Found Gates!','chooseEntry'),
        ('gateTimeout','Not all gates could be found in allocated time period. Proceed with caution!','findGates'),
        ('criticalFail','No gates could be found. Critical error! Aborting...','fail')
     ]},
     {'name':'chooseEntry',
    'mymessage':'Choosing entry gate...',
    'transitions':[
         ('entryFound','Chosen entry gate!','navEntry'),
        ('entryRandomGuess','Not sure which gate to go through; making random guess :/','navEntry'),
        ('criticalFail','Not sure which gate to go through: aborting - better safe than sorry!','fail')
     ]},
     {'name':'navEntry',
    'mymessage':'Navigating to entry...',
    'transitions':[
         ('gatePassthroughOK','Passed through entry gate!','findBuoys'),
        ('minorHindrance','Something went wrong, but we are still alive... Moving on.','findBuoys'),
        ('criticalFail','Something went pretty badly wrong. hlep pls','fail')
     ]},
     {'name':'findBuoys',
    'mymessage':'Identifying buoys...',
    'transitions':[
         ('2buoysFound','Got both buoys.','chooseBuoy'),
        ('1buoyFound','Got one buoy. Lets just use that one :3','chooseBuoy'),
        ('criticalFail','No buoys could be found. what do .-.','fail')
     ]},
     {'name':'chooseBuoy',
    'mymessage':'Choosing buoy...',
    'transitions':[
         ('buoyFoundConfident','Got a confident lock on the appropriate buoy.','navCircleBuoy'),
        ('buoyNoLock','Not sure which buoy to go around. Just choosing a random one','navCircleBuoy'),
        ('criticalFail','Aliens must have abducted the beacons or sth 3: what do .-.','fail')
     ]},
     {'name':'navCircleBuoy',
    'mymessage':'Orbiting buoys.',
    'transitions':[
         ('orbitDone','Orbit done.','chooseExit'),
        ('whereRWe','wh-- what happened? ah well im alive lets keep going','chooseExit'),
        ('criticalFail','X-X','fail')
     ]},
     {'name':'chooseExit',
    'mymessage':'Choosing exit gate...',
    'transitions':[
         ('choiceOK','Chose the exit buoy. Allg.','choiceOK'),
        ('choiceUnsure','Not sure which buoy to go through. Choosing a random one...','chooseBuoy'),
        ('criticalFail','No buoys could be found. what do .-.','fail')
     ]},
     {'name':'navigateThroughExit',
    'mymessage':'Heading through exit...',
    'transitions':[
         ('navOK','All done!','success'),
        ('navError','Something went wrong but i think i am ok...','success'),
        ('criticalFail','Nooo! So close!','fail')
     ]},
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
        stateString+="     smach.State.__init__(self, outcomes={0})\n".format(transitNames)
        stateString+="   def execute(self,userdata):\n"
        stateString+="         rospy.loginfo('{0}')\n".format(i['mymessage'])
        stateString+="         rospy.sleep(2)\n";
        for c,j in enumerate(i['transitions']):
            stateString+="         if True:\n"
            stateString+="             rospy.loginfo('{0}')\n".format(j[1])
            stateString+="             return '{0}'\n".format(j[0]);
    f.write(stateString);
    f.write("\n\nif __name__ == '__main__':\n"
    "    rospy.init_node({0})\n".format(stateMachineName)+
    "    # Create a SMACH state machine\n"
    "    sm = smach.StateMachine(outcomes={0})\n".format(finalOutcomes)+
    "    # Open the container\n"
    "    with sm:\n"
    "    # Add states to the container\n");
    stateString="";
    for i in states:
        transitDict=[(j[0],j[2]) for j in i['transitions']]
        transitDict=dict(transitDict)
        stateString+="        smach.StateMachine.add('{0}', ".format(i['name'])+i['name']+"(), \n"
        stateString+="                              transitions={0})\n".format(transitDict);
    f.write(stateString);
    f.write("    # Execute SMACH plan\n"
    "    outcome = sm.execute()\n");