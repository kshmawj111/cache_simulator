import copy
import random
n = 2
s = 2

def random_num():
    a = []
    i = 0
    while i<5000000:
        base = [0,0]
        v1 = random.randrange(0,2**n)
        base[0] = v1
        v2 = random.randrange(0,40)
        base[1] = v2
        a.append(base)
        i += 1
    return a

def initialize_cache():
    cache = dict()
    table = copy.deepcopy(n_way_table())
    for x in range(2 ** s):
        cache[x] = copy.deepcopy(table)

    return cache


# [valid bit, tag, LRU count]로 이루어진 set index당 매칭될 list 생성
def n_way_table():
    base = [0 for x in range(3)]
    table = [copy.deepcopy(base) for x in range(n)]

    return table


def all_same(list):
    return all(x == list[0] for x in list)


def find_min_value_idx(double_list, key_idx):
    sorted_list = copy.deepcopy(double_list)
    sorted_list.sort(key=lambda x: x[key_idx])  # double arrayd의 세번째 원소로 sort
    minimum_value = sorted_list[0][2]
    for x in range(len(double_list)):
        if double_list[x][2] == minimum_value:
            return x


def set_cache_data():
    output_list = []
    hit = 0
    miss = 0

    mem_address = random_num() # mem_address = [[set_idx1, tag1], [set_idx2, tag2], ...]
    cache_table = initialize_cache()  # type = dictionary

    for address in range(len(mem_address)):
        sum_valid_bit = 0
        hit_flag = 0

        set_idx = mem_address[address][0]  # input으로 주어지는 address 값의 set_idx를 구함
        cache_table_value = copy.deepcopy(cache_table[set_idx])  # 위에서 구한 set_idx에 해당하는 key의 list를 cache_table_value에 복제

        # way의 갯수 만큼 hit의 갯수를 조사. hit라면 hit_flag에 1이 더해져 그 합은 0이 아니게 될 것임
        for way in range(n):
            #      hit
            #      cache tag                      input address tag               cache valid bit
            if (cache_table_value[way][1] == mem_address[address][1]) & (cache_table_value[way][0] == 1):
                hit_flag += 1
                cache_table_value[way][2] += 1
                break

            #   miss
            else:
                hit_flag += 0

        #   output list에 mem address에 따른 hit or miss result를 쓰고 후에 대응하는 테이블을 만들기 위해 보관
        if hit_flag == 1:
            output_list.append('hit')
            hit += 1

        elif hit_flag == 0:
            output_list.append('miss')
            miss += 1

        else:
            print('error')
        '''

        cache table에 tag를 저장할 때, way들의 valid bit 중 한 개라도 0이면 비어있다고 추정하여 valid bit이 0인 way의 tag에 저장
        만약, valid bit의 합이 way의 갯수와 같아진다면 way의 tag는 이미 찼다고 판단하여 LRU value를 조사함
        LRU value가 가장 작은 way의 tag를 새로운 input_tag로 수정하고
        만약 LRU가 모두 같다면 way[0]의 tag를 수정함. 


        '''
        # valid bit의 합 구하기
        for way in range(n):
            sum_valid_bit += cache_table_value[way][0]

        # way의 요소가 꽉 찼을 때. 즉, LRU를 참조해야 할때
        if sum_valid_bit == n:
            lru_value = []

            # 모든 lru를 조사함
            for idx in range(n):
                lru_value.append(cache_table_value[idx][2])

                # 모든 lru가 같다면
                if all_same(lru_value) is True:
                    cache_table_value[0][1] = mem_address[address][1]  # way0에 새로운 tag로 수정
                    cache_table[
                        set_idx] = cache_table_value  # 수정된 cache_table_value list를 cache_table의 key에 overwrite
                    break

                else:
                    way = find_min_value_idx(cache_table_value,
                                                  2)  # double list cache_table_value에 2번째 항목의 idx를 리턴
                    cache_table_value[way][1] = mem_address[address][1]  # cache tag에 mem address tag wrtie
                    cache_table[set_idx] = cache_table_value  # 수정된 cache_table_value list를 cache_table의 key에 overwrite
                    break

        # way의 요소가 비어 있는게 있을 때
        else:
            for i in range(n):
                if cache_table_value[i][0] == 0:  # valid bit이 0이면 비어있다고 추정해 insert
                    cache_table_value[i][0] = 1  # valid bit을 1로 수정
                    cache_table_value[i][1] = mem_address[address][1]  # cache tag에 mem address tag wrtie
                    cache_table[
                        set_idx] = cache_table_value  # 수정된 cache_table_value list를 cache_table의 key에 overwrite
                    break
                else:
                    continue

        #print(len(output_list), ': ', cache_table)

    #print(mem_address)
    print('hit: ', hit)
    print('miss: ', miss)
    print('hit rate: ', (hit/(miss+hit)) * 100)
    return cache_table

if __name__ == '__main__':
    print(set_cache_data())