# CGSC6004 - Python ACT-R Modelling - Final Project
#   Grid Clearance, submitted by Fraydon Karimi, MCogSc and Gautam Sukumar, MCogSc

# This model has a goal of grid clearance, i.e. upon being placed in a square-grid environment, 
#   agent(s) wander(s) throughout the grid, while appropriately negotiating distractors 
#   (i.e. ignoring bunnies and killing monsters). 
# The agent(s) stop(s) once it/they has/have achieved the goal of visiting all squares.

# We would like to thank Prof. Rob West for his steady supervision, as well as
#   Warren MacDougall for his guidance and generosity in conceptualising and completing
#   this project. 


world_size=4
world_x_range=world_size
world_y_range=world_size
number_of_agents=1


import sys
import os
sys.path.append(os.getcwd() + '\\CCMSuite')

import ccm
log=ccm.log(html=False)   
from ccm.lib.actr import *  

import random

goal_square = str(random.choice(range(world_x_range))), str(random.choice(range(world_y_range)))
##print goal_square
agent_list = []



class Environment(ccm.Model):        # Items in the environment look and act like chunks; 
                                    #   but note the syntactic differences
    prepping_world = True

    while prepping_world:
        occupied_tally = 0
        squares = [ccm.Model(isa='square', x=x, y=y, occupied=0, occupant='nil') \
            for x in range(world_x_range) for y in range(world_y_range)]
        
        for square in squares:
            if (str(square.x), str(square.y)) == goal_square:
                square.occupied = 1
                square.occupant = 'goal'
                
        for square in squares:
            x = random.choice(range(10))
            if x == 5 and \
                (str(square.x), str(square.y)) != goal_square:
                square.occupant = 'monster'
                square.occupied = 1

            elif x == 2 and \
                (str(square.x), str(square.y)) != goal_square:
                square.occupant = 'bunny'
                square.occupied = 1

        for s in squares:
            if s.occupied == 1:
                occupied_tally += 1
        if occupied_tally + number_of_agents >= world_x_range * world_y_range:
            continue
        else: 
            prepping_world = False

    agent_list = []


