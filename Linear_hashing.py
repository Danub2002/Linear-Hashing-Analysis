import math

class Linear_hashing:

  def __init__(self,page_size:int,m:int, alpha_max: float, alpha_min:float):
    self.page_size = page_size
    self.alpha_max = alpha_max
    self.alpha_min = alpha_min
    
    # self.buckets = [[None]*page_size] * m
    self.buckets = [[] for _ in range(m)]
    self.N = 0
    self.l = 0
    self.m = m
    self.occupied_spaces = 0
    self.spaces = m * page_size

    print(self.buckets)


  def check_insertion(self,key,i):
    num_pages_before = math.ceil(len(self.buckets[i]) / self.page_size)
    self.buckets[i].append(key)

    num_pages_after = math.ceil(len(self.buckets[i]) / self.page_size)
    
    if num_pages_after > num_pages_before and len(self.buckets[i]) > 1:
      # Se temos mais paginas depois de inserir quer dizer que encadeamos
      print(f'encadeia pq pags antes {num_pages_before} e dps e {num_pages_after}')
      self.spaces += self.page_size
    
    self.occupied_spaces += 1

  def insert(self,key):
    i = key % (self.m * 2 **self.l)

    print(f'inserir {key} na pos {i}',sep= " ")
    if i < self.N:
      i = key % (self.m * 2 ** (self.l + 1))
      print("usa do outro nivel",sep = " ")
    
    
    self.check_insertion(key,i)

    cur_alpha = self.occupied_spaces / self.spaces
    print(cur_alpha)
    while cur_alpha > self.alpha_max:
      dif = self.N + 2**self.l - len(self.buckets)
      new_rows = [[] for _ in range(dif)]
      self.buckets += new_rows
      print("quebra",sep = " ")
      
      
      print(self.buckets)
      self.spaces += self.page_size

      removing_key = []
      for k in self.buckets[self.N]:
        new_pos = k % (self.m * 2 ** (self.l + 1))

        if new_pos != self.N:
          removing_key.append((k,new_pos))
        
      for (k,pos) in removing_key:
        print(f'realoca {k} pra {pos}',sep = " ")
        self.buckets[self.N].remove(k)
        self.buckets[pos].append(k)
        self.check_insertion(k,pos)

      if self.N >= self.m * 2 ** self.l:
        self.N = 0; self.l += 1
    print(self.buckets)
    print()
  def print(self):
    for i in range(len(self.buckets)):
      print(f'L{i}')
      for j in range(len(self.buckets[i])):

        print(self.buckets[i][j],sep=" ")
      print("--------------------------")

h = Linear_hashing(page_size=2,m=2,alpha_max=0.8,alpha_min=0.5)
lista = [8, 11, 10, 15, 17, 25, 44, 12]
for l in lista:
  h.insert(l)

h.print()
