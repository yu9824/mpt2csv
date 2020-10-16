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

layout_main = [
    [sg.Text('convert mpt files.', size = Text_size)],
    [sg.Text('input mpt files : ', size = Text_size), sg.Input(key = '-INPUT-', size = InputBrowse_size), sg.FilesBrowse(file_types = (("mpt files", "*.mpt"),))],
    [sg.Text('output folder : ', size = Text_size), sg.Input(key = '-OUTPUT-', size = InputBrowse_size), sg.FolderBrowse()],
    [sg.Text("output files' extension", size = Text_size), sg.Combo(cand, size = (10, 1), key = 'saveas', default_value = cand[0])],
    [sg.Submit('Run'), sg.Cancel()],
]

window_main = sg.Window('mpt2csv', layout_main, **window_options)

while True:
    print(os.environ['PWD'], os.environ['OLDPWD'])
    event, values = window_main.read()

    if event is None or event == 'Cancel':
        break
    elif event == 'Run':
        path_inputs = values['-INPUT-'].split(';')
        path_diroutput = values['-OUTPUT-']
        saveas = values['saveas']
        if len(path_inputs) != 0 and len(path_diroutput) != 0:
            m2c = mpt2csv(path_inputs)
            m2c.save(path_diroutput, saveas = saveas)

            layout_rename = [
                [sg.Text('Please rename files if you want. (A number of files is {}.)'.format(len(m2c.filenames)))],
                [sg.Multiline(default_text = '\n'.join(m2c.filenames), size = (100, None), key = '-FILENAMES-')],
                [sg.OK(), sg.Cancel()]
            ]
            window_rename = sg.Window('mpt2csv', layout_rename, **window_options)

            while True:
                event_rename, values_rename = window_rename.read()
                if event_rename in (None, 'Cancel'):
                    sg.popup_timed('Finished!', **window_options)
                    break
                elif event_rename == 'OK':
                    filenames = values_rename['-FILENAMES-']
                    r = sg.popup_ok_cancel('May I change filenames?', **window_options)
                    if r == 'OK':
                        if m2c.filenames != filenames.split('\n'):
                            for old_filename, new_filename in zip(m2c.filenames, filenames.replace('\r', '').split('\n')):
                                if old_filename != new_filename:
                                    os.rename(os.path.join(path_diroutput, old_filename + '.' + saveas), os.path.join(path_diroutput, new_filename + '.' + saveas))
                        sg.popup_timed('Finished!', **window_options)
                        break
                    else:
                        continue
            window_rename.close()
        else:
            sg.popup_error('You have to fill all boxes.', **window_options)
window_main.close()
            