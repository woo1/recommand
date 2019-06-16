# 콘텐츠 기반 필터링
# 한 사람의 평가 데이터만 가지고 추천하는 방법
# 새로 추가된 또는 인기 없는 아이템 추천 가능
# 정규화 및 TF-IDF 사용

import math

# _INPUT_NAME = 'C:\hanyang\data_cbf.csv'
# _OUTPUT_NAME = 'C:\hanyang\data_cbf_out.csv'
# _RATING_COL_IDX = 14

# content 1
# _INPUT_NAME = 'C:\hanyang\paper\data_cbf_train.csv'
# _OUTPUT_NAME = 'C:\hanyang\paper\output\data_cbf_train_result_content.csv'
# _RATING_COL_IDX = 23

# content_menu
# _INPUT_NAME = 'C:\hanyang\paper\data_cbf_menu_train.csv'
# _OUTPUT_NAME = 'C:\hanyang\paper\output\data_cbf_menu_train_result_content.csv'
# _RATING_COL_IDX = 105

def null2void(val):
    if val == '':
        return 0
    else:
        return val

fst_line = ''
with open(_INPUT_NAME, 'r') as f:
    lines_origin = f.readlines()
    fst_line = lines_origin[0]
    lines_origin = lines_origin[1:]
    lines_2 = []
    for line in lines_origin:
        lines_2.append(line.replace('\n', ''))
    lines = lines_2
    del lines_2

# 정규화
lines_2 = []
for line in lines:
    data = line.split(',')
    no_zero_cnt = 0

    for i, data_val in enumerate(data):
        if i > 0 and i<_RATING_COL_IDX:
            if data_val != '' and data_val != '0':
                no_zero_cnt += 1
    if no_zero_cnt == 0:
        print(line)

    line_str = ''
    for i, data_val in enumerate(data):
        if i > 0 and i<_RATING_COL_IDX:
            line_str += str(int(null2void(data_val)) / math.sqrt(no_zero_cnt)) + ','
        else:
            line_str += data_val + ','
    line_str = line_str[:-1]
    lines_2.append(line_str)

# print('\n'.join(lines_2))

user_prof_list = []
idf_arr_list = []

empty = []

len_words = len(lines_origin[1].replace('\n', '').split(','))
for k in range(_RATING_COL_IDX, len_words):
    user_prof = []
    idf_arr = []
    # 아이템 프로파일 값 계산
    for i in range(_RATING_COL_IDX):
        if i > 0:
            prof_val = 0
            df = 0
            for j, line in enumerate(lines_2):
                line = line.split(',')

                if float(null2void(line[i])) != 0:
                    df += 1
                prof_val += float(null2void(line[i])) * int(null2void(line[k])) # line[_RATING_COL_IDX]
            user_prof.append(prof_val)

            # if df == 0:
            #     fuck = fst_line.replace('\n', '').split(',')[i]
            #     if fuck not in empty:
            #         empty.append(fuck)
            idf_arr.append(1/df)
    user_prof_list.append(user_prof)
    idf_arr_list.append(idf_arr)

# print(empty)


# 평가 안된 아이템의 추천값 계산
rcmd_arr_list = []

for k in range(_RATING_COL_IDX, len_words):
    rcmd_arr = []
    user_prof = user_prof_list[k - _RATING_COL_IDX]
    idf_arr = idf_arr_list[k - _RATING_COL_IDX]
    for j, line in enumerate(lines_2):
        line = line.split(',')
        rcmd = 0
        if line[k] != '': # [_RATING_COL_IDX]
            rcmd_arr.append(int(line[k])) # [_RATING_COL_IDX]
        else:
            for i in range(_RATING_COL_IDX):
                if i > 0:
                    rcmd += float(null2void(line[i])) * user_prof[i-1] * idf_arr[i-1]
            rcmd_arr.append(rcmd)

    rcmd_arr_list.append(rcmd_arr)

f_out = open(_OUTPUT_NAME, 'w')
f_out.write(fst_line)
for j, line in enumerate(lines_2):
    arr = line.split(',')[:_RATING_COL_IDX]

    for k in range(_RATING_COL_IDX, len_words):
        rate = line.split(',')[k] #_RATING_COL_IDX
        rcmd_arr = rcmd_arr_list[k - _RATING_COL_IDX]
        if rate == '':
            # arr = line.split(',')[:-1]
            arr.append(str(rcmd_arr[j]))
            # print(arr)
            # f_out.write(','.join(arr)+'\n')
        else:
            arr.append('')
            # f_out.write(line+'\n')

    f_out.write(','.join(arr) + '\n')
f_out.close()
print('rcmd_arr', rcmd_arr)