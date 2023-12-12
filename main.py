import os
import sys

from backward_chaining import BackwardChaining
from forward_chaining import ForwardChaining
from class_chatbot import *
from class_chatbot import ConvertData



# biến khởi tạo
validate = Validate()

db = ConvertData()
db.converttrangphuc()  # bang trang phuc
db.convertdacdiem()  # bang dac diem
db.convertkhuyetdiem()
db.convertmausac()
db.getfc()
db.getbc()
luat_lui = db.groupbc()
luat_tien = db.groupfc()




#################################################
# 1. câu hỏi chào hỏi
def welcome_question():
    print("-->Chatbot: Xin chào, tôi là chatbot tư vấn trang phục!")

user = User(None,None,None,None,None)

def question():

    
    AllSymLst = [db.resultdacdiem[0], db.resultdacdiem[1],
                 db.resultdacdiem[2], db.resultdacdiem[3],
                 db.resultdacdiem[4],db.resultdacdiem[5]]

    NewAllSymLst = []

    for i in AllSymLst:
        NewAllSymLst.append(i["iddacdiem"])
            
    print(f'-->Chatbot: Trang phục bạn muốn tư vấn sử dụng cho sự kiện: ')
    print(f'-->Chatbot: (Nhập số thứ tự để chọn)')

    while(1):
        count = 1
        for i in AllSymLst:
            print(f'{count}. {i["tendacdiem"]} \n')
            count += 1
        answer = validate.validate_input_number_form(input())
        print(f'-->Người dùng: Câu trả lời của tôi là {answer}')

        if (int(answer) < 0 or int(answer) > 4):
            print('-->Chatbot: Vui lòng nhập 1 số từ 0 tới 4')
            continue
        else:
            print(AllSymLst[int(answer)-1])
            user.purpose = AllSymLst[int(answer)-1]
            break


    print(f'-->Chatbot: Sau đây là một vài câu hỏi chúng tôi dành cho bạn để có thêm thông tin để có thể đưa ra tư vấn chính xác nhất')
    print("-->Chatbot : Tuổi của bạn hiện tại là bao nhiêu? ")
    
    while(1):
        age = validate.validate_input_number_form(input())
        print(f'-->Người dùng: {age}')
        if age > 100:
            print("-->Chatbot : Số tuổi không hợp lệ. Vui lòng nhập lại ")
            continue
        else:
            user.age = age
            break

    print("-->Chatbot : Giới tính của bạn là gì? ")
    user.gender = validate.validate_gender(input())
    print(f'-->Người dùng: Giới tính {user.gender}')

    
    print("-->Chatbot : Bạn muốn tìm trang phục mặc trong thời tiết nào dưới đây? ")
    print("-->Chatbot : Thời tiết lạnh - Thời tiết nóng ")
    user.weather_preference = validate.validate_weather(input())
    print(f'-->Người dùng: {user.weather_preference}')
    
    
    print("-->Chatbot : Phong cách ăn mặc của bạn giống với phong cách nào dưới đây?")
    print("-->Chatbot : Phong cách đơn giản - Phong cách trang trọng -  Phong cách năng động - Phong cách công sở - Phong cách cá tính")
    user.style = validate.validate_style(input())
    print(f'-->Người dùng: {user.style}')

    return user

def handle_question(list_characteristic_of_person, user):

    #lấy mục đích của người dùng 
    list_characteristic_of_person.append(user.purpose)

    #lấy tuổi của người dùng 

    list_age = [db.resultdacdiem[6], db.resultdacdiem[7],
                db.resultdacdiem[8], db.resultdacdiem[9]]
    if user.age <= 18 and user.age >= 15:
        list_characteristic_of_person.append(list_age[0])
    elif user.age <= 30 and user.age >= 18:
        list_characteristic_of_person.append(list_age[1])
    elif user.age <= 50 and user.age >= 30:
        list_characteristic_of_person.append(list_age[2])
    else:
        list_characteristic_of_person.append(list_age[3])

    #lấy thời tiết khi mặc trang phục của người dùng

    list_weather = [db.resultdacdiem[10], db.resultdacdiem[11]]
    all_dd = []
    for i in list_weather:
        all_dd.append(i["tendacdiem"])  
    count = 0    
    for j in all_dd:
        if(j == user.weather_preference):
            list_characteristic_of_person.append(list_weather[count])
        count += 1

    #lấy giới tính của người dùng

    list_gender = [db.resultdacdiem[12], db.resultdacdiem[13]]
    all_dd = []
    for i in list_gender:
        all_dd.append(i["tendacdiem"])  
    count = 0
    for j in all_dd:
        if(j == user.gender):
            list_characteristic_of_person.append(list_gender[count])
        count += 1

    #lấy phong cách của người dùng

    list_style = [db.resultdacdiem[14], db.resultdacdiem[15], 
                  db.resultdacdiem[16], db.resultdacdiem[17], 
                  db.resultdacdiem[18]]
    all_dd = []
    for i in list_style:
        all_dd.append(i["tendacdiem"])   
    count = 0
    for j in all_dd:
        if(j == user.style):
            list_characteristic_of_person.append(list_style[count])
        count += 1

    return list_characteristic_of_person    


################################################################
# 6 phần suy diễn tiến
def forward_chaining(rule, fact, goal, file_name,user):
    fc = ForwardChaining(rule, fact, None, file_name)

    list_predicted_disease = [i for i in fc.facts if i[0] == "T"]
    return list_predicted_disease

