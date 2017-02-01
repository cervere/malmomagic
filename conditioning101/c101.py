import MalmoPython
import os
import random
import sys
import time
import json
import random
import errno
from collections import namedtuple
from malmoutils import *
EntityInfo = namedtuple('EntityInfo', 'x, y, z, name, quantity')
EntityInfo.__new__.__defaults__ = (0, 0, 0, "", 1)


def GetItemDrawingXML():
    ''' Build an XML string that contains 400 randomly positioned bits of food'''
    xml=""
    CS = [-45, -25, -5, 15, 35]
    for item in CS:
        x = str(2)#str(random.randint(-50,50))
        z = str(item+3)#str(random.randint(-50,50))
        type = random.choice(["apple"])
        xml += '''<DrawItem x="''' + x + '''" y="227" z="''' + z + '''" type="''' + type + '''"/>'''
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
    count = 0   # for counting turn time.
    waitCycles = 0
    turnSequence  = ""#move 1; wait 10;"
    turnSequence += "setYaw 45; wait 10;"
    turnSequence += "setYaw -45; wait 10; tpx 5.5;"
    turnSequence += "setYaw 0; "
    currentSequence = "move 1;"
    energy = 20
    while world_state.is_mission_running:
        world_state = agent_host.getWorldState()
        if world_state.number_of_observations_since_last_state > 0:
            if waitCycles > 0: waitCycles -= 1
            msg = world_state.observations[-1].text
            ob = json.loads(msg)
            current_x = ob.get(u'XPos', 0)
            current_z = ob.get(u'ZPos', 0)
            current_y = ob.get(u'YPos', 0)
            yaw = ob.get(u'Yaw', 0)
            pitch = ob.get(u'Pitch', 0)
            grid = ob.get(u'floor3x3', 0)
            print  yaw
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
                energy -= 1
                SendChat("Spending energy to JUMP. Energy left : "+str(energy))
            if grid[4]==u'cobblestone':
                currentSequence = turnSequence
            elif grid[7]==u'lava':
                agent_host.sendCommand("jump 1")
                jumping = True


        if world_state.number_of_rewards_since_last_state > 0:
            # A reward signal has come in - see what it is:
            delta = world_state.rewards[0].getValue()
            energy += delta
        if waitCycles == 0:
        # Time to execute the next command, if we have one:
            if currentSequence != "":
                commands = currentSequence.split(";", 1)
                command = commands[0].strip()
                if len(commands) > 1:
                    currentSequence = commands[1]
                else:
                    currentSequence = ""
                verb,sep,param = command.partition(" ")
                if verb == "wait":
                    waitCycles = int(param.strip())
                else:
                    agent_host.sendCommand(command) # Send the command to Minecraft.

        time.sleep(0.1)

    # mission has ended.
    print "Mission " + str(iRepeat+1) + ": Reward = " + str(reward)
    for error in world_state.errors:
        print "Error:",error.text
    time.sleep(0.5) # Give the mod a little time to prepare for the next mission.
