import PySimpleGUI as sg
import os
import json
import cv2
import pygame
import pydirectinput
import pyautogui
import time
import hand_recognition as hrs
import numpy as np

import logging

sg.theme('DarkTeal11')
pygame.mixer.init()
filepath = os.path.dirname(__file__)
CONSTANT_COMMAND_DICT = {'Index': ['', '', ''], 'Mid Finger': ['', '', ''], 'Call': ['', '', ''],
                         'Thumb Up': ['', '', ''],
                         'Thumb Down': ['', '', ''], 'Horns': ['', '', ''], 'Pinkie': ['', '', ''],
                         'Index Mid': ['', '', ''], 'Index Mid Pinkie': ['', '', ''], 'Ring Pinkie': ['', '', '']}

selected_gesture = None
detector = None
img = f"{filepath}/Resources/png/blank.png"
picture = sg.Image(img, key="-IMG-", size=(533, 300))

gesture_dict = {'Index': 'index', 'Mid Finger': 'mid_finger', 'Call': 'call', 'Thumb Up': 'thumb_up', 'Horns': 'horns',
                'Thumb Down': 'thumb_down', 'Pinkie': 'pinkie', 'Index Mid': 'index_mid',
                'Index Mid Pinkie': 'index_mid_pinkie', 'Ring Pinkie': 'pinkie_ring'}

command_dict = {'Index': ['', '', ''], 'Mid Finger': ['', '', ''], 'Call': ['', '', ''], 'Thumb Up': ['', '', ''],
                'Thumb Down': ['', '', ''], 'Horns': ['', '', ''], 'Pinkie': ['', '', ''],
                'Index Mid': ['', '', ''], 'Index Mid Pinkie': ['', '', ''], 'Ring Pinkie': ['', '', '']}

press_hold_dict = {'Index': False, 'Mid Finger': False, 'Call': False, 'Thumb Up': False,
                   'Thumb Down': False, 'Horns': False, 'Pinkie': False,
                   'Index Mid': False, 'Index Mid Pinkie': False, 'Ring Pinkie': False}
list_of_entries = []
combo_list = []
combo_options = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7',
                 '8', '9', '!', '"', '#', '$', '%', '&', "'", '(',
                 ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
                 '{', '|', '}', '~', 'alt', 'altleft', 'altright', 'backspace',
                 'capslock', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
                 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
                 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
                 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
                 'final', 'fn', 'help', 'home', 'insert', 'junja',
                 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
                 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
                 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
                 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
                 'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
                 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
                 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
                 'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'lock/unlock'
                 ]

pyautogui_commands = {'volumedown', 'volumemute', 'volumeup', 'playpause', 'prevtrack', 'nexttrack', 'tab', 'altleft',
                      'altright', 'fn', 'playpause', 'stop'}


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
    if lm_list[4][2] < lm_list[3][2] < lm_list[2][2] < lm_list[1][2] < lm_list[0][2] and lm_list[2][2] < lm_list[5][2]:
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
        if mid_finger_up(lm_list) is False and ring_finger_up(lm_list) is False and index_finger_up(lm_list) is False:
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
            if lm_list[8][1] > lm_list[6][1] and lm_list[12][1] > lm_list[10][1] and lm_list[16][1] > lm_list[14][1] and \
                    lm_list[13][2] < lm_list[0][2] < lm_list[17][2]:
                return True
        else:
            return False
    else:
        return False


def save_settings(delay, sound_volume, detection_con, track_con):
    settings_dict = {'delay': delay, 'sound_volume': sound_volume, 'detection_con': detection_con,
                     'track_con': track_con}

    with open("settings.json", 'w') as settings_save_file:
        json.dump(settings_dict, settings_save_file)


