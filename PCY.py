from itertools import combinations
from collections import defaultdict
import random
import time
import pandas as pd


def get_frequent_items_and_hashtable(dataset, min_support, dataset_size):
    item_counts = defaultdict(int)
    hashmap = defaultdict(int)
    itemset = []
    for items in dataset:
        pairs = list(combinations(items, 2))
        for i in items:
            item_counts[i] += 1
        for pair in pairs:
            hashmap[int(pair[0])*int(pair[1])%dataset_size] += 1
    for key in list(item_counts.keys()):
        if item_counts[key] >= min_support:
            itemset.append(key)

    return itemset, hashmap


def get_candidate_pairs(frequent_items):
    pairs = list(combinations(frequent_items, 2))
    return pairs


def PCY(dataset, min_support, dataset_size):
    frequent_itemsets, hashmap= get_frequent_items_and_hashtable(dataset, min_support*len(dataset), dataset_size)
    candidate_pairs = get_candidate_pairs(frequent_itemsets)
    pair_counts = defaultdict(int)
    for pair in candidate_pairs:
        if hashmap[int(pair[0])*int(pair[1]) % dataset_size] >= min_support*len(dataset):
            for transaction in dataset:
                if set(pair).issubset(transaction):
                    pair_counts[pair] += 1
    frequent_pairs = []
    for key in list(pair_counts.keys()):
        if pair_counts[key] >= min_support*len(dataset):
            frequent_pairs.append(key)
    return frequent_pairs


file_path = "retail.txt"
# Open the file in read mode
with open(file_path, "r") as file:
    # Read the contents of the file
    file_contents = file.readlines()
# Change to list
data = []
file_contents = [line.split(",") for line in file_contents]
for i in range(len(file_contents)):
    buckets = []
    buckets = file_contents[i][0].split(" ")
    buckets.pop()
    data.append(buckets)
dataset = [set(transaction) for transaction in data]
run_times = []
chunk_sizes = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
for chunk_size in chunk_sizes:
    start_time = time.time()
    print("Chunk size: ", chunk_size)
    dataset_size = int(len(dataset) * chunk_size)
    subset = random.sample(dataset, dataset_size)
    PCY(subset, 0.01, len(dataset))
    end_time = time.time()
    run_times.append((end_time - start_time)*1000)

df = pd.read_csv('report_0.01.csv')
new_df = pd.DataFrame({'PCY': run_times})
df = df.join(new_df)
df.to_csv('report_0.01.csv', index=False)
