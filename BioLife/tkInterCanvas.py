from tkinter import *
from BioConstants import map_ratio, playFileld_x_size, playFileld_y_size

#graphic initialization
root_window=Tk()
canv = Canvas(root_window, width=map_ratio*playFileld_x_size, height=map_ratio*playFileld_y_size, bg="tan4", cursor="pencil")
canv.pack()

def canv_redraw():
    canv.update_idletasks()
    canv.update()
    canv.delete("all")

def c_redraw(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

       # canv.update_idletasks()
        # canv.update()
    return wrapper

def inc_x_y(func):
    def wrapper(x, y, *size, **kwargs):
        x+=1
        y+=1
        func(x, y, *size, **kwargs)
    return wrapper





#======DRAW FUNCTIONS ================
#@c_redraw
@inc_x_y
def draw_mouse_family(x, y, number_of_mouses):
    p_size=number_of_mouses/290 # 100 - max mouse counter
    #left ear
    canv.create_oval(map_ratio*(x-p_size-p_size*0.7), map_ratio*(y-p_size-p_size*0.7), map_ratio*(x-p_size+p_size*0.7),map_ratio*(y-p_size+p_size*0.7), fill="gray" )
    #righth ear
    canv.create_oval(map_ratio*(x+p_size-p_size*0.7), map_ratio*(y-p_size-p_size*0.7), map_ratio*(x+p_size+p_size*0.7),map_ratio*(y-p_size+p_size*0.7), fill="gray" )
    #FACE
    canv.create_oval(map_ratio*(x-p_size), map_ratio*(y-p_size), map_ratio*(x+p_size),map_ratio*(y+p_size), fill="gray" )
    #nose
    canv.create_oval(map_ratio*(x-p_size/5), map_ratio*(y-p_size/5+p_size/3), map_ratio*(x+p_size/5),map_ratio*(y+p_size/5+p_size/3), fill="gray25" )
    #eyes
    canv.create_oval(map_ratio*(x-p_size/5-p_size/2), map_ratio*(y-p_size/5-p_size/3), map_ratio*(x+p_size/5-p_size/2),map_ratio*(y+p_size/5-p_size/3), fill="" )
    canv.create_oval(map_ratio*(x-p_size/5+p_size/2), map_ratio*(y-p_size/5-p_size/3), map_ratio*(x+p_size/5+p_size/2),map_ratio*(y+p_size/5-p_size/3), fill="" )
@inc_x_y
def draw_barley(x, y, b_size, collor_):
    canv.create_rectangle([x*map_ratio, y*map_ratio],[x*map_ratio+b_size*map_ratio/105, y*map_ratio+b_size*map_ratio/105],fill=collor_, stipple='gray50' )
@inc_x_y
def draw_corn_food(x, y, size):
    canv.create_oval([x*map_ratio-size, y*map_ratio-size],[x*map_ratio+size, y*map_ratio+size] )
@inc_x_y
def draw_fox(x, y, f_size, fox_color_D='orange', fox_color_r='dim gray'):
    size=f_size/10
    canv.create_polygon(map_ratio*(x-size),map_ratio*(y),
                        map_ratio*x, map_ratio*(y+size),
                        map_ratio*(x+size),map_ratio*(y),
                        map_ratio*(x+size),map_ratio*(y-size),
                        map_ratio*(x+size+size/2),map_ratio*(y-size-size),
                        map_ratio*(x+size/2),map_ratio*(y-size),
                        map_ratio*(x-size/2),map_ratio*(y-size),
                        map_ratio*(x-size-size/2),map_ratio*(y-size-size),
                        map_ratio*(x-size),map_ratio*(y-size),
                        fill=fox_color_D,)

    canv.create_polygon(   map_ratio*(x+size-size/12),map_ratio*(y-size-size/12),
                        map_ratio*(x+size+size/3),map_ratio*(y-size-size*3/4),
                        map_ratio*(x+size/2+size/9),map_ratio*(y-size-size/9),
                        fill=fox_color_r,)

    canv.create_polygon(   map_ratio*(x-size/2-size/9),map_ratio*(y-size-size/9),
                        map_ratio*(x-size-size/3),map_ratio*(y-size-size*3/4),
                        map_ratio*(x-size+size/12),map_ratio*(y-size-size/12),
                        fill=fox_color_r,)



    canv.create_oval(map_ratio*(x-size/2-size/4),map_ratio*(y-size/2-size/4),
                     map_ratio*(x-size/2+size/4),map_ratio*(y-size/2+size/4),width=2, fill="white", outline="saddle brown")
    canv.create_oval(map_ratio*(x-size/2-size/10),map_ratio*(y-size/2-size/10),
                     map_ratio*(x-size/2+size/10),map_ratio*(y-size/2+size/10),width=2, fill="black")


    canv.create_oval(map_ratio*(x+size/2-size/4),map_ratio*(y-size/2-size/4),
                     map_ratio*(x+size/2+size/4),map_ratio*(y-size/2+size/4),width=2, fill="white", outline="saddle brown")
    canv.create_oval(map_ratio*(x+size/2-size/10),map_ratio*(y-size/2-size/10),
                     map_ratio*(x+size/2+size/10),map_ratio*(y-size/2+size/10), fill="black")


    canv.create_oval(map_ratio*(x-size/4),map_ratio*(y+size/2-size/4),
                     map_ratio*(x+size/4),map_ratio*(y+size/2+size/4), fill="black")

@inc_x_y
def draw_fox_hole(x, y, f_size, in_use=1, collor="black", *active):
    fill=""

    if active:
        fill="red"
        size=f_size/3
    size=f_size/10
    canv.create_polygon(map_ratio*(x-size),map_ratio*(y),
                        map_ratio*x, map_ratio*(y+size),
                        map_ratio*(x+size),map_ratio*(y),
                        map_ratio*(x+size),map_ratio*(y-size),
                        map_ratio*(x+size+size/2),map_ratio*(y-size-size),
                        map_ratio*(x+size/2),map_ratio*(y-size),
                        map_ratio*(x-size/2),map_ratio*(y-size),
                        map_ratio*(x-size-size/2),map_ratio*(y-size-size),
                        map_ratio*(x-size),map_ratio*(y-size),
                        outline=collor, fill="", width=in_use)

#TEMPORARY, Fox mark drow
#@c_redraw
@inc_x_y
def draw_fox_mark(x, y, f_size, collor="green",):
    fill=""
    size=f_size/20
    canv.create_polygon(map_ratio*(x-size),map_ratio*(y),
                        map_ratio*x, map_ratio*(y+size),
                        map_ratio*(x+size),map_ratio*(y),
                        map_ratio*(x+size),map_ratio*(y-size),
                        map_ratio*(x+size+size/2),map_ratio*(y-size-size),
                        map_ratio*(x+size/2),map_ratio*(y-size),
                        map_ratio*(x-size/2),map_ratio*(y-size),
                        map_ratio*(x-size-size/2),map_ratio*(y-size-size),
                        map_ratio*(x-size),map_ratio*(y-size),
                        outline=collor, fill="")