def load_settings():
    global delay
    global sound_volume
    global detection_con
    global track_con
    global detector
    settings_file = "settings.json"
    try:
        with open(settings_file, 'r') as save_file:
            settings_dict = json.load(save_file)
            delay = settings_dict['delay']
            sound_volume = settings_dict['sound_volume']
            pygame.mixer.music.set_volume(sound_volume / 100)
            detector.detection_con = settings_dict['detection_con'] / 10
            detector.track_con = settings_dict['track_con'] / 10
            detector.hands = detector.mp_hands.Hands(detector.mode, detector.max_hands, detector.detection_con,
                                                     detector.track_con)
    except Exception as ex:
        print(ex)
        pass


def macro(key_list, press_is_on):
    # Since function keys are not included in pydirectinput, pyautogui library has to be used instead.
    # First loop checks if pyautogui has to be used.
    global lock_on

    if lock_on is True:
        for i in key_list:
            if i == 'lock/unlock':
                if lock_on is True:
                    lock_on = False
                    pygame.mixer.music.load('Resources/unlocked.mp3')
                    pygame.mixer.music.play()
                    sg.popup_timed("Gestures are now un-locked", auto_close_duration=1,
                                   icon=r'Resources\manucap_icon.ico', title="Un-locked")
                else:
                    lock_on = True
            else:
                return

    for i in key_list:
        if i == 'lock/unlock':
            if lock_on is False:
                lock_on = True
                pygame.mixer.music.load('Resources/locked.mp3')
                pygame.mixer.music.play()
                sg.popup_timed("Gestures are now locked", auto_close_duration=1, icon=r'Resources\manucap_icon.ico',
                               title="Locked")
                return
        for element in pyautogui_commands:
            if i == element:
                pyautogui.hotkey(key_list[0], key_list[1], key_list[2])
                return

    # This is for the normal case when a key is to be pressed and released, not held down.
    if press_is_on is False:
        for i in key_list:
            pydirectinput.keyDown(f"{i}", _pause=False)
            time.sleep(.005)
        for i in key_list:
            pydirectinput.keyUp(f"{i}", _pause=False)
    else:
        for i in key_list:
            pydirectinput.keyDown(f"{i}", _pause=False)


def press_and_hold_macro(key_list):
    if lock_on is False:
        for i in key_list:
            for element in pyautogui_commands:
                if i == element:
                    pyautogui.keyDown(f"{i}", _pause=False)
                else:
                    pydirectinput.keyDown(f"{i}", _pause=False)


def release_macro():
    global keys_to_release
    for i in keys_to_release:
        pydirectinput.keyUp(f"{i}", _pause=False)
    keys_to_release.clear()


# New window for audio settings

def settings_window():
    global sound_volume
    global delay
    global detector

    sound_volume_frame = [[sg.Text('Sound Volume:')],
                          [sg.Slider((0, 100), orientation='h', pad=(10, 5), key='volume_slider')]]

    layout_settings = [
        [sg.Spin([i for i in range(1, 11)], pad=(0, 10), key='hand_detection'),
         sg.Text('Hand Detection Confidence')],
        [sg.Spin([i for i in range(1, 11)], initial_value=6, pad=(0, 10), key='hand_tracking'),
         sg.Text('Hand Tracking Confidence')],
        [sg.Text('Interval between each macro activation (in seconds): '), sg.InputText(default_text=delay, size=(3, 0),
                                                                                        pad=(5, 10),
                                                                                        key="delay_input")],
        [sg.Frame(layout=sound_volume_frame, title='', element_justification='center')],
        [sg.Button("OK", key="ok_settings"), sg.Cancel("Cancel", key="cancel_but")]]
    new_window = sg.Window("Settings", layout_settings, margins=(10, 10), icon=r'Resources\manucap_icon.ico',
                           element_justification='center', finalize=True)

    new_window.Element('volume_slider').update(sound_volume)  # Sets the slider to current sound volume level
    new_window.Element('hand_detection').update(
        int(detector.detection_con * 10))  # Sets the slider to current detection confidence level
    new_window.Element('hand_tracking').update(
        int(detector.track_con * 10))  # Sets the slider to current tracking confidence level

    while True:
        event, values = new_window.read()
        if event == sg.WIN_CLOSED:
            new_window.close()
            break

        if event == "ok_settings":
            delay = float(values['delay_input'])
            sound_volume = values['volume_slider']
            pygame.mixer.music.set_volume(sound_volume / 100)
            detector.detection_con = values['hand_detection'] / 10
            detector.track_con = values['hand_tracking'] / 10
            detector.hands = detector.mp_hands.Hands(detector.mode, detector.max_hands, detector.detection_con,
                                                     detector.track_con)
            save_settings(delay, sound_volume, values['hand_detection'], values['hand_tracking'])
            new_window.close()
            break

        elif event == "cancel_but":
            new_window.close()
            break

    new_window.close()


