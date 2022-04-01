def check_pose(objects, normalized_peaks):

    i = 18
    neck = 6
    neck_posx = []
    neck_posy = []
    left_ankle = 7
    left_ankle_posx = []
    left_ankle_posy = []
    right_ankle= 12
    right_ankle_posx = []
    right_ankle_posy = []
    height = 224
    width = 224
    fall_value = 20
    pose_position = 0

    obj = objects[0][i]
    C = obj.shape[0]
    for j in range(C):
        k = int(obj[j])
        if k >= 0:
            peak = normalized_peaks[0][j][k]
            x = round(float(peak[1]) * width)
            y = round(float(peak[0]) * height)
            if j == neck:
                neck_posx = x
                neck_posy = y
            if j == left_ankle:
                left_ankle_posx = x
                left_ankle_posy = y
            if j == right_ankle:
                right_ankle_posx = x
                right_ankle_posy = y
        else:
            pose_position = 0

    if neck_posy - left_ankle_posy < fall_value:
        pose_position = -1
    
    elif neck_posy - right_ankle_posy < fall_value:
        pose_position = -1

    elif neck_posx - left_ankle_posx < fall_value or neck_posx - right_ankle_posx < fall_value:
        pose_position = 2

    else:
        pose_position = 1

    print(pose_position)
    return pose_position