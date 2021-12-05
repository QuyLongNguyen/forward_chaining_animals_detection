import codecs
import os
# Define constant
FACTS = 0
CONCLUSION = 1

# Define function

def standardlize(row : str):
    nega_pos = row.find("không")
    if nega_pos != -1:
        row = row.split("không")[1].strip()
        row = row.replace(" ","_")
        row = "không " + row
    else:
        row = row.strip().replace(" ","_")
    return row

def isContainedIn(ls:list,st:set):
    count = -1
    for i in range(len(ls)):
        for j in st:
            if j in ls[i]:
                count += 1
        if count != i:
            return False
        i += 1
    return True

def loc(gt : set, rules : dict):
    sat = []
    for index in rules:
        rule:tuple = rules[index]
        sub_fact = str(rule[FACTS]).split(" và ")
        if isContainedIn(sub_fact,gt):
            sat.append(index)
    return sat

def loc_cuoi(gt:set,rules : dict):

    gt_copy = gt.copy()
    for i in gt:
        for index in rules:
            rule:tuple = rules[index]
            sub_fact = str(rule[FACTS]).split(" và ")
            for s in sub_fact:
                if str(s) in i:
                    gt_copy.discard(i)
    return gt_copy

if __name__ == "__main__":
    

    rules = {}
    rules_copy = {}
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        f = codecs.open(dir_path+"\data.txt","r","UTF-8")
        index = 0
        for line in f:
            facts = line.split("->")[FACTS].strip()
            conclusion = line.split("->")[CONCLUSION].rstrip("\r\n")
            rules[index] = (facts,conclusion)
            index += 1
        print("Đã nạp tập luật")
    except FileNotFoundError:
        print("Không tìm thấy tập luật")
 
    gt = set()
    print("Nhập dữ kiện của bạn (Gõ stop để dừng): ")
    while True:
        row = input()
        if row in "stop":
            break
        gt.add(standardlize(row))

    sat = loc(gt,rules)
    while len(sat) != 0:
        r = sat.pop(0)
        rule = rules[r]
        rules_copy[r] = rule 
        gt.add(rule[CONCLUSION])
        del rules[r]
        sat = loc(gt,rules)
    animals = loc_cuoi(gt,rules_copy)
    print("Động vật dự đoán: ",animals)
