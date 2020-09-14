def skip_elements(elements):
    return [v for k,v in enumerate(elements) if k % 2 == 0]


el = ['a','b','c','d','e','f','g']
num = ['1','2','3','4']

asd =[f'{x} fuckin {n}' for x,n in zip(el, num)]

print(asd[0])


#print(skip_elements(el))