import time
import random
from robodk.robolink import *
from robodk.robomath import *

RDK = Robolink()

# item select
robot = RDK.Item('RoboDK RDK-COBOT-1200', ITEM_TYPE_ROBOT)
gripper = RDK.Item('RobotiQ 2F-140 Gripper (Mechanism)')
table = RDK.Item('Table 1400x800x800mm')
tool = RDK.Item('Tool 1')
robot.setPoseTool(tool)

# box random postion range
MIN_X, MAX_X = 100, 700
MIN_Y, MAX_Y = -900, -400
BOX_SIZE = 110  #box size with gap

placed_positions = []  # box position list for checking

# define box positon without collsions
box_list = []
for i in range(1, 11):
    box = RDK.Item(f'boxs {i}')
    if box.Valid():
        while True:
            rand_x = random.uniform(MIN_X, MAX_X - 100)
            rand_y = random.uniform(MIN_Y, MAX_Y - 100)

            # (Overlap check)
            overlap = False
            for (px, py) in placed_positions:
                if abs(rand_x - px) < BOX_SIZE and abs(rand_y - py) < BOX_SIZE:
                    overlap = True
                    break

            if not overlap:
                placed_positions.append((rand_x, rand_y))
                box.setPose(transl(rand_x, rand_y, 50))
                break  # জায়গা পাওয়া গেছে, তাই লুপ থেকে বের হয়ে যাবে

        # color set(Red, Green, Blue)
        color_choice = random.choice([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
        box.setColor(color_choice)
        box_list.append(box)

# home position of robot
home_joints = [-1.71, 19.62, -98.34, -5.12, 89.57, 104.08]
robot.MoveJ(home_joints)

time.sleep(1)

r_cnt, g_cnt, b_cnt = 0, 0, 0

for target_box in box_list:
    box_pos = target_box.Pose()
    x, y, z = box_pos.Pos()
    color = target_box.Color()

    # sorting location with color.
    if color == [1, 0, 0, 1]:
        p_x, p_y = 1000 - (r_cnt * 120), -200
        r_cnt += 1
    elif color == [0, 1, 0, 1]:
        p_x, p_y = 1000 - (g_cnt * 120), 0
        g_cnt += 1
    else:
        p_x, p_y = 1000 - (b_cnt * 120), 200
        b_cnt += 1

    # pick and place movements
    pick_target = transl(x, y, z) * rotx(pi) * rotz(pi / 2)
    pick_apprch = transl(x, y, z + 150) * rotx(pi) * rotz(pi / 2)
    place_target = transl(p_x, p_y, 50) * rotx(pi) * rotz(pi / 2)
    place_apprch = transl(p_x, p_y, 200) * rotx(pi) * rotz(pi / 2)

    robot.MoveJ(pick_apprch)
    robot.MoveL(pick_target)
    gripper.setJoints([100])
    time.sleep(0.5)
    target_box.setParentStatic(gripper)
    robot.MoveL(pick_apprch)

    robot.MoveJ(place_apprch)
    robot.MoveL(place_target)
    gripper.setJoints([140])
    target_box.setParentStatic(table)
    time.sleep(0.5)
    robot.MoveL(place_apprch)

robot.MoveJ(home_joints)