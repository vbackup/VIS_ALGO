from tkinter.font import BOLD
from tkinter import *
import tkinter
from PIL import Image, ImageTk
import time
import knapsack

root = Tk()

is_paused = False
x = 0
y = 0
w = int(600/8)
h = int(450/5) 
txt = 1
curr_row = 0
curr_col = 0

def intialize_var():
    global x,y,w,h,txt, curr_row, curr_col,tablecell,run_clicked,is_paused,K,no_of_items,max_weigth, tablecell
    run_clicked = True
    
    values = list(value_arr.get().split(" "))
    values = [int(x) for x in values]
    weigths = list(weight_arr.get().split(" "))
    weigths = [int(x) for x in weigths]
    no_of_items = len(values)
    max_weigth = int(k_weigth.get())

    tablecell = [[0 for x in range(max_weigth+1)] for y in range(no_of_items+1)]
    K = knapsack.knapsack(max_weigth,weigths,values,no_of_items)

    table.delete('all')
    w = int(600/ (max_weigth+1))
    h = int(450/ (no_of_items+1))
    t_x=0
    t_y=0
    for r in range(no_of_items+1):
        for c in range(max_weigth+1):
            table.create_rectangle(t_x,t_y,t_x+w,t_y+h)
            t_x+=w
        t_y+=h
        t_x=0

    x = 0
    y = 0 
    curr_row = 0
    curr_col = 0
    run_clicked = False
    if is_paused:
        is_paused = False
        stop_b.config(image=stop_img)
    animate_cell(table)

def next(table):
    global x,y,w,h,K,curr_col,curr_row,i,j
    if(curr_col==max_weigth+1):
        curr_col = 0
    cell = table.create_rectangle(x,y,x+w,y+h)
    table.itemconfig(cell,fill='Green')
    rowtxt = "  "+str(curr_row)+"  "
    i.config(text = rowtxt)
    coltxt = "  "+str(curr_col)+"  "
    j.config(text = coltxt)
    tablecell[curr_row][curr_col] = table.create_text(x + int(w/2),y + int(h/2),text = K[curr_row][curr_col],fill="black",font = ('Helvetica 20 bold'))

    root.update()
    time.sleep(0.7 / speed_s.get())
    table.delete(cell)
    if curr_col==max_weigth:
        x = 0
        y+=h
        curr_col=0
        curr_row+=1
    else:
        curr_col+=1
        x+=w
    if(curr_row==no_of_items+1 and curr_col==max_weigth+1):
        res = " "+str(K[-1][-1])+" "
        final_res.config(bg='green', text=res)

def back(table):
    global curr_col,curr_row,x,y,w,h,i,j
    if(curr_col==0):
        table.delete(tablecell[curr_row-1][curr_col-1])
        curr_row-=1
        curr_col = max_weigth
        rowtxt = "  "+str(curr_row)+"  "
        i.config(text = rowtxt)
        coltxt = "  "+str(curr_col)+"  "
        j.config(text = coltxt)
        y-=h
        x = max_weigth*w
    elif (curr_col>0 and curr_col<max_weigth+1):
        table.delete(tablecell[curr_row][curr_col-1])
        curr_col-=1
        coltxt = "  "+str(curr_col)+"  "
        j.config(text = coltxt)
        x-=w
    else:
        table.delete(tablecell[curr_row-1][curr_col-1])
        curr_row-=1
        curr_col-=1
        rowtxt = "  "+str(curr_row)+"  "
        i.config(text = rowtxt)
        coltxt = "  "+str(curr_col)+"  "
        j.config(text = coltxt)
        x-=w
        y-=h
    
def toggle_pause():
    global is_paused
    
    if is_paused != True:
        is_paused = True
        stop_b.config(image=resume_img)
    else:
        is_paused = False
        stop_b.config(image=stop_img)
        animate_cell(table)

def animate_cell(table):
    global is_paused,x,y,w,h,txt, curr_row, curr_col,tablecell, run_clicked
    root.update()
    time.sleep(1)

    for r in range(curr_row,no_of_items+1):
        if curr_col>=max_weigth+1:
            curr_col = 0
        rowtxt = "  "+str(curr_row)+"  "
        i.config(text = rowtxt)

        for c in range(curr_col,max_weigth+1):
            if (run_clicked):
                return
            if not is_paused:

                coltxt = "  "+str(curr_col)+"  "
                j.config(text = coltxt)
                cell = table.create_rectangle(x,y,x+w,y+h)
                table.itemconfig(cell,fill='Green')
                tablecell[r][c] = table.create_text(x + int(w/2),y + int(h/2),text = K[r][c],fill="black",font = ('Helvetica 20 bold'))

                root.update()
                time.sleep(0.7 / speed_s.get())
                table.delete(cell)
                x+=w
                curr_col+=1
            else:
                break
        if is_paused == True:
            if curr_col>=max_weigth+1:
                x = 0
                y+=h
                curr_row+=1
            break
        y+=h
        x=0
        curr_row+=1

    if(curr_row==no_of_items+1 and curr_col==max_weigth+1):
        res = " "+str(K[-1][-1])+" "
        final_res.config(bg='green', text=res)

