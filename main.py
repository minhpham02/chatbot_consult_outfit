import os
import sys

from backward_chaining import BackwardChaining
from forward_chaining import ForwardChaining
from class_chatbot import *
from class_chatbot import ConvertData
from fuzzyLogic import *


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
user = User(None,None,None,None,None)



#################################################
# 1. Người dùng lựa chọn mục đích sử dụng trang phục
def welcome_question():
    print("-->Chatbot: Xin chào, tôi là chatbot tư vấn trang phục!")
# 2. Các câu hỏi để lấy thêm thông tin tư vấn
def question():

    
    AllSymLst = [db.resultdacdiem[0], db.resultdacdiem[1],
                 db.resultdacdiem[2], db.resultdacdiem[3],
                 db.resultdacdiem[4],db.resultdacdiem[5],
                 db.resultdacdiem[6]]

    NewAllSymLst = []

    for i in AllSymLst:
        NewAllSymLst.append(i["iddacdiem"])
            
    print(f'-->Chatbot: Mời bạn chọn mục đích để tư vấn trang phục: ')
    print(f'-->Chatbot: (Nhập số thứ tự để chọn)')

    while(1):
        count = 1
        for i in AllSymLst:
            print(f'{count}. {i["tendacdiem"]} \n')
            count += 1
        answer = validate.validate_input_number_form(input())
        print(f'-->Người dùng: Câu trả lời của tôi là {answer}')

        if (int(answer) < 0 or int(answer) > 8):
            print('-->Chatbot: Vui lòng nhập 1 số từ 1 tới 7')
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
        if int(age) > 100:
            print("-->Chatbot : Số tuổi không hợp lệ. Vui lòng nhập lại ")
            continue
        else:
            user.age = int(age)
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
# 3. Xử lý các câu hỏi để lấy thông tin từ db
def handle_question(list_characteristic_of_person, user):

    #lấy mục đích của người dùng 
    list_characteristic_of_person.append(user.purpose)

    #lấy tuổi của người dùng 

    list_age = [db.resultdacdiem[7], db.resultdacdiem[8],
                db.resultdacdiem[9], db.resultdacdiem[10]]
    if user.age <= 18 and user.age >= 15:
        list_characteristic_of_person.append(list_age[0])
    elif user.age <= 30 and user.age >= 18:
        list_characteristic_of_person.append(list_age[1])
    elif user.age <= 50 and user.age >= 30:
        list_characteristic_of_person.append(list_age[2])
    else:
        list_characteristic_of_person.append(list_age[3])

    #lấy thời tiết khi mặc trang phục của người dùng

    list_weather = [db.resultdacdiem[11], db.resultdacdiem[12]]
    all_dd = []
    for i in list_weather:
        all_dd.append(i["tendacdiem"])  
    count = 0    
    for j in all_dd:
        if(j == user.weather_preference):
            list_characteristic_of_person.append(list_weather[count])
        count += 1

    #lấy giới tính của người dùng

    list_gender = [db.resultdacdiem[13], db.resultdacdiem[14]]
    all_dd = []
    for i in list_gender:
        all_dd.append(i["tendacdiem"])  
    count = 0
    for j in all_dd:
        if(j == user.gender):
            list_characteristic_of_person.append(list_gender[count])
        count += 1

    #lấy phong cách của người dùng

    list_style = [db.resultdacdiem[15], db.resultdacdiem[16], 
                  db.resultdacdiem[17], db.resultdacdiem[18], 
                  db.resultdacdiem[19]]
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
# 4. phần suy diễn tiến
def forward_chaining(rule, fact, goal, file_name,user):
    fc = ForwardChaining(rule, fact, None, file_name)

    list_predicted_outfit = [i for i in fc.facts if i[0] == "T"]
    return list_predicted_outfit

########################################################################
# 5. phần suy diễn lùi
def backward_chaining(luat_lui,list_characteristic_of_person,list_predicted_outfit,file_name ):
    predictD=list_predicted_outfit
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
            print("-->Chatbot : Trang phục chúng tôi tư vấn cho bạn là {}- {}".format(goal,D['tentrangphuc']))
            print(f"-->Chatbot : Phụ kiện")
            D['phukien']=D['phukien'].replace("/n","\n")
            print(f"-->Chatbot : {D['phukien']}")
            return goal,fact_real     
    if trangphuc==0:
        print(f"-->Chatbot : Xin lỗi chúng tôi không tìm được trang phục phù hợp trong bộ dữ liệu với những đặc điểm của bạn.Cám ơn bạn đã sử dụng Chatbot")
        sys.exit()

# 6. Câu hỏi để tư vấn về màu sắc trang phục
def question_color(goal):

    print("-->Chatbot : Tiếp theo chúng tôi sẽ tư vấn về màu sắc trang phục cho bạn?")
    print("-->Chatbot : Màu da của bạn thuộc loại nào sau đây?")
    print("-->Chatbot : Da trắng - Da ngăm đen - Da vàng") 
    color = validate.validate_color(input())
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
# 7. Câu hỏi để đưa ra lời khuyên về cách khắc phục khuyết điểm dựa trên trang phục
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
            #print("-->Chatbot : Cám ơn bạn đã sử dụng Chatbot")
            break
        elif(int(answer) > count):
            print("-->Chatbot : Vui lòng nhập đúng số")
            continue
        else:
            print(all_lk[int(answer)-1])
            break    
# 8. Câu hỏi để tư vấn size quần áo
def question_size():
    print(f'-->Chatbot: Để có một bộ trang phục vừa vặn với cơ thể của bạn chúng tôi sẽ tư vấn về size quần áo cho bạn')
    print(f' Vui lòng nhập chiều cao và cân nặng để được tư vấn')
    # Nhập chiều cao và cân nặng từ người dùng
    chieu_cao = float(input("Nhập chiều cao của bạn (cm): "))
    can_nang = float(input("Nhập cân nặng của bạn (kg): "))
    print(f'-->Chatbot: Size áo phù hợp với bạn là {ketQua(chieu_cao, can_nang)}')
    print(f'-->Chatbot: Bạn có thể mặc thêm hoặc giảm 1 size tùy thuộc vào cơ thể để có một bộ trang phục ưng ý nhất')
    print(f'-->Chatbot: Trên đây là toàn bộ tư vấn của chúng tôi về trang phục. Cảm ơn bạn đã sử dụng chatbot')


welcome_question()  # list các đối tượng triệu chứng
user = question()
list_characteristic_of_person = []
handle_question(list_characteristic_of_person, user)

list_characteristic_of_person_id = [i['iddacdiem'] for i in list_characteristic_of_person]
list_characteristic_of_person_id = list(set(list_characteristic_of_person_id))
list_characteristic_of_person_id.sort()


list_predicted_outfit = forward_chaining(luat_tien, list_characteristic_of_person_id, None, 'ex', user)
print(list_predicted_outfit)

if len(list_predicted_outfit)==0 :
    print("-->Chatbot : Xin lỗi chúng tôi không tìm được trang phục phù hợp.Cám ơn bạn đã sử dụng ChatBot")
    sys.exit()

outfit,list_characteristic_of_person_id= backward_chaining(luat_lui,list_characteristic_of_person_id,list_predicted_outfit,"ex")
    
question_color(outfit)
question_weakness(outfit)
question_size()
