# 아이템 기반 협업필터링, 가중평균, Top-5 선정
# output에 추천값이 없는 경우는 유사 아이템 Top-5도 안 먹어본 곳이라 그런 거임
# TOP-10 사용. 아이템은 좀 많아서.
import math
from operator import itemgetter

def null2void(val):
    if val == '':
        return 0
    else:
        return val

_INPUT_NAME  = 'C:\hanyang\paper\data_2_train.csv'
_OUTPUT_NAME = 'C:\hanyang\paper\output\data_2_train_result_item.csv'
_TOP_N = 50

with open(_INPUT_NAME) as f:
    data_in_org = f.readlines()
    data_in = data_in_org[1:]
    sumsq_arr = []
    data_rcmd = []

    new_data = [data_in_org[0]]

    line_1 = data_in[0].replace('\n', '').split(',') # skip name column
    item_len = len(line_1)
    for i, item in enumerate(line_1):
        if i > 0:
            sumsq = 0
            # item 별 sqrt 계산
            for j in range(len(data_in)):
                if data_in[j].replace('\n', '').split(',')[i] != '':
                    sumsq = sumsq + int(data_in[j].replace('\n', '').split(',')[i])**2
            sumsq_arr.append(math.sqrt(sumsq))

    for i, data_target in enumerate(data_in):
        cos_arr = []
        data_target = data_target.replace('\n', '')
        t_data = data_target.split(',')
        recm_pred = {}
        new_output = ""

        for k in range(len(t_data)):
            if k > 0:
                if t_data[k] == '': # 해당 아이템에 대한 유사도 찾기
                    sqrt_t = sumsq_arr[k-1]
                    cos_arr = []
                    for j in range(len(t_data)):
                        if k != j and j > 0:
                            sqrt_j = sumsq_arr[j-1]
                            sumprd = 0
                            for jj, data_row in enumerate(data_in):
                                data_row = data_row.replace('\n', '')
                                data_r_1 = data_row.split(',')
                                sumprd += int(null2void(data_r_1[j]))*int(null2void(data_r_1[k]))
                            cos_arr.append((j, sumprd/(sqrt_t*sqrt_j)))

                    # Top-N 선정
                    cos_arr.sort(key=itemgetter(1), reverse=True)
                    if len(cos_arr) > _TOP_N:
                        cos_arr = cos_arr[:_TOP_N]
                    com_idx_arr = []
                    cos_dic = {}
                    for cos_data in cos_arr:
                        com_idx_arr.append(cos_data[0])
                        cos_dic[cos_data[0]] = cos_data[1]

                    bunja = 0
                    bunmo = 0

                    for j in range(len(t_data)):
                        if j in com_idx_arr:
                            if t_data[j] != '':
                                bunja += int(t_data[j]) * cos_dic[j]
                                bunmo += cos_dic[j]
                    if bunmo != 0:
                        recm_pred[k] = '%.2f' % (bunja / bunmo)

            if k == 0:
                new_output += t_data[k] + ','
            else:
                if t_data[k] == '':
                    if k in recm_pred:
                        new_output += str(recm_pred[k]) + ','
                    else:
                        new_output += ','
                else:
                    new_output += t_data[k] + ','

        new_output = new_output[:-1]
        new_data.append(new_output+'\n')

    f_out = open(_OUTPUT_NAME, 'w')
    for line in new_data:
        f_out.write(line)
    f_out.close()
