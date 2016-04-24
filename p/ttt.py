#print Product.objects.filter(price__gte=100).values("category_id").order_by("category_id").annotate(count=Count("category_id")).filter(count__gt=2)

'''
categories = Category.objects.values("id", "name")
category_info = {}
for c in categories:
    category_info[c["id"]] = c["name"]

products = Product.objects.values("category_id", "name", "price")
for p in products:
    print "Name: %s, Category: %s, Price: %.2f" % (p["name"], category_info[p["category_id"]], p["price"]) 

'''
import re

test_line = [
    "",
    "e",
    "(",
    ")",
    "((",
    "()",
    "()(",
    "()((",
    "esdfd",
    "esdfd(",
    "esdfd((",
    "esdfd((esdf",
    "esdfd((esdf)",
    "esdfd((esdf)(",
    "esdfd((esdf)(esdf",
    "esdfd((esdf)(esdf(",
    "esdfd((esdf)(esdf()",
    "esdfd((esdf)(esdf()e",
    "e+d\"d((e^$f)(esdf()e",
    "esdfd((esdf)(esdf((((((e"
    ]

def cut_break_while(line):
    cut_i = len(line)
    i = cut_i - 1
    while i>=0:
        if line[i:i+1] == "(": cut_i = i
        elif line[i:i+1] == ")": i = 0
        i = i - 1
    return line[:cut_i]

def cut_break_regular(line):
    cut_i = len(line)
    result = re.search(r'\([^\)]*$', line)
    if result != None:
        cut_i = result.start()
    return line[:cut_i]
    
for line in test_line:
    print "INPUT: %s\nWHILE: %s\nREGUL: %s\n" % (line, cut_break_while(line), cut_break_regular(line))

    
    
