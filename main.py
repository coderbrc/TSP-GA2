# coding:utf:8
import math
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import operator
import mutations
import time
def main():
    global p_mutation, max_generation  #Mutasyon olasılığı ve maximum iterasyon sayısı
    generation = 1
    population_cur = init_population()  #Mevcut popülasyon sayısı.
    fitness = get_fitness(population_cur)  #Bireylerin fitnesslarını hesapla
    time_start = time.time()
    # Termination condition
    while generation < max_generation:
        population_next = select_sorted_population(fitness, population_cur, population_size // 4)
        for i in range(population_size):
            p1, p2 = selection(fitness, 2)
            child1, child2 = crossover(population_cur[p1], population_cur[p2])
            # Mutasyonlar
            if random.random() < p_mutation:
                child1 = mutations.select_best_mutaion(child1, distmat)
            if random.random() < p_mutation:
                child2 = mutations.select_best_mutaion(child2, distmat)
            population_next.append(child1)
            population_next.append(child2)
        # Bir sonraki neslin bireylerini seç, Popülasyondaki birey sayısı
        population_next = select_sorted_population(get_fitness(population_next), population_next, population_size)
        # En iyi kaydı bul
        pre_max_fitness, pre_max_individual = get_elite(fitness, population_cur)
        record(pre_max_fitness)
        # Replacement
        population_cur = population_next
        generation += 1
        # Fitnessları güncelle
        fitness = get_fitness(population_cur)
    # Kaydet ve çiz
    final_fitness, final_individual = get_elite(fitness, population_cur)
    record_distance = record(final_fitness)
    time_end = time.time()
    print('Evolution takes time:', time_end - time_start)
    print('Last path distance (m):',get_distance(final_individual)*111000)
    plot(final_individual)
    return
# Sırala ve popülasyon uzunluğunu döndür
def select_sorted_population(fitness, population, length):
    global population_size  #toplam grup numarası
    sort_dict = {}
    for i in range(len(population)):
        sort_dict[(fitness[i], 1 / fitness[i])] = i
    sorted_key = sorted(sort_dict.keys(), key=operator.itemgetter(0), reverse=True)
    sorted_index = [sort_dict[i] for i in sorted_key]
    sorted_population = [population[i] for i in sorted_index]
    # İlk elemanları al
    return sorted_population[:length]
# Grafiği çizme
def plot(sequnce):
    global record_distance, coordinates
    plt.figure(figsize=(15, 6))
    plt.subplot(121)
    plt.plot(record_distance)
    plt.ylabel('distance')
    plt.xlabel('iteration ')
    plt.subplot(122)
    x_list = []
    y_list = []
    for i in range(len(sequnce)):
        x_list.append(coordinates[sequnce[i]][1])
        y_list.append(coordinates[sequnce[i]][0])
    x_list.append(coordinates[sequnce[0]][1])
    y_list.append(coordinates[sequnce[0]][0])
    plt.plot(x_list, y_list, 'c-', label='Route')
    plt.plot(x_list, y_list, 'ro', label='Location')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    plt.xlabel("İteration")
    plt.ylabel("Distance")
    plt.title("Tsp Route")
    plt.grid(True)
    plt.legend()
    plt.show()
# En iyi veriyi al
def get_elite(fitness, population):
    max_index = fitness.index(max(fitness))  #En yüksek fitness indexini döndür
    max_fitness = fitness[max_index]         #En yüksek fitnessı döndür
    max_individual = population[max_index]   #En yüksek uygunluğa karşılık gelen bireye geri dönün
    return max_fitness, max_individual
def record(f):
    global record_distance
    return record_distance.append(1 / f * 111000)
# Rulet çarkı dönüş operatörleri
def selection(fitness, num):
    def select_one(fitness, fitness_sum):
        size = len(fitness)
        i = random.randint(0, size - 1)
        while True:
            if random.random() < fitness[i] / fitness_sum:
                return i
            else:
                i = (i + 1) % size
    res = set()
    fitness_sum = sum(fitness)
    while len(res) < num:
        t = select_one(fitness, fitness_sum)
        res.add(t)
    return res
# Bir gezi yolunun mesafesini hesapla
def get_distance(sequence):
    global distmat
    cost = 0
    for i in range(len(sequence)):
        cost += distmat[sequence[i - 1]][sequence[i]]
    return cost
# Fitness değerlerini hesapla
def get_fitness(population):
    fitness = []
    for i in range(len(population)):
        fitness.append(1 / get_distance(population[i]))
    return fitness
def crossover(parent1, parent2):
    global individual_size
    a = random.randint(1, individual_size - 1)
    child1, child2 = parent1[:a], parent2[:a]
    for i in range(individual_size):
        if parent2[i] not in child1:
            child1.append(parent2[i])
        if parent1[i] not in child2:
            child2.append(parent1[i])
    return child1, child2
# Başlangıç popülasyonu. Contains 10 individuals, each with 78 features
def init_population():
    global individual_size, population_size
    population_init = []
    for i in range(population_size):
        l = list(range(individual_size))
        population_init.append(random.sample(l, individual_size))
    return population_init
# Şehirler arasındaki mesafe matrisi al
def get_distmat(M):
    length = M.shape[0]
    distmat = np.zeros((length, length))
    for i in range(length):
        for j in range(i + 1,length):
            distmat[i][j] = distmat[j][i] = np.linalg.norm(M[i] - M[j])
            """x1 = M[i][0]
            y1 = M[i][1]
            x2 = M[j][0]
            y2 = M[j][1]
            distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            if (i == 0):
                distmat[i][j] = distmat[length-1][j] = distmat[j][i] = distmat[j][length-1] = distance
            else:
                distmat[i][j] = distmat[j][i] = distance"""
    return distmat
if __name__ == "__main__":
    # Verileri hazırla
    file = "coord.csv"
    coordinates = np.loadtxt(file, delimiter=';')
    distmat = get_distmat(coordinates)
    # Başlangıç parametreleri
    individual_size = coordinates.shape[0]
    max_generation = 100  #İterason sayısı
    population_size = 20   #Popülasyon büyüklüğü (Dahil edilen kişi sayısı)
    p_mutation = 0.2  #Mutasyon olasılığı
    record_distance = []
    main()

