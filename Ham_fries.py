###### You want fries with that?! Sandwich-and-sideorder production DM model ######

import ccm      
log=ccm.log()   

from ccm.lib.actr import *  

class MyEnvironment(ccm.Model):
    pass

class MyAgent(ACTR):
    focus=Buffer()
    DMbuffer=Buffer()                           # create a buffer for DM
    DM=Memory(DMbuffer)                         # create DM and connect it to its buffer
    DM2buffer=Buffer()                          # create a buffer for DM2
    DM2=Memory(DM2buffer)                       # create DM2 and connect it to its buffer
    
    DM.add('condiment:mustard')                 # put a chunk into DM
    DM.add('condiment:relish')                  # put a second chunk into DM
    DM2.add('side:fries')                       # put a chunk into DM2
    DM2.add('side:wedges')                      # put a second chunk into DM2
    
    focus.set('sandwich bread')
        
    def bread_bottom(focus='sandwich bread'):   
        print "I have a piece of bread"         
        focus.set('sandwich cheese')    

    def cheese(focus='sandwich cheese'):        
        print "I have put cheese on the bread"  
        focus.set('sandwich ham')

    def ham(focus='sandwich ham'):
        print "I have put  ham on the cheese"
        focus.set('get_condiment')

    def condiment(focus='get_condiment'):
        print "recalling the order"
        DM.request('condiment:?')               # retrieve a chunk from DM into the DM buffer
        focus.set('sandwich condiment')         # ? means that slot can match any content

    def order(focus='sandwich condiment', DMbuffer='condiment:?condiment'):     # match to DMbuffer as well
        print "I recall they wanted..."                                         # put slot 2 value in ?condiment
        print condiment             
        print "i have put the condiment on the sandwich"
        focus.set('sandwich bread_top')

    def bread_top(focus='sandwich bread_top'):
        print "I have put bread on the ham"
        print "I have made a ham and cheese sandwich"
        focus.set('get_side')

    def side(focus='get_side'):
        print "recalling side order"
        DM2.request('side:?')                   # retrieve a chunk from DM2 into the DM2 buffer
        focus.set('sandwich side')
        
    def sideorder(focus='sandwich side', DM2buffer='side:?side'):               # match to DM2buffer as well
        print "I recall they wanted..."                                         # put slot 2 value in ?side
        print side
        print "I have added the side order"
        focus.set('stop')
        
    def stop_production(focus='stop'):
        self.stop()


gautam=MyAgent()                                # name the agent
harveys=MyEnvironment()                         # name the environment
harveys.agent=gautam                            # put the agent in the environment
ccm.log_everything(harveys)                     # print out what happens in the environment

harveys.run()                                   # run the environment
ccm.finished()                                  # stop the environment
