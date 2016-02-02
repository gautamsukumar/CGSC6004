import ccm      
log=ccm.log()   

from ccm.lib.actr import *  

#####
# Python ACT-R requires an environment
# but in this case we will not be using anything in the environment
# so we 'pass' on putting things in there

class MyEnvironment(ccm.Model):
    pass

#####
# create an act-r agent

class MyAgent(ACTR):
    
    focus=Buffer()

    def init():
        focus.set('goal:boardbus object:busstop')

    def correct_bus(focus='goal:boardbus object:busstop'):     # if focus buffer has this chunk then....
        print "I see the route 8 bus"                            # print
        focus.set('goal:boardbus object:stop_at_flag')                   # change chunk in focus buffer

    def stop_at_flag(focus='goal:boardbus object:stop_at_flag'):          # the rest of the productions are the same
        print "I am standing at the flag"                # but carry out different actions
        focus.set('goal:boardbus object:open_door')

    def open_door(focus='goal:boardbus object:open_door'):
        print "I am waiting for the door to open"
        focus.set('goal:boardbus object:climb_in')

    def climb_in(focus='goal:boardbus object:climb_in'):
        print "I have climbed in"
        print "I have boarded the bus"
        focus.set('goal:stop')   

    def stop_production(focus='goal:stop'):
        self.stop()                                           # stop the agent

gautam=MyAgent()                              # name the agent
octranspo=MyEnvironment()                     # name the environment
octranspo.agent=gautam                           # put the agent in the environment
ccm.log_everything(octranspo)                 # print out what happens in the environment

octranspo.run()                               # run the environment
ccm.finished()                             # stop the environment