video_feed_on = False
sound_volume = 100
delay = 1
lock_on = False
button_container = [[sg.Button('Run'), sg.Button('Stop')]]

# Container for the Save and Clear buttons
save_clear_container = [[sg.Button('Save', key='command_save'), sg.Button('Clear')]]

image_and_commands_container = [[picture], [sg.Text('Type in values or select one from list:')],
                                [sg.Combo(combo_options, default_value='', key="-COMMAND_1-")],
                                [sg.Combo(combo_options, default_value='', key="-COMMAND_2-")],
                                [sg.Combo(combo_options, default_value='', key="-COMMAND_3-")],
                                [sg.Checkbox('Press and hold', key='press')]]

listbox_container = [[sg.Text('Select hand gesture:')], [sg.Listbox(
    values=['Index', 'Mid Finger', 'Call', 'Thumb Up', 'Thumb Down', 'Horns', 'Pinkie', 'Index Mid', 'Index Mid Pinkie',
            'Ring Pinkie'], enable_events=True, size=(20, 15), key='dropdown')], [sg.Button('Select')]]

left_column = [[sg.Frame(title='', layout=listbox_container, element_justification='center')]]

right_column = [[sg.Frame(title='', layout=image_and_commands_container, element_justification='center')],
                [sg.Frame(title='', layout=save_clear_container, element_justification='center', pad=(0, 0))]]

menu = [['Menu', ['Save', 'Load', '---', 'Settings', '---', 'Exit']], ['About']]

layout = [
    [sg.Menu(menu)],
    [sg.Column(left_column, element_justification='center'),
     sg.Column(right_column, element_justification='center')],
    [sg.HSeparator(pad=(0, 20))],
    [sg.Column(button_container, justification='center')],
]

cap = cv2.VideoCapture(0)
cam_w = 400
cam_h = 250
cap.set(3, cam_w)
cap.set(4, cam_h)

# List of keyes to be released once gesture is no longer shown:
keys_to_release = []

# Create the window
window = sg.Window("ManuCap", layout, icon=r'Resources\manucap_icon.ico', margins=(30, 30), resizable=True)


