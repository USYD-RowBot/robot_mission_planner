stateMachineName="totem_finder"
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
        ('start','Start signal recieved.','getSequence'),
     ]},
     {'name':'getSequence',
    'mymessage':'Gathering sequence info...',
    'transitions':[
        ('sequenceOK','Sequence detected.','findTotems'),
        ('sequenceMissing','Some sequence elements missing. Moving randomly...','findTotems'),
        ('criticalFail','Something went badly wrong 3:','fail')
     ]},
     {'name':'findTotems',
    'mymessage':'Identifying totems...',
    'transitions':[
        ('totemsFound','Totems found!','sequenceMoves'),
        ('totemsFoundEnough','Found enough totems to go ahead. Proceeding with caution','sequenceMoves'),
        ('criticalFail','Something went badly wrong 3:','fail')
     ]},
     {'name':'sequenceMoves',
    'mymessage':'Identifying sequence and planning moves...',
    'transitions':[
        ('sequenceOK','Sequence planning ok.','performSequence'),
        ('criticalFail','Something went badly wrong 3:','fail')
     ]},
     {'name':'performSequence',
    'mymessage':'Performing required sequence...',
    'transitions':[
        ('sequenceExecutionOK','Sequence navigation complete. ','gotoExit'),
        ('minorHindrance','Something went wrong. Going to exit...','gotoExit'),
        ('criticalFail','Something went badly wrong 3:','fail')
     ]},
     {'name':'gotoExit',
    'mymessage':'Going to exit..',
    'transitions':[
        ('arrivedAtExit','Got to exit. Hooray!','success'),
        ('criticalFail','Something went badly wrong 3:','fail')
     ]}
]