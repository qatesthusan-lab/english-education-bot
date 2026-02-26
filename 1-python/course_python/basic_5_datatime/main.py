from calendar import Month, day_name
from datetime import datetime, date, time

today = date.today()
print(today)
today_time = datetime.now()
print(today_time.hour, today_time.minute, today_time.second)
day_name = day_name[today.weekday()]
# print(f"Bugun {day_name} kuni")
day_name = (
    day_name.replace("Monday", "Dushanba")
    .replace("Tuesday", "Seshanba")
    .replace("Wednesday", "Chorshanba")
    .replace("Thursday", "Payshanba")
    .replace("Friday", "Juma")
    .replace("Saturday", "Shanba")
    .replace("Sunday", "Yakshanba")
)
print(f"Bugun {day_name} kuni")
# from datetime import time, date, datetime

# # from datetime import date

# # bugun = date.today()

# # # Turli formatlar
# # print(bugun.strftime("%d/%m/%Y"))  # 03/08/2024
# # print(bugun.strftime("%d-%m-%Y"))  # 03-08-2024
# # print(bugun.strftime("%B %d, %Y"))  # August 03, 2024
# # print(bugun.strftime("%A, %d %B"))  # Saturday, 03 August
# # print(bugun.strftime("%y-%m-%d"))

# # hafta_kuni = bugun.weekday()
# # print(day_name[hafta_kuni])


# bugun = datetime.now()

# ask = input("Bugun sana va vaqtni ko'rsatish uchun 'ha' deb yozing: ")
# if ask.lower() == "ha":
#     print("Bugun sana va vaqt:")
#     print(bugun.strftime("%Y-%m-%d %H:%M:%S"))


# def get_hafta_kuni():
#     return bugun.weekday()


# hafta_kuni = get_hafta_kuni()
# print(day_name[hafta_kuni])
# if hafta_kuni == 0:
#     print("Bugun dushanba kuni")
#     print(bugun.strftime("%Y-%m-%d %H:%M:%S"))
# elif hafta_kuni == 1:
#     print("Bugun seshanba kuni")
#     print(bugun.strftime("%Y-%m-%d %H:%M:%S"))
# elif hafta_kuni == 2:
#     print("Bugun chorshanba kuni")
#     print(bugun.strftime("%Y-%m-%d %H:%M:%S"))
# elif hafta_kuni == 3:
#     print("Bugun payshanba kuni")
#     print(bugun.strftime("%Y-%m-%d %H:%M:%S"))
# elif hafta_kuni == 4:
#     print("Bugun juma kuni")
#     print(bugun.strftime("%Y-%m-%d %H:%M:%S"))
# elif hafta_kuni == 5:
#     print("Bugun shanba kuni")
#     print(bugun.strftime("%Y-%m-%d %H:%M:%S"))
# elif hafta_kuni == 6:
#     print("Bugun yakshanba kuni")
#     print(bugun.strftime("%Y-%m-%d %H:%M:%S"))
# else:
#     print("Noma'lum sana")
