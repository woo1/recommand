import os

def make2():
    fnm = 'data_naive_2.csv'
    new_f = open(fnm, 'w')
    _INPUT_NAME = 'C:\hanyang\paper\data_2.csv'
    with open(_INPUT_NAME) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                new_f.write(line)
            else:
                user_nm = line.split(',')[0]
                line = ','.join(line.split(',')[1:])
                line = line.replace('3', 'like').replace('4', 'like').replace('5', 'like').replace('2', 'dislike').replace('1', 'dislike')
                line_arr = line.split(',')
                line_arr.insert(0, user_nm)
                line = ','.join(line_arr)
                new_f.write(line)
    new_f.close()

def make3():
    fnm = 'data_naive_3.csv'
    new_f = open(fnm, 'w')
    _INPUT_NAME = 'C:\hanyang\paper\data_2.csv'
    with open(_INPUT_NAME) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                new_f.write(line)
            else:
                user_nm = line.split(',')[0]
                line = ','.join(line.split(',')[1:])
                line = line.replace('3', 'normal').replace('4', 'like').replace('5', 'like').replace('2','dislike').replace('1', 'dislike')
                line_arr = line.split(',')
                line_arr.insert(0, user_nm)
                line = ','.join(line_arr)
                new_f.write(line)
    new_f.close()

if __name__ == '__main__':
    make2()
    # make3()