########################################################################
# 7 phần suy diễn lùi
def backward_chaining(luat_lui,list_characteristic_of_person,list_predicted_disease,file_name ):
    predictD=list_predicted_disease
    rule=luat_lui
    all_rule=db.getdacdiem()
    fact_real=list_characteristic_of_person_id
    trangphuc=0
    for g in predictD:
        goal=g
        D=db.get_trangphuc_by_id(goal) #Chứa thông tin id == goal
        all_s_in_D=all_rule[goal]
        all_s_in_D=sorted(set(all_s_in_D)-set(fact_real))
        
        b=BackwardChaining(rule,fact_real,goal,file_name) # kết luận trong trường hợp các luât đã suy ra đk luôn
        
        if b.result1==True:# đoạn đầu
            print("-->Chatbot : Trang phục chúng tôi dự đoán là {}- {}".format(goal,D['tentrangphuc']))
            print(f"-->Chatbot : Phụ kiện")
            D['phukien']=D['phukien'].replace("/n","\n")
            print(f"-->Chatbot : {D['phukien']}")
            return goal,fact_real     
    if trangphuc==0:
        print(f"-->Chatbot : Xin lỗi chúng tôi không tìm được trang phục phù hợp.Cám ơn bạn đã sử dụng ChatBot")
        sys.exit()

def question_color(goal):

    print("-->Chatbot : Tiếp theo chúng tôi sẽ tư vấn về màu sắc trang phục cho bạn?")
    print("-->Chatbot : Màu da của bạn thuộc loại nào sau đây?")
    print("-->Chatbot : Da trắng - Da ngăm đen - Da vàng")
    color = (input())
    print(f'-->Người dùng: {color}')

    list_color = [db.resultmausac[0], db.resultmausac[1], db.resultmausac[2]
                  , db.resultmausac[3], db.resultmausac[4], db.resultmausac[5]
                  , db.resultmausac[6], db.resultmausac[7], db.resultmausac[8]
                  , db.resultmausac[9], db.resultmausac[10], db.resultmausac[11]
                  , db.resultmausac[12], db.resultmausac[13], db.resultmausac[14]
                  , db.resultmausac[15], db.resultmausac[16], db.resultmausac[17]
                  , db.resultmausac[18], db.resultmausac[19], db.resultmausac[20]
                  ]
    all_dd = []
    all = []
    all_1 = []
    list = []
    for i in list_color:
        all_dd.append(i["idTrangPhuc"])
        all_1.append(i["MauDa"])
        all.append(i["LoiKhuyen"])
    for j in range(len(all_dd)):
        if(all_dd[j] == goal and all_1[j] == color):
            list.append(all[j])
    print(list)

def question_weakness(goal):
    print("-->Chatbot : Nếu bạn có những khuyết điểm sau đây, hãy lựa chọn để chúng tôi có thể đưa ra tư vấn về cách khắc phục dựa trên bộ trang phục chúng tôi dự đoán")
    print("-->Chatbot : Bạn có thể bỏ qua nếu không có khuyết điểm")

    list_kd = [db.resultkhuyetdiem[0], db.resultkhuyetdiem[1], db.resultkhuyetdiem[2]
              , db.resultkhuyetdiem[3], db.resultkhuyetdiem[4], db.resultkhuyetdiem[5]
              , db.resultkhuyetdiem[6], db.resultkhuyetdiem[7], db.resultkhuyetdiem[8]
              , db.resultkhuyetdiem[9], db.resultkhuyetdiem[10], db.resultkhuyetdiem[11]
              , db.resultkhuyetdiem[12], db.resultkhuyetdiem[13], db.resultkhuyetdiem[14]
              , db.resultkhuyetdiem[15], db.resultkhuyetdiem[16], db.resultkhuyetdiem[17]
              , db.resultkhuyetdiem[18], db.resultkhuyetdiem[19]]
    all_kd = []
    all_lk = []

    for i in list_kd:
        if i["idTrangPhuc"] == goal:
            all_kd.append(i["KDNgoaiHinh"])
            all_lk.append(i["LoiKhuyen"])
    while(1):
        count = 1
        for i in all_kd:
            print(f'{count}. {i} \n')
            count += 1
        print('0. Bỏ qua \n')
        answer = validate.validate_input_number_form(input())
        print(f'-->Người dùng: Câu trả lời của tôi là {answer}')
        if(answer == '0'):
            print("-->Chatbot : Cám ơn bạn đã sử dụng Chatbot")
            break
        elif(int(answer) > count):
            print("-->Chatbot : Vui lòng nhập đúng số")
            continue
        else:
            print(all_lk[int(answer)-1])
            break    

welcome_question()  # list các đối tượng triệu chứng
user = question()
list_characteristic_of_person = []
handle_question(list_characteristic_of_person, user)

list_characteristic_of_person_id = [i['iddacdiem'] for i in list_characteristic_of_person]
list_characteristic_of_person_id = list(set(list_characteristic_of_person_id))
list_characteristic_of_person_id.sort()


list_predicted_disease = forward_chaining(luat_tien, list_characteristic_of_person_id, None, 'ex', user)
print(list_predicted_disease)

if len(list_predicted_disease)==0 :
    print("-->Chatbot : Xin lỗi chúng tôi không tìm được trang phục phù hợp.Cám ơn bạn đã sử dụng ChatBot")
    sys.exit()

disease,list_characteristic_of_person_id= backward_chaining(luat_lui,list_characteristic_of_person_id,list_predicted_disease,"ex")
    
question_color(disease)
question_weakness(disease)
#question_size()
