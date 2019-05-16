from tkinter import *
from random import uniform
from time import clock
import tkinter.messagebox

# asking user for size and amount of mines
class Size_win:
    def __init__(self, tike):

        grid_size_window = Frame(tike)
        space_frame = Frame(grid_size_window, height=7, width=230)
        sub_01 = Label(grid_size_window, text="Grid settings:")
        space_frame_02 = Frame(grid_size_window, height=6, width=230)
        sub_02 = Label(grid_size_window, text="Width:", padx=10)
        self.ex = Entry(grid_size_window, width=26, justify=CENTER)
        space_frame_03 = Frame(grid_size_window, height=6, width=230)
        sub_03 = Label(grid_size_window, text="Height:", padx=10)
        self.ey = Entry(grid_size_window, width=26, justify=CENTER)
        space_frame_04 = Frame(grid_size_window, height=6, width=230)
        sub_04 = Label(grid_size_window, text="Mines:")
        self.em = Entry(grid_size_window, width=26, justify=CENTER)
        space_frame_05 = Frame(grid_size_window, height=15, width=230)
        size_ready = Button(grid_size_window, text="READY", command=self.download_size)
        space_frame_06 = Frame(grid_size_window, height=8, width=230)
        grid_size_window.grid(row=0, column=1)
        space_frame.grid(row=1, column=1)
        sub_01.grid(row=2, column=1)
        space_frame_02.grid(row=3, column=1)
        sub_02.grid(row=4, column=1)
        self.ex.grid(row=5, column=1)
        space_frame_03.grid(row=6, column=1)
        sub_03.grid(row=7, column=1)
        self.ey.grid(row=8, column=1)
        space_frame_04.grid(row=9, column=1)
        sub_04.grid(row=10, column=1)
        self.em.grid(row=11, column=1)
        space_frame_05.grid(row=12, column=1)
        size_ready.grid(row=13, column=1)
        space_frame_06.grid(row=14, column=1)

    def download_size(self): # gets values entered by user and checks them after clicking button
        self.wid = self.ex.get()
        self.hei = self.ey.get()
        self.min = self.em.get()
        if self.wid != "" or self.wid == 0:
            try: # not integer
                self.wid = int(self.wid)
            except ValueError:
                print("Wrong value, use only numbers!")
                raise ValueError("Incorrect width")
        else: # default size is 8x8
            self.wid = 8
        if self.hei != "" or self.hei == 0: # if its blank or 0 its uses default 8x8
            try:
                self.hei = int(self.hei)
            except ValueError:
                print("Wrong value, use only numbers!")
                raise ValueError("Incorrect height")
        else:
            self.hei = 8
        # if user wont enter mine amount its uses original minesweeper formula and takes the minimum value by default
        if self.min != "":
            try:
                self.min = int(self.min)
            except ValueError:
                print("Wrong mine value, you can use only numbers!")
                raise ValueError("Incorrect amount of mines")
        else:
            self.min = int(self.wid * self.hei / 8)
        if int(self.min) > int((self.wid - 1) * (self.hei - 1)):
            self.min = (self.wid - 1) * (self.hei - 1)
        if int(self.min) < int(self.wid * self.hei / 10):
            self.min = int(self.wid * self.hei / 10)
        size_window.destroy()

