# Import Module
from tkinter import *
import tkinter.font as tkFont
import codecs
import os

# Define constant
FACTS = 0
CONCLUSION = 1


def startProgram():
  
    root = Tk()

    # root window title and dimension
    root.title("Forward Chaining Program")

    # Set geometry (widthxheight)
    root.geometry('500x500')

    # draw components
    lbl = Label(root, text = "Animal guessing",font=tkFont.Font(size=16)).place(relx=0.5,rely=0.05,anchor="n")
    lbl = Label(root, text = "Input your facts: ").place(relx=0.1,rely=0.1,anchor="n")
    lbl = Label(root, text = "My conclusions: ").place(relx=0.1,rely=0.6,anchor="n")

    txt_fact = Text(root, height = 9, width = 45)
    txt_fact.place(relx=0.5,rely=0.15,anchor="n")
    txt_conclu = Text(root, height = 5, width = 45)
    txt_conclu.place(relx=0.5,rely=0.65,anchor="n")
    txt_conclu.config(state=DISABLED)

    btn_guess = Button(root, text = "Guess" , fg = "black",command = lambda : guess())
    btn_guess.place(relx=0.5,rely=0.5,anchor="n")
    btn_reset = Button(root, text = "Reset" , fg = "black",command = lambda: reset())
    btn_reset.place(relx=0.5,rely=0.9,anchor="n")

    # button's functions
    def guess():
        rules = loadRules()
        rules_copy = {} 
        input = txt_fact.get("1.0",END).splitlines()
        gt = set(input)
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
        output = ",".join(kl)
        txt_conclu.config(state=NORMAL)
        txt_conclu.insert(END,output)
        txt_conclu.config(state=DISABLED)


    def reset():
        txt_conclu.delete("1.0",END)
        txt_fact.delete("1.0",END)
        

    # Execute Tkinter
    root.mainloop()

def loadRules():

    # Danh sách các luật 
    rules = {}

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
    return rules

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


if __name__ == "__main__":

    startProgram()
