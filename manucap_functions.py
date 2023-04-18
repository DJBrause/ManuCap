def hand_up(lm_list):
    wrist_height = lm_list[0][2]
    hand_is_up = True
    for element in list(lm_list):
        if element[0] != 0:
            if element[2] > wrist_height:
                hand_is_up = False
    return hand_is_up


def index_finger_up(lm_list):
    if lm_list[8][2] < lm_list[7][2] < lm_list[6][2] < lm_list[5][2]:
        return True
    else:
        return False


def mid_finger_up(lm_list):
    if lm_list[12][2] < lm_list[11][2] < lm_list[10][2] < lm_list[9][2]:
        return True
    else:
        return False


def just_mid_finger_up(lm_list):
    if mid_finger_up(lm_list) and index_finger_up(lm_list) is False and pinkie_up(lm_list) is False and ring_finger_up(
            lm_list) is False:
        return True
    else:
        return False


def ring_finger_up(lm_list):
    if lm_list[16][2] < lm_list[15][2] < lm_list[14][2] < lm_list[13][2]:
        return True
    else:
        return False


def pinkie_up(lm_list):
    if lm_list[20][2] < lm_list[19][2] < lm_list[18][2] < lm_list[17][2]:
        return True
    else:
        return False


def thumb_up(lm_list):  # Hand has to be opened as well due to amend detection issues.
    if lm_list[4][2] < lm_list[3][2] < lm_list[2][2] < lm_list[1][2] < lm_list[0][2] and lm_list[2][2] < lm_list[5][
        2]:
        if lm_list[8][1] < lm_list[6][1] and lm_list[20][1] < lm_list[18][1] and \
                lm_list[4][1] > (lm_list[5][1] + 40):
            return True
        else:
            return False
    else:
        return False


def thumb_down(lm_list):  # Hand has to be opened as well due to amend detection issues.
    if lm_list[4][2] > lm_list[3][2] > lm_list[2][2] > lm_list[1][2] > lm_list[0][2] and lm_list[2][2] > lm_list[5][2]:
        if lm_list[8][1] < lm_list[6][1] and lm_list[20][1] < lm_list[18][1] and \
                lm_list[4][1] > (lm_list[5][1] + 40):
            return True
        else:
            return False
    else:
        return False


def horns(lm_list):
    if index_finger_up(lm_list) and pinkie_up(lm_list) and mid_finger_up(lm_list) is False and ring_finger_up(
            lm_list) is False:
        return True
    else:
        return False


def index_mid_up(lm_list):
    if index_finger_up(lm_list) and mid_finger_up(lm_list):
        if ring_finger_up(lm_list) is False and pinkie_up(lm_list) is False:
            return True
        else:
            return False
    else:
        return False


def index_mid_pinkie(lm_list):
    if index_finger_up(lm_list) and mid_finger_up(lm_list) and pinkie_up(lm_list):
        if ring_finger_up(lm_list) is False:
            return True
        else:
            return False
    else:
        return False


def ring_pinkie_up(lm_list):
    if ring_finger_up(lm_list) and pinkie_up(lm_list):
        if index_finger_up(lm_list) is False and mid_finger_up(lm_list) is False:
            return True
        else:
            return False
    else:
        return False


def just_pinkie(lm_list):
    if pinkie_up(lm_list) is True and lm_list[5][2] > lm_list[18][2]:
        if mid_finger_up(lm_list) is False and ring_finger_up(lm_list) is False and index_finger_up(
                lm_list) is False:
            return True
        else:
            return False
    else:
        return False


def just_index(lm_list):
    if index_finger_up(lm_list) is True:
        if mid_finger_up(lm_list) is False and ring_finger_up(lm_list) is False and pinkie_up(lm_list) is False:
            return True
        else:
            return False
    else:
        return False


def call(lm_list):
    if lm_list[4][2] < lm_list[3][2] < lm_list[2][2] < lm_list[1][2] < lm_list[0][2]:
        if lm_list[20][1] < lm_list[19][1] < lm_list[18][1] < lm_list[17][1]:
            if lm_list[8][1] > lm_list[6][1] and lm_list[12][1] > lm_list[10][1] and lm_list[16][1] > lm_list[14][
                1] and \
                    lm_list[13][2] < lm_list[0][2] < lm_list[17][2]:
                return True
        else:
            return False
    else:
        return False


