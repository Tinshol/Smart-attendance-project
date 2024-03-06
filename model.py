import tkinter as tk
import util
import attendance_project
  


class App:
    def __init__(self):
        self.main_window=tk.Tk()
        self.main_window.geometry('1100x510+100+100')
        self.main_window.config(bg='magenta')
        self.main_window.title('SLFC ATTENDANCE SYSTEM')


        self.login_button=util.get_button(self.main_window,'login','green',self.login_button)
        self.login_button.place(x=720,y=400)

        self.register_button=util.get_button(self.main_window,'register','gray',self.register_button,fg='black')
        self.register_button.place(x=720,y=300)

        self.webcam=util.get_img_label(self.main_window)
        self.webcam.place(x=21,y=10,width=641,height=480)
    #     self.show=util.get_img_label(self.webcam)

    # def show(self):
    #     self.login_button()

    def login_button(self):
        self.logon=attendance_project.main()

    def register_button(self):
        pass

    def start(self):
        self.main_window.mainloop()


if __name__=='__main__':
    app=App()
    app.start()