
class CacheSimulator:
    def __init__(self, cache_slots):
        self.cache_slots = cache_slots
        self.cache_hit = 0
        self.tot_cnt = 1
        self.cache = []
    
    def do_sim(self, page):
        self.tot_cnt += 1
        if page in self.cache: # hit
            self.cache.remove(page)
            self.cache.append(page)  # 0번 index가 LRU, 마지막 인덱스가 MRU
            self.cache_hit += 1
        else:  # miss
            if len(self.cache) >= self.cache_slots:
                self.cache.pop(0)
            self.cache.append(page)
        
    def print_stats(self):
        print("cache_slot = ", self.cache_slots, "cache_hit = ", self.cache_hit, "hit ratio = ", self.cache_hit / self.tot_cnt)


if __name__ == "__main__":

    data_file = open("./linkbench.trc")
    lines = data_file.readlines() # 파일에서 모든 라인을 읽어와 리스트로 생성
    for cache_slots in range(100, 1001, 100):
        cache_sim = CacheSimulator(cache_slots)
        for line in lines:
            page = line.split()[0]
            cache_sim.do_sim(page)
        
        cache_sim.print_stats()
