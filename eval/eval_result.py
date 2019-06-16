
def get_data(line_arr, i_1, j_1):
    return line_arr[i_1].replace('\n', '').split(',')[j_1]

def calc_rslt(org_val, pred_val, threshold):
    org_val = float(org_val)
    pred_val = float(pred_val)

    if org_val > 3: # like
        if pred_val > threshold:
            return 'tp'
        else:
            return 'fn'
    else: # dislike
        if pred_val > threshold:
            return 'fp'
        else:
            return 'tn'

# network
def calc_rslt2(org_val, pred_val):
    if org_val == 'like':
        if pred_val == 'like':
            return 'tp'
        else:
            return 'fn'
    else:
        if pred_val == 'like':
            return 'fp'
        else:
            return 'fn'

# 콘텐츠 기반
def eval_cbf(output_file_path, val_file_path, threshold, first_idx=23):
    tp = 0
    fp = 0
    tn = 0
    fn = 0

    with open(output_file_path) as out:
        with open(val_file_path) as val:
            o_lines = out.readlines()
            v_lines = val.readlines()

            for i, line in enumerate(v_lines):
                if i > 0:
                    data_arr = line.replace('\n', '').split(',')
                    for j, data in enumerate(data_arr):
                        if j >= first_idx:
                            if data != '':
                                pred_val = get_data(o_lines, i, j)
                                if pred_val == '':
                                    fn += 1
                                else:
                                    rslt = calc_rslt(data, pred_val, threshold)

                                    if rslt == 'tp':
                                        tp += 1
                                    elif rslt == 'fp':
                                        fp += 1
                                    elif rslt == 'tn':
                                        tn += 1
                                    else:
                                        fn += 1

    return (tp, fp, tn, fn)

# 협업 필터링 평가
def eval_cf(output_file_path, val_file_path, threshold, is_naive=False):
    tp = 0
    fp = 0
    tn = 0
    fn = 0

    with open(output_file_path) as out:
        with open(val_file_path) as val:
            o_lines = out.readlines()
            v_lines = val.readlines()

            for i, line in enumerate(v_lines):
                if i > 0:
                    data_arr = line.replace('\n', '').split(',')
                    for j, data in enumerate(data_arr):
                        if j > 0:
                            if data != '':
                                pred_val = get_data(o_lines, i, j)
                                if pred_val == '':
                                    fn += 1
                                else:
                                    if is_naive:
                                        rslt = calc_rslt2(data, pred_val)
                                    else:
                                        rslt = calc_rslt(data, pred_val, threshold)

                                    if rslt == 'tp':
                                        tp += 1
                                    elif rslt == 'fp':
                                        fp += 1
                                    elif rslt == 'tn':
                                        tn += 1
                                    else:
                                        fn += 1

    return (tp, fp, tn, fn)

def get_accr(tp, fp, tn, fn):
    return (tp+tn)/(tp+fp+tn+fn)

def get_recall(tp, fn):
    return tp/(tp+fn)

def get_precision(tp, fp):
    return tp/(tp+fp)

def get_fscore(precision, recall):
    return 2 * (precision * recall)/(precision + recall)

def get_eval_rslt(tp, fp, tn, fn):
    recall = get_recall(tp=tp, fn=fn)
    precision = get_precision(tp=tp, fp=fp)
    f_score = get_fscore(precision=precision, recall=recall)
    accr = get_accr(tp, fp, tn, fn)

    return (recall, precision, f_score, accr)

if __name__ == '__main__':
    desc1 = ['사용자 기반 CF', '아이템 기반 CF', '네트워크 기반 - 질량 확산 접근법', '네트워크 기반 - 열 확산 접근법', '나이브 베이즈 CF : 아이템기반', '나이브 베이즈 CF : 사용자기반', '콘텐츠 기반 필터링', '콘텐츠 기반 필터링(메뉴)', '콘텐츠 기반 필터링(메뉴+기존)']
    desc2 = ['중앙값', '평균', '임의값']

    input_datas = []
    input_datas.append(('C:\hanyang\paper\output\data_2_train_result_user.csv', 'C:\hanyang\paper\data_2_val.csv', [3.25, 3.30, 2.9], 0))
    input_datas.append(('C:\hanyang\paper\output\data_2_train_result_item.csv', 'C:\hanyang\paper\data_2_val.csv', [3.51, 3.58, 3.3], 0))
    input_datas.append(('C:\hanyang\paper\output\data_3_train_result_network1.csv', 'C:\hanyang\paper\data_2_val.csv', [34.34, 39.17, 12], 0))
    input_datas.append(('C:\hanyang\paper\output\data_3_train_result_network2.csv', 'C:\hanyang\paper\data_2_val.csv', [43.54, 48.49, 15], 0))
    input_datas.append(('C:\hanyang\paper\output\data_naive_2_train_bayes_item.csv', 'C:\hanyang\paper\data_naive_2_val.csv', [0], 0))
    input_datas.append(('C:\hanyang\paper\output\data_naive_2_train_bayes_user.csv', 'C:\hanyang\paper\data_naive_2_val.csv', [0], 0))
    input_datas.append(('C:\hanyang\paper\output\data_cbf_train_result_content.csv', 'C:\hanyang\paper\data_cbf_val.csv', [1.57, 1.65, 1.1], 23))
    input_datas.append(('C:\hanyang\paper\output\data_cbf_menu_train_result_content.csv', 'C:\hanyang\paper\data_cbf_menu_val.csv', [0.54, 0.75, 0.1], 105))
    # input_datas.append(('C:\hanyang\paper\output\merged.csv', 'C:\hanyang\paper\data_cbf_menu_val.csv', [1.07, 1.20, 1.0], 105))
    # input_datas.append(('C:\hanyang\paper\output\merged2.csv', 'C:\hanyang\paper\data_cbf_menu_val.csv', [0.94, 1.11, 1.05], 105))
    # input_datas.append(('C:\hanyang\paper\output\merged3.csv', 'C:\hanyang\paper\data_cbf_menu_val.csv', [1.19, 1.29, 1.1], 105))
    # input_datas.append(('C:\hanyang\paper\output\merged4.csv', 'C:\hanyang\paper\data_cbf_menu_val.csv', [1.28, 1.38, 1.0], 105))
    input_datas.append(('C:\hanyang\paper\output\merged5.csv', 'C:\hanyang\paper\data_cbf_menu_val.csv', [1.40, 1.47, 1.2], 105))

    for j, input_data in enumerate(input_datas):
        # print(input_data)
        thresh_arr = input_data[2]
        print(desc1[j] + ' recall, precision, f_score, accr')
        for i, thresh in enumerate(thresh_arr):
            field_nm = desc2[i]
            thr_str = '(' + str(thresh) +')'
            if j == 4 or j == 5:
                field_nm = ''
                thr_str = ''
                tp, fp, tn, fn = eval_cf(output_file_path=input_data[0], val_file_path=input_data[1], threshold=thresh, is_naive=True)
            elif j == 6 or j == 7:
                tp, fp, tn, fn = eval_cbf(output_file_path=input_data[0], val_file_path=input_data[1], threshold=thresh, first_idx=input_data[3])
            else:
                tp, fp, tn, fn = eval_cf(output_file_path=input_data[0], val_file_path=input_data[1], threshold=thresh)
            recall, precision, f_score, accr = get_eval_rslt(tp, fp, tn, fn)
            print(str(i+1)+'.', field_nm, thr_str)
            print(format(recall, '10.4f'), format(precision, '10.4f'), format(f_score, '10.4f'), format(accr, '10.4f'))
        print()