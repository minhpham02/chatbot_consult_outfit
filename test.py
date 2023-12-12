value = input()
valueGetRidOfSpace = ' '.join(value.split(' '))
lower_input = valueGetRidOfSpace.lower()

if lower_input == "thời tiết nóng" or lower_input == "thời tiết lạnh":
    print(lower_input)
else:
    print ("no")