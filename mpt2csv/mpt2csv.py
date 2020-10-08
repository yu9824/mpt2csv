# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

import pandas as pd
import os
import re


class mpt2multi:
    def __init__(self, path_inputs):
        self.key_start = '(Nb header lines\s?:\s?)(\d+)'
        self.key_loops = '(Number of loops\s?:\s?)(\d+)'
        self.key_range = '(\d+)\s?to\s?(\d+)'

        self.path_inputs = path_inputs

        self.d_output = {}
        for file in self.path_inputs:
            # mptファイルを読む
            with open(file) as f:
                raw = f.read()

            # 導電率に関する情報が書かれ始める行番号を取得
            num_start = int(re.search(self.key_start, raw).groups()[1])

            # いくつの測定データが入ってるかについて何行目 (self.num_line_loops) に書いてあるか，またそのデータの数 (num_loops) はいくつか．
            m = re.search(self.key_loops, raw)
            num_loops = int(m.groups()[1])
            self.info = raw[:m.start()]
            self.num_line_loops = self.info.count('\n') + 1
            
            self.info = re.sub(self.key_start, re.search(self.key_start, self.info).groups()[0] + str(self.num_line_loops), self.info)
            # print(self.info)

            lines = raw.split('\n') # 使いやすく改行ごとにリスト化
            df = pd.DataFrame(map(self._chomp_split, lines[num_start:]), columns = self._chomp_split(lines[num_start-1]))

            i = 0
            range_ = []
            while i < num_loops:
                s = re.search(self.key_range, lines[self.num_line_loops+i])
                range_.append(list(map(int, s.groups())))
                i += 1
            
            dfs = []
            for l, r in range_:
                dfs.append(df.iloc[l:r+1].reset_index(drop = True))
            
            file_name = os.path.splitext(os.path.basename(file))[0]
            self.d_output[file_name] = dfs
    
    def get_dict(self):
        return self.d_output

    def save(self, path_diroutput, saveas = 'mpt'):
        def my_write(path, saveas):
            path_output = os.path.join(path_diroutput, k + str(i) + '.' + saveas)
            if saveas == 'mpt':
                with open(path_output, mode = 'w') as f:
                    f.write(self.info)
                df.to_csv(path_output, encoding = 'utf_8_sig', index = False, sep = ' ', mode = 'a')
            elif saveas == 'csv':
                df.to_csv(path_output, encoding = 'utf_8_sig', index = False)
            elif saveas == 'txt':
                df.to_csv(path_output, encoding = 'utf_8_sig', index = False, sep = '\t')
            else:
                raise ValueError('saveas is not correct.')


        for k, v in self.d_output.items():
            for i, df in enumerate(v):
                for col in df.columns:
                    m = re.match('-(.*Z.*)', col)
                    if m is not None:
                        break
                col_name = m.group()
                new_col_name = m.groups()[0]

                df.loc[:, col_name] = df.loc[:, col_name].map(lambda x:float(x)*-1)
                df = df.rename(columns = {col_name : new_col_name})
                my_write(path_diroutput, saveas = saveas)


    def _chomp_split(self, str_):
        return [cell for cell in str_.replace('\n', '').split('\t') if cell != '']
        
            


if __name__ == '__main__':
    pass

    
    
