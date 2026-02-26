import requests
from datetime import datetime


class NamazVaqtlari:
    """Namaz vaqtlari uchun class"""

    def __init__(self):
        self.base_url = "https://api.aladhan.com/v1/timingsByCity"
        self.method = 2  # ISNA usuli

    def internet_tekshir(self):
        """Internet aloqasini tekshiradi"""
        try:
            response = requests.get("https://www.google.com", timeout=3)
            return response.status_code == 200
        except:
            return False

    def shahar_namaz_vaqti(self, shahar, davlat="Uzbekistan"):
        """Bitta shahar uchun namaz vaqtini oladi"""

        params = {"city": shahar, "country": davlat, "method": self.method}

        try:
            response = requests.get(self.base_url, params=params, timeout=10)

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except requests.exceptions.RequestException:
            return None

    def namaz_jadval_chiqar(self, data, shahar):
        """Namaz vaqtlarini chiqaradi"""

        if not data:
            print(f"❌ {shahar} uchun ma'lumot olinmadi")
            return

        timings = data['data']['timings']
        date_info = data['data']['date']

        print(f"\n🕌 {shahar.upper()} - NAMAZ VAQTLARI")
        print("=" * 50)
        print(f"📅 Sana: {date_info['readable']}")
        print(f"📍 Joylashuv: {shahar}, O'zbekiston")
        print()
        print("🕐 BUGUNGI NAMAZ VAQTLARI:")
        print("-" * 30)
        print(f"🌅 Bomdod:      {timings['Fajr']}")
        print(f"🌞 Quyosh:      {timings['Sunrise']}")
        print(f"☀️  Peshin:      {timings['Dhuhr']}")
        print(f"🌇 Asr:         {timings['Asr']}")
        print(f"🌆 Shom:        {timings['Maghrib']}")
        print(f"🌙 Xufton:      {timings['Isha']}")

    def ozbek_shaharlari(self):
        """O'zbekiston shaharlari uchun namaz vaqtlari"""

        shaharlar = [
            "Tashkent",
            "Samarkand",
            "Bukhara",
            "Andijan",
            "Namangan",
            "Qarshi",
            "Nukus",
            "Termez",
            "Urgench",
        ]

        print("🇺🇿 O'ZBEKISTON SHAHARLARI - NAMAZ VAQTLARI")
        print("=" * 70)

        for shahar in shaharlar:
            data = self.shahar_namaz_vaqti(shahar)
            if data:
                timings = data['data']['timings']
                print(
                    f"🏙️  {shahar:<12}: Bomdod {timings['Fajr']} | Peshin {timings['Dhuhr']} | Shom {timings['Maghrib']}"
                )
            else:
                print(f"❌ {shahar}: Ma'lumot olinmadi")

    def asosiy_dastur(self):
        """Asosiy dastur"""

        print("🕌 NAMAZ VAQTLARI DASTURI")
        print("=" * 50)

        # Internet tekshirish
        if not self.internet_tekshir():
            print("❌ Internet aloqasi yo'q!")
            print("Iltimos internetni tekshiring va qayta urinib ko'ring.")
            return

        print("✅ Internet aloqasi yaxshi!")

        while True:
            print("\n📋 MENU:")
            print("1. Bitta shahar uchun namaz vaqti")
            print("2. O'zbekiston shaharlari")
            print("3. Chiqish")

            tanlov = input("\nTanlovingizni kiriting (1-3): ").strip()

            if tanlov == "1":
                shahar = input("Shahar nomini kiriting: ").strip()
                if shahar:
                    data = self.shahar_namaz_vaqti(shahar)
                    self.namaz_jadval_chiqar(data, shahar)
                else:
                    print("❌ Shahar nomini kiritishni unutdingiz!")

            elif tanlov == "2":
                self.ozbek_shaharlari()

            elif tanlov == "3":
                print("✨ Namozlaringiz qabul bo'lsin! ✨")
                break

            else:
                print("❌ Noto'g'ri tanlov! 1, 2 yoki 3 ni tanlang.")


# Dasturni ishga tushirish
if __name__ == "__main__":
    dastur = NamazVaqtlari()
    dastur.asosiy_dastur()
