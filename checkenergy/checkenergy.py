# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Sample to demonstrate use of RewardForCollectingItem mission handler - creates a map with randomly distributed food items, each of which
# gives the agent a certain reward. Agent runs around collecting items, and turns left or right depending on the detected reward.
# Also demonstrates use of ObservationFromNearbyEntities

import MalmoPython
import os
import random
import sys
import time
import json
import random
import errno
from collections import namedtuple
EntityInfo = namedtuple('EntityInfo', 'x, y, z, name, quantity')
EntityInfo.__new__.__defaults__ = (0, 0, 0, "", 1)

def GetMissionXML(summary, itemDrawingXML):
    ''' Build an XML mission string that uses the RewardForCollectingItem mission handler.'''

    return '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>''' + summary + '''</Summary>
        </About>

        <ServerSection>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" forceReset="true"/>
                <DrawingDecorator>
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="226" z2="50" type="sandstone"/>
		    <DrawBlock x="0"  y="226" z="9" type="lava" />
		    <DrawBlock x="0"  y="226" z="14" type="lava" />
		    <DrawBlock x="0"  y="226" z="19" type="lava" />
		    <DrawBlock x="0"  y="226" z="29" type="lava" />
		    <DrawBlock x="0"  y="226" z="39" type="lava" />
		    <DrawBlock x="0"  y="226" z="50" type="lapis_block" />
                    ''' + itemDrawingXML + '''
                </DrawingDecorator>
                <ServerQuitFromTimeUp timeLimitMs="15000"/>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>The Hungry Caterpillar</Name>
            <AgentStart>
                <Placement x="0.5" y="227.0" z="0.5"/>
                <Inventory>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <InventoryCommands/>
                <ChatCommands/>
                <DiscreteMovementCommands />
                <VideoProducer>
                    <Width>480</Width>
                    <Height>320</Height>
                </VideoProducer>
                <RewardForCollectingItem>
                    <Item reward="2" type="fish porkchop beef chicken rabbit mutton"/>
                    <Item reward="1" type="potato egg carrot"/>
                    <Item reward="-1" type="apple melon"/>
                    <Item reward="-2" type="sugar cake cookie pumpkin_pie"/>
                </RewardForCollectingItem>
                <ContinuousMovementCommands turnSpeedDegs="90"/>
                <ObservationFromNearbyEntities>
                    <Range name="close_entities" xrange="2" yrange="2" zrange="2" />
                    <Range name="far_entities" xrange="10" yrange="2" zrange="10" update_frequency="100"/>
                </ObservationFromNearbyEntities>
                  <ObservationFromGrid>
                      <Grid name="floor3x3">
                        <min x="-1" y="-1" z="-1"/>
                        <max x="1" y="-1" z="1"/>
                      </Grid>
                  </ObservationFromGrid>
      <AgentQuitFromTouchingBlockType>
          <Block type="lapis_block" />
      </AgentQuitFromTouchingBlockType>

            </AgentHandlers>
        </AgentSection>

    </Mission>'''


def GetItemDrawingXML():
    ''' Build an XML string that contains 400 randomly positioned bits of food'''
    xml=""
    for item in range(400):
        x = str(random.randint(-50,50))
        z = str(random.randint(-50,50))
        #type = random.choice(["sugar", "cake", "cookie", "pumpkin_pie", "fish", "porkchop", "beef", "chicken", "rabbit", "mutton", "potato", "egg", "carrot", "apple", "melon"])
        type = random.choice(["water"])
        xml += '''<DrawItem x="''' + x + '''" y="250" z="''' + z + '''" type="''' + type + '''"/>'''
    return xml

def SendChat(msg):
    agent_host.sendCommand( "chat " + msg )

def SetVelocity(vel):
    agent_host.sendCommand( "move " + str(vel) )

def SetTurn(turn):
    agent_host.sendCommand( "turn " + str(turn) )

recordingsDirectory="EatingRecordings"
try:
    os.makedirs(recordingsDirectory)
except OSError as exception:
    if exception.errno != errno.EEXIST: # ignore error if already existed
        raise

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

