import tkinter as tk
from PIL import Image, ImageTk
from gameshow import *
root = tk.Tk()
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
print(screen_width)
print(screen_height)
#Width = 1920 * 1080
root.title("Are You The One?")
canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="#48bfe3")
canvas.grid(columnspan=16,rowspan=10)

logo = Image.open("logo.jfif")

logo = logo.resize((round(.2*screen_width),round(.305*screen_height)), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(columnspan=3, rowspan=2, column=0,row=0,pady=.0741*screen_height)

begin = tk.Label(root, width = round(.0094*screen_width), height = round(.0037*screen_height), text="Press Start to begin!", font=("Raleway",round(.0078125*screen_width)), fg="white", bg="#db3c63", borderwidth=2, relief="ridge")
begin.grid(columnspan=2,column=13,row=0)

gameshow = Gameshow()

instructions = tk.Label(root, width = round(.042*screen_width), height = round(.0028*screen_height), font=("Raleway",round(.0078125*screen_width)), fg="white", bg="#db3c63", text="Enter the names of up to 16 participants, separated by spaces,\nor leave blank for default names.", borderwidth=2, relief="ridge")
def start_game():
    main_btn_text.set("Submit Participants")
    begin.destroy()
    instructions.grid(columnspan=8,column=4,row=0,pady=round(.0185*screen_height))
    nameEntered.grid(columnspan=8,column=4,row=1)
    main_btn.configure(command=submit_names)

contestant_input = None
nameEntered = tk.Entry(root, width=round(.042*screen_width))
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
        if len(contestant_input) % 2 == 0 and len(contestant_input) <= 16:
            gameshow = Gameshow(contestant_input)
            gameshow._mm.assignPerfectMatches()
            nameEntered.destroy()
            instructions.destroy()
            gameshow._currentWeek = 0
            main_btn_text.set("Begin")
            main_btn.configure(command=week)


        else:
            main_btn_text.set("Resubmit Names")
            instructions.configure(text="Invalid Input. Enter the names of up to 16 paricipants, separated by spaces,\nor leave blank for default names.\nMake sure you are entering an even number of players!")
            return
    tbInfo.configure(text="Are You The One?", font=("Raleway",round(.013*screen_width),'bold'),width=round(.01*screen_width),height=round(.0046*screen_height))
    tbInfo.grid(columnspan=8, rowspan=3, column=4, row=0, pady=round(.018*screen_height))
    weekLabel.configure(text='Press Start!')
    weekLabel.grid(columnspan=8,rowspan=1,column=4,row=3,pady=round(.0093*screen_height))
    skip_btn.grid(columnspan=2, column=13, row=0)

weekLabel = tk.Label(root, width = round(.019*screen_width), height = round(.003*screen_height), font=("Raleway",round(.013*screen_width),'bold'), fg="white", bg="#db3c63", borderwidth=2, relief="ridge")
def week():
    if gameshow.getCurrentWeek() == 0:
        main_btn_text.set("Proceed to\nNext Week!")
        tbInfo.configure(width=round(.042*screen_width),height=round(.02*screen_height),font=("Raleway",round(.0078125*screen_width)))
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
    tbInfo.configure(width=round(.042*screen_width),height=round(.02*screen_height), font=("Raleway",round(.0078125*screen_width)))
    while not(gameshow._mm.everyoneMatched()):
        gameshow._currentWeek += 1
        info = gameshow.simulateWeek()

    displayTruthBooth(info)
    displayPartners()
    weekLabel.configure(text=f"Week {gameshow.getCurrentWeek()}")
    main_btn.destroy()
    skip_btn.destroy()


tbInfo = tk.Label(root, font=("Raleway",round(.0078125*screen_width)), fg="white", bg="#db3c63", text="",width=round(.042*screen_width),height=round(.02*screen_height), borderwidth=2, relief="ridge")
def displayTruthBooth(info):
    tbInfo.configure(text=f"Truth Booth Week {gameshow.getCurrentWeek()}\n{info}")
    tbInfo.grid(columnspan=8,rowspan=3,column=4,row=0,pady=round(.019*screen_height))

perfectlyMatchedLabels = None
remainingPlayerLabels = None
label_h = round(screen_height * .0037)
label_w = round(screen_width * .0083)
def displayPartners():
    i = 0
    j = 0
    placed = 0
    nextCol = {2:5,5:9,9:12,12:2}
    currRow = 4
    currCol = 2
    global perfectlyMatchedLabels
    global remainingPlayerLabels
    perfectlyMatchedLabels = {"couple" + str(i): tk.Label(root, font=("Raleway",round(.0078125*screen_width)), fg="black", bg="#faea1e", height=label_h, width=label_w, borderwidth=2, relief="ridge") for i in range(1, (gameshow._mm._numConfirmedPerfectlyMatched // 2)+1)}
    remainingPlayerLabels = {"couple" + str(i): tk.Label(root, font=("Raleway",round(.0078125*screen_width)), fg="white", bg="#db3c63", height=label_h, width=label_w, borderwidth=2, relief="ridge") for i in range(1, (gameshow._mm._numRemainingParticipants // 2)+1)}
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
main_btn = tk.Button(root, textvariable = main_btn_text, command = start_game, font=("Raleway",round(.0078125*screen_width)), bg="#db3c63", fg="white", height=round(.0021*screen_height), width=round(.0166*screen_width))
main_btn_text.set("Start")
main_btn.grid(columnspan=2, column=13, row=1)

skip_btn_text = tk.StringVar()
skip_btn = tk.Button(root, textvariable = skip_btn_text, command = skipResults, font=("Raleway",round(.0078125*screen_width)), bg="#db3c63", fg="white", height=round(.0021*screen_height), width=round(.0166*screen_width))
skip_btn_text.set("Skip to results!")

root.mainloop()