# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import os
import re


# %%
path_dir = os.path.dirname(os.path.abspath('__file__'))
path_example_data = os.path.abspath(os.path.join(path_dir, '../example/data'))


# %%
path_inputs = [os.path.join(path_example_data, f) for f in os.listdir(path_example_data) if '.mpt' in f]


# %%
def chomp_split(str_):
    return [cell for cell in str_.replace('\n', '').split('\t') if cell != '']

key_start = 'Nb header lines\s?:\s?(\d+)'
key_loops = 'Number of loops\s?:\s?(\d+)'

d_output = {}
for file in path_inputs:
    # mptファイルを読む
    with open(file) as f:
        raw = f.read()

    # 導電率に関する情報が書かれ始める行番号を取得    
    num_start = int(re.search(key_start, raw).groups()[0])

    # いくつの測定データが入ってるかについて何行目 (num_line_loops) に書いてあるか，またそのデータの数 (num_loops) はいくつか．
    m = re.search(key_loops, raw)
    num_loops = int(m.groups()[0])
    num_line_loops = raw[:m.start()].count('\n') + 1

    lines = raw.split('\n') # 使いやすく改行ごとにリスト化
    df = pd.DataFrame(map(chomp_split, lines[num_start:]), columns = chomp_split(lines[num_start-1]))

    i = 0
    range_ = []
    while i < num_loops:
        s = re.search('(\d+)\s?to\s?(\d+)', lines[num_line_loops+i])
        range_.append(list(map(int, s.groups())))
        i += 1
    
    dfs = []
    for l, r in range_:
        dfs.append(df.iloc[l:r+1].reset_index(drop = True))
    
    d_output[file] = dfs
print(d_output)
        
            


# %%



