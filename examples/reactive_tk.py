'''
This file tests and shows example of reactive observables
'''
from utils.Event import Reactive, observable, Observer
import tkinter as tk


# Watch for button text updates
class ReactiveButton(tk.Button):
    def __init__(self, *args, **kwargs):
        if isinstance(kwargs['text'], Reactive):
            reactive = kwargs['text']
            reactive.watch(lambda : self.config(text=reactive.value))

            kwargs['text'] = reactive.value

        super().__init__(*args, **kwargs)




class App:
    def __init__(self):
        self.root = tk.Tk()

        counter = Reactive(0) # reactive value that is added to ButtonText

        self.button = ReactiveButton(self.root, text=counter)
        self.button.pack()
        self.button2 = ReactiveButton(self.root, text=counter)
        self.button2.pack()

        # increments counter by 1. causes reactive effect
        # which updates button and button2
        def increment():
            counter.value = counter.value + 1

        self.clicker = tk.Button(self.root, text="increment", command=increment)
        self.clicker.pack()




@observable("name", "surname", "fullname")
class Data(Observable):
    def __init__(self, name, surname):
        super().__init__()
        self.name = name
        self.surname = surname


    def fullName():
        return self.name + " " + self.surname


if __name__ == '__main__':

    person = Data("Tammi", "Kuu")
    pearson = Data("Barna", "bas")

    @person.events.name.register
    def print_nimi(obj, key, value):
        print("nimi muutettiin " + value)

    @person.events.surname.register
    def print_snimi(obj, key, value):
        print("sukunimi muutettiin " + value)

    @person.events.fullname.register
    def print_nimi(key, value):
        print("koko nimi on " + value)


    person.name = "Mika"
    person.surname = "Mylly"
    person.fullname()

   
    app = App()
    app.root.mainloop()


    




    