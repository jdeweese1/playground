class Tabber:
    def __init__(self, tab_level=0):
        self.__tab_level = tab_level

    def entab(self):
        self.__tab_level +=1
        return str(self)

    def detab(self):
        if self.__tab_level > 0:
            self.__tab_level -= 1
        return str(self)

    def __repr__(self):
        return f'{self.__class__.__name__}(tab_level={self.__tab_level})'

    def __str__(self):
        return self.__tab_level * '\t'


t = Tabber()

print(f'Hi i am jarod')
print(f'{t.entab()}i enjoy pizza')
print(f'{t.entab()}i like cheese')
print(f'{t}i like crust')
print(f'{t.detab()} thank you for listening')
print(repr(t))
