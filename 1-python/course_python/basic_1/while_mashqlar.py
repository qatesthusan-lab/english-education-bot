# # i = 1
# # while i <= 10:
# #     print(i)

# #     i = i + 1

# # i = 10
# # while i != 0 :
# #     print(i)
# #     i = i -1

# from time import sleep


# hidden_number = 17
# find = False
# number_try = 0
# print("raqam topish oyini")
# sleep(2)
# print("oynaymizmi ? ")
# sleep(2)
# ask = input("ha yoki yoq??? : ")
# if ask == "ha":
#     print("unda boshladik")
# else:
#     print("ok unda xayr ")
# for i in range(3,0,-1):
#     sleep(2)
#     print(i)
#     sleep(0.2)
# print("men 1 dan 20 ga qadar son oyladim uni toping ")
# while not find:
#     number_try = number_try + 1
#     guess = int(input("raqamni kiriting :"))

#     if guess == hidden_number:
#         print(f"togri topdingiz urunishlar soni :{number_try}")
#         sleep(2)
#         find = True
#     elif guess < hidden_number:
#         print("bundan kattaroq raqam kiriting ")
#     else:
#         print("bundan kichikroq raqam kiriting ")


# atm xizmatlari
# from tkinter import Button


# hisob_puli = 10_000_000

# print("ATM - pul yechish xizmati")
# print(f"sizning xisobingizda {hisob_puli} som mavjud ")

# while hisob_puli > 0 :
#     print(f"\n💳joriy balans {hisob_puli} som")
#     yechish = input(f"qancha pul yechmoqchisiz ? (0 - chiqish):")
#     if yechish == "0":
#         print("Xayr ATM dan foydalanganingiz uchun raxmat")
#         break
#     yechish = int(yechish)

#     if yechish <= hisob_puli:
#         hisob_puli = hisob_puli - yechish
#         print(f"xisobingizdan {yechish} som yechildi")


#         if hisob_puli == 0 :
#             print("xisobingiz bosh, pul yechib bolmaydi")
#     else:
#             print("xisobingizda yetarli mablag mavjud emas ")

# print("ATM dan foydalaning va biz bilan rivojlaning")

# from time import sleep
# print("NASA raketasini uchirish ")
# sleep(2)
# print("DIQQAT")
# sleep(2)
# print("Raketa uchirish tayorgarligini boshlaymiz ")
# sleep(2)

# sanash = 10
# print(f"{sanash} dan boshlab sananshni boshlaymiz ")
# while sanash>0:
#     print(f"{sanash} ...")
#     sleep(1)
#     sanash = sanash - 1
#     sleep(1.2)

# print(f"UCHIRISH ")
# sleep(1)
# print("raketa cosmosga uchdi")
# sleep(1)
# print("missiya muvofaqqiyatli amalga oshirildi ")


# print("oddiy kalkulyator")
# print("amalllar +,-,/,*")
# print("chiqish uchun 'exit' ni kiriting  ")

# while True:
#     amal = input("qaysi amalni kiritmoqchisiz(exit - chiqish ) ")
#     if amal == "exit":
#         print("dastur toxtatildi")
#         break
#     if amal == "+" or amal== "-" or amal=="*" or amal =="/":
#         a = float(input("birinchi raqam "))
#         b = float(input("ikkinchi raqam "))
#         if amal == "+":
#             natija = a + b
#             print(f"+ {a} + {b} = {natija}")
#         elif amal == "-":
#             natija = a - b
#             print(f" -  {a} - {b} = {natija}")
#             print("uylanish vaqti kelmadimikin Sarvarjon ???")
#         elif amal == "*":
#             natija = a * b
#             print(f" * {a} * {b} = {natija}")
#         elif amal == "/":
#             if b!=0:
#                natija = a / b
#                print(f" / {a} / {b} = {natija}")
#         else:
#          print("notogri amal kiritdingiz 0 ga bolish yoq ")
#     else:
#         print("notogri amal faqat +,-,*,/ ishlatish mumkin ")


# checking username and parol

import time


user = input("login: ")
parol = input("parol: ")

tries = 0
result = False
while not result:
    x_user = input("iltimos loginni kiriting :")
    x_parol = input("iltimos parolni kiriting :")
    if x_user == user and x_parol == parol:
        print("togri !!! kirishingiz mumkin")
        result = True
    else:
        tries = tries + 1
        print(f"notogri login yoki parol sizda {3 - tries} urunish qoldi ")
        while tries >= 3:
            time.sleep(0.5)
            print("urunishlar soni 3 tadan kop keyinroq urunib koring ")
            time.sleep(0.5)
            for i in range(10, 0, -1):
                time.sleep(1)
                print(f"{i} soniya qoldi")
                tries = 0
        print("sizda yana 3 ta imokinyat bor")
