# # def qoshish():
# #     print(3 + 4)


# # print(qoshish())


# # def qowiw(a, b):
# #     print(a + b)


# # print(qowiw(5, 7))
# # def plus(a, b):
# #     return a + b
# # natija = plus(10, 15)
# # print(natija)
# # salom = input("Ismingizni kiriting: ")

# # def salom_berish(ism):
# #     print(f"salom {ism} men yordamchi dasturman")
# #     return f"qanday yordam bera olaman?"


# # natija = salom_berish(salom)
# # print(natija)


# # def square(num1, num2, calculation_type):
# #     if calculation_type == "+":
# #         return num1 + num2
# #     if calculation_type == "-":
# #         return num1 - num2
# #     if calculation_type == "*":
# #         return num1 * num2
# #     if calculation_type == "/":
# #         if num2 != 0:
# #             return num1 / num2
# #         else:
# #             return "Nolga bo'lib bo'lmaydi!"
# #     return "Noto'g'ri amal!"


# # natija = square(47, 52, "*")
# # print(natija)
# # def


# def salom(ism):
#     return f"salom {ism}"


# natija = salom("husan")
# print(natija)

# l = [1, 2, 3, 4, 5, 6, 12]


# def square(lst):
#     new_list = []
#     for item in lst:
#         new_list.append(item**2)

#     return new_list


# print(square(l))


# sonlar = [23, 45, 67, 43, 21, 12, 34, 56, 78, 76]


# def xisobla(cal):
#     yangi_list = []

#     for item in cal:
#         yangi_list.append(item**2)
#     return yangi_list


# print(xisobla(sonlar))


nonushta = int(input("nonushtadagi kcal ?:"))
tushlik = int(input("tushlikdagi kcal ?:"))
kechki = int(input("kechki kcal? :"))


def ovqat_kaloriya(nonushta, tushlik, kechki):
    # kcal = nonushta = int(input("nonushta ? :"))
    # kcal = tushlik = int(input("tushlik ? :"))
    # kcal = kechki = int(input("kechki  ? :"))
    kcal = nonushta + tushlik + kechki
    if kcal >= 2001:
        print("========== KUNLIK OVQAT HISOBOTI ==========")
        print(f"🍳 Nonushta:{nonushta} kaloriya")
        print(f"🍽️ Tushlik:{tushlik} kaloriya")
        print(f"🍲 Kechki ovqat:{kechki} kaloriya")
        print("=======================================")
        print(f"📊 JAMI:{kcal} kaloriya")
        print(f"🎯 Me'yor: 2,000 kaloriya ({(kcal * 100) / 2000} %)")
        print(f"💡 Tavsiya: biroz kamroq ovqatlanishni tavsiya qilamiz !")
        return kcal
    if kcal == 2000:
        print("========== KUNLIK OVQAT HISOBOTI ==========")
        print(f"🍳 Nonushta:{nonushta} kaloriya")
        print(f"🍽️ Tushlik:{tushlik} kaloriya")
        print(f"🍲 Kechki ovqat:{kechki} kaloriya")
        print("=======================================")
        print(f"📊 JAMI:{kcal} kaloriya")
        print(f"🎯 Me'yor: 2,000 kaloriya ({(kcal * 100) / 2000} %)")
        print(f"💡 Tavsiya: juda zor shunday davom eting !")
        return kcal
    if kcal < 2000:
        print("========== KUNLIK OVQAT HISOBOTI ==========")
        print(f"🍳 Nonushta:{nonushta} kaloriya")
        print(f"🍽️ Tushlik:{tushlik} kaloriya")
        print(f"🍲 Kechki ovqat:{kechki} kaloriya")
        print("=======================================")
        print(f"📊 JAMI:{kcal} kaloriya")
        print(f"🎯 Me'yor: 2,000 kaloriya ({(kcal * 100) / 2000} %)")
        print(f"💡 Tavsiya: {2000-kcal} kaloriya kam - ko'proq ovqatlaning!")
        return kcal


ovqat_kaloriya(nonushta, tushlik, kechki)
