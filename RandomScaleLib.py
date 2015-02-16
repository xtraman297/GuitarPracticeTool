# By Eran Brodet and Moshe Simantov
# 2014
from __future__ import print_function

__author__ = 'moshest'
from os import system
from msvcrt import getch
from random import randint, randrange, choice
from winsound import Beep         # for sound
from time import sleep            # for sleep
import thread

note_to_number = {'C': 0, 'C#/Db': 1, 'D': 2, 'D#/Eb': 3, 'E': 4, 'F': 5, 'F#/Gb': 6, 'G': 7, 'G#/Ab': 8, 'A': 9, 'A#/Bb': 10, 'B': 11}

keylist = 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'G#/Ab', 'A#/Bb', 'F#/Gb', 'C#/Db', 'D#/Eb'
keylist_to_E_string = {'A': 5, 'B': 7, 'C': 8, 'D': 10, 'E': 0, 'F': 1, 'G': 3, 'G#/Ab': 4, 'A#/Bb': 6, 'F#/Gb': 2, 'C#/Db': 9, 'D#/Eb': 11}
key_freq = {'A': 440, 'B': 493, 'C': 523, 'D': 587, 'E': 659, 'F': 698, 'G': 783,
            'G#/Ab': 830, 'A#/Bb': 466, 'F#/Gb': 739, 'C#/Db': 554, 'D#/Eb': 622}
modeslist = 'Inonian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian'
modeslist_to_degree = {'Inonian': 1, 'Dorian': 2, 'Phrygian': 3, 'Lydian': 4, 'Mixolydian': 5, 'Aeolian': 6, 'Locrian': 7}
maj_min = 'Major', 'Minor'

STRINGS_ON_GUITAR = 6

def print_tab(list):
    note_tab_arr = ["e", "B", "G", "D", "A", "E"]
    for i in range(0, 6):
        print (note_tab_arr[i], end='')
        print ("|---", end='')

        for aft in range(i, STRINGS_ON_GUITAR-1):
                for z in list[aft]:
                    print ("----", end='')
        for x in list[i]:
            if x == -1:
                print ("---", end='')
            else:
                print (str(x), end='')
            if x < 10:
                print ("---", end='')
            else:
                print ("--", end='')
        for bef in range(0, i):
                for z in list[bef]:
                    print ("----", end='')
        print ('')

def list_upside_down(list):
    #tmp_list = [None] * len(list)
    print (list[0])
    print (list[1])
    tmp_list = list
    for i in list:
        tmp_list[len(list) - i] = list[i]
    return tmp_list

def get_scale_return_array(scale_name, tunning_intervals, starting_note, scale_pointer):
    major_array = [2, 2, 1, 2, 2, 2, 1]
    #scale_pointer = 0 is default for major scale
    #scale_pointer = 0
    three_note_list = []
    scale_list = []
    if scale_pointer > 6 or scale_pointer < 0:
        scale_pointer = 0
    else:
        for i in range(0, scale_pointer):
            starting_note = starting_note + major_array[i]
    if starting_note > 11:
        starting_note -= 12
    print (starting_note)

    #here will check for scale_name to change value of scale_pointer
    #scale_pointer = modeslist_to_degree[scale_name]
    for x in range(0, 6):
        for y in range(0, 3):
            three_note_list.append(starting_note)
            starting_note += major_array[scale_pointer]
            scale_pointer += 1
            if scale_pointer == 7:
                scale_pointer = 0
       # print (tunning_intervals[x])
        starting_note -= tunning_intervals[x]
        scale_list.append(three_note_list[:])  # clone of line
        three_note_list = []
    return scale_list


def input_thread(L):
    """
        Runs in UI thread
    """
    #f = getch()
    #print f
    #raw_input()
    L.append('')
    while True:
        L[0] = getch()
        #L.append(getch())


def print_practice(tempo, key, weight, modos):
    practice_type = randint(1, 2)

    if practice_type == 1:
        print (key + ' ' + modos, 'in tempo:', int((1 / tempo) * 60), 'in weight of', str(weight) + "'s")
        #return modos
    elif practice_type == 2:
        print (modos + ' of ' + key + ' ' + choice(maj_min), 'in tempo:', int((1 / tempo) * 60), 'in weight of', str(weight) + "'s")
        #return modos


def metronome_simple(tempo, key, weight, modos):
    L = []
    thread.start_new_thread(input_thread, (L,))
    local_count = 0
    freq = key_freq[key]
    print_scale_flag = 0
    system('cls')
    tuning_space = [5, 5, 5, 4, 5, 5]

    print_practice(tempo, key, weight, modos)

    tab_list = get_scale_return_array(modos, tuning_space, keylist_to_E_string[key])
    tab_list.reverse()
    print_tab(tab_list)
    while True:
        #print (str(local_count + 1), end='')
        local_count = (local_count + 1) % weight
        if local_count == 1:
            Beep(freq * 2, 250)     # frequency, duration
        else:
            Beep(freq, 250)     # frequency, duration
        sleep(tempo - 0.25)           # in seconds (0.25 is 250ms)
        if print_scale_flag == 1:
            print('SCALE')
            tab_list = get_scale_return_array(mod_from_print, tuning_space, 3)
            print_tab(tab_list)

        print ('\r', end='')

        #print L
        if L[0] != '':
            if L[0] == 'q':
                L[0] = ''
                exit()
            elif (L[0] == 'h' or L[0] == 'H') and print_scale_flag == 0:
                print_scale_flag = 1
                L[0] = ''
            elif (L[0] == 'h' or L[0] == 'H') and print_scale_flag == 1:
                L[0] = ''
                print_scale_flag = 0
            else:
                L[0] = ''
                system('cls')
                #print '\r\r',
                break


def main():
    while True:
        keychose = choice(keylist)
        tempo = (float(randint(25, 100)) * 0.01)
        weight = randint(4, 4)
        modos = choice(modeslist)
        metronome_simple(tempo, keychose, weight, modos)


if __name__ == "__main__":
    main()