# the actual tkinter frame for minesweeper
class Buttons_grid:
    def __init__(self,master):
        # downloads the values from the value windows
        try:
            self.wid = en.wid
            self.hei = en.hei
            self.mines_am = en.min
        except AttributeError:
            raise Exception("Application turned off")

        # amount of grids
        self.buttons_am = self.hei * self.wid

        self.bombs = StringVar()
        upper = Frame(master, bd = 2) # frame of upper part of window where bombs amount and reset button are
        # the middle button with the face setup
        self.face_default = PhotoImage(file ="ico1.png")
        self.face_win = PhotoImage(file="ico2.png")
        self.face_boom = PhotoImage(file ="ico3.png")
        self.face = Button(upper, command = lambda: self.reset(self.buttons_am))
        self.face.config(image = self.face_default, height = 20, width = 20)
        self.face.image = self.face_default
        self.face.grid(row = 0, column = 2)
        self.bombs_left = Label(upper, textvariable = self.bombs, bg ="red", width = 12)
        self.bombs_left.grid(row = 0, column = 1)
        # using pack to set the buttons in 'upper' frame
        upper.pack(side = TOP, fill = X)
        frame_1 = Frame(master, bd = 4)
        frame_1.pack()

        # sets value of first_click bool to true
        # important because first click start initializes the bomb field generation
        self.first_click = True

        x_kor = 1
        y_kor = 0
        self.bombs_memory= self.mines_am
        self.bombs.set(self.bombs_memory)
        self.button_id = []
        self.bombz = []
        self.safe_squares = []
        self.sq_bombs = {}
        self.buttons = {}
        # generates the button for every component of buttons_am
        for x in range(1, self.buttons_am + 1):
            self.button_id.append(x)
            self.safe_squares.append(x)
            right_clicked = 0
            status = 0
            minez = 0
            self.sq_bombs[x]=StringVar()
            self.sq_bombs[x].set("     ")
            # the structure of button is: button(where it belongs (always frame_1), text for it, colour, command)
            # id, x and y coordinates, right clicked state, mines around it, state (whether its clicked)
            self.buttons[x] = [Button(frame_1, textvariable = self.sq_bombs[x], bg ="snow2",
                                      command = lambda x=x: self.button_click(x)), x, [x_kor, y_kor],
                                      right_clicked, minez, status]
            self.buttons[x][0].bind("<Button-3>", lambda event, x=x: self.right_b(event, self.buttons[x][1]))
            x_kor += 1
            if x_kor == self.wid + 1:
                x_kor = 1
                y_kor += 1

        # sets a place for each button
        for key in self.buttons:
            self.buttons[key][0].grid(row = self.buttons[key][2][1], column = self.buttons[key][2][0])

        self.reset(self.buttons_am)
        self.run_time = clock()

    # method called every time button is clicked
    def button_click(self, x):
        if self.first_click:
            self.first_clicked(x)
        try:
            self.nearby_bombs(x)
        except KeyError:
            pass

    # method called after first click, generates the mined fields
    def first_clicked(self, x):
        self.first_click = False
        ran_var = self.mines_am
        # set the mine fields by rng'ing number between 0 and amount of grids
        # if the value isnt already int the bombs array it adds it
        while ran_var > 0:
            mine = int(uniform(0.1, self.buttons_am+0.9))

            if mine not in self.bombz and mine != x:
                try:
                    self.bombz.append(mine)
                    self.safe_squares.remove(mine)
                    ran_var -= 1
                except ValueError:
                    pass
        # after generating every button that isn't a mine field gets the value of nearby bombs
        self.bombz_mem = self.bombz
        # a loop that counts all the nearby bombs for EVERY button including mined ones
        for key in self.buttons:
            near_b = 0
            if key not in self.bombz:

                if key - self.wid in self.bombz:
                    near_b += 1
                if key + self.wid in self.bombz:
                    near_b += 1

                if self.buttons[key][2][0] != self.wid:
                    if key + 1 in self.bombz:
                        near_b += 1
                    if key - self.wid + 1 in self.bombz:
                        near_b += 1
                    if key + self.wid + 1 in self.bombz:
                        near_b += 1

                if self.buttons[key][2][0] != 1:
                    if key - 1 in self.bombz:
                        near_b += 1
                    if key - self.wid - 1 in self.bombz:
                        near_b += 1
                    if key + self.wid - 1 in self.bombz:
                        near_b += 1

                self.buttons[key][4] = near_b

            else:
                self.buttons[key][4] = 9

        # at the end button is clicked 'again' but is not treated as the first click
        self.button_click(x)

    # a method that checks clicked button
    # if its a bomb it calls for explosion method and sets the reset button image with yellow face to face_boom
    def nearby_bombs(self, key):
        self.buttons[key][5] = 1
        if key in self.bombz:
            self.face.config(image = self.face_boom)
            self.face.image = self.face_boom
            self.explosion(key)
        # if there are no bombs next to button its blank
        elif self.buttons[key][4] == 0:
            self.sq_bombs[key].set("     ")
            self.buttons[key][0].configure(bg="ivory4")
        # otherwise amount of them is set as text
        else:
            self.sq_bombs[key].set(" {}  ".format(self.buttons[key][4]))
            self.buttons[key][0].configure(bg ="ivory4")

        # the clicked button is removed from save_squares list
        if key in self.safe_squares:
            try:
                self.safe_squares.remove(key)
            except ValueError:
                pass

        if self.buttons[key][3] == 1:
            self.buttons[key][3] = 0
            self.bombs_memory += 1
            self.bombs.set(self.bombs_memory)

        # reveal blank nearby squares
        if self.buttons[key][4] == 0:
            if self.buttons[key][2][0] != self.wid:
                if key + 1 in self.safe_squares:
                    self.button_click(key + 1)
                if key + self.wid + 1 in self.safe_squares:
                    self.button_click(key + self.wid + 1)
                if key - self.wid + 1 in self.safe_squares:
                    self.button_click(key - self.wid + 1)
            if self.buttons[key][2][0] != 1:
                if key - 1 in self.safe_squares:
                    self.button_click(key - 1)
                if key + self.wid - 1 in self.safe_squares:
                    self.button_click(key + self.wid - 1)
                if key - self.wid - 1 in self.safe_squares:
                    self.button_click(key - self.wid - 1)
            if key + self.wid in self.safe_squares:
                self.button_click(key + self.wid)
            if key - self.wid in self.safe_squares:
                self.button_click(key - self.wid)
        # reveal end

        # if all safe squares are clicked the game is over
        if any(self.safe_squares) == False:
            self.face.config(image = self.face_win)
            self.face.image = self.face_win
            win_window = tkinter.messagebox.askquestion("You win!","Your time {} seconds. Play again?".format(int(clock() - self.run_time)))
            if win_window == "yes":
                self.reset(self.buttons_am)
                self.reset(self.buttons_am)
            else:
                root.quit()

    # right button click, set colour and command for button after clicking it
    def right_b(self, event, key):
        if self.buttons[key][5] == 0:
            # from normal goes to red, unclickable
            if self.buttons[key][3] == 0:
                self.buttons[key][0].configure(bg ="red", command = self.do_nothing)
                self.buttons[key][3] = 1
                self.bombs_memory -= 1
                self.bombs.set(self.bombs_memory)
            # from red goes to yellow, warning, clickable
            elif self.buttons[key][3] == 1:
                self.buttons[key][0].configure(bg ="yellow", command = lambda x=key: self.button_click(x))
                self.bombs_memory += 1
                self.bombs.set(self.bombs_memory)
                self.buttons[key][3] = 2
            # yellow turns to normal
            elif self.buttons[key][3] == 2:
                self.buttons[key][0].configure(bg="snow2")
                self.buttons[key][3] = 0
        else:
            pass

    # method called after clicking mined field
    def explosion(self, key):
        # if button was flagged red by clicking right button after explosion its greed
        # otherwise black
        if self.buttons[key][3] == 0 or self.buttons[key][3] == 2:
            self.buttons[key][0].configure(bg="black")
        else:
            self.buttons[key][0].configure(bg="green")
        self.buttons[key][5] = 1
        try:
            self.bombz.remove(key)
        except ValueError:
            pass
        except KeyError:
            pass
        # explodes all the other bombs
        try:
            for b in self.bombz:
                try:
                    self.explosion(b)
                except ValueError:
                    pass
            for m in self.buttons:
                try:
                    self.buttons[m][0].configure(command=self.do_nothing)
                    self.buttons[m][5] = 1
                except ValueError:
                    pass
        # sometimes app cant manage the simultaneous explosion so it just needs to try again
        except KeyError:
            try:
                if self.buttons[key][3] == 0 or self.buttons[key][3] == 2:
                    self.buttons[key][0].configure(bg="black")
                else:
                    self.buttons[key][0].configure(bg="green")
                self.buttons[key][5] = 1
            except:
                pass

    # method that does nothing but still needed
    def do_nothing(self):
        pass

    # reset method (goes over all buttons and recovers them to original state)
    # also sets first_click to true
    def reset(self, y):
        self.first_click = True
        self.safe_squares[:] = []
        self.bombz[:] = []
        self.face.config(image = self.face_default)
        self.face.image = self.face_default
        for x in range(1, self.buttons_am + 1):
            self.buttons[x][0].configure(bg ="snow2", command = lambda x=x: self.button_click(x))
            self.buttons[x][3] = 0
            self.buttons[x][4] = 0
            self.buttons[x][5] = 0
            self.safe_squares.append(x)
            self.sq_bombs[x].set("     ")
        self.bombs_memory = self.mines_am
        self.bombs.set(self.bombs_memory)
        self.run_time = clock()

#***************************************************************************************************#
size_window = Tk()
size_window.title("Size")
en = Size_win(size_window)
size_window.mainloop()
root = Tk()
root.title("Pysweeper")
lel = Buttons_grid(root)
root.mainloop()