validate = True
# Create a pool of Minecraft Mod clients.
# By default, mods will choose consecutive mission control ports, starting at 10000,
# so running four mods locally should produce the following pool by default (assuming nothing else
# is using these ports):
my_client_pool = MalmoPython.ClientPool()
my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))
my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10001))
my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10002))
my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10003))

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print 'ERROR:',e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)

itemdrawingxml = GetItemDrawingXML()

if True or agent_host.receivedArgument("test"):
    num_reps = 1
else:
    num_reps = 30000

jumping = False

def toggleFlags(flag1, flag2):
    temp = flag1
    flag1 = flag2
    flag2 = temp
    return flag1, flag2

for iRepeat in range(num_reps):
    my_mission = MalmoPython.MissionSpec(GetMissionXML("Nom nom nom run #" + str(iRepeat), itemdrawingxml),validate)
    # Set up a recording
    my_mission_record = MalmoPython.MissionRecordSpec(recordingsDirectory + "//" + "Mission_" + str(iRepeat) + ".tgz")
    my_mission_record.recordRewards()
    my_mission_record.recordMP4(24,400000)
    max_retries = 3
    for retry in range(max_retries):
        try:
            # Attempt to start the mission:
            agent_host.startMission( my_mission, my_client_pool, my_mission_record, 0, "itemTestExperiment" )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print "Error starting mission",e
                print "Is the game running?"
                exit(1)
            else:
                time.sleep(2)

    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()

    reward = 0.0    # keep track of reward for this mission.
    turncount = 0   # for counting turn time.
    # start running:
    checking=False
    checked=True
    count = 0
    turntime = 0
    energy = 20 # dE/dcount = 1/10 units
    # main loop:
    #if checked : SetVelocity(1)
    while world_state.is_mission_running:
        world_state = agent_host.getWorldState()
        if not energy :
	    SetVelocity(0)
	    SendChat("Cannot move anymore. No ENERGY!!")
        if checked :
	    count += 1
	    SetVelocity(1)
        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            ob = json.loads(msg)
            grid = ob.get(u'floor3x3', 0)
            print grid
            if "close_entities" in ob:
                entities = [EntityInfo(**k) for k in ob["close_entities"]]
                for ent in entities:
                    print ent.name, ent.x, ent.z, ent.quantity

            if "far_entities" in ob:
                far_entities = [EntityInfo(**k) for k in ob["far_entities"]]
                for ent in far_entities:
                    print ent.name, ent.quantity
            if jumping and grid[4]!=u'lava':
                agent_host.sendCommand("jump 0")
                jumping = False
                SendChat("Spending energy to JUMP")
                energy -= 1
            if grid[7]==u'lava':
                agent_host.sendCommand("jump 1")
                jumping = True


        if world_state.number_of_rewards_since_last_state > 0:
            # A reward signal has come in - see what it is:
            delta = world_state.rewards[0].getValue()
            if delta != 0:
                # The total reward has changed - use this to determine our turn.
                reward += delta
                turncount = delta
                if turncount < 0:   # Turn left
                    turncount = 1-turncount
                    SetTurn(-1)     # Start turning
                else:               # Turn right
                    turncount = 1+turncount
                    SetTurn(1)      # Start turning
        print "checking : %s, count : %s" % (str(checking), str(count))
        if count%10 == 0 and energy > 0:
            energy -= 1 
            SendChat("Energy spent moving. My energy : " + str(energy))
        if not checking and energy <= 5:
	    SetVelocity(0)
	    checking = True
	    checked = False
            turning = True
            turntime=10
        if checking :
            turntime -= 1  # Decrement the turn count
            if turntime == 0 and energy >= 0:
                SetTurn(0)  # Stop turning
	        checked = True
                energy += 15
                checking = False
        print "Count : %s, Turntime : %s, energy : %s" % (str(count), str(turntime), str(energy))
        time.sleep(0.1)

    # mission has ended.
    print "Count "+ str(count) + ", Mission " + str(iRepeat+1) + ": Reward = " + str(reward)
    for error in world_state.errors:
        print "Error:",error.text
    time.sleep(0.5) # Give the mod a little time to prepare for the next mission.
