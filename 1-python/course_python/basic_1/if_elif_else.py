print("===== 'telefon do'koni' =====")
narx = int(input("salom, telefoningiz naxi qancha ?: "))
if narx <= 0 or narx == None:
    print("bepulmi ??? ")
elif narx >=10_000_000:
    print("juda qimmat ")
elif narx >= 7_000_000:
    print("biroz qimmatroq")
elif narx >= 5_000_000:
    print("yaxshi narx ")
else:
    print("arzon narx ")

