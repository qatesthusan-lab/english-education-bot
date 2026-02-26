# # talabalar = ["jamol", "kamol","olim","aziz","husan"]
# # # print(talabalar[0])
# # # print(talabalar[1])
# # # print(talabalar[-1])
# # # print(talabalar[-5])

# # # for i in range(3):
# # #     print(talabalar)

# # # sonlar = list(range(50))

# # # print(sonlar[:10])
# # # print(sonlar[10:20:3])
# # # print(sonlar[20:])
# # # print(sonlar[0::3])
# # # print(sonlar[-1::-1])

# # mevalar = ["olma","anor","uzum"]
# # mevalar.append("banan")
# # mevalar.insert(2,"xurmo")

# # mevalar[0] = "limon"
# # del mevalar[2]
# # mevalar.pop(-1)
# # mevalar.remove("limon")

# # # print(mevalar)
# # print("olma" in mevalar)
# # print("anor" in mevalar)
# # print(mevalar.index("anor"))
# # print(mevalar.count("anor"))
# # print(len(mevalar))



# # mevalar = ["olma","banan","uzum","anor"]
# # mevalar.remove("banan")
# # mevalar.insert(0,"shaftoli")
# # for meva in mevalar:
# #     print(meva)


# # r_list = range(10)
# # for i in range(5,0,0-1):
#     # print("*" * i)
# # sonlar.sort()
# # sonlar.reverse()
# # len(sonlar)
# # son = len(sonlar)
# # print(son)

# for i in range(0,6,1):
#     print(f"*" * i)
# for b in range(6,0,-1):
#     print("*" * b)    


# ismlar = []
# for ism in range(5):
#     ism = input("ism:")
#     ism = ismlar.append(ism)
#     print(ismlar)
    
# ismlar = []
# while True:
#     ism = input("ism?:")
#     if ism == "stop":
#         break
#     ismlar.append(ism)
# # print(ismlar)
# barcha_sonlar = list(range(1,100))
# print(f"barcha sonlar :\n{barcha_sonlar}")

# juft_sonlar = []
# toq_sonlar = []
# for son in barcha_sonlar :
#     if son % 2 == 0: #juft son
#         juft_sonlar.append(son)
#     else:
#         toq_sonlar.append(son)

# print(f"juft_sonlar: \n{juft_sonlar}")
# print(f" toq sonlar :\n{toq_sonlar}")


barcha_sonlar = list(range(1,50))
faqat_3_ga = []
faqat_5_ga = []

for son in barcha_sonlar:
    if son % 3 == 0:
        faqat_3_ga.append(son)
    elif son % 5 == 0:
        faqat_5_ga.append(son)


print(f"barcha_sonlar:\n{barcha_sonlar}")
print(f"faqat 3 ga bolinadigan sonlar :\n{faqat_3_ga}")
print(f"faqat 5 ga bolinadigan sonlar : \n{faqat_5_ga}")
print(f"ham 5 ga, ham 3 ga bolinadigan sonlar :{faqat_3_ga} {faqat_5_ga}")