class MotorModule(ccm.ProductionSystem):     # Creating a motor module to do the actions 
                                                #   direction key: 0 = up, 1 = right, 2 = down, 3 = left
    production_time = 0.05

    def moveForward(self):
        print self.parent.instance_name, 'is trying to move forward'
        if self.parent.facing == 0:
            target_value = self.parent.y_coordinate - 1
            target_x_y = self.parent.x_coordinate, target_value
            if self.parent.y_coordinate >  0:
                for s in self.parent.parent.squares:
                    if (s.x, s.y) == target_x_y:
                        target_square = s
                        if s.occupied == '1':
                            print 'cannot pass: square occupied'
                            pass
                        else:
                            print 'target square is unoccupied'
                            print self.parent.instance_name, 'has moved forward to target'
                            print '-1y'
                            self.parent.y_coordinate -= 1         
            else: 
                print self.parent.instance_name, 'is at edge of map; cannot move forward'
                pass

        elif self.parent.facing == 1:
            target_value = self.parent.x_coordinate + 1
            target_x_y = target_value, self.parent.y_coordinate
            if self.parent.x_coordinate < world_x_range:
                for s in self.parent.parent.squares:
                    if (s.x, s.y) == target_x_y:
                        target_square = s
                        if s.occupied == '1':
                            print 'cannot pass: must engage monster first'
                            pass
                        else:
                            print 'target square is unoccupied'
                            print self.parent.instance_name, 'has moved forward to target'
                            print '+1x'
                            self.parent.x_coordinate += 1         
            else: 
                print self.parent.instance_name, ' at edge of map; cannot move forward'
                pass

        elif self.parent.facing == 2:
            target_value = self.parent.y_coordinate + 1
            target_x_y = self.parent.x_coordinate, target_value
            if self.parent.y_coordinate < world_y_range:
                for s in self.parent.parent.squares:
                    if (s.x, s.y) == target_x_y:
                        target_square = s
                        if s.occupied == '1':
                            print 'cannot pass: must engage monster first'
                            pass
                        else:
                            print 'target square is unoccupied'
                            print self.parent.instance_name, 'has moved forward to target'
                            print '-1y'
                            self.parent.y_coordinate += 1         
            else: 
                print self.parent.instance_name, ' at edge of map; cannot move forward'
                pass
        elif self.parent.facing == 3:
            target_value = self.parent.x_coordinate - 1
            target_x_y = target_value, self.parent.y_coordinate
            if self.parent.x_coordinate > 0:
                for s in self.parent.parent.squares:
                    if (s.x, s.y) == target_x_y:
                        target_square = s
                        if s.occupied == '1':
                            print 'cannot pass: must engage monster first'
                            pass
                        else:
                            print 'target square is unoccupied'
                            print self.parent.instance_name, 'has moved forward to target'
                            print '-1x'
                            self.parent.x_coordinate -= 1         
            else: 
                print self.parent.instance_name, ' at edge of map; cannot move forward'
                pass

    def turnLeft(self):
        print self.parent.instance_name, 'is turning left'
        if self.parent.facing == 0:
            self.parent.facing = 3
        else:
            self.parent.facing -= 1
        print self.parent.instance_name, 'has turned left'
    
    def turnRight(self):
        print self.parent.instance_name, 'is turning right'
        if self.parent.facing == 3:
            self.parent.facing = 0
        else:
            self.parent.facing += 1
        print self.parent.instance_name, 'has turned right'
        
                                    ## Navigation methods to approach known target
    def faceGoalY(self):
        print 'running faceGoalY'
        if self.parent.y_coordinate == int(goal_square[1]):
            pass
        elif self.parent.y_coordinate < int(goal_square[1]):
            if self.parent.facing == 2:
                pass
            elif self.parent.facing == 1:
                self.parent.motor.turnRight()
            elif self.parent.facing == 3:
                self.parent.motor.turnLeft()
            elif self.parent.facing == 0:
                self.parent.motor.turnRight()
                self.parent.motor.turnRight()
        elif self.parent.y_coordinate > int(goal_square[1]):
            if self.parent.facing == 2:
                self.parent.motor.turnRight()
                self.parent.motor.turnRight()
            elif self.parent.facing == 1:
                self.parent.motor.turnLeft()
            elif self.parent.facing == 3:
                self.parent.motor.turnRight()
            elif self.parent.facing == 0:
                pass

    def approachGoal_Y(self):
        print 'running approachGoal Y'
        
        if self.parent.y_coordinate == int(goal_square[1]):
            pass
        else: 
            delta_y = self.parent.y_coordinate - int(goal_square[1])
            for i in range(abs(delta_y)):
                self.parent.motor.moveForward()
                yield 0.05

    def faceGoalX(self):
        print 'running faceGoalX'
        if self.parent.x_coordinate == int(goal_square[0]):
            pass
        elif self.parent.x_coordinate < int(goal_square[0]):
            if self.parent.facing == 0:
                self.parent.motor.turnRight()
            elif self.parent.facing == 1:
                pass
            elif self.parent.facing == 2:
                self.parent.motor.turnLeft()
            elif self.parent.facing == 3:
                self.parent.motor.turnRight()
                self.parent.motor.turnRight()
        elif self.parent.x_coordinate > int(goal_square[0]):
            if self.parent.facing == 0:
                self.parent.motor.turnLeft()
            elif self.parent.facing == 1:
                self.parent.motor.turnRight()
                self.parent.motor.turnRight()
            elif self.parent.facing == 2:
                self.parent.motor.turnRight()
            elif self.parent.facing == 3:
                pass

    def approachGoal_X(self):
        print 'running approachGoal X'
        if self.parent.x_coordinate == int(goal_square[0]):
            pass
        else:
            delta_x = self.parent.x_coordinate - int(goal_square[0])
            for i in range(abs(delta_x)):
                self.parent.motor.moveForward()
                yield 0.05

