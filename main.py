from tkinter import *
import math
# ---------------------- CONSTANTS ----------------------------- #
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

# -------------------------- TIMER RESET ---------------------------- #
def reset_timer():
    start_button.config(state="normal")
    window.after_cancel(timer)  #取消之前設定的計時器(timer)，時間暫停
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    checkmark_label.config(text="")
    global reps
    reps = 0

# ------------------------- TIMER MECHANISM ----------------------------- #
def start_timer():
    start_button.config(state="disabled")
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:   # final break
        title_label.config(text="Break", fg=RED, font=(FONT_NAME, 50), bg=YELLOW)
        count_down(long_break_sec)
    elif reps % 2 == 0:    # if it is 2nd/4th/6th rep:
        title_label.config(text="Break", fg=PINK, font=(FONT_NAME, 50), bg=YELLOW)
        count_down(short_break_sec)
    else:          # if it is the 1st/3rd/5th/7th rep:
        title_label.config(text="Work", fg=GREEN, font=(FONT_NAME, 50), bg=YELLOW)
        count_down(work_sec)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec <= 9:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:        #mainloop 中無法使用while 迴圈；1000表示每1000毫秒在跑一次count_down函數，以更新畫面
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:                     #當倒數計時為0時，呼叫計時器函數，進行下個階段的番茄鐘
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)  #顯示工作階段
        for _ in range(work_sessions):
            marks += "✔"
        checkmark_label.config(text=marks, fg=GREEN, bg=YELLOW)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

title_label = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 50), bg=YELLOW)
title_label.grid(column=1, row=0)

checkmark_label = Label(fg=GREEN, bg=YELLOW)
checkmark_label.grid(column=1, row=3)


start_button = Button(text="Start",highlightbackground=YELLOW, command=start_timer)
start_button.grid(column=0, row=2)


reset_button = Button(text="Reset",highlightbackground=YELLOW, command=reset_timer)
reset_button.grid(column=2, row=2)



window.mainloop()

