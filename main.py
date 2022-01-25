import PySimpleGUI as sg
import os
import sys
import re
import pandas as pd
from collections.abc import Generator

LATIN_1 = 'latin-1'
UTF_8_SIG = 'utf-8-sig'

class Mpt2Csv:
    def __init__(self):
        # Constants
        self.col_freq = 'freq/Hz'
        self.col_real = 'Re(Z)/Ohm'
        self.col_imag = '-Im(Z)/Ohm'
        self.col_n_cycle = 'cycle number'
    
    def read_mpt(self, fpath:str)->tuple[list, pd.DataFrame]:
        if not os.path.isfile(fpath):
            raise FileNotFoundError('file not found: {}'.format(fpath))
        with open(fpath, mode='r', encoding=LATIN_1) as f:
            for i, line in enumerate(f):
                key = r'Nb header lines\s*:\s*(\d+)'
                result = re.search(key, line)
                if result:
                    n_header_lines = int(result.group(1))
                    break
                elif i > 100:
                    raise ValueError('Could not find header lines')
        
        with open(fpath, mode='r', encoding=LATIN_1) as f:
            info_ = f.readlines()[:n_header_lines-1]

        return info_, pd.read_table(fpath, skiprows=n_header_lines-1).astype({
            self.col_n_cycle: int,
        })
    
    def split(self, df:pd.DataFrame)->Generator[pd.DataFrame, None, None]:
        if self.col_n_cycle not in df.columns:
            raise ValueError('df does not have column {}'.format(self.col_n_cycle))
        for _n_cycle, _df in df.groupby(self.col_n_cycle):
            yield _df
    
    def my_save(self, df:pd.DataFrame, fname_base_output:str, dirpath_output:str, info:str = None, ext:str='mpt'):
        fpath_output = os.path.join(dirpath_output, f'{fname_base_output}.{ext}')
        if ext == 'mpt':
            with open(fpath_output, mode = 'w', encoding = LATIN_1) as f:
                if info:
                    f.write(info)
            df.to_csv(fpath_output, encoding = LATIN_1, index = False, sep = '\t', mode = 'a')
        elif ext == 'csv':
            df.to_csv(fpath_output, encoding = UTF_8_SIG, index = False)
        elif ext == 'txt':
            df.to_csv(fpath_output, encoding = UTF_8_SIG, index = False, sep = '\t')
        else:
            raise NotImplementedError('extension is not supported: {}.'.format(ext))

def main():
    window_options = {}
    window_options['font'] = 'Helvetica 18'
    window_options['resizable'] = True

    # for overwrite
    yes_to_all = False
    quit_now = False

    sg.theme('Dark Blue')

    cand = ['mpt', 'csv', 'txt']
    Text_size = (20, 1)
    InputBrowse_size = (20, 1)

    layout_main = [
        [sg.Text('convert mpt files.', size = Text_size)],
        [sg.Text('input mpt files : ', size = Text_size), sg.Input(key = '-INPUT-', size = InputBrowse_size, expand_x = True), sg.FilesBrowse(file_types = (("mpt files", "*.mpt"),))],
        [sg.Text('output folder : ', size = Text_size), sg.Input(key = '-OUTPUT-', size = InputBrowse_size, expand_x = True), sg.FolderBrowse()],
        [sg.Text("output files' extension", size = Text_size), sg.Combo(cand, size = (10, 1), key = 'ext', default_value = cand[0])],
        [sg.Submit('Run'), sg.Cancel('Cancel')],
    ]

    window_main = sg.Window('mpt2csv', layout_main, **window_options)

    while True:
        event, values = window_main.read()

        if event is None or event == 'Cancel':
            break
        elif event == 'Run':
            fpaths_input = values['-INPUT-']
            if fpaths_input:
                fpaths_input = fpaths_input.split(';')
            else:
                sg.popup_error('input file is empty.')
            dirpath_output = values['-OUTPUT-']
            if not dirpath_output:
                sg.popup_error('output folder is empty.')
            ext = values['ext']

        
            mpt2csv = Mpt2Csv()
            for fpath_input in fpaths_input:
                info_, df_input_ = mpt2csv.read_mpt(fpath_input)

                for n_cycle_, df_ in enumerate(mpt2csv.split(df=df_input_)):
                    df_.dropna(axis=1, how='all', inplace=True)
                    fname_base_output_ = f'{os.path.splitext(os.path.basename(fpath_input))[0]}_{n_cycle_}'
                    if os.path.isfile(os.path.join(dirpath_output, f'{fname_base_output_}.{ext}')):
                        while not yes_to_all:
                            window_overwrite = sg.Window('Can I overwrite?', layout=[
                                [sg.Text('{} already exists.'.format(fname_base_output_))],
                                [sg.Button('Yes'), sg.Button('Yes to All'), sg.Button('No')],
                            ], **window_options)
                            event_overwrite, values_overwrite = window_overwrite.read()
                            if event_overwrite == 'Yes':
                                yes_to_all = False
                                quit_now = False
                                break
                            elif event_overwrite == 'Yes to All':
                                yes_to_all = True
                                quit_now = False
                                break
                            elif event_overwrite in ('No', None):
                                yes_to_all = False
                                quit_now = True
                                break
                            else:
                                sg.popup_error('unknown event{}.'.format(event_overwrite))
                                yes_to_all = False
                                quit_now = True
                                break
                        window_overwrite.close()
                        
                        if quit_now:
                            break
                    if type(info_) == list:
                        info_ = ''.join(info_)
                    elif info_ is None or type(info_) == str:
                        pass
                    else:
                        sg.popup_error('unknown info type {}.'.format(type(info_)))
                        break
                    mpt2csv.my_save(df=df_, fname_base_output=fname_base_output_, dirpath_output=dirpath_output, info=info_, ext=ext)
                if quit_now:
                    break
            else:
                sg.popup_ok('Done.', font = window_options['font'])

    window_main.close()

if __name__ == '__main__':
    main()
