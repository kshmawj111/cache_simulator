import copy
import random

n = 2
s = 2
class LRU:
    size = 0
    LRU_queue = []

    def __init__(self, size):
        self.size = size

    def last_idx(self):
        return len(self.LRU_queue) - 1

    def set_data(self, value):

        if value not in self.LRU_queue:
            self.LRU_queue.insert(0, value)
            if len(self.LRU_queue) > self.size:
                del self.LRU_queue[self.last_idx()]

    def request_data(self, value):
        try:
            if value in self.LRU_queue:
                self.LRU_queue.remove(value)
                self.LRU_queue.insert(0, value)
                return value

        except:
            return False

    def is_in(self, value):
        if value in self.LRU_queue:
            return True
        else:
            return False

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
    base = [0 for x in range(2)]
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

    mem_address = random_num()  # mem_address = [[set_idx1, tag1], [set_idx2, tag2], ...]
    cache_table = initialize_cache()    # type = dictionary
    lru = LRU(int(n*2))

    for address in range(len(mem_address)):
        sum_valid_bit = 0
        hit_flag = 0

        set_idx = mem_address[address][0]  # input으로 주어지는 address 값의 set_idx를 구함
        input_tag = mem_address[address][1] # memory tag
        cache_table_value = copy.deepcopy(cache_table[set_idx])  # 위에서 구한 set_idx에 해당하는 key의 list를 cache_table_value에 복제

        lru.set_data(mem_address[address][1])

        # way의 갯수 만큼 hit의 갯수를 조사. hit라면 hit_flag에 1이 더해져 그 합은 0이 아니게 될 것임
        for way in range(n):
            #      hit
            #      cache tag             input address tag         cache valid bit
            if (cache_table_value[way][1] == input_tag) & (cache_table_value[way][0] == 1):
                hit_flag += 1
                lru.request_data(input_tag)
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
            way = 0
            lru_flag = False

            '''
            LRU_queue에 tag가 없는 way 블록의 값을 순차적으로 검사함. LRU policy에 따라 least recently used에 따라 가장
            오래전에 쓰여진 데이터가 있는 way 값에 input tag를 작성, iru_flag 역시 True로 바꿈
            만약 모든 way 블록의 값이 같아서 input tag를 작성하지 못하면, 즉 iru_flag가 계속 False라면
            way0 블럭의 tag를 수정하도록 함
            '''
            while way < n:
                _tag = cache_table_value[way][1]
                
                if lru.is_in(_tag):
                    way += 1

                else:  # cache table tag를 address tag로 수정
                    cache_table_value[way][1] = input_tag  # cache tag에 mem address tag wrtie
                    cache_table[set_idx] = cache_table_value  # 수정된 cache_table_value list를 cache_table의 key에 overwrite

            if lru_flag is True:
                continue

            else:
                cache_table_value[0][1] = input_tag
                cache_table[set_idx] = cache_table_value


        # way의 요소가 비어 있는게 있을 때
        else:
            for i in range(n):
                if cache_table_value[i][0] == 0:  # valid bit이 0이면 비어있다고 추정해 insert
                    cache_table_value[i][0] = 1  # valid bit을 1로 수정
                    cache_table_value[i][1] = input_tag # cache tag에 mem address tag wrtie
                    cache_table[set_idx] = cache_table_value  # 수정된 cache_table_value list를 cache_table의 key에 overwrite
                    break
                else:
                    continue
        #print(len(output_list),': ', cache_table)

    #print(mem_address)
    print('hit: ',hit)
    print('miss: ',miss)
    print('hit rate: ', (hit/(miss+hit)) * 100)
    return cache_table
if __name__ == '__main__':
    print(set_cache_data())
    '''lru = LRU(4)
    set_list = ['a', 'b', 'c', 'c', 'b', 'a', 'c', 'd', 'd', 'a', 'b', 'e']
    request_list = ['a', 'd', 'b', 'a', 'b', 'd','a', 'b', 'd', 'b', 'd', 'a']

    for x in range(len(request_list)):
        lru.set_data(set_list[x])
        lru.request_data(request_list[x])'''