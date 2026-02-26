# # l = range(1, 16)

# # natija = list(map(lambda x: x**2,l))
# # print(natija)


# # j = range(1, 21)

# # natija = list(filter(lambda i: i % 2 == 0, j))
# # print(natija)


# from functools import reduce
# from itertools import count


# mashqlar = [
#     {"foydalanuvchi": "Ali", "mashq": "yugurish", "daqiqa": 30, "kalori": 300},
#     {"foydalanuvchi": "Vali", "mashq": "suzish", "daqiqa": 45, "kalori": 400},
#     {"foydalanuvchi": "Ali", "mashq": "velosiped", "daqiqa": 60, "kalori": 500},
#     {"foydalanuvchi": "Salim", "mashq": "yugurish", "daqiqa": 25, "kalori": 250},
# ]


# mashq = filter(lambda m: m["foydalanuvchi"] == "Ali", mashqlar)
# kalori = map(lambda k: k["kalori"], mashq)
# natija = reduce(lambda x, y: x + y, kalori)

# print(natija)

# mashq30 = list(filter(lambda m: m["daqiqa"] > 30, mashqlar))
# print(f"{len(mashq30)} ta Ular:\n{mashq30} ")


from functools import reduce

sonlar = [1, 2, 3, 4, 5, 6, 7, 8, 9]

juftlar = list(filter(lambda x: x % 2 == 0, sonlar))
kvadrati = list(map(lambda k: k**2, juftlar))
yigindi = reduce(lambda s, n: s + n, juftlar)
natija = juftlar, kvadrati, yigindi
print(natija)


ishchilar = [
    {"ism": "Ali", "maosh": 1000},
    {"ism": "Vali", "maosh": 1500},
    {"ism": "Salim", "maosh": 900},
    {"ism": "Nodir", "maosh": 2000},
]

salary_f = list(filter(lambda m: m["maosh"] > 1000, ishchilar))

only_salalry = list(map(lambda o: o["maosh"], salary_f))

all_salary = reduce(lambda x, y: x + y, only_salalry)

result = salary_f, only_salalry, all_salary

print(result)


buyurtmalar = [
    {"mijoz": "Ali", "narx": 120, "soni": 2},
    {"mijoz": "Vali", "narx": 200, "soni": 1},
    {"mijoz": "Ali", "narx": 80, "soni": 3},
    {"mijoz": "Salim", "narx": 150, "soni": 1},
]

# {"mijoz":"Ali","narx":120,"soni":2}
# {"mijoz":"Ali","narx":80,"soni":3},

ali_buyurtma = list(filter(lambda a: a["mijoz"] == "Ali", buyurtmalar))
qiymat = list(map(lambda n: n["narx"] * n["soni"], ali_buyurtma))
result3 = reduce(lambda x, y: x + y, qiymat)
natija2 = ali_buyurtma, qiymat, result3

print(natija2)
