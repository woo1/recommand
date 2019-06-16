# 임계값 계산

# 1. 협업 필터링
# 사용자 : Top-5 사용, 총 15명
# 아이템 : TOP-10 사용, 총 92개

## 아래 논문에서 협업 필터링 사용 시 유사 사용자 그룹 30, 50, 100 이렇게 늘릴 때 차이 발생하므로
# 사용자는 3, 6, 10. 아이템은 10, 30, 50 으로 시도
## http://sclab.yonsei.ac.kr/publications/Papers/KC/2011_DC03.pdf (학술대회 논문 참조)

# 임계값은 중앙값, 평균 또는 내가 정한 값으로 처리

import numpy as np
# 협업필터링 추천값의 분포 계산 (중앙값, 평균, 추천된 데이터 수, 추천대상 데이터 수 - 추천 안돼있는 상태인 거)
def get_cf_dist(input_path, output_path):
    # 1. input_path 에서 값이 빈 걸 찾는다.
    input_empty = {}
    empty_cnt = 0

    with open(input_path) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i > 0:
                data_arr = line.replace('\n', '').split(',')
                for j, data in enumerate(data_arr):
                    if j > 0:
                        if data == '':
                            input_empty[str(i)+'_'+str(j)] = 1
                            empty_cnt += 1

    v_list = []
    # 2. 빈 값 위치에 값이 있으면 배열에 넣는다.
    with open(output_path) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i > 0:
                data_arr = line.replace('\n', '').split(',')
                for j, data in enumerate(data_arr):
                    if j > 0:
                        key = str(i) + '_' + str(j)
                        if key in input_empty and data != '':
                            v_list.append(float(data))

    # 3. 값 계산
    print('v_list', v_list)
    list_len = len(v_list)
    v_list = np.array(v_list)
    mean = np.mean(v_list)
    median = np.median(v_list)
    max1 = np.max(v_list)
    min1 = np.min(v_list)

    print('중앙값', format(median, '10.4f'), '평균', format(mean, '10.4f'), '추천된 데이터 수', list_len, '추천대상 데이터 수', empty_cnt,
          '최대값', format(max1, '10.4f'), '최소값', format(min1, '10.4f'))

# 컨텐츠 기반
def get_cbf_dist(input_path, output_path, data_max_idx=22):
    # 1. input_path 에서 값이 빈 걸 찾는다.
    input_empty = {}
    empty_cnt = 0

    with open(input_path) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i > 0:
                data_arr = line.replace('\n', '').split(',')
                print(len(data_arr))
                for j, data in enumerate(data_arr):
                    if j > data_max_idx:
                        if data == '':
                            input_empty[str(i)+'_'+str(j)] = 1
                            empty_cnt += 1

    v_list = []
    # 2. 빈 값 위치에 값이 있으면 배열에 넣는다.
    with open(output_path) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i > 0:
                data_arr = line.replace('\n', '').split(',')
                for j, data in enumerate(data_arr):
                    if j > data_max_idx:
                        key = str(i) + '_' + str(j)
                        if key in input_empty and data != '':
                            v_list.append(float(data))

    # 3. 값 계산
    print('v_list', v_list)
    list_len = len(v_list)
    v_list = np.array(v_list)
    mean = np.mean(v_list)
    median = np.median(v_list)
    max1 = np.max(v_list)
    min1 = np.min(v_list)

    print('중앙값', format(median, '10.4f'), '평균', format(mean, '10.4f'), '추천된 데이터 수', list_len, '추천대상 데이터 수', empty_cnt,
          '최대값', format(max1, '10.4f'), '최소값', format(min1, '10.4f'))

