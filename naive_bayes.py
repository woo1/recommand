# 나이브 베이즈 CF : 아이템기반

_INPUT_NAME = 'C:\hanyang\paper\data_naive_2_train.csv'
_OUTPUT_NAME = 'C:\hanyang\paper\output\data_naive_2_train_bayes_item.csv'

with open(_INPUT_NAME, 'r') as f:
    lines_origin = f.readlines()
    lines = lines_origin[1:]

    item_con = {}

    item_cnt = len(lines[0].split(','))-1
    for i in range(item_cnt):
        for j, data_row in enumerate(lines):
            data_row = data_row.replace('\n', '')
            data_row = data_row.split(',')[1:]
            if data_row[i] != '':
                if i in item_con:
                    item_con[i].append(j)
                else:
                    item_con[i] = [j]

    print('item_con', item_con)
    # like_value = '1'
    # dislike_value = '0'
    like_value = 'like'
    dislike_value = 'dislike'

    pred_rcmd = {}

    for i, line in enumerate(lines):
        line = line.replace('\n', '')
        l_data = line.split(',')
        for j, data_row in enumerate(l_data):
            if j > 0: # skip username column
                if data_row == '': # 평가되지 않은 항목
                    # 해당 아이템이 like(1)일 확률 계산
                    # P(R1 = like)
                    p_r_like = 0
                    p_r_dislike = 0
                    like_cnt = 0
                    dislike_cnt = 0

                    for data_idx in item_con[j-1]:
                        val1 = lines[data_idx].replace('\n', '').split(',')[j]
                        if val1 == like_value:
                            like_cnt += 1
                        elif val1 == dislike_value:
                            dislike_cnt += 1

                    p_r_like = like_cnt / (like_cnt + dislike_cnt)
                    p_r_dislike = dislike_cnt / (like_cnt + dislike_cnt)
                    like_mult = p_r_like
                    dislike_mult = p_r_dislike
                    # if i == 0:
                    #     print('')
                    #     print('p_r_dislike', p_r_dislike)

                    for jj, data_row_jj in enumerate(l_data):
                        p_col1_like = 0
                        p_col1_dislike = 0
                        p_col1 = 0
                        p_col1_d = 0

                        if jj > 0 and data_row_jj != '' and jj != j:
                            for data_idx in item_con[j - 1]:
                                line_val = lines[data_idx].replace('\n', '').split(',')
                                val1 = line_val[j]

                                if val1 == like_value:
                                    if line_val[jj] == data_row_jj:
                                        p_col1_like += 1
                                        p_col1 += 1
                                    elif line_val[jj] != '':
                                        p_col1 += 1
                                elif val1 == dislike_value:
                                    if line_val[jj] == data_row_jj:
                                        p_col1_dislike += 1
                                        p_col1_d += 1
                                    elif line_val[jj] != '':
                                        p_col1_d += 1

                            if p_col1 != 0:
                                # if i == 0:
                                #     print('p_col1_like / p_col1:', p_col1_like,  '/', p_col1, 'jj', jj, 'data_row_jj', data_row_jj)
                                like_mult *= p_col1_like / p_col1
                            if p_col1_d != 0:
                                # if i == 0:
                                #     print('p_col1_dislike / p_col1:', p_col1_dislike,  '/', p_col1_d, 'jj', jj, 'data_row_jj', data_row_jj)
                                dislike_mult *= p_col1_dislike / p_col1_d

                    if i == 0:
                        print('row', i, 'column', j, data_row, ' ', 'LIKE RATE:', like_mult)
                        print('row', i, 'column', j, data_row, ' ', 'DISLIKE RATE:', dislike_mult)

                    if like_mult >= dislike_mult:
                        pred_rcmd[str(i)+'_'+str(j)] = like_value
                    else:
                        pred_rcmd[str(i) + '_' + str(j)] = dislike_value

    out_f = open(_OUTPUT_NAME, 'w')

    for i, line in enumerate(lines_origin):
        if i == 0:
            out_f.write(line)
            continue
        data_arr = line.replace('\n', '').split(',')
        for j, data in enumerate(data_arr):
            key = str(i-1) + '_' + str(j)
            if key in pred_rcmd:
                data_arr[j] = pred_rcmd[key]

        out_f.write(','.join(data_arr) + '\n')

    print('pred_rcmd', pred_rcmd)
    out_f.close()