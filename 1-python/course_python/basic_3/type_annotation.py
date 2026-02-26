def kitob_malumot(nomi: str, muallif: str, sahifa: int, narx: int = 0):
    if sahifa <= 0:
        return "Sahifa soni noto'g'ri!"

    jami_qiymat = ""

    if narx > 0:
        jami_qiymat = narx
    else:
        jami_qiymat = "Narx ko'rsatilmagan"

    return {
        "kitob_nomi": nomi,
        "muallif": muallif,
        "sahifalar": sahifa,
        "narx": jami_qiymat,
        "qalinlik": "Yupqa",
    }


print(kitob_malumot("Python asoslari", "John Doe", 300, 45000))
