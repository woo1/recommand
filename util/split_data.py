from random import *

def is_one2():
    a = randint(1, 8)
    if a == 1:
        return True
    else:
        return False

def split_data(_INPUT_NAME = 'C:\hanyang\paper\data_2.csv', TRN = 'C:\hanyang\paper\data_2_train.csv', VAL = 'C:\hanyang\paper\data_2_val.csv'):
    VAL_NO = 5

    t_file = open(TRN, 'w')
    v_file = open(VAL, 'w')

    cnt = []

    with open(_INPUT_NAME) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                t_file.write(line)
                v_file.write(line)
                continue

            data_arr = line.replace('\n', '').split(',')
            data_val = data_arr[:]
            val_added = 0

            print('data_arr', data_arr)

            cnt_1 = 0
            if i > 0:
                data_idx_arr = []
                for j, data in enumerate(data_arr):
                    if j > 0 and data != '':
                        data_idx_arr.append(j)

                for j_idx, j in enumerate(data_idx_arr):
                    if val_added < VAL_NO:
                        if is_one2():
                            data_arr[j] = ''
                            val_added += 1
                        else:
                            if j_idx > len(data_idx_arr) - 5:
                                data_arr[j] = ''
                                val_added += 1
                            else:
                                data_val[j] = ''
                    else:
                        data_val[j] = ''

            t_file.write(','.join(data_arr) + '\n')
            v_file.write(','.join(data_val) + '\n')
    t_file.close()
    v_file.close()

# 네트워크, 나이브 베이즈
def split_data2(_INPUT_NAME='C:\hanyang\paper\data_3.csv', TRN='C:\hanyang\paper\data_3_train.csv',
               VAL='C:\hanyang\paper\data_3_val.csv', refer_file='C:\hanyang\paper\data_2_val.csv'):
    t_file = open(TRN, 'w')
    v_file = open(VAL, 'w')

    cnt = []
    line_val_idxs = []

    with open(refer_file) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                line_val_idxs.append([])
                continue

            data = line.replace('\n', '').split(',')
            idxs = []
            for j, d in enumerate(data):
                if j > 0 and d != '':
                    idxs.append(j)
            line_val_idxs.append(idxs)

    with open(_INPUT_NAME) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                t_file.write(line)
                v_file.write(line)
                continue
            line_val_idx = line_val_idxs[i]
            data_arr = line.replace('\n', '').split(',')
            data_val = data_arr[:]

            print('data_arr', data_arr)

            cnt_1 = 0
            for j in line_val_idx:
                data_arr[j] = ''

            for j, data in enumerate(data_arr):
                if j > 0 and j not in line_val_idx:
                    data_val[j] = ''

            t_file.write(','.join(data_arr) + '\n')
            v_file.write(','.join(data_val) + '\n')
    t_file.close()
    v_file.close()

# 컨텐츠 기반
def split_data3(_INPUT_NAME = 'C:\hanyang\paper\data_cbf.csv', TRN = 'C:\hanyang\paper\data_cbf_train.csv', VAL = 'C:\hanyang\paper\data_cbf_val.csv', refer_file='C:\hanyang\paper\data_2_val.csv', feature_cnt=23):
    t_file = open(TRN, 'w')
    v_file = open(VAL, 'w')

    cnt = []
    line_val_idxs = []

    with open(refer_file) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                continue

            data = line.replace('\n', '').split(',')
            idxs = []
            for j, d in enumerate(data):
                if j > 0 and d != '':
                    idxs.append(j)
            line_val_idxs.append(idxs)

    with open(_INPUT_NAME) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                t_file.write(line)
                v_file.write(line)
                continue

            data_arr = line.replace('\n', '').split(',')
            data_val = data_arr[:]

            # print('data_arr', data_arr)

            # one item, users
            for j in range(feature_cnt, len(data_arr)):
                user_idx = j - feature_cnt

                line_val_idx = line_val_idxs[user_idx]
                print('i', i, 'line_val_idx', line_val_idx, 'user_idx', user_idx)
                if i in line_val_idx:
                    data_arr[j] = ''
                else:
                    data_val[j] = ''

            t_file.write(','.join(data_arr) + '\n')
            v_file.write(','.join(data_val) + '\n')
    t_file.close()
    v_file.close()


if __name__ == '__main__':

    # split_data()

    # split_data2()

    # split_data3()

    # split_data3(_INPUT_NAME='C:\hanyang\paper\data_cbf_menu.csv', TRN='C:\hanyang\paper\data_cbf_menu_train.csv', VAL='C:\hanyang\paper\data_cbf_menu_val.csv', refer_file='C:\hanyang\paper\data_2_val.csv', feature_cnt=105)

    # split_data2(_INPUT_NAME='C:\hanyang\paper\data_naive_2.csv', TRN='C:\hanyang\paper\data_naive_2_train.csv',
    #             VAL='C:\hanyang\paper\data_naive_2_val.csv', refer_file='C:\hanyang\paper\data_2_val.csv')

    # ----------------------------------------------------------

    # split_data2(_INPUT_NAME='C:\hanyang\paper\data_naive_3.csv', TRN='C:\hanyang\paper\data_naive_3_train.csv',
    #             VAL='C:\hanyang\paper\data_naive_3_val.csv', refer_file='C:\hanyang\paper\data_2_val.csv')

    pass