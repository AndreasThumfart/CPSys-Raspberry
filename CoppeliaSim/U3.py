from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import math

client = RemoteAPIClient()
sim = client.require('sim')

# Handles
robot = sim.getObject('/PioneerP3DX')
left_motor = sim.getObject('/PioneerP3DX/leftMotor')
right_motor = sim.getObject('/PioneerP3DX/rightMotor')
sensors = [sim.getObject(f'/PioneerP3DX/ultrasonicSensor[{i}]') for i in range(16)]
waypoints = [sim.getObject(f'/wp{i}') for i in range(1, 9)]

# Parameter
v0 = 2.0
noDetectionDist = 0.4
maxDetectionDist = 0.2
braitenbergL = [-0.8, -1.0, -1.0, -1.2, -1.4, -1.6, -1.6, -1.6, 0.0, 0.0,0.0,0.0,0.0,0.0,0.0,0.0]
braitenbergR = [0.8, 1.0, 1.0, 1.2, 1.4, 1.6, 1.6, 1.6, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
detect = [0.0] * 16
threshold = 0.2

def get_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def get_angle_to_target(robot_pos, robot_ori, target_pos):
    dx = target_pos[0] - robot_pos[0]
    dy = target_pos[1] - robot_pos[1]
    angle_to_target = math.atan2(dy, dx)
    robot_yaw = robot_ori[2]
    return angle_to_target - robot_yaw

def update_sensor_readings():
    for i, sensor in enumerate(sensors):
        res, dist, *_ = sim.readProximitySensor(sensor)
        if res > 0 and dist < noDetectionDist:
            dist = max(dist, maxDetectionDist)
            detect[i] = 1 - ((dist - maxDetectionDist) / (noDetectionDist - maxDetectionDist))
        else:
            detect[i] = 0.0

def compute_braitenberg_speeds():
    vL = sum(braitenbergL[i] * detect[i] for i in range(16))
    vR = sum(braitenbergR[i] * detect[i] for i in range(16))
    return vL, vR

def compute_goal_speeds(angle_to_target):
    # Einfacher P-Regler für Drehung
    turn_gain = 2.0
    turn = turn_gain * angle_to_target
    return v0 - turn, v0 + turn

def move_robot(vL, vR):
    sim.setJointTargetVelocity(left_motor, vL)
    sim.setJointTargetVelocity(right_motor, vR)

# Simulation starten
sim.setStepping(True)
sim.startSimulation()

for wp in waypoints:
    target_pos = sim.getObjectPosition(wp, -1)
    print(wp)
    while True:
        sim.step()
        robot_pos = sim.getObjectPosition(robot, -1)
        robot_ori = sim.getObjectOrientation(robot, -1)

        if get_distance(robot_pos, target_pos) < threshold:
            break

        update_sensor_readings()
        angle = get_angle_to_target(robot_pos, robot_ori, target_pos)

        # Steuerung berechnen
        v_goal_L, v_goal_R = compute_goal_speeds(angle)
        v_brai_L, v_brai_R = compute_braitenberg_speeds()

        # Kombinieren: 50% Navigation, 50% Hindernisvermeidung
        vL = 0.5 * v_goal_L + 0.5 * v_brai_L
        vR = 0.5 * v_goal_R + 0.5 * v_brai_R

        move_robot(vL, vR)

# Stoppen
move_robot(0, 0)
sim.stopSimulation()