class Top_Down_Vision_Module(ccm.ProductionSystem):
    production_time = 0.05

    def check_self_location(self):
        visual_string_temp = str('x_loc:' + str(self.parent.x_coordinate) \
            + ' y_loc:' + str(self.parent.y_coordinate) + ' facing:' + str(self.parent.facing))
        self.parent.visual_buffer.set(visual_string_temp)
        
        visual_mem_temp = (self.parent.x_coordinate, self.parent.y_coordinate) 
                                    # Creating (and displaying) a chunk to be loaded into the 
                                    #   visual memory buffer
        print "agent's coordinates:", visual_mem_temp
                                                        # Keeping track of squares visited
               

        if visual_mem_temp in self.parent.squares_remain:
            print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            print 'goal status:', len(self.parent.squares_remain)
            self.parent.squares_remain.remove(visual_mem_temp)
            print 'squares remaining:', len(self.parent.squares_remain)
            
            
        
        print self.parent.instance_name, 'visual buffer contains -', self.parent.visual_buffer.chunk
           
    def line_of_sight_constructor(self):
                                                # line_of_sight_vector = squares in front of the agent, 
                                                #   until edge of map
        print self.parent.instance_name, 'is at: ', '(', self.parent.x_coordinate, ',' , self.parent.y_coordinate, ')'

        if self.parent.facing == 0:
            line_of_sight_vector = [s for s in env.squares if \
                s.x == self.parent.x_coordinate and s.y < self.parent.y_coordinate]
        elif self.parent.facing == 1:
            line_of_sight_vector = [s for s in env.squares if \
                s.y == self.parent.y_coordinate and s.x > self.parent.x_coordinate]
        elif self.parent.facing == 2:
            line_of_sight_vector = [s for s in env.squares if \
                s.x == self.parent.x_coordinate and s.y > self.parent.y_coordinate]
        elif self.parent.facing == 3:
            line_of_sight_vector = [s for s in env.squares if \
                s.y == self.parent.y_coordinate and s.x < self.parent.x_coordinate]

        for i in range(len(line_of_sight_vector)):
            if line_of_sight_vector[i].occupant == 'monster':
                line_of_sight_vector = line_of_sight_vector[0:i+1]
                                    # ^^ this causes the agent to see only 
                                    #   up to the first obstruction, i.e. monster
                break
        print 'Line of Sight vector is:'
        for s in line_of_sight_vector:
            print '(', s.x, ',', s.y, ')'
            pass 
            
        self.parent.line_of_sight = line_of_sight_vector

    def update_top_down_vision(self):
        for square in self.parent.line_of_sight:
            if square.occupant == 'goal':
                self.parent.visual_buffer.set('goal:visible')
            elif square.occupant == 'monster' or square.occupant == 'bunny':
                self.parent.visual_buffer.set(square)


    def check_goal(self):
        print self.parent.instance_name, 'is checking goal status'    
        if len(self.parent.squares_remain) == 0:
            print 'grid cleared!'
            self.parent.focus_buffer.set('at_goal')
        else:
            print self.parent.instance_name, 'is not yet at goal'

    def vision_update(self):    # Wraps all vision methods, and calls them all together

        self.parent.top_down_vision.check_self_location()
        self.parent.top_down_vision.line_of_sight_constructor()
        self.parent.top_down_vision.update_top_down_vision()
        self.parent.top_down_vision.check_goal()

class Bottom_Up_Vision_Module(ccm.ProductionSystem):
    ##production_time = 0.01
    def monsterSpotting(DMbuffer='planning_unit:!kill_monster', visual_buffer='occupant:monster', DM='busy:False', unit_task_buffer=''):
        print self.parent.instance_name, 'initiating monster slaying protocol'
        DM.request('planning_unit:kill_monster')
        context_buffer.set('last_action:none')
        unit_task_buffer.clear()

    def bunnySpotting(DMbuffer='planning_unit:!kill_monster', visual_buffer='occupant:bunny', DM='busy:False', unit_task_buffer=''):
        print 'bunny spotted; ignoring it'
        print self.parent.instance_name, 'is ignoring bunny'
        DM.request('planning_unit:wander')
        visual_buffer.clear()
        context_buffer.set('last_action:none')
        unit_task_buffer.clear()
                                                                # This does not exist in the Wander Model,
                                                                #   and is applicable to multiple agents
