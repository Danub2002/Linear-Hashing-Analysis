import math

class Linear_hashing:

  def __init__(self,page_size:int,m:int, alpha_max: float, alpha_min:float):
    self.page_size = page_size
    self.alpha_max = alpha_max
    self.alpha_min = alpha_min
    self.buckets = [[] for _ in range(m)]
    self.N = 0
    self.l = 0
    self.m = m
    self.occupied_spaces = 0
    self.spaces = m * page_size

    #print(self.buckets)


  def check_insertion(self,key,i,realocation=False):
    num_pages_before = math.ceil(len(self.buckets[i]) / self.page_size)
    self.buckets[i].append(key)

    num_pages_after = math.ceil(len(self.buckets[i]) / self.page_size)

    if num_pages_after > num_pages_before and len(self.buckets[i]) > 1:
      # Se temos mais paginas depois de inserir quer dizer que encadeamos
      #print(f'encadeia pq pags antes {num_pages_before} e dps e {num_pages_after}')
      self.spaces += self.page_size

    if not realocation:
      self.occupied_spaces += 1

  def insert(self,key):
    #print(f'nivel: {self.l}, N: {self.N}')
    i = key % (self.m * 2 **self.l)


    if i < self.N:
      i = key % (self.m * 2 ** (self.l + 1))
      #print("usa do outro nivel",sep = " ")


    self.check_insertion(key,i)
    #print(f'inserir {key} na pos {i}',sep= " ")
    #print(self.buckets)
    cur_alpha = self.occupied_spaces / self.spaces

    #print(cur_alpha)
    while cur_alpha > self.alpha_max:
      #print(f'quebra pq alpha: {cur_alpha}')
      # Calculate the desired size of self.buckets
      desired_size = self.N + self.m * (2 ** self.l)

      # Calculate the difference
      dif = desired_size - len(self.buckets) + 1
      for _ in range(dif):
        self.buckets.append([])

      #print("cria mais pag",self.buckets)
      self.spaces += self.page_size

      removing_key = []
      for k in self.buckets[self.N]:
        new_pos = k % (self.m * 2 ** (self.l + 1))

        if new_pos != self.N:
          removing_key.append((k,new_pos))
    
      num_paginas_original = math.ceil(len(self.buckets[self.N])/self.page_size)

      for (k,pos) in removing_key:
        #print(f'realoca {k} pra {pos}',sep = " ")
        self.buckets[self.N].remove(k)
        self.check_insertion(k,pos,realocation=True)

      # Depois de realocarmos precisamos verificar se o encadeamento de pags em N não é mais necessário e decrementar spaces
      # a quantidade de paginas encadeadas retiradas e floor(qnt_chaves_removidas / tam_pag)
      
    
      num_paginas_novo = math.ceil(len(self.buckets[self.N])/self.page_size)
      if num_paginas_novo == 0 and num_paginas_original != 0:
        num_paginas_novo = 1
      self.spaces -= (num_paginas_original - num_paginas_novo) * self.page_size

      self.N += 1
      #print(self.buckets)
      if self.N >= self.m * 2 ** self.l:
        self.N = 0; self.l += 1

      cur_alpha = self.occupied_spaces / self.spaces
      #print(f'dps de realocar ocupados {self.occupied_spaces}, espacos {self.spaces} e alpha: {cur_alpha}')
    #print()

  def remove(self, key):
    print(self.buckets)
    print(f'nivel: {self.l}, N: {self.N}')
    print(f'Removendo a chave {key}')

    i = key % (self.m * (2 ** self.l))

    if i < self.N:
        i = key % (self.m * (2 ** (self.l + 1)))

    # Removendo k da lista Li
    if key in self.buckets[i]:
        self.buckets[i].remove(key)
        self.occupied_spaces -= 1 # Atualizando a quantidade de espacos ocupados

    # Verificando se α < α_min
    cur_alpha = self.occupied_spaces / self.spaces
    print(self.buckets)
    print("α = ", cur_alpha, " \n")

    while cur_alpha < self.alpha_min:
        print(f'Eliminar pagina! Limite do fator de carga α_min violado (α = {cur_alpha}).\n')

        #Decrementando N
        self.N -= 1

        #Verificando se N < 0
        if self.N < 0:
            print('Como N < 0, entao todas as listas pertencem ao nivel l. Eh necessario retornar ao nivel anterior')
            self.l -= 1
            self.N = 2 ** self.l - 1

        #Realocando registros da lista L_(N+2^l*m) para L_N usando hl
        src_idx = self.N + (2 ** self.l) * self.m
        for k in self.buckets[src_idx]:
            new_pos = k % (self.m * 2 ** (self.l)) # Sempre sera igual a N
            self.check_insertion(k,new_pos,realocation=True)
            print(f'Realocando a chave {k} da lista L{src_idx} para L{new_pos}')
            print(self.buckets)

        # Depois de realocarmos precisamos decrementar spaces de acordo a quantidade de pags removidas em 'self.buckets[src_idx]'
        self.spaces -= self.page_size * math.ceil(len(self.buckets[src_idx]) / self.page_size)

        # Removendo a lista L_(N+2^l*m)
        print(f'Removendo a lista {src_idx}')
        self.buckets.pop(src_idx)
        print(self.buckets)

        cur_alpha = self.occupied_spaces / self.spaces

        print("α (apos eliminar pagina) = ", cur_alpha, " \n")
        print(f'nivel: {self.l}, N: {self.N} \n')

  def search(self, key):
    i = key % (self.m * (2 ** self.l))
    number_of_acesses = 1

    if i < self.N:
        i = key % (self.m * (2 ** (self.l + 1)))
    
    for k in self.buckets[i]:
        number_of_acesses += 1
        if k == key:        
            return math.ceil(number_of_acesses / self.page_size)

    return math.ceil(number_of_acesses / self.page_size)

  def get_alpha_medio(self):
    cur_alpha = self.occupied_spaces / self.spaces
    return cur_alpha

  def get_p_asterisk(self):
    val = 0
    for i in range(0, len(self.buckets)):
      val += math.ceil(len(self.buckets[i]) / self.page_size)

    return_val = val / len(self.buckets)

    return return_val
  
  def get_number_of_buckets(self):
    return len(self.buckets)


  def get_L_max2(self):
    maior_bucket = 0
    for bucket in self.buckets:
      if len(bucket) > maior_bucket:
        maior_bucket = len(bucket)
    maior_num_paginas = math.ceil(maior_bucket/self.page_size)
    #maior_num_paginas = round(maior_bucket/self.page_size, 2)
    if maior_bucket == 0:
      return 1
    return maior_num_paginas
    

  def print(self):
    for i in range(len(self.buckets)):
      print(f'L{i}')
      for j in range(len(self.buckets[i])):

        print(self.buckets[i][j],sep=" ")
      print("--------------------------")