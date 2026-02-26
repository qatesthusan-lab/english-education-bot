# match case boyicha oylar mashqi. 
oylar = int(input("iltimos 1/12 gacha raqam kiriting: "))
match oylar:
    case h if h < 1 or h >= 13: # h ozgaruvchi yaratildi va if sharti berildi
     print("aldama bolam") # shart true bolganda print ishlaydi
    case 1 :
     print("yanavr ")
    case 2 :
     print("fevral")
    case 3 :
     print("mart")
    case 4 :
     print("aprel")
    case 5 :
     print("may")
    case 6 :
     print("iyun")
    case 7 :
     print("iyul")
    case 8 :
     print("avgust")
    case 9 :
     print("sentabr")
    case 10 :
     print("oktabr")
    case 11 :
     print("noyabr")
    case 12 :
     print("dekabr")

  