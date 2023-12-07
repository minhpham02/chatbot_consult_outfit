import re

import mysql.connector
import json
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nkok!minh36",
    database="testcht"
)


class ConvertData:
    """
    Truy vấn và xử lý dữ liệu
    """
    def __init__(self):
        self.resulttrangphuc = []
        self.resultdacdiem = []
        self.resultkhuyetdiem = []
        self.resultmausac = []
        self.resultfc = []
        self.resultbc = []
        self.resulttt = []

    def converttrangphuc(self):
        """
        Lấy dữ liệu bảng trang phục
        """
        dbtrangphuc = mydb.cursor()
        dbtrangphuc.execute("SELECT * FROM testcht.trangphuc;")
        trangphuc = dbtrangphuc.fetchall()
        dirtrangphuc = {}
        for i in trangphuc:
            dirtrangphuc['idtrangphuc'] = i[0]
            dirtrangphuc['tentrangphuc'] = i[1]
            dirtrangphuc["phukien"] = i[2]
            self.resulttrangphuc.append(dirtrangphuc)
            dirtrangphuc = {}

    def convertdacdiem(self):
        """
        Lấy dữ liệu từ bảng đặc điểm
        """
        dbdacdiem = mydb.cursor()
        dbdacdiem.execute("SELECT * FROM testcht.dacdiem;")
        dacdiem = dbdacdiem.fetchall()
        dirdacdiem = {}
        for i in dacdiem:
            dirdacdiem['iddacdiem'] = i[0]
            dirdacdiem['tendacdiem'] = i[1]
            self.resultdacdiem.append(dirdacdiem)
            dirdacdiem = {}
    
    def convertkhuyetdiem(self):
        dbkhuyetdiem = mydb.cursor()
        dbkhuyetdiem.execute("SELECT * FROM testcht.khuyetdiem;")
        khuyetdiem = dbkhuyetdiem.fetchall()
        dirkhuyetdiem = {}

        for i in khuyetdiem:
            dirkhuyetdiem['idTrangPhuc'] = i[1]
            dirkhuyetdiem['KDNgoaiHinh'] = i[2]
            dirkhuyetdiem['LoiKhuyen'] = i[3]
            self.resultkhuyetdiem.append(dirkhuyetdiem)
            dirkhuyetdiem = {}
    
    def convertmausac(self):    
        dbmausac = mydb.cursor()
        dbmausac.execute("SELECT * FROM testcht.mauda;")
        mausac = dbmausac.fetchall()
        dirmausac = {}
        
        for i in mausac:
            dirmausac['idTrangPhuc'] = i[1]
            dirmausac['MauDa'] = i[2]
            dirmausac['LoiKhuyen'] = i[3]
            self.resultmausac.append(dirmausac)
            dirmausac = {}
            
    def getfc(self):
        """
        Nhóm các trang phục cùng 1 đặc điểm
        """
        dbfc = mydb.cursor()
        dbfc.execute(
            "select idsuydien, luat.idluat, iddacdiem, idtrangphuc, trangthai from suydien, luat where suydien.idluat=luat.idluat and trangthai='0'")
        fc = dbfc.fetchall()
        s = []
        d = []
        for i in range(len(fc)):
            s.append(fc[i][2])
            d.append(fc[i][3])

        tt = s[0]
        trangphuc = []
        dicfc = {}
        for i in range(len(s)):
            if s[i] == tt:
                trangphuc.append(d[i])
            else:
                dicfc['dacdiem'] = tt
                dicfc['trangphuc'] = trangphuc
                tt = s[i]
                self.resultfc.append(dicfc)
                trangphuc = []
                trangphuc.append(d[i])
                dicfc = {}

    def getbc(self):
        """
        Nhóm các đặc điểm cùng 1 trang phục
        """
        dbbc = mydb.cursor()
        dbbc.execute("select idsuydien, luat.idluat, iddacdiem, idtrangphuc, trangthai from suydien, luat where suydien.idluat=luat.idluat and trangthai='1' order by idtrangphuc")
        fc = dbbc.fetchall()
        rule = []
        s = []
        d = []
        for i in range(len(fc)):
            rule.append(fc[i][1])
            s.append(fc[i][2])
            d.append(fc[i][3])
        # print(rule)
        vtrule = rule[0]
        tt = []
        trangphuc = None
        # result=[]
        dicbc = {}
        for i in range(len(rule)):
            if rule[i] == vtrule:
                tt.append(s[i])
                trangphuc = d[i]
            else:
                dicbc['rule'] = vtrule
                dicbc['trangphuc'] = trangphuc
                dicbc['dacdiem'] = tt
                vtrule = rule[i]
                self.resultbc.append(dicbc)
                trangphuc = d[i]
                tt = []
                tt.append(s[i])
                dicbc = {}

    def groupbc(self):
        """
        
        """
        p = []
        vt = self.resultbc[0]['trangphuc']
        temp = []
        for i in self.resultbc:
            t = []
            t.append(i['trangphuc'])
            for j in i['dacdiem']:
                t.append(j)
            temp.append(t)
        return temp

    def groupfc(self):
        res = []
        for i in self.resultfc:
            for j in range(len(i['trangphuc'])):
                res.append([i['trangphuc'][j], i['dacdiem']])
        return res

    def getdacdiem(self):
        """
        Nhóm tất cả đặc điểm trong 1 trang phục
        """
        dbdacdiem=mydb.cursor()
        dbdacdiem.execute("SELECT * FROM testcht.suydien order by idtrangphuc")
        dttt=dbdacdiem.fetchall()
        trangphuc=[]
        tt=[]
        rule=[]
        for i in dttt:
            trangphuc.append(i[2])
            tt.append(i[3])
            rule.append(i[1])
        vttrangphuc=trangphuc[0]
        lstt=[]
        dirtt={}
        
        for i in range(len(trangphuc)):
            if trangphuc[i]==vttrangphuc:
                lstt.append(tt[i])
            else:
                dirtt[vttrangphuc]=sorted(set(lstt))
                lstt=[]
                vttrangphuc=trangphuc[i]
                lstt.append(tt[i])
        dirtt[vttrangphuc]=sorted(set(lstt))
        self.resulttt=dirtt
        return self.resulttt
    
    def get_trangphuc_by_id(self, id_trangphuc):
        """
        Tìm trang phuc dựa trên id
        """
        for i in self.resulttrangphuc:
            if i["idtrangphuc"] == id_trangphuc:
                return i
        return 0

    def get_dacdiem_by_id(self, id_dacdiem):
        for i in self.resultdacdiem    :
            if i["iddacdiem"] == id_dacdiem:
                return i
        return 0

    

