stateMachineName="docking"
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
        ('start','Start signal recieved.','navigateToDocks'),
     ]},
     {'name':'approachDock',
    'mymessage':'Navigating to dock area',
    'transitions':[
        ('travelOK','Arrived at or near dock area.','identifyColours'),
        ('criticalFail','No light buoy found.','fail')
     ]},
     {'name':'identifyColours',
    'mymessage':'Identifying dock shape and colour...',
    'transitions':[
        ('colourOK','Dock colours detected; moving to correct location','navigateTodock'),
        ('criticalFail','Could not station keep - critical fail!','fail')
     ]},
     {'name':'navigateTodock',
    'mymessage':'Navigating to dock...',
    'transitions':[
        ('readOK','Reached dock!','dockAtDock'),
        ('criticalFail','Something went badly wrong 3:','fail')
     ]},
     {'name':'navigateTodock',
    'mymessage':'Docking at dock...',
    'transitions':[
        ('readOK','Docking ok.','navEnd'),
        ('criticalFail','Something went badly wrong 3:','fail')
     ]},
     {'name':'navEnd',
    'mymessage':'Navigating to end...',
    'transitions':[
        ('OKnavOK','Navigated to end successfully.','success'),
        ('failNavOK','Navigated to end successfully; task was not completed','fail'),
        ('criticalFail','Something went badly wrong 3:','fail')
     ]}
]