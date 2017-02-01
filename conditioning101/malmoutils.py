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
		    <DrawBlock x="5"  y="226" z="9" type="lava" />
		    <DrawBlock x="5"  y="226" z="14" type="lava" />
		    <DrawBlock x="5"  y="226" z="19" type="lava" />
		    <DrawBlock x="5"  y="226" z="29" type="lava" />
		    <DrawBlock x="5"  y="226" z="39" type="lava" />
		    <DrawBlock x="5"  y="226" z="50" type="lapis_block" />
		    <DrawBlock x="5"  y="226" z="35" type="cobblestone" />
		    <DrawBlock x="5"  y="226" z="15" type="cobblestone" />
		    <DrawBlock x="5"  y="226" z="-5" type="cobblestone" />
		    <DrawBlock x="5"  y="226" z="-25" type="cobblestone" />
		    <DrawBlock x="5"  y="226" z="-45" type="cobblestone" />
                    ''' + itemDrawingXML + '''
                </DrawingDecorator>
                <ServerQuitFromTimeUp timeLimitMs="50000"/>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>The Hungry Caterpillar</Name>
            <AgentStart>
                <Placement x="5.5" y="227.0" z="-49.5"/>
                <Inventory>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <InventoryCommands/>
                <ChatCommands/>
                <AbsoluteMovementCommands/>
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
                <ContinuousMovementCommands turnSpeedDegs="50"/>
                <ObservationFromFullStats/>
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