def merge_cbf(input_path1, input_path2, file_path1, file_path2, data_max_idx1=22, data_max_idx2=104):
    # 1. input_path 에서 값이 빈 걸 찾는다.
    input_empty1 = {}
    empty_cnt = 0

    with open(input_path1) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i > 0:
                data_arr = line.replace('\n', '').split(',')
                for j, data in enumerate(data_arr):
                    if j > data_max_idx1:
                        if data == '':
                            input_empty1[str(i) + '_' + str(j-data_max_idx1)] = 1
                            empty_cnt += 1

    print('empty_cnt1', empty_cnt)
    with open(input_path2) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i > 0:
                data_arr = line.replace('\n', '').split(',')
                for j, data in enumerate(data_arr):
                    if j > data_max_idx2:
                        if data == '':
                            key = str(i) + '_' + str(j-data_max_idx2)
                            if key not in input_empty1:
                                input_empty1[key] = 1
                                empty_cnt += 1

    v_list = []
    file_data = {}
    # 2. 빈 값 위치에 값이 있으면 배열에 넣는다.
    with open(file_path1) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i > 0:
                data_arr = line.replace('\n', '').split(',')
                for j, data in enumerate(data_arr):
                    if j > data_max_idx1:
                        key = str(i) + '_' + str(j-data_max_idx1)
                        if key in input_empty1 and data != '':
                            # v_list.append(float(data))
                            file_data[key] = float(data)

    percent1 = 0.8
    percent2 = 0.2
    with open(file_path2) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i > 0:
                data_arr = line.replace('\n', '').split(',')
                for j, data in enumerate(data_arr):
                    if j > data_max_idx2:
                        key = str(i) + '_' + str(j-data_max_idx2)
                        if key in input_empty1 and data != '':
                            if key in file_data:
                                file_data[key] = file_data[key] * percent1 + float(data) * percent2
                            else:
                                file_data[key] = float(data) * percent2
                            v_list.append(file_data[key])

    print('v_list', v_list)
    list_len = len(v_list)
    v_list = np.array(v_list)
    mean = np.mean(v_list)
    median = np.median(v_list)
    max1 = np.max(v_list)
    min1 = np.min(v_list)

    print('중앙값', format(median, '10.4f'), '평균', format(mean, '10.4f'), '추천된 데이터 수', list_len, '추천대상 데이터 수', empty_cnt,
          '최대값', format(max1, '10.4f'), '최소값', format(min1, '10.4f'))

def merge_cbf_file(input_path1, input_path2, file_path1, file_path2, data_max_idx1=22, data_max_idx2=104):
    # 1. input_path 에서 값이 빈 걸 찾는다.
    input_empty1 = {}
    empty_cnt = 0

    with open(input_path1) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i > 0:
                data_arr = line.replace('\n', '').split(',')
                for j, data in enumerate(data_arr):
                    if j > data_max_idx1:
                        if data == '':
                            input_empty1[str(i) + '_' + str(j-data_max_idx1)] = 1
                            empty_cnt += 1

    print('empty_cnt1', empty_cnt)
    with open(input_path2) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i > 0:
                data_arr = line.replace('\n', '').split(',')
                for j, data in enumerate(data_arr):
                    if j > data_max_idx2:
                        if data == '':
                            key = str(i) + '_' + str(j-data_max_idx2)
                            if key not in input_empty1:
                                input_empty1[key] = 1
                                empty_cnt += 1

    v_list = []
    file_data = {}
    # 2. 빈 값 위치에 값이 있으면 배열에 넣는다.
    with open(file_path1) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i > 0:
                data_arr = line.replace('\n', '').split(',')
                for j, data in enumerate(data_arr):
                    if j > data_max_idx1:
                        key = str(i) + '_' + str(j-data_max_idx1)
                        if key in input_empty1 and data != '':
                            # v_list.append(float(data))
                            file_data[key] = float(data)

    percent1 = 0.8
    percent2 = 0.2
    f_out = 'merged.csv'
    f_out = open(f_out, 'w')
    with open(file_path2) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                f_out.write(line)
            else:
                data_arr = line.replace('\n', '').split(',')
                for j, data in enumerate(data_arr):
                    if j > data_max_idx2:
                        key = str(i) + '_' + str(j-data_max_idx2)
                        if key in input_empty1 and data != '':
                            if key in file_data:
                                file_data[key] = file_data[key] * percent1 + float(data) * percent2
                            else:
                                file_data[key] = float(data) * percent2
                            data_arr[j] = str(file_data[key])
                f_out.write(','.join(data_arr) + '\n')

    f_out.close()

