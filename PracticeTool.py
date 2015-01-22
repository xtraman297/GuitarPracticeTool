#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

This example shows text which 
is entered in a QtGui.QLineEdit
in a QtGui.QLabel widget.
 
author: Jan Bodnar
website: zetcode.com 
last edited: August 2011
"""
STRINGS_ON_GUITAR = 6
import sys
from random import randint, randrange, choice
from winsound import Beep         # for sound
import RandomScaleLib 
import sfml as sf
from time import sleep
import threading
from PyQt4 import QtGui, QtCore

note_to_number = {'C': 0, 'C#/Db': 1, 'D': 2, 'D#/Eb': 3, 'E': 4, 'F': 5, 'F#/Gb': 6, 'G': 7, 'G#/Ab': 8, 'A': 9, 'A#/Bb': 10, 'B': 11}
all_notes = ['C', 'C#/DB', 'D', 'D#/EB', 'E', 'F', 'F#/GB', 'G', 'G#/AB', 'A', 'A#/BB', 'B']
notes_tuning_arr = ["e", "B", "G", "D", "A", "E"]

key_freq = {'A': 440, 'B': 493, 'C': 523, 'D': 587, 'E': 659, 'F': 698, 'G': 783,
            'G#/Ab': 830, 'A#/Bb': 466, 'F#/Gb': 739, 'C#/Db': 554, 'D#/Eb': 622}

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):

        list = (1, 1, 1, 2, 1), (1, 2, 2), (1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 2, 6)

        self.freq = key_freq['A']

        self.start_metronome = QtGui.QPushButton('Start', self)
        self.start_metronome.move(10, 10)
        self.start_metronome.setMinimumSize(100, 100)
        self.start_metronome.clicked.connect(self.stopStartMetronome)
        self.start_metronome.started = False
        self.thread1 = threading.Thread(target=self.print_loop)

        self.change_scale = QtGui.QPushButton('Change Scale', self)
        self.change_scale.move(120, 10)
        self.change_scale.setMinimumSize(100, 100)
        self.change_scale.clicked.connect(self.stopStartMetronome)

        self.num_of_strings = QtGui.QPushButton('Set number of strings', self)
        self.num_of_strings.move(230, 10)
        self.num_of_strings.setMinimumSize(100, 100)
        self.num_of_strings.clicked.connect(self.stopStartMetronome)

        self.change_tuning = QtGui.QPushButton('Change Tuning', self)
        self.change_tuning.move(350, 10)
        self.change_tuning.setMinimumSize(100, 100)
        self.change_tuning.clicked.connect(self.stopStartMetronome)

        self.change_tabs_mode = QtGui.QPushButton('Change Tabs Mode', self)
        self.change_tabs_mode.move(460, 10)
        self.change_tabs_mode.setMinimumSize(100, 100)
        self.change_tabs_mode.clicked.connect(self.stopStartMetronome)

        self.hide_scale = QtGui.QPushButton('Unhide', self)
        self.hide_scale.move(10, 175)
        self.hide_scale.setMinimumSize(100, 10)
        self.hide_scale.setToolTip('This will hide/unhide the scale')
        self.hide_scale.resize(self.hide_scale.sizeHint())
        self.hide_scale.clicked.connect(self.clickButton)
        self.hide_scale.moshe = True

        self.txt = QtGui.QTextEdit(self)
        self.txt.move(10, 200)
        self.txt.setEnabled(False)
        self.txt.setMinimumWidth(550)
        self.txt.setMaximumHeight(95)
        self.txt.geometry()
        self.txt.insertPlainText(print_tab_full(get_scale_return_array('D#/EB', 1, 1)))
        self.txt.adjustSize()

        self.setGeometry(750, 700, 570, 310)
        self.setWindowTitle('Guitar Trainer')
        self.show()

        self.clickButton()
        get_scale_return_array('E', 1, 1)

    def onChanged(self, text):
        self.txt.setText(text)

    def clickButton(self):
        if self.hide_scale.moshe:
            self.txt.setStyleSheet('color:#FFF8DC;Background:#FFF8DC;')
            self.hide_scale.setText('Unhide')
        else:
            self.txt.setStyleSheet('font-family: "Courier New", Courier, monospace;Background:#FFF8DC;')
            self.hide_scale.setText('Hide')
        self.hide_scale.moshe = not self.hide_scale.moshe

    def stopStartMetronome(self):

        if self.start_metronome.started:
            self.start_metronome.setStyleSheet("background-color: light gray")
            self.start_metronome.setText('start')
            self.start_metronome.started = False
        else:
            self.start_metronome.setStyleSheet("background-color: red")
            self.start_metronome.setText('stop')
            self.start_metronome.started = True
            self.thread1 = threading.Thread(target=self.print_loop)
            self.thread1.start()
            #print 1

    def print_loop(self):
        local_count = 0
        weight = randint(4, 4)

        tempo = (float(randint(25, 100)) * 0.01)
        while self.start_metronome.started:
            #print (str(local_count + 1), end='')
            local_count = (local_count + 1) % weight
            if local_count == 1:
                Beep(self.freq * 2, 250)     # frequency, duration
            else:
                Beep(self.freq, 250)     # frequency, duration
            sleep(tempo - 0.25)           # in seconds (0.25 is 250ms)
        return



def print_tab_3_per_string(list):
    note_tab_arr = ["e", "B", "G", "D", "A", "E"]
    #some_string = ''
    some_array = []
    for i in range(0, 6):
        some_array.append(note_tab_arr[i])
        some_array.append("|---")

        for aft in range(i, STRINGS_ON_GUITAR-1):
                for z in list[aft]:
                    some_array.append("----")
        for x in list[i]:
            if x == -1:
                some_array.append("---")
            else:
                some_array.append(str(x))
            if x < 10:
                some_array.append("---")
            else:
                some_array.append("--")
        for bef in range(0, i):
                for z in list[bef]:
                    some_array.append("----")
        some_array.append("\n")
    some_string = "".join(some_array)

    return some_string[:-1] # [:-1] -> Removing last \n

def print_tab_full(list):
    #note_tab_arr = ["e", "B", "G", "D", "A", "E"]
    #some_string = ''
    some_array = []
    for i in range(0, 6):
        some_array.append(notes_tuning_arr[i])
        some_array.append("|---")

        #for aft in range(i, STRINGS_ON_GUITAR-1):
        #        for z in list[aft]:
        #            some_array.append("----")
        for x in list[i]:
            if x == -1:
                some_array.append("-")
            else:
                some_array.append(str(x))
            if x < 10:
                some_array.append("---")
            else:
                some_array.append("--")
        #for bef in range(0, i):
        #        for z in list[bef]:
        #            some_array.append("----")
        some_array.append("\n")
    some_string = "".join(some_array)

    return some_string[:-1] # [:-1] -> Removing last \n

def get_scale_return_array(scale_note, tunning_intervals, starting_note):
    major_array = [2, 2, 1, 2, 2, 2, 1]
    scale_pointer = 0

    twelve_note_list = []
    scale_list = []
    scale_temp = []
    start_tmp = all_notes.index(scale_note)
    major_num = 0

    for num in xrange(all_notes.index(scale_note), all_notes.index(scale_note)+7):
        #print start_tmp % len(all_notes)
        scale_temp.append(all_notes[start_tmp % len(all_notes)])
        start_tmp += major_array[major_num]
        major_num += 1
    #print scale_temp

    for num in xrange(len(notes_tuning_arr)):
        note_index = all_notes.index(notes_tuning_arr[num].upper())
        for tab in xrange(13):
            if all_notes[note_index % len(all_notes)] in scale_temp:
                twelve_note_list.append(tab)
            else:
                twelve_note_list.append(-1)
            note_index += 1
        scale_list.append(twelve_note_list[:])
        twelve_note_list = []
    return scale_list




def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
