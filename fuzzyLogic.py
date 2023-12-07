
import mysql.connector

from class_chatbot import *

db = ConvertData()
db.convertdacdiem()
validate = Validate()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nkok!minh36",
    database="testcht"
)

user = User(None,None,None,None,None)

def question():
    print(f'-->Chatbot : sau đây là một vài câu hỏi chúng tôi dành cho bạn trước khi đưa ra tư vấn')
    print(f'-->Chatbot : vui lòng trả lời câu hỏi theo gợi ý để chúng tôi có thể đưa ra tư vấn chính xác nhất dành cho bạn')
    
    
    print("-->Chatbot : bạn muốn lựa chọn trang phục đi đâu? ")
    print("Gợi ý : Đi làm công sở, Đi làm ngoài trời; Đi lễ tết; Đi sự kiện trang trọng; Đi sự kiện vui chơi, giải trí, thể thao; Đi sự kiện văn hóa, nghệ thuật")
    user.purpose = validate.validate_name(input())
    print(f'-->Người dùng: {user.purpose}')

    
    print("-->Chatbot : tuổi của bạn hiện tại là bao nhiêu? ")
    user.age = (input())
    print(f'-->Người dùng: {user.age}')

    
    print("-->Chatbot : giới tính của bạn là gì? ")
    user.gender = validate.validate_name(input())
    print(f'-->Người dùng: {user.gender}')

    
    print("-->Chatbot : bạn muốn tìm trang phục mặc trong thời tiết nào? ")
    user.weather_preference = validate.validate_name(input())
    print(f'-->Người dùng: {user.weather_preference}')
    
    
    print("-->Chatbot : phong cách ăn mặc của bạn như thế nào? ")
    user.style = validate.validate_name(input())
    print(f'-->Người dùng: {user.style}')

    return user

def handle_question(list_symptom_of_person, user):

    #lấy mục đích của người dùng 

    list_purpose = [db.resultdacdiem[0], db.resultdacdiem[1], 
                    db.resultdacdiem[2], db.resultdacdiem[3], 
                    db.resultdacdiem[4], db.resultdacdiem[5]]
    all_dd = []
    for i in list_purpose:
        all_dd.append(i["tendacdiem"])
    count = 0    
    for j in all_dd:
        if(j == user.purpose):
            list_symptom_of_person.append(list_purpose[count])
        count += 1

    #lấy tuổi của người dùng 

    list_age = [db.resultdacdiem[6], db.resultdacdiem[7],
                db.resultdacdiem[8], db.resultdacdiem[9]]
    all_dd = []
    for i in list_age:
        all_dd.append(i["tendacdiem"])  
    count = 0      
    for j in all_dd:
        if(j == user.age):
            list_symptom_of_person.append(list_age[count])
        count += 1

    #lấy thời tiết khi mặc trang phục của người dùng

    list_weather = [db.resultdacdiem[10], db.resultdacdiem[11]]
    all_dd = []
    for i in list_weather:
        all_dd.append(i["tendacdiem"])  
    count = 0    
    for j in all_dd:
        if(j == user.weather_preference):
            list_symptom_of_person.append(list_weather[count])
        count += 1

    #lấy giới tính của người dùng

    list_gender = [db.resultdacdiem[12], db.resultdacdiem[13]]
    all_dd = []
    for i in list_gender:
        all_dd.append(i["tendacdiem"])  
    count = 0
    for j in all_dd:
        if(j == user.gender):
            list_symptom_of_person.append(list_gender[count])
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
            list_symptom_of_person.append(list_style[count])
        count += 1

    return list_symptom_of_person    



user = question()
list_symptom_of_person = []
handle_question(list_symptom_of_person,user)
print(list_symptom_of_person)