def draw():
    global canvas,table,text_can, stop_b, i,j, k_weigth,value_arr,weight_arr, speed_s,final_res
    global photo, run_img, stop_img, resume_img, back_img, next_img
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry('%dx%d'%(sw,sh))
    root.state('zoomed')

    canvas = Canvas(root,bg='black',highlightthickness=0)
    canvas.pack(fill=tkinter.BOTH, expand=True)

    canvas.create_line(int(sw*0.0000),int(sh*0.1736),int(sw*0.6510),int(sh*0.1736),fill='white')
    canvas.create_line(int(sw*0.6510),int(sh*0.0000),int(sw*0.6510),int(sh*1.0000),fill='white')
    canvas.create_line(int(sw*0.6510),int(sh*0.1157),int(sw*1.0000),int(sh*0.1157),fill='white')
    canvas.create_line(int(sw*0.6510),int(sh*0.8101),int(sw*1.0000),int(sh*0.8101),fill='white')

    UI_frame1 = Frame(canvas,bg='black',width=int(sw*0.6510),height=int(sh*0.1580))
    canvas.create_window(0,0, anchor=NW,window=UI_frame1)
    
    N = Label(UI_frame1,text='Knapsack Weight',bg ='black',fg='white',font=(12))
    N.grid(row=0,column=0, padx=65,pady=22)
    weights = Label(UI_frame1,text='Weights',bg ='black',fg='white',font=(12))
    weights.grid(row=0,column=1,padx=140,pady=22)
    val = Label(UI_frame1,text='Values',bg ='black',fg='white',font=(12))
    val.grid(row=0,column=2,padx=140,pady=22)
    
    k_weigth = Entry(UI_frame1,bg='white',width=4,font=(12))
    k_weigth.grid(row=1,column=0,padx=50,pady=17)
    k_weigth.insert(0,'7')
    value_arr = Entry(UI_frame1,bg='white',font=(12))
    value_arr.grid(row=1,column=1,padx=50,pady=17)
    value_arr.insert(0,'1 4 5 7')
    weight_arr = Entry(UI_frame1,bg='white',font=(12))
    weight_arr.grid(row=1,column=2,padx=50,pady=17)
    weight_arr.insert(0,'1 3 4 5')

    Label(canvas,text='i',bg='black',fg='white',font=(14)).place(x=150,y=185)
    i = Label(canvas,text = "  0  ",bg='white',font = ('Helvetica 15 bold'))
    i.place(x=175,y=185)

    Label(canvas,text='j',bg='black',fg='white',font=(14)).place(x=525,y=185)
    j = Label(canvas,text="  0  ",bg='white',font = ('Helvetica 15 bold'))
    j.place(x=550,y=185)

    table = Canvas(canvas,bg='red',width=600,height=450)
    table.place(x=75,y=300)

    t_w = int(600/8)
    t_h = int(450/5)
    t_x=0
    t_y=0
    for r in range(5):
        for c in range(8):
            table.create_rectangle(t_x,t_y,t_x+t_w,t_y+t_h)
            t_x+=t_w
        t_y+=t_h
        t_x=0
    
    UI_frame2 = Frame(canvas,width=250,height=250)
    canvas.create_window(int(sw*0.55),int(sh*0.73), anchor=CENTER,window=UI_frame2)

    image_c = Canvas(UI_frame2,bg='black',highlightthickness=0,width=250,height=250)
    image_c.grid(row=0,column=0,padx=0,pady=0)

    image = Image.open('knapsack.png')
    resize_img = image.resize((500,490),Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(resize_img)
    image_c.create_image(125,140,image=photo,anchor=CENTER)
    
    run_b = Button(bd=0,bg ='black',activebackground='black',command=intialize_var)
    image = Image.open('run.png')
    resized_run = image.resize((105,42))
    run_img = ImageTk.PhotoImage(resized_run)
    run_b.config(image=run_img)
    run_b.place(x = 1100,y=30)

    stop_b = Button(bd=0,bg='black',activebackground='black',command=toggle_pause)
    image = Image.open('stop.png')
    resized_stop = image.resize((105,42))
    stop_img = ImageTk.PhotoImage(resized_stop)
    stop_b.config(image=stop_img)
    stop_b.place(x=1300,y=30)

    image = Image.open('resume.png')
    resized_resume = image.resize((105,42))
    resume_img = ImageTk.PhotoImage(resized_resume)

    speed_L = Label(canvas,text='Speed',bg='black',fg='white',font=('Aerial',14,BOLD))
    speed_L.place(x=1050,y=714)
    speed_s = Scale(canvas,from_=0.25,to=2.00,resolution=0.25,orient=HORIZONTAL,length=300,bd=0,bg='black',fg='white',highlightbackground='black',activebackground='#5FA8F5')
    speed_s.set(1)
    speed_s.place(x=1150,y=700)

    back_b = Button(bd=0,bg='black',activebackground='black', command= lambda: back(table))
    image = Image.open('back.png')
    resized_b = image.resize((100,30)) 
    back_img = ImageTk.PhotoImage(resized_b)
    back_b.config(image=back_img)
    back_b.place(x=1150,y=750)

    next_b = Button(bd=0,bg='black',activebackground='black',command=lambda: next(table))
    image = Image.open('next.png')
    resized_next = image.resize((100,30)) 
    next_img = ImageTk.PhotoImage(resized_next)
    next_b.config(image=next_img)
    next_b.place(x=1300,y=750)

    final_res = Label (image_c,text="    ",bg='white', font= ('Helvetica 20 bold'))
    final_res.place(x=115, y=145)

    algo_canvas = Canvas(canvas,width= sw - int(sw*0.6510), height=sh - (sh*0.1157 + (sh - int(sh*0.8101))), bg = 'black')
    algo_canvas.place(x = int(sw*0.6510),y = int(sh*0.1157))
    algo = "for i in range(no_of_items + 1):\n\n     for j in range(Knapsack_Weight + 1):\n\n          if (i == 0 or j == 0):\n               K[i][j] = 0\n\n          elif (Weights[i-1] <= W):\n               K[i][j] = max(Values[i-1] +\n                  K[i-1][j-Weights[i-1]], K[i-1][j])\n\n          else:\n               K[i][j] = K[i-1][j]"
    algo_canvas.create_text(270,300,text=algo,fill='white', font= ('Helvetica 20 bold')) 

draw()
root.mainloop()
