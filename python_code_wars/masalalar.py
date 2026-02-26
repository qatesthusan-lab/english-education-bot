# # lst = [1, -5, 4, 6, 8, 48, 54, -12, 5]


# # # def invert(lst):
# # #     yng = []
# # #     for i in lst:
# # #         yng.append(-i)
# # #     return yng


# # def invert(lst):
# #     return [-i for i in lst]


# # print(invert(lst))


# # def kopaytma(x):
# #     lst = 1
# #     for i in x:
# #         lst = lst * i
# #     return lst


# # print(kopaytma(lst))


# # print(kopaytma(lst2))
# from functools import reduce

# lst = [1, 5, 4, 5, 64, 2, 1, 3, 4]
# lst2 = [4, 5, 75, 6, 4, 2, 1, 3, 4]


# def kopaytr(s, a):
#     return reduce(lambda x, y: x * y, lst)
# s = "1,2,3,4,5,6"

# lambda s: int(s)
# print(s)


# import string


# strng = "hello"


# def remove_char(s):
#     x = "" + s[1:-1]
#     return x


# print(remove_char(strng))


# def basic_op(operator, v1, v2):
#     if operator == "+":
#         return v1 + v2
#     if operator == "-":
#         return v1 - v2
#     if operator == "*":
#         return v1 * v2
#     if operator == "/":
#         return v1 / v2


# def basic_op(operator, value1, value2):
# return eval(f'{value1}{operator}{value2}')


# s = ["DUBL1N", "51NGAP0RE", "BUDAPE5T", "PAR15"]


# def correct(s):
#     h = s.replace("5", "S").replace("0", "O").replace("1", "I")
#     return h


# print(correct(s))


# def abbrev_name(name):
#     ism = name.split()
#     harf1 = ism[0][0]
#     harf2 = ism[1][0]

#     return harf1.upper() + "." + harf2.upper()


# print(abbrev_name("tom harris"))


# def switch_it_up(number):
#     match number:
#         case 0:
#             return "Zero"
#         case 1:
#             return "one"
#         case 2:
#             return "two"
#         case 3:
#             return "Three"
#         case 4:
#             return "Four"
#         case 5:
#             return "Five"
#         case 6:
#             return "Six"
#         case 7:
#             return "Seven"
#         case 8:
#             return "Eight"
#         case 9:
#             return "Nine"


# def lovefunc( flower1, flower2 ):
#  return (if flower1%2==0 and flower2 %2==1 or flower1 %2==1 and flower2 %2==0)


# def move(position, roll):
#     s = roll *2
#     x = position + s
#     return x

# move = lambda p,r:r*2 + p

# from shlex import join


# def pig_it(text):
#     matn = text.split()
#     sozlar = []
#     for soz in matn:
#      soz[0]=[-1]
#      soz[1:]= ["ay"]
#      sozlar.append(soz)
#      return sozlar

# arr1 = [3, 4, 5, 6, 7, 5]
# arr2 = [3, 4, 5, 2, 3, 1]


# def array_plus_array(arr1, arr2):
#     total = 0
#     for i in arr1 + arr2:
#         total += i
#     return total


# def count_sheep(n):
#     s = ""
#     for i in range(1, n + 1):
#         s += f"{i}  sheep..."

#     return s


# print(count_sheep(5))


# def multi_table(number):

#        rows = []
#         for i in range(...):
#             rows.append(...)

#         return "\n".join(rows)


# def multi_table(num):
#     arr = []
#     for i in range(1, 11):
#         arr.append(i * i)
#     return "\n".join(arr)


# print(multi_table(5))


# def count_by(x, n):
#     lst = []
#     for i in range(1,n+1):
#         s = i * x
#         lst.append(s)
#     return lst


# def how_many_dalmatians(n):
#     dogs = ["Hardly any", "More than a handful!", "Woah that's a lot of dogs!", "101 DALMATIONS!!!"]
#     if n <= 10:
#         return dogs[0]
#     elif n <= 50 :
#          return dogs[1]
#     elif n <= 101:
#         return dogs[3]
#     else:
#         return dogs[2]


# from pickle import FALSE


# def set_alarm(employed, vacation):
#     if employed == True and vacation == False:
#         return True
#     elif not vacation and employed == False:
#         return True


# def sum_array(arr):
#     if arr is None or len(arr) <=2:
#         return 0
#     else :
#        s =  min(arr) + max(arr)
#        return sum(arr) - s


# def get_average(marks):
#     s = marks // len(marks)
# return int(s)


# def fake_bin(x):
#     new_str = ""
#     for i in x:
#         if int(i) <5:
#             new_str = new_str + "0"
#         else:
#             new_str = new_str + "1"
#     return str


# def digitize(n):
#     s = str(n)
#     s[::-1]
#     [int(x) for x in s]
