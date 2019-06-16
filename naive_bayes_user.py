# 나이브 베이즈 CF : 사용자기반

# _INPUT_NAME = 'C:\hanyang\data_naive2.csv'
# _OUTPUT_NAME = 'C:\hanyang\data_naive2_out.csv'
_INPUT_NAME = 'C:\hanyang\paper\data_naive_2_train.csv'
_OUTPUT_NAME = 'C:\hanyang\paper\output\data_naive_2_train_bayes_user.csv'

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
                    like_idx = []
                    dislike_idx = []

                    for jj, data_row_jj in enumerate(l_data):
                        if jj > 0:  # skip username column
                            if data_row_jj == like_value:
                                like_cnt += 1
                                like_idx.append(jj)
                            elif data_row_jj == dislike_value:
                                dislike_cnt += 1
                                dislike_idx.append(jj)

                    p_r_like = like_cnt / (like_cnt + dislike_cnt)
                    p_r_dislike = dislike_cnt / (like_cnt + dislike_cnt)
                    like_mult = p_r_like
                    dislike_mult = p_r_dislike
                    # if i == 0:
                    #     print('')
                    #     print('p_r_like', p_r_like)
                    #     print('\tp_r_dislike', p_r_dislike)

                    row_idx_arr = item_con[j-1]
                    row_rate_arr = [] # like / dislike 값

                    for row_idx in row_idx_arr:
                        like_cnt2_1 = 0
                        dislike_cnt2_1 = 0
                        like_cnt2_2 = 0
                        dislike_cnt2_2 = 0
                        line_data = lines[row_idx].replace('\n', '').split(',')
                        row_rate_arr.append(line_data[j])
                        # [2, 4, 5]
                        for ii in range(item_cnt):
                            if l_data[ii+1] == like_value:
                                if line_data[ii+1] == line_data[j]:
                                    like_cnt2_1 += 1
                                elif line_data[ii+1] != '':
                                    dislike_cnt2_1 += 1
                            elif l_data[ii+1] == dislike_value:
                                if line_data[ii+1] == line_data[j]:
                                    dislike_cnt2_2 += 1
                                elif line_data[ii+1] != '':
                                    like_cnt2_2 += 1
                        # 확률 계산
                        # print('i', i, 'j', j, 'row_idx', row_idx)
                        if like_cnt2_1 + dislike_cnt2_1 != 0:
                            like_mult *= like_cnt2_1 / (like_cnt2_1 + dislike_cnt2_1)
                            # print('like!', like_cnt2_1, '/', like_cnt2_1 + dislike_cnt2_1)
                        if like_cnt2_2 + dislike_cnt2_2 != 0:
                            dislike_mult *= dislike_cnt2_2 / (like_cnt2_2 + dislike_cnt2_2)
                            # print('\tdislike!', dislike_cnt2_2, '/', like_cnt2_2 + dislike_cnt2_2)

                    # if i == 0:
                    #     print('')
                    #     print(j, 'row_idx_arr', row_idx_arr)
                    #     print(j, 'row_rate_arr', row_rate_arr)

                    # if i == 0:
                    #     print('row', i, 'column', j, data_row, ' ', 'LIKE RATE:', like_mult)
                    #     print('row', i, 'column', j, data_row, ' ', 'DISLIKE RATE:', dislike_mult)

                    if like_mult >= dislike_mult:
                        pred_rcmd[str(i)+'_'+str(j)] = like_value
                    else:
                        pred_rcmd[str(i) + '_' + str(j)] = dislike_value

    print('pred_rcmd', pred_rcmd)

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