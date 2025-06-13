import math
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient


# Verbindung zur CoppeliaSim-Instanz
client = RemoteAPIClient()
sim = client.require('sim')

# Hole Joint-Handles
joint_names = [
    '/NiryoOne/Joint',
    '/NiryoOne/Link/Joint',
    '/NiryoOne/Link/Joint/Link/Joint',
    '/NiryoOne/Link/Joint/Link/Joint/Link/Joint',
    '/NiryoOne/Link/Joint/Link/Joint/Link/Joint/Link/Joint',
    '/NiryoOne/Link/Joint/Link/Joint/Link/Joint/Link/Joint/Link/Joint'
]
joint_handles = [sim.getObject(name) for name in joint_names]


# Hole Greifer-Name
connection = sim.getObject('/connection')
gripper = sim.getObjectChild(connection, 0)
if gripper != -1:
    gripper_name = sim.getObjectAlias(gripper, 4)
else:
    gripper_name = 'NiryoNoGripper'
# gripper_name="NiryoLGripper"

# RML-Parameter
deg2rad = math.pi / 180
vel = 20 * deg2rad
accel = 40 * deg2rad
jerk = 80 * deg2rad
max_vel = [vel] * 6
max_accel = [accel] * 6
max_jerk = [jerk] * 6

# Zielpositionen
target_pos1 = [90 * deg2rad, -54 * deg2rad, 0, 0, -36 * deg2rad, -90 * deg2rad]
target_pos2 = [-90 * deg2rad, -54 * deg2rad, 0, 0, -36 * deg2rad, -90 * deg2rad]
target_pos3 = [0, 0, 0, 0, 0, 0]



def move_to_config(joints, target_pos, max_vel, max_accel, max_jerk):
    #sim.moveToConfig([0], [0], joints, [], [], [], target_pos, max_vel, max_accel, max_jerk)
    sim.moveToConfig({
        'joints': joints,
        'targetPos': target_pos,
        'maxVel': max_vel,
        'maxAccel': max_accel,
        'maxJerk': max_jerk
    })

# Simulation starten
sim.setStepping(True)
sim.startSimulation()


sim.clearInt32Signal(gripper_name + '_close') #greifer öffnen
print("Greifer geöffnet")
time.sleep(2)


# Bewegung 1: Greifen
move_to_config(joint_handles, target_pos1, max_vel, max_accel, max_jerk)
time.sleep(2)
sim.setInt32Signal(gripper_name + '_close', 1) #greifer schließen
print("Greifer geschlossen")
time.sleep(3)


# Bewegung 2: Zurück zur Mitte
move_to_config(joint_handles, target_pos3, max_vel, max_accel, max_jerk)


# Bewegung 3: Ablegen
move_to_config(joint_handles, target_pos2, max_vel, max_accel, max_jerk)
sim.clearInt32Signal(gripper_name + '_close') #greifer öffnen
print("Greifer geöffnet")
time.sleep(4)

# Bewegung 4: Zurück zur Mitte
move_to_config(joint_handles, target_pos3, max_vel, max_accel, max_jerk)

# Stoppen
sim.stopSimulation()
