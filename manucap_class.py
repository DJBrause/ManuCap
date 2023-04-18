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
import manucap_functions as mf
import logging


class Manucap:
    def __init__(self):
        self.lm_list = []
        self.time_var = 0
        self.hand_detected = False
        sg.theme('DarkTeal11')
        pygame.mixer.init()
        # Model complexity needs to be 1 at all time. This if for detector.hands
        self.model_complexity = 1
        self.filepath = os.path.dirname(__file__)
        self.CONSTANT_COMMAND_DICT = {'Index': ['', '', ''], 'Mid Finger': ['', '', ''], 'Call': ['', '', ''],
                                      'Thumb Up': ['', '', ''],
                                      'Thumb Down': ['', '', ''], 'Horns': ['', '', ''], 'Pinkie': ['', '', ''],
                                      'Index Mid': ['', '', ''], 'Index Mid Pinkie': ['', '', ''],
                                      'Ring Pinkie': ['', '', '']}

        # List of keyes to be released once gesture is no longer shown:
        self.keys_to_release = []


        self.video_feed_on = False
        self.sound_volume = 100
        self.delay = 1
        self.lock_on = False
        self.selected_gesture = None
        self.detector = None
        self.img = f"{self.filepath}/Resources/png/blank.png"
        self.picture = sg.Image(self.img, key="-IMG-", size=(533, 300))

        self.gesture_dict = {'Index': 'index', 'Mid Finger': 'mid_finger', 'Call': 'call', 'Thumb Up': 'thumb_up',
                             'Horns': 'horns',
                             'Thumb Down': 'thumb_down', 'Pinkie': 'pinkie', 'Index Mid': 'index_mid',
                             'Index Mid Pinkie': 'index_mid_pinkie', 'Ring Pinkie': 'pinkie_ring'}

        self.command_dict = {'Index': ['', '', ''], 'Mid Finger': ['', '', ''], 'Call': ['', '', ''],
                             'Thumb Up': ['', '', ''],
                             'Thumb Down': ['', '', ''], 'Horns': ['', '', ''], 'Pinkie': ['', '', ''],
                             'Index Mid': ['', '', ''], 'Index Mid Pinkie': ['', '', ''], 'Ring Pinkie': ['', '', '']}

        self.press_hold_dict = {'Index': False, 'Mid Finger': False, 'Call': False, 'Thumb Up': False,
                                'Thumb Down': False, 'Horns': False, 'Pinkie': False,
                                'Index Mid': False, 'Index Mid Pinkie': False, 'Ring Pinkie': False}
        self.list_of_entries = []
        self.combo_list = []
        self.combo_options = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                              'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6',
                              '7',
                              '8', '9', '!', '"', '#', '$', '%', '&', "'", '(',
                              ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^',
                              '_', '`',
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
                              'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
                              'lock/unlock'
                              ]

        self.pyautogui_commands = {'volumedown', 'volumemute', 'volumeup', 'playpause', 'prevtrack', 'nexttrack', 'tab',
                                   'altleft',
                                   'altright', 'fn', 'playpause', 'stop'}

        self.button_container = [[sg.Button('Run'), sg.Button('Stop')]]

        # Container for the Save and Clear buttons
        self.save_clear_container = [[sg.Button('Save', key='command_save'), sg.Button('Clear')]]

        self.image_and_commands_container = [[self.picture], [sg.Text('Type in values or select one from list:')],
                                             [sg.Combo(self.combo_options, default_value='', key="-COMMAND_1-")],
                                             [sg.Combo(self.combo_options, default_value='', key="-COMMAND_2-")],
                                             [sg.Combo(self.combo_options, default_value='', key="-COMMAND_3-")],
                                             [sg.Checkbox('Press and hold', key='press')]]

        self.listbox_container = [[sg.Text('Select hand gesture:')], [sg.Listbox(
            values=['Index', 'Mid Finger', 'Call', 'Thumb Up', 'Thumb Down', 'Horns', 'Pinkie', 'Index Mid',
                    'Index Mid Pinkie',
                    'Ring Pinkie'], enable_events=True, size=(20, 15), key='dropdown')], [sg.Button('Select')]]

        self.left_column = [[sg.Frame(title='', layout=self.listbox_container, element_justification='center')]]

        self.right_column = [[sg.Frame(title='', layout=self.image_and_commands_container,
                                       element_justification='center')],
                             [sg.Frame(title='', layout=self.save_clear_container, element_justification='center',
                                       pad=(0, 0))]]

        self.menu = [['Menu', ['Save', 'Load', '---', 'Settings', '---', 'Exit']], ['About']]

        self.layout = [
            [sg.Menu(self.menu)],
            [sg.Column(self.left_column, element_justification='center'),
             sg.Column(self.right_column, element_justification='center')],
            [sg.HSeparator(pad=(0, 20))],
            [sg.Column(self.button_container, justification='center')],
        ]

        self.cap = cv2.VideoCapture(0)
        self.cam_w = 400
        self.cam_h = 250
        self.cap.set(3, self.cam_w)
        self.cap.set(4, self.cam_h)

        # Create the window
        self.window = sg.Window("ManuCap", self.layout, icon=r'Resources\manucap_icon.ico', margins=(30, 30),
                                resizable=True)

    def load_settings(self):
        # global delay
        # global sound_volume
        # global detection_con
        # global track_con
        # global detector
        settings_file = "settings.json"
        try:
            with open(settings_file, 'r') as save_file:
                settings_dict = json.load(save_file)
                self.delay = settings_dict['delay']
                self.sound_volume = settings_dict['sound_volume']
                pygame.mixer.music.set_volume(self.sound_volume / 100)
                self.detector.detection_con = settings_dict['detection_con'] / 10
                self.detector.track_con = settings_dict['track_con'] / 10
                self.detector.hands = self.detector.mp_hands.Hands(self.detector.mode, self.detector.max_hands,
                                                                   self.model_complexity, self.detector.detection_con,
                                                                   self.detector.track_con)
        except FileNotFoundError:
            with open("settings.json", 'w') as settings_save_file:
                json.dump(None, settings_save_file)

        except TypeError:
            pass

    def macro(self, key_list, press_is_on):
        # Since function keys are not included in pydirectinput, pyautogui library has to be used instead.
        # First loop checks if pyautogui has to be used.

        if self.lock_on is True:
            for i in key_list:
                if i == 'lock/unlock':
                    if self.lock_on is True:
                        self.lock_on = False
                        pygame.mixer.music.load('Resources/unlocked.mp3')
                        pygame.mixer.music.play()
                        sg.popup_timed("Gestures are now un-locked", auto_close_duration=1,
                                       icon=r'Resources\manucap_icon.ico', title="Un-locked")
                    else:
                        self.lock_on = True
                else:
                    return

        for i in key_list:
            if i == 'lock/unlock':
                if self.lock_on is False:
                    self.lock_on = True
                    pygame.mixer.music.load('Resources/locked.mp3')
                    pygame.mixer.music.play()
                    sg.popup_timed("Gestures are now locked", auto_close_duration=1, icon=r'Resources\manucap_icon.ico',
                                   title="Locked")
                    return
            for element in self.pyautogui_commands:
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

    def press_and_hold_macro(self, key_list):
        if self.lock_on is False:
            for i in key_list:
                for element in self.pyautogui_commands:
                    if i == element:
                        pyautogui.keyDown(f"{i}", _pause=False)
                    else:
                        pydirectinput.keyDown(f"{i}", _pause=False)

    def release_macro(self):

        for i in self.keys_to_release:
            pydirectinput.keyUp(f"{i}", _pause=False)
        self.keys_to_release.clear()

    # New window for audio settings

    def settings_window(self):
        sound_volume_frame = [[sg.Text('Sound Volume:')],
                              [sg.Slider((0, 100), orientation='h', pad=(10, 5), key='volume_slider')]]

        layout_settings = [
            [sg.Spin([i for i in range(1, 11)], pad=(0, 10), key='hand_detection'),
             sg.Text('Hand Detection Confidence')],
            [sg.Spin([i for i in range(1, 11)], initial_value=6, pad=(0, 10), key='hand_tracking'),
             sg.Text('Hand Tracking Confidence')],
            [sg.Text('Interval between each macro activation (in seconds): '),
             sg.InputText(default_text=self.delay, size=(3, 0),
                          pad=(5, 10),
                          key="delay_input")],
            [sg.Frame(layout=sound_volume_frame, title='', element_justification='center')],
            [sg.Button("OK", key="ok_settings"), sg.Cancel("Cancel", key="cancel_but")]]
        new_window = sg.Window("Settings", layout_settings, margins=(10, 10), icon=r'Resources\manucap_icon.ico',
                               element_justification='center', finalize=True)

        new_window.Element('volume_slider').update(self.sound_volume)  # Sets the slider to current sound volume level
        new_window.Element('hand_detection').update(
            int(self.detector.detection_con * 10))  # Sets the slider to current detection confidence level
        new_window.Element('hand_tracking').update(
            int(self.detector.track_con * 10))  # Sets the slider to current tracking confidence level

        while True:
            event, values = new_window.read()
            if event == sg.WIN_CLOSED:
                new_window.close()
                break

            if event == "ok_settings":
                self.delay = float(values['delay_input'])
                self.sound_volume = values['volume_slider']
                pygame.mixer.music.set_volume(self.sound_volume / 100)
                self.detector.detection_con = values['hand_detection'] / 10
                self.detector.track_con = values['hand_tracking'] / 10
                self.detector.hands = self.detector.mp_hands.Hands(self.detector.mode, self.detector.max_hands, self.model_complexity,
                                                                   self.detector.detection_con, self.detector.track_con)
                self.save_settings(self.delay, self.sound_volume, values['hand_detection'], values['hand_tracking'])
                new_window.close()
                break

            elif event == "cancel_but":
                new_window.close()
                break

        new_window.close()

    def save_settings(self, delay, sound_volume, detection_con, track_con):
        settings_dict = {'delay': delay, 'sound_volume': sound_volume, 'detection_con': detection_con,
                         'track_con': track_con}

        with open("settings.json", 'w') as settings_save_file:
            json.dump(settings_dict, settings_save_file)


    # Create an event loop
    def main(self):
        self.detector = hrs.HandDetector()
        self.load_settings()

        while True:
            event, values = self.window.read(timeout=15)
            macro_release_switch = False
            if event == "Settings":
                self.settings_window()

            elif event == "command_save":
                command_list = self.command_dict.get(self.selected_gesture)
                if command_list is not None:
                    command_list.clear()
                    command_list.append(values["-COMMAND_1-"])
                    command_list.append(values["-COMMAND_2-"])
                    command_list.append(values["-COMMAND_3-"])
                    self.command_dict.update({self.selected_gesture: command_list})
                    self.press_hold_dict[self.selected_gesture] = values['press']

            elif event == "Clear":
                self.window.Element("-COMMAND_1-").update('')
                self.window.Element("-COMMAND_2-").update('')
                self.window.Element("-COMMAND_3-").update('')
                self.command_dict[self.selected_gesture] = ['', '', '']

            elif event == "Select":
                name = (values['dropdown'][0])
                self.selected_gesture = name
                pic_name = self.gesture_dict[name]
                img = f"{self.filepath}/Resources/png/{pic_name}.png"
                self.window["-IMG-"].update(filename=img, size=(533, 300))
                if self.selected_gesture is not None:
                    try:
                        command_list = self.command_dict.get(self.selected_gesture)
                        self.window.Element("-COMMAND_1-").update(command_list[0])
                        self.window.Element("-COMMAND_2-").update(command_list[1])
                        self.window.Element("-COMMAND_3-").update(command_list[2])
                        self.window.Element("press").update(self.press_hold_dict[self.selected_gesture])
                    except TypeError:
                        sg.popup_error(
                            'Error occured. Most likely the save file is corrupted. \nPlease try a different file. \nAll commands will default to empty values.')
                        self.command_dict = self.CONSTANT_COMMAND_DICT
                        self.window.Element("-COMMAND_1-").update('')
                        self.window.Element("-COMMAND_2-").update('')
                        self.window.Element("-COMMAND_3-").update('')

            elif event == "Run":

                pygame.mixer.music.load('Resources/dcs_detector_on.mp3')
                pygame.mixer.music.play()
                self.video_feed_on = True

            elif event == "Stop":
                img = np.full((300, 533), 0)
                imgbytes = cv2.imencode('.png', img)[1].tobytes()
                self.window['-IMG-'].update(data=imgbytes)
                self.video_feed_on = False

            elif event == "Save":
                self.filename = sg.popup_get_file('Save as:', 'Save', save_as=True, file_types=(("JSON", "*.json*"),))
                with open(f"{self.filename}.json", 'w') as save_file:
                    json.dump((self.command_dict, press_hold_dict), save_file)

            elif event == "Load":
                try:
                    self.filename = sg.popup_get_file('Select a file to load:', 'Load', file_types=(("JSON", "*.json*"),),
                                                 no_window=False)
                    with open(self.filename, 'r') as save_file:
                        command_list_from_save = json.load(save_file)
                        self.command_dict = command_list_from_save[0]
                        press_hold_dict = command_list_from_save[1]

                        if self.selected_gesture is not None:
                            command_list = self.command_dict.get(self.selected_gesture)
                            self.window.Element("-COMMAND_1-").update(command_list[0])
                            self.window.Element("-COMMAND_2-").update(command_list[1])
                            self.window.Element("-COMMAND_3-").update(command_list[2])
                        sg.popup_ok("File loaded")
                except Exception as ex:
                    print(ex)

            elif event == "OK" or event == sg.WIN_CLOSED:
                break

            elif event == "Exit" or event == sg.WIN_CLOSED:
                break

            if self.video_feed_on:
                success, img = self.cap.read()
                img = self.detector.find_hands(img)
                self.lm_list = self.detector.find_position(img)
                imgbytes = cv2.imencode('.png', img)[1].tobytes()
                self.window["-IMG-"].update(data=imgbytes, size=(533, 300))

            if len(self.lm_list) != 0:
                if self.hand_detected is False:
                    pygame.mixer.music.load('Resources/dcs_hand_detected.mp3')
                    pygame.mixer.music.play()
                    self.hand_detected = True

                if mf.horns(self.lm_list):
                    time_fun = time.time()
                    horns_list = self.command_dict['Horns']
                    if (time_fun - self.time_var) > self.delay:
                        self.macro(horns_list, self.press_hold_dict['Horns'])
                        self.time_var = time_fun
                    elif self.press_hold_dict['Horns']:
                        if len(self.keys_to_release) < 1:
                            self.keys_to_release = horns_list.copy()
                        self.press_and_hold_macro(horns_list)
                        macro_release_switch = True

                if mf.index_mid_up(self.lm_list) and mf.hand_up(self.lm_list):
                    time_fun = time.time()
                    index_mid_list = self.command_dict['Index Mid']
                    if (time_fun - self.time_var) > self.delay:
                        self.macro(index_mid_list, self.press_hold_dict['Index Mid'])
                        self.time_var = time_fun
                    elif self.press_hold_dict['Index Mid']:
                        if len(self.keys_to_release) < 1:
                            self.keys_to_release = index_mid_list.copy()
                        self.press_and_hold_macro(index_mid_list)
                        macro_release_switch = True

                if mf.just_pinkie(self.lm_list) and mf.hand_up(self.lm_list):
                    time_fun = time.time()
                    pinkie_list = self.command_dict['Pinkie']
                    if (time_fun - self.time_var) > self.delay and self.press_hold_dict['Pinkie'] is False:
                        self.macro(pinkie_list, press_hold_dict['Pinkie'])
                        self.time_var = time_fun
                    elif self.press_hold_dict['Pinkie']:
                        if len(self.keys_to_release) < 1:
                            self.keys_to_release = pinkie_list.copy()
                        self.press_and_hold_macro(pinkie_list)
                        macro_release_switch = True

                if mf.just_index(self.lm_list) and mf.hand_up(self.lm_list):
                    time_fun = time.time()
                    index_list = self.command_dict['Index']
                    if (time_fun - self.time_var) > self.delay:
                        self.macro(index_list, self.press_hold_dict['Index'])
                        self.time_var = time_fun
                    elif self.press_hold_dict['Index']:
                        if len(self.keys_to_release) < 1:
                            self.keys_to_release = index_list.copy()
                        self.press_and_hold_macro(index_list)
                        macro_release_switch = True

                if mf.call(self.lm_list):
                    time_fun = time.time()
                    call_list = self.command_dict['Call']
                    if (time_fun - self.time_var) > self.delay:
                        self.macro(call_list, self.press_hold_dict['Call'])
                        self.time_var = time_fun
                    elif self.press_hold_dict['Call']:
                        if len(self.keys_to_release) < 1:
                            keys_to_release = call_list.copy()
                        self.press_and_hold_macro(call_list)
                        macro_release_switch = True

                if mf.ring_pinkie_up(self.lm_list) and mf.hand_up(self.lm_list):
                    time_fun = time.time()
                    ring_pinkie_list = self.command_dict['Ring Pinkie']
                    if (time_fun - self.time_var) > self.delay:
                        self.macro(ring_pinkie_list, self.press_hold_dict['Ring Pinkie'])
                        self.time_var = time_fun
                    elif self.press_hold_dict['Ring Pinkie']:
                        if len(self.keys_to_release) < 1:
                            self.keys_to_release = ring_pinkie_list.copy()
                        self.press_and_hold_macro(ring_pinkie_list)
                        macro_release_switch = True

                if mf.thumb_up(self.lm_list):
                    time_fun = time.time()
                    thumb_up_list = self.command_dict['Thumb Up']
                    if (time_fun - self.time_var) > self.delay:
                        self.macro(thumb_up_list, self.press_hold_dict['Thumb Up'])
                        self.time_var = time_fun
                    elif self.press_hold_dict['Thumb Up']:
                        if len(self.keys_to_release) < 1:
                            self.keys_to_release = thumb_up_list.copy()
                        self.press_and_hold_macro(thumb_up_list)
                        macro_release_switch = True

                if mf.thumb_down(self.lm_list):
                    time_fun = time.time()
                    thumb_down_list = self.command_dict['Thumb Down']
                    if (time_fun - self.time_var) > self.delay:
                        self.macro(thumb_down_list, self.press_hold_dict['Thumb Down'])
                        self.time_var = time_fun
                    elif press_hold_dict['Thumb Down']:
                        if len(self.keys_to_release) < 1:
                            keys_to_release = thumb_down_list.copy()
                        self.press_and_hold_macro(thumb_down_list)
                        macro_release_switch = True

                if mf.index_mid_pinkie(self.lm_list):
                    time_fun = time.time()
                    index_mid_pinkie_list = self.command_dict['Index Mid Pinkie']
                    if (time_fun - self.time_var) > self.delay:
                        self.macro(index_mid_pinkie_list, self.press_hold_dict['Index Mid Pinkie'])
                        self.time_var = time_fun
                    elif self.press_hold_dict['Index Mid Pinkie']:
                        if len(self.keys_to_release) < 1:
                            self.keys_to_release = index_mid_pinkie_list.copy()
                        self.press_and_hold_macro(index_mid_pinkie_list)
                        macro_release_switch = True

                if mf.just_mid_finger_up(self.lm_list):
                    time_fun = time.time()
                    mid_finger_list = self.command_dict['Mid Finger']
                    if (time_fun - self.time_var) > self.delay:
                        self.macro(mid_finger_list, self.press_hold_dict['Mid Finger'])
                        self.time_var = time_fun
                    elif self.press_hold_dict['Mid Finger']:
                        if len(self.keys_to_release) < 1:
                            self.keys_to_release = mid_finger_list.copy()
                        self.press_and_hold_macro(mid_finger_list)
                        macro_release_switch = True

                if len(self.keys_to_release) > 0 and macro_release_switch is False:
                    self.release_macro()
                    self.keys_to_release.clear()

            else:
                if self.hand_detected is True:
                    pygame.mixer.music.load('Resources/dcs_no_hand.mp3')
                    pygame.mixer.music.play()
                    self.hand_detected = False

                if len(self.keys_to_release) > 0:
                    self.release_macro()
                    self.keys_to_release.clear()

        self.window.close()


if __name__ == "__main__":
    program = Manucap()
    program.main()
