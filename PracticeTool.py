#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Guitar Practice Tool by Moshe Siman-Tov
"""
STRINGS_ON_GUITAR = 6
import sys
from random import randint, randrange, choice
from winsound import Beep         # for sound
import RandomScaleLib
from time import sleep
import threading
from PyQt4 import QtGui, QtCore

note_to_number = {'C': 0, 'C#/Db': 1, 'D': 2, 'D#/Eb': 3, 'E': 4, 'F': 5, 'F#/Gb': 6, 'G': 7, 'G#/Ab': 8, 'A': 9, 'A#/Bb': 10, 'B': 11}
all_notes = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
notes_tuning_arr = ["e", "B", "G", "D", "A", "E"]
#tuning_interval = []
key_freq = {'A': 440, 'B': 493, 'C': 523, 'D': 587, 'E': 659, 'F': 698, 'G': 783,
            'G#/Ab': 830, 'A#/Bb': 466, 'F#/Gb': 739, 'C#/Db': 554, 'D#/Eb': 622}
glob_first_note = 0
def get_first_note_and_scale_return_first_note_tab(tab_note, scale_note):
    tab_note = note_to_number[tab_note]
    scale_note = note_to_number[scale_note]
    returned_note = scale_note - tab_note
    if returned_note < 0:
        returned_note += 12
    return returned_note

def tuning_notes_to_intervals(notes_tuning):
    tuning_interval_internal = []
    count_intervals = 0
    tuning_interval_internal.append(5)
    for i in range(notes_tuning.__len__() - 1):
        x = all_notes.index(notes_tuning[i].upper())
        for b in range(all_notes.__len__()):
            if notes_tuning[i + 1] == all_notes[x % len(all_notes)].upper():
                tuning_interval_internal.append(count_intervals)
            x -= 1
            count_intervals += 1
        count_intervals = 0
    x = 0
    a_arr = []

    for some in xrange(len(tuning_interval_internal)).__reversed__():
        #print some
        a_arr.append(tuning_interval_internal[some])
    #print a_arr
    return a_arr

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.tuning_interval = []
        self.tuning_interval = tuning_notes_to_intervals(notes_tuning_arr)
        #get self.random_note
        self.random_note = all_notes[randint(0, 11)]
        #get the frequency of that note from the note-to-frequency array
        self.freq = key_freq[self.random_note]

        #Here we set all of the buttons and their labels
        self.start_metronome_button = QtGui.QPushButton('Start', self)
        self.change_scale = QtGui.QPushButton('Change Scale', self)
        self.num_of_strings = QtGui.QPushButton('Set number of strings', self)
        self.change_tuning = QtGui.QPushButton('Change Tuning', self)
        self.change_tabs_mode = QtGui.QPushButton('Change Tabs Mode', self)
        self.hide_scale = QtGui.QPushButton('UnHide', self)

        #Setting the drop down menu
        self.modes_list = ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"]
        self.menu = QtGui.QComboBox(self)
        self.menu.addItems(self.modes_list)
        self.menu.move(483, 177)
        #self.menu.connect(self.change_modos, QtCore.pyqtSignal("currentIndexChanged(int)"))
        self.menu.activated.connect(lambda: self.change_modos())
        #self.connect(self.menu, QtCore.SIGNAL('activated(QString)'), self.change_modos())

        #Set the metronome start button X,Y location, Size, Function to start 'stopStartMetronome' and if clicked to false
        self.start_metronome_button.move(10, 10)
        self.start_metronome_button.setMinimumSize(100, 100)
        self.start_metronome_button.clicked.connect(self.stopStartMetronome)
        self.start_metronome_button.started = False


        self.change_scale.move(120, 10)
        self.change_scale.setMinimumSize(100, 100)
        self.change_scale.clicked.connect(self.stopStartMetronome)

        self.num_of_strings.move(230, 10)
        self.num_of_strings.setMinimumSize(100, 100)
        self.num_of_strings.clicked.connect(self.stopStartMetronome)

        self.change_tuning.move(350, 10)
        self.change_tuning.setMinimumSize(100, 100)
        self.change_tuning.clicked.connect(self.stopStartMetronome)

        self.change_tabs_mode.move(460, 10)
        self.change_tabs_mode.setMinimumSize(100, 100)
        self.change_tabs_mode.clicked.connect(self.stopStartMetronome)

        self.hide_scale.move(10, 175)
        self.hide_scale.setMinimumSize(100, 10)
        self.hide_scale.setToolTip('This will hide/unhide the scale')
        self.hide_scale.resize(self.hide_scale.sizeHint())
        self.hide_scale.clicked.connect(self.clickHideUnHide)
        self.hide_scale.moshe = True

        self.txt = QtGui.QTextEdit(self)
        self.txt.move(10, 200)
        self.txt.setEnabled(False)
        self.txt.setMinimumWidth(550)
        self.txt.setMaximumHeight(95)
        self.txt.geometry()
        self.txt.insertPlainText(print_tab_full(get_scale_return_array(self.random_note, 1, 1)))
        self.txt.adjustSize()

        self.three_notes = QtGui.QTextEdit(self)
        self.three_notes.move(10,300)
        self.three_notes.setMinimumWidth(550)
        self.three_notes.setMaximumHeight(95)
        self.three_notes.setEnabled(False)
        some_list = RandomScaleLib.get_scale_return_array("test", self.tuning_interval, get_first_note_and_scale_return_first_note_tab('E', self.random_note), self.menu.currentIndex())
        some_list.reverse()
        self.three_notes.insertPlainText(print_tab_3_per_string(some_list))

        self.setGeometry(750, 400, 570, 410)
        self.setWindowTitle('Guitar Trainer')
        self.show()

        self.thread1 = threading.Thread(target=self.print_loop)
        self.clickHideUnHide()
        get_scale_return_array('E', 1, 1)

    def onChanged(self, text):
        self.txt.setText(text)

    def clickHideUnHide(self):
        if self.hide_scale.moshe:
            self.txt.setStyleSheet('color:#FFF8DC;Background:#FFF8DC;')
            self.three_notes.setStyleSheet('color:#FFF8DC;Background:#FFF8DC;')
            self.hide_scale.setText('UnHide')
        else:
            self.txt.setStyleSheet('font-family: "Courier New", Courier, monospace;Background:#FFF8DC;')
            self.three_notes.setStyleSheet('font-family: "Courier New", Courier, monospace;Background:#FFF8DC;')
            self.hide_scale.setText('Hide')
        self.hide_scale.moshe = not self.hide_scale.moshe

    def stopStartMetronome(self):

        if self.start_metronome_button.started:
            self.start_metronome_button.setStyleSheet("background-color: light gray")
            self.start_metronome_button.setText('start')
            self.start_metronome_button.started = False
        else:
            self.start_metronome_button.setStyleSheet("background-color: red")
            self.start_metronome_button.setText('stop')
            self.start_metronome_button.started = True

            #Change Scale Randomly
            self.random_note = all_notes[randint(0, 11)]
            #get the frequency of that note from the note-to-frequency array
            self.freq = key_freq[self.random_note]
            some_list = RandomScaleLib.get_scale_return_array("test", self.tuning_interval, get_first_note_and_scale_return_first_note_tab('E', self.random_note), self.menu.currentIndex())            #some_list.reverse()
            some_list.reverse()
            self.three_notes.setText("")
            self.three_notes.insertPlainText(print_tab_3_per_string(some_list))
            self.txt.setText("")
            self.txt.insertPlainText(print_tab_full(get_scale_return_array(self.random_note, 1, 1)))

            #Start Metronome Loop
            self.thread1 = threading.Thread(target=self.print_loop)
            self.thread1.start()

    def change_modos(self):
        #print self.menu.currentIndex()

        some_list = RandomScaleLib.get_scale_return_array("test", self.tuning_interval, get_first_note_and_scale_return_first_note_tab('E', self.random_note), self.menu.currentIndex())            #some_list.reverse()
        some_list.reverse()
        self.three_notes.setText("")
        self.three_notes.insertPlainText(print_tab_3_per_string(some_list))

    def print_loop(self):
        local_count = 0
        weight = randint(4, 4)

        tempo = (float(randint(25, 100)) * 0.01)
        while self.start_metronome_button.started:
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
