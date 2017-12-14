

f = open('bupt.txt',r)

for l in f:
	print(l)
	a = l.split('\t')
	print(a[0])
	print(a[1])