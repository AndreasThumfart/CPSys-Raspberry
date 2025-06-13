from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from ikpy.chain import Chain
from ikpy.link import OriginLink
import numpy as np
import time
import math

client = RemoteAPIClient()
sim = client.getObject('sim')

# UR5-Kinematikkette laden
ur5_chain = Chain.from_urdf_file("c:\\Projekte\\CPSys-Raspberry\\CoppeliaSim\\ur5.urdf", base_elements=["base_link"])

# Handles
pioneer = sim.getObject('/PioneerP3DX')
left_motor = sim.getObject('/PioneerP3DX/leftMotor')
right_motor = sim.getObject('/PioneerP3DX/rightMotor')

ur5_tip = sim.getObject('/UR5/connection')
# ur5_target = sim.getObject('/UR5_target')
box_handle = sim.getObject('/Cuboid')

# ik_target = sim.getObject('/UR5/target')


# Gelenke des UR5
joint_names = [
    '/UR5/joint',
    '/UR5/link/joint',
    '/UR5/link/joint/link/joint',
    '/UR5/link/joint/link/joint/link/joint',
    '/UR5/link/joint/link/joint/link/joint/link/joint',
    '/UR5/link/joint/link/joint/link/joint/link/joint/link/joint'
]
joint_handles = [sim.getObject(name) for name in joint_names]

# Bewegungsparameter
deg2rad = math.pi / 180
vel = 180 * deg2rad
accel = 40 * deg2rad
jerk = 80 * deg2rad

max_vel = [vel] * 6
max_accel = [accel] * 6
max_jerk = [jerk] * 6

# Zielkonfigurationen
target_pos1 = [90, 90, -90, 90, 90, 90]
target_pos2 = [-90, 45, 90, 135, 90, 90]
target_pos3 = [0, 0, 0, 0, 0, 0]

# In Radiant umrechnen
target_pos1 = [angle * deg2rad for angle in target_pos1]
target_pos2 = [angle * deg2rad for angle in target_pos2]
target_pos3 = [angle * deg2rad for angle in target_pos3]


# Zielkoordinaten für mobilen Roboter
target_pos = [0.75,1.0, 0.137]
tolerance = 0.05


def distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


def drive_to_position(robot, left_motor, right_motor, goal, speed=1.0):
    current_pos = sim.getObjectPosition(robot, -1)

    # Einfache Steuerung: beide Motoren an, dann stoppen
    sim.setJointTargetVelocity(left_motor, speed)
    sim.setJointTargetVelocity(right_motor, speed)
    
    # time.sleep(distance / speed * 2.5)
    while True:
        current_pos = sim.getObjectPosition(pioneer, -1)
        dist = distance(current_pos, target_pos)
        if dist < tolerance:
            # Stoppe Motoren
            sim.setJointTargetVelocity(left_motor, 0.0)
            sim.setJointTargetVelocity(right_motor, 0.0)
            print("Ziel erreicht.")
            break
        time.sleep(0.05) # Kurze Pause zur Entlastung der CPU

def move_to_config(joints, target_pos, max_vel, max_accel, max_jerk):
    sim.moveToConfig({
        'joints': joints,
        'targetPos': target_pos,
        'maxVel': max_vel,
        'maxAccel': max_accel,
        'maxJerk': max_jerk
    })


print(ur5_chain.links)

# Simulation starten
# sim.setStepping(False)
sim.startSimulation()

# 1. P3DX fährt zur Zielposition
print("Pioneer fährt zur Zielposition...")
drive_to_position(pioneer, left_motor, right_motor, target_pos)
time.sleep(2)

# # 2. Greifen: UR5 bewegt sich zum Objekt
print("UR5 greift das Objekt...")
box_pos = sim.getObjectPosition(box_handle, -1)
approach_pos = [box_pos[0], box_pos[1], box_pos[2] + 0.1]

# Roboterarm zu Box bewegen
target_frame = np.eye(4)
target_frame[:3, 3] = approach_pos
joint_angles = ur5_chain.inverse_kinematics(target_frame)

move_to_config(joint_handles, joint_angles, max_vel, max_accel, max_jerk)
time.sleep(2)

# Greifen simulieren
# sim.setObjectParent(box_handle, ur5_tip, True)  # Box an UR5 befestigen

# Roboterarm zu Ziel bewegen
move_to_config(joint_handles, target_pos2, max_vel, max_accel, max_jerk)
time.sleep(2)

#
move_to_config(joint_handles, target_pos3, max_vel, max_accel, max_jerk)
time.sleep(2)



# # Warte auf Bewegung (vereinfacht)
# time.sleep(2)

# # Greifen simulieren
# sim.setObjectParent(box_handle, ur5_tip, True)  # Box an UR5 befestigen
# print("Objekt aufgenommen.")

# # 3. Zurückziehen
# home_pos = [0.0, -0.5, 0.6]
# sim.setObjectPosition(ur5_target, -1, home_pos)

# print("Bewegung abgeschlossen.")


# Stoppen
time.sleep(3)
sim.stopSimulation()