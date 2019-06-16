# 사용자 기반 협업필터링, 가중평균, Top-3 선정
# output에 추천값이 없는 경우는 유사 사용자 Top-5도 안 먹어본 곳이라 그런 거임
# Top-5 사용. 총 15명
import math
from operator import itemgetter

_INPUT_NAME = 'C:\hanyang\paper\data_2_train.csv'
_OUTPUT_NAME = 'C:\hanyang\paper\output\data_2_train_result_user.csv'
_TOP_N = 10

with open(_INPUT_NAME) as f:
    data_in_org = f.readlines()
    data_in = data_in_org[1:]
    sumsq_arr = []
    data_rcmd = []

    for i, data_target in enumerate(data_in):
        data_target = data_target.replace('\n', '')
        data = data_target.split(',')
        sumsq = 0
        for j, data_val in enumerate(data):
            if j != 0 and data_val != '':
                sumsq = sumsq + (int(data_val)*int(data_val))
        sumsq_arr.append(math.sqrt(sumsq))

    for i, data_target in enumerate(data_in):
        cos_arr = []
        sqrt_t = sumsq_arr[i]
        data_target = data_target.replace('\n', '')
        t_data = data_target.split(',')
        recm_pred = {}

        for j, data_comp in enumerate(data_in):
            data_comp = data_comp.replace('\n', '')
            c_data = data_comp.split(',')
            sumprd = 0

            if i != j:
                sqrt_c = sumsq_arr[j]
                for k in range(len(t_data)):
                    if k > 0:
                        if t_data[k] != '' and c_data[k] != '':
                            sumprd += int(t_data[k]) * int(c_data[k])
                cos_arr.append((j, sumprd / (sqrt_t*sqrt_c)))
            # else:
            #     cos_arr.append((j, 1))

        cos_arr.sort(key=itemgetter(1), reverse=True)
        if len(cos_arr) > _TOP_N:
            cos_arr = cos_arr[:_TOP_N]
        com_idx_arr = []
        cos_dic = {}
        for cos_data in cos_arr:
            com_idx_arr.append(cos_data[0])
            cos_dic[cos_data[0]] = cos_data[1]

        print('cos_dic', cos_dic)

        # 평가 안된 항목 대상으로 가중평균 평가값 추정
        print('t_data', t_data)
        for j, data_val in enumerate(t_data):
            if j > 0:
                bunja = 0
                bunmo = 0

                if data_val == '':
                    for k, data_comp in enumerate(data_in):
                        if k not in com_idx_arr:
                            continue
                        if i != k:
                            data_comp = data_comp.replace('\n', '')
                            c_data = data_comp.split(',')
                            # print('c_data', c_data, 'j', j, c_data[j])
                            if c_data[j] != '':
                                # print('.............', cos_arr[k], 'k', k)
                                bunja += int(c_data[j]) * cos_dic[k]
                                bunmo += cos_dic[k]
                    if bunmo != 0:
                        recm_pred[j] = bunja / bunmo

        data_rcmd.append(recm_pred)

    print(data_rcmd)
    f_out = open(_OUTPUT_NAME, 'w')
    f_out.write(data_in_org[0])  # 1st line .. column info
    for i, org_data in enumerate(data_in):
        org_data = org_data.replace('\n', '')
        o_data = org_data.split(',')
        out_str = ''
        for j, o_data_val in enumerate(o_data):
            if o_data_val != '':
                out_str += o_data_val + ','
            else:
                if len(data_rcmd) > i and j in data_rcmd[i]:
                    out_str += '%.2f' % (data_rcmd[i][j]) + ','
                else:
                    out_str += ','
        out_str = out_str[:-1]
        f_out.write(out_str+'\n')
    f_out.close()
