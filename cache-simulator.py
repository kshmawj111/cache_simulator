import argparse
import math
import copy

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
                return True

        except:
            return False

class CacheSimulator:

    # 변수 설정
    # 세트의 갯수, 블록 사이즈, 워드 사이즈
    s, n, m = 0, 0, 0
    filename = ''

    #  입력 값이 2의 거듭제곱이 아니거나 음수일 때 False를 리턴, 거듭제곱 꼴일 때만 True를 리턴
    def is_power_of_two(self, n):
        # 정수가 아닐경우
        if not isinstance(n, int):
            return False

        # 비트 연산에서 거듭제곱은 비트 자리 중에 단 하나를 차지하는 성질을 이용하여 연산
        elif n > 0:
            return (n & (n - 1)) == 0

        # 음수일 경우 혹은 그 외의 경우
        else:
            return False


    def main(self):
        parser = argparse.ArgumentParser(description='Associative Cache Simulator')
        # '-s: 세트 수, -n: 세트 당 블록 개수, -m: 워드 크기, -target: 파일이름'

        parser.add_argument('-s', type=int, required=True, help='number of sets. Must be power of two')
        parser.add_argument('-n', type=int, required=True, help='number of blocks per set. Must be power of two')
        parser.add_argument('-m', type=int, required=True, help="word size. Must be power of two")
        parser.add_argument('filename', default='test.in', help="file name containing address")

        args = parser.parse_args()

        if self.is_power_of_two(args.s) & self.is_power_of_two(args.n) & self.is_power_of_two(args.m) is True:
            self.s = int(math.log(args.s, 2))
            self.n = args.n
            self.m = int(math.log(args.m, 2))
            self.filename = args.filename
            return True

        else:
            print("모든 연산자는 2의 n승 꼴이어야 합니다.")
            return False


    def read_memory(self):
        file = open(self.filename, 'r')
        hex_address_list = []

        while True:
            line = file.readline()
            if line:
                line = line[2:10]
                hex_address_list.append(line)

            else:
                break

        file.close()
        return hex_address_list


    def hex_to_binary(self):
        bi_address_list = []
        hex_address_list = self.read_memory()
        for i in range(len(hex_address_list)):
            temp = bin(int(hex_address_list[i], 16))
            temp = temp[2:].zfill(32)
            bi_address_list.append(str(temp))

        return bi_address_list

    # 한 개의 binary memory address를 인자로 받아 입력 받은 s, n, m 값을 바탕으로 분해하고
    # 나온 결과 값을 decomposed란 [set_idx, tag] 형태로 return
    def decompose_address(self, bi_address):
        block_address = bi_address[0:32-(self.m + 2)]
        tag = bi_address[0:32-(self.s + self.m + 2)]
        set_idx = int(block_address, 2) % (2**self.s)
        decomposed = [set_idx, tag]
        return decomposed

        '''set_idx = block_address[32-(self.s + self.m + 2):]
               print('original: ', bi_address)
               print('word:     ', word_address)
               print('block:    ',block_address)
               print('tag add:  ',tag)
               print('setidx add', set_idx)
               print('')'''

    # bi_address_list로부터 받은 모든 address를 decompose 하여 새로운 decomposed_list로 저장
    def set_decomposed_list(self):
        bi_address_list = self.hex_to_binary()
        decomposed_list = []

        for address in bi_address_list:
            temp = self.decompose_address(address)
            decomposed_list.append(temp)

        return decomposed_list

    # Key = set_idx, Value = [valid bit = 0, tag = 0bXXXXXXXXXXXX]로 이루어진 dict를 생성
    # 입력받은 s값 만큼 key value를 생성하고 그에 대응하여 value를 match
    def initialize_cache(self):
        cache = dict()
        table = copy.deepcopy(self.n_way_table())
        for x in range(2 ** self.s):
            cache[x] = copy.deepcopy(table)

        return cache

    # [valid bit, tag, LRU count]로 이루어진 set index당 매칭될 list 생성
    def n_way_table(self):
        base = [0 for x in range(3)]
        table = [copy.deepcopy(base) for x in range(self.n)]

        return table

    def all_same(self, list):
        return all(x == list[0] for x in list)

    def find_min_value_idx(self, double_list, key_idx):
        sorted_list = copy.deepcopy(double_list)
        sorted_list.sort(key=lambda x: x[key_idx])  # double arrayd의 세번째 원소로 sort
        minimum_value = sorted_list[0][2]
        for x in range(len(double_list)):
            if double_list[x][2] == minimum_value:
                return x

    def set_cache_data(self):
        output_list = []
        hit = 0
        miss = 0

        mem_address = self.set_decomposed_list()  # mem_address = [[set_idx1, tag1], [set_idx2, tag2], ...]
        cache_table = self.initialize_cache()  # type = dictionary

        for address in range(len(mem_address)):
            sum_valid_bit = 0
            hit_flag = 0

            set_idx = mem_address[address][0]  # input으로 주어지는 address 값의 set_idx를 구함
            cache_table_value = copy.deepcopy(cache_table[set_idx])  # 위에서 구한 set_idx에 해당하는 key의 list를 cache_table_value에 복제

            # way의 갯수 만큼 hit의 갯수를 조사. hit라면 hit_flag에 1이 더해져 그 합은 0이 아니게 될 것임
            for way in range(self.n):
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
            for way in range(self.n):
                sum_valid_bit += cache_table_value[way][0]

            # way의 요소가 꽉 찼을 때. 즉, LRU를 참조해야 할때
            if sum_valid_bit == self.n:
                lru_value = []

                # 모든 lru를 조사함
                for idx in range(self.n):
                    lru_value.append(cache_table_value[idx][2])

                    # 모든 lru가 같다면
                    if self.all_same(lru_value) is True:
                        cache_table_value[0][1] = mem_address[address][1]  # way0에 새로운 tag로 수정
                        cache_table[
                            set_idx] = cache_table_value  # 수정된 cache_table_value list를 cache_table의 key에 overwrite
                        break

                    else:
                        way = self.find_min_value_idx(cache_table_value, 2)  # double list cache_table_value에 2번째 항목의 idx를 리턴
                        cache_table_value[way][1] = mem_address[address][1]  # cache tag에 mem address tag wrtie
                        cache_table[set_idx] = cache_table_value  # 수정된 cache_table_value list를 cache_table의 key에 overwrite
                        break

            # way의 요소가 비어 있는게 있을 때
            else:
                for i in range(self.n):
                    if cache_table_value[i][0] == 0:  # valid bit이 0이면 비어있다고 추정해 insert
                        cache_table_value[i][0] = 1  # valid bit을 1로 수정
                        cache_table_value[i][1] = mem_address[address][1]  # cache tag에 mem address tag wrtie
                        cache_table[
                            set_idx] = cache_table_value  # 수정된 cache_table_value list를 cache_table의 key에 overwrite
                        break
                    else:
                        continue



if __name__ == "__main__":
    a = CacheSimulator()
    if a.main() is True:
        # print(a.decompose_address('00000000000011000001010010111000'))
        pass



