import codecs
import os


# Define function
def loc(gt : set, rules : dict):
    sat = []
    # Duyệt từng chỉ số của tập luật
    for index in rules:
        # Lấy dòng luật
        rule:tuple = rules[index]
        # Tách các mệnh đề theo toán tử "và"
        sub_fact = str(rule[FACTS]).split(" và ")
        # Duyệt từng phần tử trong gt
        for s in gt:
            # Lấy các giả thiết con
            # sub_gt = str(s).split(" và ")
            # print(sub_gt)
            # Kiểm tra giả thiết từ tập luật có thuộc vào gt không
            check = all(item in s for item in sub_fact)
            # Nếu có, thêm chỉ số luật vào sat
            if(check):
                print(s)
                print(sub_fact)
                print("trùng: ",index)
                sat.append(index)
    return sat

def loc_cuoi(gt:set,rules : dict):

    gt_copy = gt.copy()
    # Duyệt từng gt
    for i in gt:
        # Duyệt từng dòng luật
        for index in rules:
            rule:tuple = rules[index]
            sub_fact = str(rule[FACTS]).split(" và ")
            for s in sub_fact:
                # Nếu gt thuộc vào gt_copy thì xoá khỏi gt
                if str(s) in i:
                    gt_copy.discard(i)
    return gt_copy

# Define constant
FACTS = 0
CONCLUSION = 1

if __name__ == "__main__":
    
    # Danh sách các luật 
    rules = {}
    # Danh sách các luật đã lấy từ SAT
    rules_copy = {}

    try:
        # Lấy đường dẫn tới file chương trình
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Mở file, mã hoá ký tự kiểu UTF-8 và lưu vào f 
        f = codecs.open(dir_path+"\data.txt","r","UTF-8")
        index = 0
        # Đọc từng dòng trong file
        for line in f:
            # Lưu giả thiết vào facts
            facts = line.split("->")[FACTS].strip()
            # Lưu kết luận vào conclusion
            conclusion = line.split("->")[CONCLUSION].rstrip("\r\n")
            # Chuyển dòng luật thành kiểu dictionary (key = index và value = (fact,conclusion))
            rules[index] = (facts,conclusion)
            index += 1
        print("Đã nạp tập luật")
    except FileNotFoundError:
        print("Không tìm thấy tập luật")

    # Khởi tạo tập GT chứa giả thiết do người dùng nhập
    gt = set()
    print("Nhập dữ kiện của bạn (Gõ stop để dừng): ")
    while True:
        # Đọc dòng từ bàn phím nhập
        row = input()
        if row in "stop":
            break
        # Thêm dòng vào gt
        gt.add(row)

    # Khởi tạo tập tg với giá trị từ gt
    tg = gt
    # Khởi tạo tập sat chứa dòng luật có giả thiết thuộc vào tg
    sat = loc(tg,rules)
    # Kiểm tra xem sat đã rỗng chưa
    i = 0
    while len(sat) != 0:
        # Lấy chỉ số dòng luật đầu tiên trong sat
        r = sat.pop(0)
        # Lấy dòng luật với chỉ số trong R
        rule = rules[r]
        # Thêm luật đã lấy vào bản sao luật
        rules_copy[r] = rule 
        # Thêm kết luận của luật đã lấy vào tg
        print("vòng:", i)
        tg.add(rule[CONCLUSION])
        print(tg)
        # Xoá dòng luật trong R
        del rules[r]
        # Cập nhật lại sat
        sat = loc(tg,rules)
        print(sat)
    # Lấy ra những tg không bị trùng với giả thiệt của luật trong rules_copy
    kl = loc_cuoi(tg,rules_copy)
    print("Động vật dự đoán: ",kl)