class Bottom_Up_Communication_Module(ccm.ProductionSystem):
    callOutMade = False
    def call_out_goal(visual_buffer='goal:visible'):
        if callOutMade == True:
            print 'call out already made, not making it again'
            pass
        elif callOutMade == False:
            print 'goal has been spotted: communicating planning unit to teammates'
            for agent in self.parent.parent.agent_list: 
                agent.DM.add('planning_unit:navigation_sequential UnitTask1:approach_Y UnitTask2:approach_X UnitTask3:conclude')
                agent.DM.add('planning_unit:navigation_sequential2 UnitTask1:approach_X UnitTask2:approach_Y UnitTask3:conclude')
                callOutMade = True
                visual_buffer.clear()


                                                    # Defining agent properties and methods
class MyAgent(ACTR): 
 
                                                    # Class attributes: buffers, modules, variables   
    focus_buffer=Buffer()
    visual_buffer=Buffer()
    visual_mem_buffer=Buffer()
    context_buffer=Buffer()
    unit_task_buffer=Buffer()

    DMbuffer=Buffer()                               # Creating a buffer for declarative memory (henceforth DM), latency=0.3, threshold=0
    DM=Memory(DMbuffer)                             # Creating DM and connecting it to its buffer, 
                                                    #   dm_bl=DMBaseLevel (DM, decay=0.5, limit=None)

    motor=MotorModule()
    ##communicationModule=Bottom_Up_Communication_Module()
    top_down_vision=Top_Down_Vision_Module()
    bottom_up_vision = Bottom_Up_Vision_Module()
    moveList = [motor.moveForward, motor.turnLeft, motor.turnRight]
    line_of_sight = []
                            # These set the class variable to the global variable; 
                            #   allows for agent positioning to be tied to world size
    world_x_range = world_x_range
    world_y_range = world_y_range
                            # Need a global reference to the goal square for calculating delta
    goal_coord = goal_square
    finished = False
    placed = False

    def init():
        DM.add('planning_unit:wander UnitTask1:random_movement UnitTask2:conclude')
        DM.add('planning_unit:kill_monster UnitTask1:ready UnitTask2:aim UnitTask3:fire UnitTask4:conclude')
                            # Finding an open square to place the agent
        while not self.placed:
            x = random.choice(range(world_x_range))
            y = random.choice(range(world_y_range))
            init_x_y = (x,y)
            for s in self.parent.squares:
                if (s.x, s.y) == (x,y):
                    init_square = s
                    if init_square.occupied == 1:
                        continue
                    elif init_square.occupied == 0:
                        self.x_coordinate = x 
                        self.y_coordinate = y 
                        self.placed = True
        self.facing = random.randint(0,3)
        initial_delta=(abs(self.x_coordinate - int(goal_coord[0])) + abs(self.y_coordinate - int(goal_coord[1])))
        self.log.delta=initial_delta
        self.squares_remain_temp = [s for s in self.parent.squares]
        self.squares_remain = []
        for s in self.squares_remain_temp:
            temp = (s.x, s.y)
            self.squares_remain.append(temp)        # Logging the squares visited
            
            
        
        
        top_down_vision.check_self_location()
        DM.request('planning_unit:!kill_monster')
        context_buffer.set('last_action:none')
        

                                        # Planning-unit-selection productions
    def start_planning_unit(DMbuffer='planning_unit:?planning_unit', context_buffer='last_action:none'):
        x = sorted(DMbuffer.chunk.keys())
        
        y = DMbuffer.chunk[x[0]]
        context_buffer.clear()
        unit_task_buffer.set(y)

    def continue_planning_unit(DMbuffer='planning_unit:?planning_unit', context_buffer='last_action:?last_action!none!conclude', DM='busy:False'):
        x = sorted(DMbuffer.chunk.keys())
        a = [key for key,value in DMbuffer.chunk.items() if value==last_action]
        nextUnitTask = x.index(a[0]) + 1
        y = DMbuffer.chunk[x[nextUnitTask]]
        context_buffer.clear()
        unit_task_buffer.set(y)

    def finish_planning_unit(DMbuffer='planning_unit:?planning_unit', context_buffer='last_action:conclude'):
        print 'planning unit', planning_unit, 'finished'
        context_buffer.set('last_action:none')
        unit_task_buffer.clear()
        DM.request('planning_unit:?')
        ##fix

                                        # Sequential navigation unit-tasks
    def approach_Y(unit_task_buffer='approach_Y'):
        motor.faceGoalY()
        motor.approachGoal_Y()
        top_down_vision.vision_update()
        unit_task_buffer.clear()
        context_buffer.set('last_action:approach_Y')

    def approach_X(unit_task_buffer='approach_X'):
        motor.faceGoalX()
        motor.approachGoal_X()
        top_down_vision.vision_update()
        unit_task_buffer.clear()
        context_buffer.set('last_action:approach_X')

                                        # Random movement navigation unit-task
    def wander(unit_task_buffer='random_movement'):
        random.choice(moveList)()
        top_down_vision.vision_update()
        unit_task_buffer.clear()
        context_buffer.set('last_action:random_movement')

                                        # Monster killing unit-tasks
    def ready(unit_task_buffer='ready'):
        if self.line_of_sight == []:
            print self.instance_name, 'has nothing in sight; passing on ready'
            DM.request('planning_unit:!kill_monster')
            context_buffer.set('last_action:none')
            unit_task_buffer.clear()
            visual_buffer.clear()
        else:
            for s in self.line_of_sight:
                if s.occupant == 'monster':
                    print self.instance_name, 'preparing to engage enemey'
                    unit_task_buffer.clear()
                    context_buffer.set('last_action:ready')
                    continue
        if all(s.occupant != 'monster' for s in self.line_of_sight):
            print 'no monsters here; passing on ready'
            DM.request('planning_unit:!kill_monster')
            context_buffer.set('last_action:none')
            unit_task_buffer.clear()
            visual_buffer.clear()

    def aim(unit_task_buffer='aim'):
        print 'aiming weapon'
        unit_task_buffer.clear()
        context_buffer.set('last_action:aim')

    def fire(unit_task_buffer='fire'):
        print 'fire!!!!!!'
        for i in self.parent.squares:
            if (i.x, i.y) == (visual_buffer.chunk['x'], visual_buffer.chunk['y']):
                i.occupant='nil'
                i.occupied=0
                print 'monster slain  x.x'
        unit_task_buffer.clear()
        context_buffer.set('last_action:fire')
        
                                    # Generic planning unit conclude unit-task
    def conclude(unit_task_buffer='conclude', DMbuffer='planning_unit:?planning_unit'):
        print 'concluding the planning unit', planning_unit
        top_down_vision.vision_update()
        unit_task_buffer.clear()
        context_buffer.set('last_action:conclude')
 
                                    # Goal-confirmation productions
    def reached_goal(focus_buffer='at_goal'):
        print self.instance_name, 'ending from focus buffer'
        unit_task_buffer.clear()
        DMbuffer.clear()
        context_buffer.clear()
        visual_buffer.clear()
        self.finished = True
        focus_buffer.set('waiting_for_teammate')

    def wait_for_teammate_to_finish(focus_buffer='waiting_for_teammate'):
        production_time = 0.1
        if all(a.finished == True for a in self.parent.agent_list):
            print 'all agents have finished'
            self.stop()
        else: 
            print self.instance_name, 'is waiting'
            print self.parent.agent_list
            for a in self.parent.agent_list: print a.finished

            focus_buffer.set('waiting_for_teammate')
            print 'xxxxxxxxxxxxxxxxxxxxxxxx'

env=Environment()

for a,i in enumerate(range(number_of_agents)):
    a = MyAgent()
    a.instance_name = str('agent' + str(i))
    env.agent = a
    env.agent.log = log
    env.agent_list.append(a)


#ccm.log_everything(env)
env.run()
# for s in env.squares:
#     print s.occupant
# exit()
ccm.finished()  