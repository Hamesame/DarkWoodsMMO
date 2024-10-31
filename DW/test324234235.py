class weird:
    def __init__(self):
        self.coiso = {"oi":32, "treco":34}

    def append(self, tal):
        if tal in self.coiso:
            self.coiso[tal] += 1
        else:
            self.coiso[tal] = 1

class bag:
    def __init__(self):
        self.coiso = weird()



new_coiso = bag()

print(new_coiso.coiso.coiso)

new_coiso.coiso.append("asjkdhaskjd")
new_coiso.coiso.append("oi")

print(new_coiso.coiso.coiso)
