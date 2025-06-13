# from zmqRemoteApi import RemoteAPIClient # use the local source code for testing
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.getObject('sim')

# Start simulation
sim.setStepping(True)
sim.startSimulation()

# Get handle and set joint position
# joint_handle = sim.getObject('/joint1')
# sim.setJointTargetPosition(joint_handle, 1.0)

# Get motor handles
left_motor = sim.getObject('/PioneerP3DX/leftMotor')
right_motor = sim.getObject('/PioneerP3DX/rightMotor')

# Set target velocities (in radians/second)
sim.setJointTargetVelocity(left_motor, 2.0)
sim.setJointTargetVelocity(right_motor, 2.0)

# Let it move for 5 seconds
start_time = sim.getSimulationTime()
while sim.getSimulationTime() - start_time < 5:
    sim.step()

# Stop the robot
sim.setJointTargetVelocity(left_motor, 0.0)
sim.setJointTargetVelocity(right_motor, 0.0)

# Stop simulation after a delay
sim.stopSimulation()
