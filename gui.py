import tkinter as tk
from PIL import Image, ImageTk
from gameshow import *
root = tk.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.title("Are You The One?")
canvas = tk.Canvas(root,width=w,height=h,bg="#48bfe3")
canvas.grid(columnspan=16,rowspan=10)

logo = Image.open("logo.jfif")
scale = .3
logo = logo.resize((round(1280*scale),round(1098*scale)), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(columnspan=3, rowspan=2, column=0,row=0,pady=80)

begin = tk.Label(root, width = 18, height = 4, text="Press Start to begin!", font="Raleway", fg="white", bg="#db3c63", borderwidth=2, relief="ridge")
begin.grid(columnspan=2,column=13,row=0)

gameshow = Gameshow()

instructions = tk.Label(root, width = 80, height = 3, font="Raleway", fg="white", bg="#db3c63", text="Enter the names of up to 24 participants, separated by spaces,\nor leave blank for default names.", borderwidth=2, relief="ridge")
def start_game():
    main_btn_text.set("Submit Participants")
    begin.destroy()
    instructions.grid(columnspan=8,column=4,row=0,pady=20)
    nameEntered.grid(columnspan=8,column=4,row=1)
    main_btn.configure(command=submit_names)

contestant_input = None
nameEntered = tk.Entry(root, width=80)
def submit_names():
    global contestant_input
    contestant_input = str(nameEntered.get())
    global gameshow
    if contestant_input == "":
        gameshow = Gameshow()
        gameshow._mm.assignPerfectMatches()
        nameEntered.destroy()
        instructions.destroy()
        gameshow._currentWeek = 0
        main_btn_text.set("Enter Week 1...")
        main_btn.configure(command=week)
    else:
        contestant_input = contestant_input.strip().split(" ")
        if len(contestant_input) % 2 == 0 and len(contestant_input) <= 24:
            gameshow = Gameshow(contestant_input)
            gameshow._mm.assignPerfectMatches()
            nameEntered.destroy()
            instructions.destroy()
            gameshow._currentWeek = 0
            main_btn_text.set("Begin")
            main_btn.configure(command=week)


        else:
            main_btn_text.set("Resubmit Names")
            instructions.configure(text="Invalid Input. Enter the names of up to 24 paricipants, separated by spaces,\nor leave blank for default names.\nMake sure you are entering an even number of players!")
            return
    tbInfo.configure(text="Are You The One?", font=("Raleway",25,'bold'),width=20,height=5)
    tbInfo.grid(columnspan=8, rowspan=3, column=4, row=0, pady=20)
    weekLabel.configure(text='Press Start!')
    weekLabel.grid(columnspan=8,rowspan=1,column=4,row=3,pady=10)
    skip_btn.grid(columnspan=2, column=13, row=0)

weekLabel = tk.Label(root, width = 36, height = 3, font=("Raleway",25,'bold'), fg="white", bg="#db3c63", borderwidth=2, relief="ridge")
def week():
    if gameshow.getCurrentWeek() == 0:
        main_btn_text.set("Proceed to\nNext Week!")
        tbInfo.configure(width=80,height=22,font='Raleway')
        gameshow._currentWeek = 1
    inf = gameshow.simulateWeek()
    displayTruthBooth(inf)
    displayPartners()
    weekLabel.configure(text=f'Week {gameshow.getCurrentWeek()}!')
    gameshow._currentWeek += 1
    if gameshow._mm.everyoneMatched():
        main_btn.destroy()
        skip_btn.destroy()

def skipResults():
    tbInfo.configure(width=80, height=22, font='Raleway')
    while not(gameshow._mm.everyoneMatched()):
        gameshow._currentWeek += 1
        info = gameshow.simulateWeek()

    displayTruthBooth(info)
    displayPartners()
    weekLabel.configure(text=f"Week {gameshow.getCurrentWeek()}")
    main_btn.destroy()
    skip_btn.destroy()


tbInfo = tk.Label(root, font="Raleway", fg="white", bg="#db3c63", text="",width=80,height=22, borderwidth=2, relief="ridge")
def displayTruthBooth(info):
    tbInfo.configure(text=f"Truth Booth Week {gameshow.getCurrentWeek()}\n{info}")
    tbInfo.grid(columnspan=8,rowspan=3,column=4,row=0,pady=20)

perfectlyMatchedLabels = None
remainingPlayerLabels = None
def displayPartners():
    i = 0
    j = 0
    placed = 0
    nextCol = {2:5,5:9,9:12,12:2}
    currRow = 4
    currCol = 2
    global perfectlyMatchedLabels
    global remainingPlayerLabels
    perfectlyMatchedLabels = {"couple" + str(i): tk.Label(root, font="Raleway", fg="white", bg="#06d6a0", height=4, width=16, borderwidth=2, relief="ridge") for i in range(1, (gameshow._mm._numConfirmedPerfectlyMatched // 2)+1)}
    remainingPlayerLabels = {"couple" + str(i): tk.Label(root, font="Raleway", fg="white", bg="#db3c63", height=4, width=16, borderwidth=2, relief="ridge") for i in range(1, (gameshow._mm._numRemainingParticipants // 2)+1)}
    for person, partner in gameshow._mm._GUIconfirmedPerfectlyMatched.items():
        perfectlyMatchedLabels["couple"+str(i+1)].configure(text=f"{person} & {partner}")
        perfectlyMatchedLabels["couple"+str(i+1)].grid(columnspan = 2, column = currCol, row = currRow)
        i += 1
        placed += 1
        currCol = nextCol[currCol]
        if placed >= 4:
            currRow += 1
            placed = 0
    for person, partner in gameshow._mm._GUIcurrentPartners.items():
        remainingPlayerLabels["couple"+str(j+1)].configure(text=f"{person} & {partner}")
        remainingPlayerLabels["couple"+str(j+1)].grid(columnspan = 2, column = currCol, row = currRow)
        j += 1
        placed += 1
        currCol = nextCol[currCol]
        if placed >= 4:
            currRow += 1
            placed = 0

main_btn_text = tk.StringVar()
main_btn = tk.Button(root, textvariable = main_btn_text, command = start_game, font="Raleway", bg="#db3c63", fg="white", height=4, width=18)
main_btn_text.set("Start")
main_btn.grid(columnspan=2, column=13, row=1)

skip_btn_text = tk.StringVar()
skip_btn = tk.Button(root, textvariable = skip_btn_text, command = skipResults, font="Raleway", bg="#db3c63", fg="white", height=4, width=18)
skip_btn_text.set("Skip to results!")

root.mainloop()