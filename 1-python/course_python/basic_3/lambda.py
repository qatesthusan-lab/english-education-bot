# ortacha = lambda a, b: (a + b) / 2
# print(ortacha(5, 10))
# print(ortacha(50, 10))


# birichi_oxirgi = lambda s: "".join(x for x in s if x in "pn")
# print(birichi_oxirgi("python"))


# a_bormi = lambda x: "a" in x
# print(a_bormi("Lambda"))


# teskari = lambda tes: tes[::-1]
# print(teskari("salom"))


yigindi = 0
for i in range(0, 15):
    yigindi = yigindi + i
print(yigindi)


xisobla = sum(range(0, 15))

print(xisobla)

summa = lambda s: sum(range(s))
print(summa(15))