class Validate:
    def __init__(self) -> None:
        pass

    def validate_input_number_form(self,value):
        while (1):
            valueGetRidOfSpace = ''.join(value.split(' '))
            check = valueGetRidOfSpace.isnumeric()
            if (check):
                return valueGetRidOfSpace
            else:
                print("-->Chatbot: Vui lòng nhập 1 số dương")
                value = input()

    def validate_phonenumber(self,value):
        while (1):
            valueGetRidOfSpace = ''.join(value.split(' '))
            check = valueGetRidOfSpace.isnumeric()
            if (check):
                return valueGetRidOfSpace
            else:
                print("-->Chatbot: Vui lòng nhập 1 số điện thoại đúng định dạng")
                value = input()


    def validate_email(self, email):
        while (1):
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            if (re.fullmatch(regex, email)):
                # print("Chatbot:Tôi đã nhận được thông tin Email của bạn")
                return email

            else:
                print("-->Chatbot: Vui lòng nhập lại email")
                email = input()

    def validate_name(self, value):
        while (1):
            valueGetRidOfSpace = ''.join(value.split(' '))

            check = valueGetRidOfSpace.isalpha()
            if (check):
                # print("Tôi đã nhận được thông tin Tên của bạn")
                return value
            else:
                print("-->Chatbot: Vui lòng nhập lại tên ! ")
                value = input()

    def validate_binary_answer(self, value):
        acceptance_answer_lst = ['1', 'y', 'yes', 'co', 'có']
        decline_answer_lst = ['0', 'n', 'no', 'khong', 'không']
        value = value+''
        while (1):
            if (value) in acceptance_answer_lst:
                return True
            elif value in decline_answer_lst:
                return False
            else:
                print(
                    "-->Chatbot: Câu trả lời không hợp lệ. Vui lòng nhập lại câu trả lời")
                value = input()


class Person:
    def __init__(self, name, phoneNumber, email):
        self.name = name
        self.phoneNumber = phoneNumber
        self.email = email

    def __str__(self):
        return f"{self.name} - {self.phoneNumber} - {self.email}"

class User:
    def __init__(self, purpose, age, weather_preference, gender, style):
        self.purpose = purpose
        self.age = age
        self.weather_preference = weather_preference
        self.gender = gender
        self.style = style
    def __str__(self):
        return f"{self.purpose} - {self.age} - {self.weather_preference} - {self.gender} - {self.style}"

class Symptom:
    def __init__(self, code, detail):
        self.code = code
        self.detail = detail


def printTree(node, level=0):
    if node != None:
        printTree(node.left, level + 1)
        print(' ' * 10 * level + '-> ' + str(node.value))
        printTree(node.right, level + 1)
        

def searchindexrule(rule,goal):
    
    index=[]
    for r in range(len(rule)):
        if rule[r][0]==goal:
            index.append(r)
    return index
def get_s_in_d(answer,goal,rule,d,flag):

    result=[]
    index=[]
    if flag==1:
        for i in range(len(rule)):
            if (rule[i][0]==goal) and (answer in rule[i]) and (i in d):
                for j in rule[i]:
                    if j[0]=='T':
                        result.append(j)
                        # result=set()
    else:
        for i in range(len(rule)):
            if (rule[i][0]==goal) and (answer in rule[i]): index.append(i)
            if (rule[i][0]==goal) and (answer not in rule[i]) and (i in d):
                for j in rule[i]:
                    if j[0]=='T':
                        result.append(j)        

    return sorted(set(result)),index


