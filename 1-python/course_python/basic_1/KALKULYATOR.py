#terminal kalkulyator
from time import sleep

print("terminal kalkulyator ")
print("=" * 40)

#hisoblash sonini kuzatish 
hisoblash_soni = 0 

while True:
    #menyuni korsatish 
    print("math operations :")
    sleep(0.5)
    print("1. qo'shishi +")
    sleep(0.5)
    print("2 ayirish -")
    sleep(0.5)
    print("3 kopaytirish *")
    sleep(0.5)
    print("4 bo'lish /")
    sleep(0.5)
    print("5 kvadrat **")
    sleep(0.5)
    print("6 qoldiq %")
    sleep(0.5)
    print("0 exit ")
    sleep(0.5)
    print("-" * 30)

    amal = float(input("choose math operations :"))

    #exit way from calculator 
    if amal == 0:
        print(f"bye !!! thank you for using app {hisoblash_soni} ")
        break
    #wrong choose:
    amal = float(amal)
    if amal!= 1 and amal != 2 and amal!= 3 and amal != 4 and  amal!= 5 and amal != 6 and amal    !=  0:
     print("you have choosen the wrong math operation")
     continue
    sleep(1)
    print("\nplease use only number ")
    sleep(1)
    print("enter the numbers ")
    num1 = float(input("first number : "))
    num2 = float(input("second  number : "))
    
    #xisoblash

    if amal == 1:
        result = num1 + num2
        print(f"{num1} + {num2} = {result}")
    elif amal == 2:
        ruselt = num1 - num2 
        print(f"{num1} - {num2} = {result}")
    elif amal == 3:
        result = num1 * num2 
        print(f"{num1} * {num2} = {result}")
    elif amal == 4:
        result = num1 / num2
        print(f"{num1} / {num2} = {result}")
    elif amal == 5:
        result = num1 ** num2
        print(f"The square of {num1} is {num2} ")
    elif amal == 6:
        if num2 == 0:
            print("wrong!!! it's not possible to divide by 0")
            continue
        result = num1 % num2
        print(f"the remaining remainder is {result}")

    hisoblash_soni += 1
    print(f"the number of calculations is equal to {hisoblash_soni} times")
    print("-" * 45)

    while True:
        davom = input("\n🔄 Yana hisoblash qilasizmi? (ha/yo'q): ")
        if davom == "ha" or davom == "h" or davom == "yes" or davom == "y":
            break
        elif davom == "yo'q" or davom == "yoq" or davom == "no" or davom == "n":
            print(f"\n👋 Xayr! Siz {hisoblash_soni} ta hisoblash bajardingiz.")
            print("📊 Kalkulyatordan foydalanganingiz uchun rahmat!")
            exit()
        else:
            print("❌ Iltimos, 'ha' yoki 'yo'q' deb javob bering!")
