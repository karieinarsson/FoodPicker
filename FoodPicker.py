import pandas as pd
import random as rand
import curses
from os.path import exists

csv_dir = "csv/"
data = csv_dir + "data.csv"
buff = csv_dir + "buffer.csv"

def init():
    if not exists(data):
        df = pd.DataFrame({"name": [],"url": []})
        df.to_csv(data, index = False)
    if not exists(buff):
        df = pd.DataFrame({"buff": [0,1]})
        df.to_csv(buff, index = False)


def add_course(screen):
    screen.clear()
    screen.addstr(0,0,"Course name: \n")
    screen.refresh()
    name = get_string(screen) 

    screen.addstr(2,0,"Url: \n")
    screen.refresh()
    url = get_string(screen)
   
    df = pd.read_csv(data)
    df = df.append({"name":name, "url":url}, ignore_index = True)
    df.to_csv(data, index = False)
    
    return print_all_courses(screen)


def get_string(screen):
    curses.echo()
    string = ""
    while True:
        c = screen.getch()
        if c == curses.KEY_ENTER or c == 10 or c == 13:
            curses.noecho()
            return string
        string = string+chr(c)


def print_all_courses(screen):
    df = pd.read_csv(data)
    screen.clear()
    for i, name in enumerate(df["name"]):
        screen.addstr(i,0,str(i) + ": " + name)
    screen.refresh()
    return screen.getch()


def new_courses(screen):
    df = pd.read_csv(data)
    buff_df = pd.read_csv(buff)

    courses = list(range(len(df["name"])))

    courses.pop(buff_df["buff"][1])
    courses.pop(buff_df["buff"][0])

    idx = rand.sample(courses, 2)

    idx.sort()

    name0 = df["name"][idx[0]]
    name1 = df["name"][idx[1]]
    
    url0 = df["url"][idx[0]]
    url1 = df["url"][idx[1]]
    
    buff_df = pd.DataFrame({"buff": idx})
    buff_df.to_csv(buff, index = False)

    screen.clear()
    screen.addstr(0,0,"Course: " + name0 + "\nUrl: " + url0)
    screen.addstr(4,0,"Course: " + name1 + "\nUrl: " + url1)
    screen.refresh()
    return screen.getch()


def get_courses(screen):
    data_df = pd.read_csv(data)
    buff_df = pd.read_csv(buff)
    
    c0 = buff_df["buff"][0]
    c1 = buff_df["buff"][1]
    
    name0 = data_df["name"][c0]
    name1 = data_df["name"][c1]
    
    url0 = data_df["url"][c0]
    url1 = data_df["url"][c1]    

    screen.clear()
    screen.addstr(0,0,"Course: " + name0 + "\nUrl: " + url0)
    screen.addstr(4,0,"Course: " + name1 + "\nUrl: " + url1)
    screen.refresh()
    return screen.getch()


def main():
    init()
    screen = curses.initscr()
    curses.curs_set(0)  # Turn cursor off
    curses.cbreak()     # Turn off cbreak mode
    curses.noecho()     # Turn echo back on
    screen.keypad(True)
    screen.refresh()
    
    while True:
        screen.clear()
        screen.addstr(0,0,"1: Add Course")
        screen.addstr(1,0,"2: New courses")
        screen.addstr(2,0,"3: Get current courses")
        screen.addstr(3,0,"4: Show all courses")
        screen.addstr(4,0,"q: quit")
        screen.refresh()
        
        answer = chr(screen.getch())
       
        print(answer)

        if answer == "q":
            break
        
        elif answer == "1":
            c = add_course(screen)
        
        elif answer == "2":
            c = new_courses(screen)
       
        elif answer == "3":
            c = get_courses(screen)
        
        elif answer == "4":
            c = print_all_courses(screen)

        if chr(c) == "q":
            break
    
    screen.keypad(False)
    curses.nocbreak()   # Turn off cbreak mode
    curses.echo()       # Turn echo back on
    curses.curs_set(1)  # Turn cursor back on
    curses.endwin()


if __name__ == "__main__":
    main()
