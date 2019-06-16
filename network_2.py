# 네트워크 기반 - 열 확산 접근법
# Recall 계산 - Like로 나와야 될 것(3점 이상) 중 Like로 나온 것

# _INPUT_NAME = 'C:\hanyang\data_3.csv'
# _OUTPUT_NAME = 'C:\hanyang\data_3_network_2.csv'
_INPUT_NAME = 'C:\hanyang\paper\data_3_train.csv'
_OUTPUT_NAME = 'C:\hanyang\paper\output\data_3_train_result_network2.csv'

m = 100
with open(_INPUT_NAME) as f:
    data_in_org = f.readlines()
    data_in = data_in_org[1:]
    data_rcmd = []

    # print('data_in', data_in)

    # item별 연결 정보 확인
    item_con = {}
    # 사용자별 연결 정보 확인
    row_con = {}
    item_cnt = len(data_in[0].split(',')) - 1

    for j, data_row in enumerate(data_in):
        data_row = data_row.replace('\n', '')
        data_row = data_row.split(',')[1:]
        for k, d in enumerate(data_row):
            if d != '':
                if j in row_con:
                    row_con[j].append(k)
                else:
                    row_con[j] = [k]

    for i in range(item_cnt):
        for j, data_row in enumerate(data_in):
            data_row = data_row.replace('\n', '')
            data_row = data_row.split(',')[1:]
            if data_row[i] != '':
                if i in item_con:
                    item_con[i].append(j)
                else:
                    item_con[i] = [j]

    print('item_con', item_con)
    print('row_con', row_con)

    item_val_arr = []

    for j, data_row in enumerate(data_in):
        data_row = data_row.replace('\n', '')
        item_val = {}
        user_val = {}
        data_row = data_row.split(',')[1:]

        # 아이템에 초기값 m 세팅
        for i in range(item_cnt):
            if i in row_con[j]:
                item_val[i] = m
            else:
                item_val[i] = 0

        # 아이템 -> 사용자 계산
        for m_item_idx in row_con[j]:
            for c_user_idx in item_con[m_item_idx]:
                if c_user_idx not in user_val:
                    user_val[c_user_idx] = item_val[m_item_idx] / len(row_con[c_user_idx])
                else:
                    user_val[c_user_idx] += item_val[m_item_idx] / len(row_con[c_user_idx])

        item_val = {}
        # 사용자 -> 아이템 계산
        for uid in user_val:
            for item_id in row_con[uid]:
                if item_id in row_con[j]: # 이미 평가된 항목
                    continue

                if item_id not in item_val:
                    item_val[item_id] = user_val[uid] / len(item_con[item_id])
                else:
                    item_val[item_id] += user_val[uid] / len(item_con[item_id])

        item_val_arr.append(item_val)

    print('item_val_arr', item_val_arr)
    f_out = open(_OUTPUT_NAME, 'w')
    f_out.write(data_in_org[0])
    for j, data_row in enumerate(data_in):
        out_str_1 = ""
        data_row = data_row.replace('\n', '')
        data_row = data_row.split(',')
        for k, d in enumerate(data_row):
            if d == '':
                if k-1 in item_val_arr[j]:
                    out_str_1 += str(item_val_arr[j][k-1]) + ','
                else:
                    out_str_1 += ','
            else:
                out_str_1 += d + ','
        out_str_1 = out_str_1[:-1]
        f_out.write(out_str_1+'\n')
    f_out.close()