# Create an event loop
def main():
    global video_feed_on
    global selected_gesture
    global command_dict
    global press_hold_dict
    global detector
    global keys_to_release
    hand_detected = False

    detector = hrs.HandDetector()
    time_var = 0
    lm_list = []
    load_settings()
    while True:
        event, values = window.read(timeout=15)
        macro_release_switch = False
        if event == "Settings":
            settings_window()

        elif event == "command_save":
            command_list = command_dict.get(selected_gesture)
            if command_list is not None:
                command_list.clear()
                command_list.append(values["-COMMAND_1-"])
                command_list.append(values["-COMMAND_2-"])
                command_list.append(values["-COMMAND_3-"])
                command_dict.update({selected_gesture: command_list})
                press_hold_dict[selected_gesture] = values['press']

        elif event == "Clear":
            window.Element("-COMMAND_1-").update('')
            window.Element("-COMMAND_2-").update('')
            window.Element("-COMMAND_3-").update('')
            command_dict[selected_gesture] = ['', '', '']

        elif event == "Select":
            name = (values['dropdown'][0])
            selected_gesture = name
            pic_name = gesture_dict[name]
            img = f"{filepath}/Resources/png/{pic_name}.png"
            window["-IMG-"].update(filename=img, size=(533, 300))
            if selected_gesture is not None:
                try:
                    command_list = command_dict.get(selected_gesture)
                    window.Element("-COMMAND_1-").update(command_list[0])
                    window.Element("-COMMAND_2-").update(command_list[1])
                    window.Element("-COMMAND_3-").update(command_list[2])
                    window.Element("press").update(press_hold_dict[selected_gesture])
                except TypeError:
                    sg.popup_error(
                        'Error occured. Most likely the save file is corrupted. \nPlease try a different file. \nAll commands will default to empty values.')
                    command_dict = CONSTANT_COMMAND_DICT
                    window.Element("-COMMAND_1-").update('')
                    window.Element("-COMMAND_2-").update('')
                    window.Element("-COMMAND_3-").update('')

        elif event == "Run":

            pygame.mixer.music.load('Resources/dcs_detector_on.mp3')
            pygame.mixer.music.play()
            video_feed_on = True

        elif event == "Stop":
            img = np.full((300, 533), 0)
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['-IMG-'].update(data=imgbytes)
            video_feed_on = False

        elif event == "Save":
            filename = sg.popup_get_file('Save as:', 'Save', save_as=True, file_types=(("JSON", "*.json*"),))
            with open(f"{filename}.json", 'w') as save_file:
                json.dump((command_dict, press_hold_dict), save_file)

        elif event == "Load":
            try:
                filename = sg.popup_get_file('Select a file to load:', 'Load', file_types=(("JSON", "*.json*"),),
                                             no_window=False)
                with open(filename, 'r') as save_file:
                    command_list_from_save = json.load(save_file)
                    command_dict = command_list_from_save[0]
                    press_hold_dict = command_list_from_save[1]

                    if selected_gesture is not None:
                        command_list = command_dict.get(selected_gesture)
                        window.Element("-COMMAND_1-").update(command_list[0])
                        window.Element("-COMMAND_2-").update(command_list[1])
                        window.Element("-COMMAND_3-").update(command_list[2])
                    sg.popup_ok("File loaded")
            except Exception as ex:
                print(ex)

        elif event == "OK" or event == sg.WIN_CLOSED:
            break

        elif event == "Exit" or event == sg.WIN_CLOSED:
            break

        if video_feed_on:
            success, img = cap.read()
            img = detector.find_hands(img)
            lm_list = detector.find_position(img)
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window["-IMG-"].update(data=imgbytes, size=(533, 300))

        if len(lm_list) != 0:
            if hand_detected is False:
                pygame.mixer.music.load('Resources/dcs_hand_detected.mp3')
                pygame.mixer.music.play()
                hand_detected = True

            if horns(lm_list):
                time_fun = time.time()
                horns_list = command_dict['Horns']
                if (time_fun - time_var) > delay:
                    macro(horns_list, press_hold_dict['Horns'])
                    time_var = time_fun
                elif press_hold_dict['Horns']:
                    if len(keys_to_release) < 1:
                        keys_to_release = horns_list.copy()
                    press_and_hold_macro(horns_list)
                    macro_release_switch = True

            if index_mid_up(lm_list) and hand_up(lm_list):
                time_fun = time.time()
                index_mid_list = command_dict['Index Mid']
                if (time_fun - time_var) > delay:
                    macro(index_mid_list, press_hold_dict['Index Mid'])
                    time_var = time_fun
                elif press_hold_dict['Index Mid']:
                    if len(keys_to_release) < 1:
                        keys_to_release = index_mid_list.copy()
                    press_and_hold_macro(index_mid_list)
                    macro_release_switch = True

            if just_pinkie(lm_list) and hand_up(lm_list):
                time_fun = time.time()
                pinkie_list = command_dict['Pinkie']
                if (time_fun - time_var) > delay and press_hold_dict['Pinkie'] is False:
                    macro(pinkie_list, press_hold_dict['Pinkie'])
                    time_var = time_fun
                elif press_hold_dict['Pinkie']:
                    if len(keys_to_release) < 1:
                        keys_to_release = pinkie_list.copy()
                    press_and_hold_macro(pinkie_list)
                    macro_release_switch = True

            if just_index(lm_list) and hand_up(lm_list):
                time_fun = time.time()
                index_list = command_dict['Index']
                if (time_fun - time_var) > delay:
                    macro(index_list, press_hold_dict['Index'])
                    time_var = time_fun
                elif press_hold_dict['Index']:
                    if len(keys_to_release) < 1:
                        keys_to_release = index_list.copy()
                    press_and_hold_macro(index_list)
                    macro_release_switch = True

            if call(lm_list):
                time_fun = time.time()
                call_list = command_dict['Call']
                if (time_fun - time_var) > delay:
                    macro(call_list, press_hold_dict['Call'])
                    time_var = time_fun
                elif press_hold_dict['Call']:
                    if len(keys_to_release) < 1:
                        keys_to_release = call_list.copy()
                    press_and_hold_macro(call_list)
                    macro_release_switch = True

            if ring_pinkie_up(lm_list) and hand_up(lm_list):
                time_fun = time.time()
                ring_pinkie_list = command_dict['Ring Pinkie']
                if (time_fun - time_var) > delay:
                    macro(ring_pinkie_list, press_hold_dict['Ring Pinkie'])
                    time_var = time_fun
                elif press_hold_dict['Ring Pinkie']:
                    if len(keys_to_release) < 1:
                        keys_to_release = ring_pinkie_list.copy()
                    press_and_hold_macro(ring_pinkie_list)
                    macro_release_switch = True

            if thumb_up(lm_list):
                time_fun = time.time()
                thumb_up_list = command_dict['Thumb Up']
                if (time_fun - time_var) > delay:
                    macro(thumb_up_list, press_hold_dict['Thumb Up'])
                    time_var = time_fun
                elif press_hold_dict['Thumb Up']:
                    if len(keys_to_release) < 1:
                        keys_to_release = thumb_up_list.copy()
                    press_and_hold_macro(thumb_up_list)
                    macro_release_switch = True

            if thumb_down(lm_list):
                time_fun = time.time()
                thumb_down_list = command_dict['Thumb Down']
                if (time_fun - time_var) > delay:
                    macro(thumb_down_list, press_hold_dict['Thumb Down'])
                    time_var = time_fun
                elif press_hold_dict['Thumb Down']:
                    if len(keys_to_release) < 1:
                        keys_to_release = thumb_down_list.copy()
                    press_and_hold_macro(thumb_down_list)
                    macro_release_switch = True

            if index_mid_pinkie(lm_list):
                time_fun = time.time()
                index_mid_pinkie_list = command_dict['Index Mid Pinkie']
                if (time_fun - time_var) > delay:
                    macro(index_mid_pinkie_list, press_hold_dict['Index Mid Pinkie'])
                    time_var = time_fun
                elif press_hold_dict['Index Mid Pinkie']:
                    if len(keys_to_release) < 1:
                        keys_to_release = index_mid_pinkie_list.copy()
                    press_and_hold_macro(index_mid_pinkie_list)
                    macro_release_switch = True

            if just_mid_finger_up(lm_list):
                time_fun = time.time()
                mid_finger_list = command_dict['Mid Finger']
                if (time_fun - time_var) > delay:
                    macro(mid_finger_list, press_hold_dict['Mid Finger'])
                    time_var = time_fun
                elif press_hold_dict['Mid Finger']:
                    if len(keys_to_release) < 1:
                        keys_to_release = mid_finger_list.copy()
                    press_and_hold_macro(mid_finger_list)
                    macro_release_switch = True

            if len(keys_to_release) > 0 and macro_release_switch is False:
                release_macro()
                keys_to_release.clear()

        else:
            if hand_detected is True:
                pygame.mixer.music.load('Resources/dcs_no_hand.mp3')
                pygame.mixer.music.play()
                hand_detected = False

            if len(keys_to_release) > 0:
                release_macro()
                keys_to_release.clear()

    window.close()


if __name__ == "__main__":
    main()
