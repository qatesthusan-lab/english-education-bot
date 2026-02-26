from datetime import datetime, timedelta

try:
    sana = input("Oxirgi hayz sanasi (YYYY-MM-DD): ")

    oxirgi_sana = datetime.strptime(sana, "%Y-%m-%d")
    bugun = datetime.now()

    if oxirgi_sana > bugun:  # kelajak
        print("Xato: hali u kun kelmadi sabr.")
    else:
        farq = bugun - oxirgi_sana
        kunlar = farq.days

        hafta = kunlar // 7  # qoldiqsiz bolish
        qolgan_kun = kunlar % 7

        tugruq_sana = oxirgi_sana + timedelta(days=280)

        print("\n Natija:")
        print(f"{hafta} hafta {qolgan_kun} kun")
        print("Taxminiy tug‘ruq sanasi:", tugruq_sana.date())

except ValueError:
    print("Xato: Sanani to‘g‘ri formatda kiriting (YYYY-MM-DD)")
except TypeError:
    print("togri yozing - chalar bilan")
