import os
import sys
from tkinter import *

# Constants
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Timer reset
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    my_label.config(text="TIMER")
    check_marks.config(text="")
    global reps
    reps = 0

# Timer mechanism
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_brk_sec = SHORT_BREAK_MIN * 60
    long_brk_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_brk_sec)
        my_label.config(text="Break", fg=GREEN)
    elif reps % 2 == 0:
        count_down(short_brk_sec)
        my_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        my_label.config(text="Work!", fg=RED)

# Countdown mechanism
def count_down(count):
    count_min = int(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = int(reps / 2)
        for _ in range(work_sessions):
            marks += "✅"
        check_marks.config(text=marks)

# UI Setup
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Label
my_label = Label(text="TIMER", fg=GREEN, font=(FONT_NAME, 50), bg=YELLOW)
my_label.grid(column=1, row=0)

# Canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file=resource_path("tomato.png"))
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Buttons
start_btn = Button(text="Start", highlightthickness=0, command=start_timer)
start_btn.grid(column=0, row=2)

reset_btn = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_btn.grid(column=2, row=2)

# Checkmarks
check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

window.mainloop()
