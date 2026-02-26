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
