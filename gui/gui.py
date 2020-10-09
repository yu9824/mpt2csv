import PySimpleGUI as sg
import pandas as pd
import os
import sys

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.abspath(os.path.join(DIR_PATH, '../')))
# print(sys.path)
from mpt2csv.mpt2csv import mpt2csv

window_options = {}
window_options['font'] = 'Helvetica 18'


sg.theme('Dark Blue')

cand = ['mpt', 'csv', 'txt']
Text_size = (20, 1)
InputBrowse_size = (20, 1)

layout = [
    [sg.Text('convert mpt files.', size = Text_size)],
    [sg.Text('input mpt files : ', size = Text_size), sg.Input(key = '-INPUT-', size = InputBrowse_size), sg.FilesBrowse(file_types = (("mpt files", "*.mpt"),))],
    [sg.Text('output folder : ', size = Text_size), sg.Input(key = '-OUTPUT-', size = InputBrowse_size), sg.FolderBrowse()],
    [sg.Text("output files' extension", size = Text_size), sg.Combo(cand, size = (10, 1), key = 'saveas', default_value = cand[0])],
    [sg.Submit('Run'), sg.Cancel()],
]

window = sg.Window('mpt2csv', layout, **window_options)

while True:
    event, values = window.read()
    path_inputs = values['-INPUT-'].split(';')
    path_diroutput = values['-OUTPUT-']

    if event in (None, 'Cancel'):
        break
    elif event == 'Run':
        if len(path_inputs) != 0 and len(path_diroutput) != 0:
            # try:
            #     mpt2csv(path_inputs).save(path_diroutput, saveas = values['saveas'])
            # except:
            #     sg.popup_error('There is something wrong when converting.', **window_options)
            # else:
            #     sg.popup_ok('Finish!', **window_options)
            mpt2csv(path_inputs).save(path_diroutput, saveas = values['saveas'])
            sg.popup_ok('Finish!', **window_options)
        else:
            sg.Popup('You have to fill all boxes.', **window_options)
            