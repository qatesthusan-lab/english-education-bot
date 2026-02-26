# sonlar = tuple(range(1,11))
# print("yigindi :",sum(sonlar))#barcha sonlar yigindisi
# juft_sonlar = []
# toq_sonlar = []
# for son in sonlar:
#     if son % 2 ==0:
#         son = juft_sonlar.append(son)
#     else:
#         son = toq_sonlar.append(son)
# print(f"juft sonlar :{juft_sonlar}\n toq sonlar: {toq_sonlar}")
# print(f"eng katta son :{max(sonlar)}\n eng kichik son:{min(sonlar)}")
# print(f"ortacha yigindi: {sum(sonlar) / 10 }")


from time import sleep

user = "admin"
parol = "python0"
tries = 0
result = False 
while not result:
    login = input("login:")
    par = input("parol:")
    if login == user and par == parol:
        print("welcome to your page !!!")
        result = True
    else:
        tries+=1
        print("wrong login or parol try again")
        sleep(0.5)
        print(f"you have {3 - tries} attempts")
        while tries >=3:
            print("you tried more than 3 !!! please wait for your next attempts ")
            for i in range(10,0,-1):
                sleep(1)
                print(i)
                sleep(1)
                tries = 0
            print("you have 3 attempts again !!!")
        
                