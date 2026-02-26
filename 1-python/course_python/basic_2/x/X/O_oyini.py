print("🎮 X/O O'yiniga xush kelibsiz!")
print("=" * 40)
print("📋 O'yin qoidalari:")
print("• 3x3 maydonda o'ynaysiz")
print("• X va O belgilari bilan")
print("• 3 ta belgini bir qator, ustun yoki diagonalga joylang")
print("• Birinchi muvaffaq bo'lgan yutadi!")
print("=" * 40)

# O'yin maydonini yaratish
maydon = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

# O'yinchilar ma'lumotlari
oyinchilar = {"X": "1-O'yinchi", "O": "2-O'yinchi"}

# G'alaba kombinatsiyalari
galaba_kombinatsiyalari = [
    # Gorizontal
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    # Vertikal
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    # Diagonal
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)],
]

# Hozirgi o'yinchi
joriy_oyinchi = "X"

# Asosiy o'yin halqasi
while True:
    # Maydonni ko'rsatish
    print("\n📋 Hozirgi maydon:")
    print("   0   1   2")

    for qator_index in range(3):
        print(f"{qator_index} ", end="")
        for ustun_index in range(3):
            print(f" {maydon[qator_index][ustun_index]} ", end="")
            if ustun_index < 2:
                print("|", end="")
        print()
        if qator_index < 2:
            print("  -----------")
    print()

    # O'yinchi yurishini olish
    print(f"🎯 {oyinchilar[joriy_oyinchi]} ({joriy_oyinchi}) navbati!")

    # Qator kiritish
    while True:
        qator = input("📍 Qator raqamini kiriting (0-2): ")
        if qator == "0" or qator == "1" or qator == "2":
            qator = int(qator)
            break
        else:
            print("❌ Noto'g'ri qator! 0, 1 yoki 2 kiriting.")

    # Ustun kiritish
    while True:
        ustun = input("📍 Ustun raqamini kiriting (0-2): ")
        if ustun == "0" or ustun == "1" or ustun == "2":
            ustun = int(ustun)
            break
        else:
            print("❌ Noto'g'ri ustun! 0, 1 yoki 2 kiriting.")

    # Katakni tekshirish va belgi qo'yish
    if maydon[qator][ustun] == " ":
        maydon[qator][ustun] = joriy_oyinchi
        print(f"✅ {joriy_oyinchi} belgisi ({qator}, {ustun}) ga qo'yildi!")
    else:
        print("❌ Bu katak band! Boshqa katak tanlang.")
        continue

    # G'olibni tekshirish
    galaba_bor = False
    for kombinatsiya in galaba_kombinatsiyalari:
        q1, u1 = kombinatsiya[0]
        q2, u2 = kombinatsiya[1]
        q3, u3 = kombinatsiya[2]

        if (
            maydon[q1][u1] == joriy_oyinchi
            and maydon[q2][u2] == joriy_oyinchi
            and maydon[q3][u3] == joriy_oyinchi
        ):
            galaba_bor = True
            break

    # G'alaba natijasi
    if galaba_bor:
        # Oxirgi maydonni ko'rsatish
        print("\n🏆 YAKUNIY MAYDON:")
        print("   0   1   2")
        for qator_index in range(3):
            print(f"{qator_index} ", end="")
            for ustun_index in range(3):
                print(f" {maydon[qator_index][ustun_index]} ", end="")
                if ustun_index < 2:
                    print("|", end="")
            print()
            if qator_index < 2:
                print("  -----------")

        print(f"\n🎉 {oyinchilar[joriy_oyinchi]} ({joriy_oyinchi}) yutdi!")
        print("🏆 Tabriklaymiz!")
        break

    # Durrangni tekshirish
    maydon_tola = True
    for qator in maydon:
        for katak in qator:
            if katak == " ":
                maydon_tola = False
                break
        if not maydon_tola:
            break

    if maydon_tola:
        # Oxirgi maydonni ko'rsatish
        print("\n🤝 YAKUNIY MAYDON:")
        print("   0   1   2")
        for qator_index in range(3):
            print(f"{qator_index} ", end="")
            for ustun_index in range(3):
                print(f" {maydon[qator_index][ustun_index]} ", end="")
                if ustun_index < 2:
                    print("|", end="")
            print()
            if qator_index < 2:
                print("  -----------")

        print("\n🤝 Durrang! Hech kim yutmadi.")
        print("🎮 Ikkalangiz ham yaxshi o'ynadingiz!")
        break

    # Navbatni almashtirish
    if joriy_oyinchi == "X":
        joriy_oyinchi = "O"
    else:
        joriy_oyinchi = "X"

print("\n👋 O'yindan foydalanganingiz uchun rahmat!")
print("🎮 Yana o'ynash uchun dasturni qayta ishga tushiring!")
