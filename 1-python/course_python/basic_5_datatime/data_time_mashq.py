from calendar import day_name
from datetime import date, datetime, time
from re import M, S

bugun = date.today()
print(bugun)

vaqt = datetime.now()
print(vaqt.hour, vaqt.minute, vaqt.second)

bugungi_kun = (
    day_name[bugun.weekday()]
    .replace("Monday", "Dushanba")
    .replace("Tuesday", "Seshanba")
    .replace("Wednesday", "Chorshanba")
    .replace("Thursday", "Payshanba")
    .replace("Friday", "Juma")
    .replace("Saturday", "Shanba")
    .replace("Sunday", "Yakshanba")
)

print(bugungi_kun)


bugun_vaqt = datetime.now()
ask = input("Bugun sana va vaqtni ko'rsatish uchun 'ha' deb yozing: ")
if ask.lower() == "ha":
    print("Bugun sana va vaqt:")
    print(bugun_vaqt.strftime("%Y-%m-%d %H:%M:%S"))
    print(bugungi_kun)


todays_day = date.today()
print("bugungi kun :", todays_day.strftime("%Y %m %d"))

yil_oxiri = date(2026, 12, 31)
print("yil oxiri :", yil_oxiri)

print(f"yil oxirigacha {yil_oxiri - todays_day} kun qoldi ")
