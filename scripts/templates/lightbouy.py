stateMachineName="light_buoy"
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
        ('start','Start signal recieved.','approachBuoy'),
     ]},
     {'name':'approachBuoy',
    'mymessage':'Navigating to light buoy...',
    'transitions':[
        ('travelOK','Arrived at or near light buoy.','stationKeep'),
        ('criticalFail','No light buoy found.','fail')
     ]},
     {'name':'stationKeep',
    'mymessage':'Holding position at light buoy...',
    'transitions':[
        ('stationKeepOK','Station Keeping OK!','readAndReport'),
        ('criticalFail','Could not station keep - critical fail!','fail')
     ]},
     {'name':'readAndReport',
    'mymessage':'Reading and reporting light buoy location...',
    'transitions':[
        ('readOK','Read location ok. Proceeding to exit.','navEnd'),
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