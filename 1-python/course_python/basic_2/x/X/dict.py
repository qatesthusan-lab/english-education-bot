# talaba = {
#     "ism": "ali",
#     "sharif": "valiyev",
#     "jinsi": "erkak",
#     "oilaviy_xolat": "uylangan",
# }
# talaba["ism"] = "sarvar".title()
# talaba["sharif"] = "karimov".title()
# talaba["oilaviy_xolat"] = "uylanmagan"
# # talaba = "kurs"
# talaba["kurs"] = "4 kurs"
# print(talaba)
# talaba.update({"kurs": "3 kurs"})
# talaba["kurs"] = "3 kurs"
# talaba.update({"kasbi": "dasturchi"})
# print(talaba)


from time import sleep
from turtle import title


maktab = {
    "10-A": {
        "o_quvchilar": ["Ali", "Vali", "Salim", "Malika"],
        "sinf_rahbari": "Farid Karimov",
        "xonasi": 101,
    },
    "10-B": {
        "o_quvchilar": ["Sevara", "Bobur", "Diyora", "Jasur"],
        "sinf_rahbari": "Malika Tohirova",
        "xonasi": 102,
    },
}

maktab.setdefault(
    "10-V",
    {
        "o_quvchilar": ["Husan", "Fotima", "Sarvar", "Jasur"],
        "sinf_rahbari": "Sardor Karimov",
        "xonasi": 103,
    },
)

print(
    f'10-A da {len(maktab["10-A"]["o_quvchilar"])} ta oquvchi bor \n10-b da {len(maktab["10-B"]["o_quvchilar"])} ta oquvchi bor '
)
print(
    f'ular :\n 10-A : {maktab['10-A']["o_quvchilar"]}\n 10-B :{maktab["10-B"]["o_quvchilar"]}\n10-V:{maktab["10-V"]["o_quvchilar"]}'
)
while True:
    print("O'quvchilarni sinfini aniqlovchi dastur")
    sleep(1)
    oquvchi = input("O'quvchiu ismini kiriting : ")
    oquvchi = oquvchi.title()
    if oquvchi.title() in maktab["10-A"]["o_quvchilar"]:
        print(f"{oquvchi} 10-A da oqiydi")
    elif oquvchi.title() in maktab["10-B"]["o_quvchilar"]:
        print(f"{oquvchi} 10-B sinfida oqiydi")
    elif oquvchi.title() in maktab["10-V"]["o_quvchilar"]:
        print(f"{oquvchi} 10-V sinf oqiydi ")
    else:
        print(f"{oquvchi} bu maktabda oqimaydi")
        sleep(1)
        break
