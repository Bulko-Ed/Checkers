class Cat:
    def __init__(self, color, name):
        self.color = color
        self.name = name

    def meow(self, n):
        for i in range (n):
            print (f'{self.name} says meow')

Winkie = Cat('brown', 'Winkie') 
Winkie.meow(2)           

for i in range (4):
    for j in range (i):
        print ('*', end = ' ')
    print()    