if __name__ == '__main__':
    # get_cf_dist(input_path='C:\hanyang\paper\data_2_train.csv', output_path='C:\hanyang\paper\output\data_2_train_result_user.csv')
    # get_cf_dist(input_path='C:\hanyang\paper\data_2_train.csv',
    #             output_path='C:\hanyang\paper\output\data_2_train_result_item.csv')
    # 사용자 기반 CF
    # 중앙값     3.2500 평균     3.3010 추천된 데이터 수 465 추천대상 데이터 수 465 최대값     5.0000 최소값     2.2300

    # 아이템 기반 CF
    # 중앙값     3.5100 평균     3.5843 추천된 데이터 수 353 추천대상 데이터 수 465 최대값     5.0000 최소값     2.0000

    # get_cf_dist(input_path='C:\hanyang\paper\data_3_train.csv', output_path='C:\hanyang\paper\output\data_3_train_result_network1.csv')
    # get_cf_dist(input_path='C:\hanyang\paper\data_3_train.csv',
    #             output_path='C:\hanyang\paper\output\data_3_train_result_network2.csv')
    # 네트워크 기반 - 질량 확산 접근법
    # 중앙값    34.3488 평균    39.1734 추천된 데이터 수 465 추천대상 데이터 수 465 최대값   118.5852 최소값     5.7776

    # 네트워크 기반 - 열 확산 접근법
    # 중앙값    43.5485 평균    48.4981 추천된 데이터 수 465 추천대상 데이터 수 465 최대값    94.5540 최소값    14.0328

    # 나이브 베이즈는 threshold 정할 필요가 없음 (like/dislike 이기 때문에)

    # get_cbf_dist(input_path='C:\hanyang\paper\data_cbf_train.csv', output_path='C:\hanyang\paper\output\data_cbf_train_result_content.csv', data_max_idx=22)
    # get_cbf_dist(input_path='C:\hanyang\paper\data_cbf_menu_train.csv',
    #              output_path='C:\hanyang\paper\output\data_cbf_menu_train_result_content.csv', data_max_idx=104)
    # 콘텐츠 기반
    # 중앙값     1.5733 평균     1.6570 추천된 데이터 수 465 추천대상 데이터 수 465 최대값     4.1603 최소값     0.3221

    # 콘텐츠 기반 - 메뉴
    # 중앙값     0.5443 평균     0.7567 추천된 데이터 수 465 추천대상 데이터 수 465 최대값     5.2206 최소값     0.0000

    # 콘텐츠 기반 - 메뉴 + 기존 방식
    # merge_cbf(input_path1='C:\hanyang\paper\data_cbf_train.csv', input_path2='C:\hanyang\paper\data_cbf_menu_train.csv', file_path1='C:\hanyang\paper\output\data_cbf_train_result_content.csv', file_path2='C:\hanyang\paper\output\data_cbf_menu_train_result_content.csv', data_max_idx1=22, data_max_idx2=104)
    merge_cbf_file(input_path1='C:\hanyang\paper\data_cbf_train.csv', input_path2='C:\hanyang\paper\data_cbf_menu_train.csv',file_path1='C:\hanyang\paper\output\data_cbf_train_result_content.csv',
              file_path2='C:\hanyang\paper\output\data_cbf_menu_train_result_content.csv', data_max_idx1=22, data_max_idx2=104)

    # 중앙값     1.0774 평균     1.2068 추천된 데이터 수 465 추천대상 데이터 수 465 최대값     4.1978 최소값     0.1610

    # 0.4(기존) : 0.6(menu)
    # 중앙값     0.9441 평균     1.1168 추천된 데이터 수 465 추천대상 데이터 수 465 최대값     4.4023 최소값     0.1288
    # 0.6(기존) : 0.4(menu)
    # 중앙값     1.1996 평균     1.2969 추천된 데이터 수 465 추천대상 데이터 수 465 최대값     3.9932 최소값     0.1932
    # 0.7(기존) : 0.3(menu)
    # 중앙값     1.2802 평균     1.3869 추천된 데이터 수 465 추천대상 데이터 수 465 최대값     3.8056 최소값     0.2254
    # 0.8(기존) : 0.2(menu)
    # 중앙값     1.4051 평균     1.4769 추천된 데이터 수 465 추천대상 데이터 수 465 최대값     3.9238 최소값     0.2576
    pass

