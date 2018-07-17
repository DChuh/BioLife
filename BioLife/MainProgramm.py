from tkInterCanvas import *
from random import *
from datetime import date, timedelta
from landClasses import *
from plantsClasses import Barley
from collections import Counter
from vegeterians_classes import MouseFamily
from BioConstants import *
from predator_classes import *

errors_=list()
collors_=[ "red", "blue", "gray50", "green", "pink", "white", "yellow","magenta"]

directions=[(-1*mouse_rush, -1*mouse_rush), (-1*mouse_rush, 0),(-1*mouse_rush, 1*mouse_rush), (0, -1*mouse_rush), (0, 1*mouse_rush),(1*mouse_rush, -1*mouse_rush), (1*mouse_rush, 0),(1*mouse_rush, 1*mouse_rush)]
print ("start")

def get_x_direction(x=int(playFileld_x_size/2)):
    if (x!=0)&(x!=playFileld_x_size-1):
        x_wind=choice([-1, 0, 1])
    elif x==0:
        x_wind=choice([0, 1])
    elif x==playFileld_x_size-1:
        x_wind=choice([0, -1])
    return x_wind

def get_y_direction(y=int(playFileld_y_size/2)):
    if (y!=0)&(y!=playFileld_y_size-1):
        y_wind=choice([-1, 0, 1])
    elif y==0:
        y_wind=choice([0, 1])
    elif y==playFileld_y_size-1:
        y_wind=choice([0, -1])
    return y_wind

def seek_to_move(a):
    if abs(a)==0:
        b=0
    elif abs(a)>=1:
        b=int(mouse_move_radius * a / abs(a))
    return b

def max_corn_food_direction(x_current, y_current, seek_radius=mouse_seek_radius, food_needed_=330):
    if seek_radius>mouse_seek_radius:
        seek_radius=mouse_seek_radius
    max_food=0#playField[x_current][y_current].corn_food_stored
    coords=(110,110)
    for x_i in range(x_current-seek_radius, x_current+seek_radius):
        for y_i in range(y_current-seek_radius, y_current+seek_radius):
            if (x_i<0)or(x_i>playFileld_x_size-1)or (y_i<0)or(y_i>playFileld_y_size-1):
                pass
            else:
                if playField[x_i][y_i].corn_food_stored>max_food:
                    max_food=playField[x_i][y_i].corn_food_stored
                    coords=(seek_to_move(x_i-x_current), seek_to_move(y_i-y_current))

    if max_food*food_consumption_coeficient<food_needed_:
        coords=choice(directions)
    return coords

#every cell is populated with 1 initial Barley
#for x in range(40, 50):
 #   for y in range(30, 40):
  #      playField[x][y].add_citizen(Barley())

seed1=Counter(Barley=99)
for x in range(2,55):
    for y in range(2, 35, 15, ):
        playField[x][y].seeds_slots+=seed1
    for y in range(3, 36, 15, ):
        playField[x][y].seeds_slots+=seed1

#seed1=Counter(Barley=99)
#for x in range(2,40, 5):
 #   for y in range(67, 80, 5):
  #      playField[x][y].seeds_slots+=seed1


#[MouseFamily(10, 20), MouseFamily(30, 40), MouseFamily(70, 80)]
# populate with mouses
for x in range(10, 14, 1):
    for y in range(5, 13, 1):
        one_mouse_family=MouseFamily(x, y)
        one_mouse_family.old_members=99
        playField[x][y].corn_food_stored=4000000
        allMouses.append(one_mouse_family)

#place one fox
for x in range(10,13):
    for y in range(10, 11):
        one_fox=Fox()
        one_fox.x_axis=x
        one_fox.y_axis=y
        allFoxes.append(one_fox)

###MAIN CYCLE######==================================================
while True:
    ### dayly redraw
    canv_redraw()

    print("Today is {} day of {}, of {} year".format(gameDate.day, gameDate.month, gameDate.year))
    print("Errors: ", errors_)

    for x in range(playFileld_x_size):
        for y in range(playFileld_y_size):

            #cleanup mouse mark
            if playField[x][y].mouse_mark:
                #print("x={} y={} mark={}".format(x, y, playField[x][y].mouse_mark))
                playField[x][y].mouse_mark.clear()

            #draw fox holes
            if playField[x][y].fox_hole!=None:
                if (playField[x][y].fox_hole.in_use)and((playField[x][y].fox_hole.couple_use)):
                    playField[x][y].fox_hole.reset_counter()
                    width=3
                    collor="red"
                elif (playField[x][y].fox_hole.in_use):
                    playField[x][y].fox_hole.reset_counter()
                    width=2
                    collor="black"
                else:
                    width=1
                    playField[x][y].fox_hole.inc_counter()
                    collor="gray25"

                playField[x][y].fox_hole.in_use=False
                playField[x][y].fox_hole.couple_use=False
                draw_fox_hole(x, y, playField[x][y].fox_hole.size, width, collor )

                if playField[x][y].fox_hole.not_used_counter>playField[x][y].fox_hole.max_not_used_counter:
                    playField[x][y].fox_hole=None

            #draw stored corn
            if playField[x][y].corn_food_stored>1000:
                draw_corn_food(x, y, playField[x][y].corn_food_stored/300000)

            #draw fox marks and cleanup
            for fox_mark_ in playField[x][y].fox_marks:
                mark_size=2+int(10 * fox_mark_["Weight"]/Fox.max_weight)
                if fox_mark_["Sex"]=="male":
                    collor="blue"
                elif fox_mark_["Sex"]=="female":
                    collor="pink"
                draw_fox_mark(x, y,mark_size,collor)
                if (gameDate-fox_mark_["Date"])>fox_marks_duration:
                    playField[x][y].fox_marks.remove(fox_mark_)


######### PLANTS Cycle  ====================================================================================================================
            if (playField[x][y].get_citizen(0)!=None)or(playField[x][y].seeds_slots['Barley']>0):
                #printing las citizen Weight, numer of citizens and land cell soil parameters
                #print (x, y, "Weight={}".format(int(playField[x][y].get_citizen(len(playField[x][y].citizens)-1).weight)),
                   #    "slots={}".format(len(playField[x][y].citizens)),
                      # "mineral={:07f}".format(playField[x][y].mineral_percent),
                   ##    "humus={:05f}".format(playField[x][y].humus_percent),
                      # "detreet={:05f}".format(playField[x][y].detreet_percent),
                    #   "food_stored={}".format(int(playField[x][y].corn_food_stored+playField[x][y].grass_food_stored)),
                   #    " {}day of {}, of {} year".format(gameDate.day, gameDate.month, gameDate.year),
                   #    "seed_slots={}".format(playField[x][y].seeds_slots['Barley']))

                #colloring and sizing cells accordingly to population
                plantsNumber=len(playField[x][y].plant_citizens)
                # last member weight colloring
                corn_weight_=playField[x][y].get_citizen(len(playField[x][y].plant_citizens) - 1).corn_weight

                if corn_weight_<=0:
                    collor="spring green"
                elif 0<corn_weight_<Barley.corn_productivity/15:
                    collor="lawn green"
                elif Barley.corn_productivity/15<=corn_weight_<Barley.corn_productivity/10:
                    collor="green yellow"
                elif Barley.corn_productivity/10<=corn_weight_<Barley.corn_productivity/5:
                    collor="yellow"
                elif Barley.corn_productivity/5<=corn_weight_<Barley.corn_productivity/2:
                    collor="gold"
                elif corn_weight_>Barley.corn_productivity/2:
                    collor="coral"
            else:
                collor="gray50"

            #for all not empty cells run dayly cycle
            if playField[x][y].get_citizen(0)!=None:
                playField[x][y].dayly_cycle()
                draw_barley(x, y, plantsNumber, collor)
            #display seeds
            elif playField[x][y].seeds_slots['Barley']>0:
                draw_barley(x, y, 1, "black")

            # annual soil parameters change cycle. triggering once per year, 1 Jan
            if (gameDate.day==1)&(gameDate.month==1):
                playField[x][y].year_cycle()

            if (gameDate.day==1)&(gameDate.month==4):
                playField[x][y].spring_detreeting()

            # populate land cell with seeds
            if gameDate.month in Barley.seasons:
                while (playField[x][y].seeds_slots['Barley'])>0:
                    return_code=playField[x][y].add_citizen(Barley())
                    if return_code==1:
                        playField[x][y].seeds_slots['Barley']-=1
                # when cell is up to it's capacity, we propagate it to nearest sell (by random)
                    elif return_code==0:
                        playField[x+get_x_direction(x)][y+get_y_direction(y)].add_citizen(Barley())
                        playField[x][y].seeds_slots['Barley']-=1

##### ANIMALS cycle################################################
###Mouse cycle########################
    print ("{} mouse families. Up to 100 members of 25g wight".format(len(allMouses)))
    for mouse_number in range(len(allMouses)):
        if allMouses[mouse_number]:
            x_mouse=allMouses[mouse_number].get_x()
            y_mouse=allMouses[mouse_number].get_y()
            #print("x_={}, y_={}, unique_id={}, members={}, number={}".format(x_mouse, y_mouse, allMouses[mouse_number].uniqe_id, allMouses[mouse_number].old_members, mouse_number))
            #marking cell with mouse id
            if allMouses[mouse_number].old_members>10:
                #print("x_={}, y_={}, unique_id={}, members={}, number={}".format(x_mouse, y_mouse, allMouses[mouse_number].uniqe_id, allMouses[mouse_number].old_members, mouse_number))
                playField[x_mouse][y_mouse].mouse_mark.append(mouse_number)

            size_=allMouses[mouse_number].old_members

            draw_mouse_family(x_mouse, y_mouse, size_)
            #1/150 of capacity can be eaten at one day
            food_availiable_=int(playField[x_mouse][y_mouse].corn_food_stored * food_consumption_coeficient)

            # move_direction=max_food_direction(x_, y_)
            #running FOOD CONSUMPTION func.
            # return:
            # out_: [0]consumed food, [1]new_family object(or None), [2]moove flag, [3]detreted mouses [needed food]
            out_=allMouses[mouse_number].food_consume(food_availiable_)
            playField[x_mouse][y_mouse].corn_food_stored-=out_[0]
            playField[x_mouse][y_mouse].detreet_percent+= (out_[0] / 2 + out_[3]) / mass_of_soil

            if out_[1]!=None:
                allMouses.append(out_[1])
            if out_[2]:
                seek_radius_=int(allMouses[mouse_number].old_members)
                move_to=max_corn_food_direction(x_mouse, y_mouse, seek_radius_, out_[4] / 3)
                allMouses[mouse_number].move_dxy(move_to[0], move_to[1])
            #print ("Mouse_N={}, members={}, food_av={}, consumed={} Is_preg={}, preg_count={}, childs={}, ch_age{}".format(mouse_id, allMouses[mouse_id].old_members, food_availiable_, out_[0], allMouses[mouse_id].is_pregnant, allMouses[mouse_id].pregnance_counter, allMouses[mouse_id].childs_members, allMouses[mouse_id].childs_age))
            if allMouses[mouse_number].old_members<=1:
               allMouses[mouse_number]=None
        else:
            err=(gameDate, ("x_={}, y_={}, unique_id={}, members={}, number={}".format(allMouses[mouse_number].x_axis, allMouses[mouse_number].y_axis, allMouses[mouse_number].uniqe_id, allMouses[mouse_number].old_members, mouse_number)))
            errors_.append(err)
            print("EEEEEEEEERRRRRRRRRRR", ("x_={}, y_={}, unique_id={},  members={}, number={}".format(allMouses[mouse_number].x_axis, allMouses[mouse_number].y_axis, allMouses[mouse_number].uniqe_id, allMouses[mouse_number].old_members, mouse_number)))


    #cleanup None Mouses
    while (None in allMouses):
            for mouse_number in range(len(allMouses)):
                if (allMouses[mouse_number]==None):
                    del allMouses[mouse_number]
                    break

####  FOX CYCLE============================================================
    for i in range(len(allFoxes)):
        x_fox=allFoxes[i].x_axis
        y_fox=allFoxes[i].y_axis

        #hunting
        allFoxes[i].clock_update(gameDate)
        hunted_=allFoxes[i].fox_hunting()
        trash=allFoxes[i].hunt_redistribution(hunted_)
        #trash_detreeting
        playField[x_mouse][y_mouse].detreet_percent+=(trash / mass_of_soil)


        allFoxes[i].fox_marking()
        allFoxes[i].dayly_lifecycle_check()

       #draw and print(x_fox, y_fox)
        fox_size=2+int(10 * allFoxes[i].weight/allFoxes[i].max_weight)

        draw_fox(x_fox, y_fox, fox_size, allFoxes[i].color_D, allFoxes[i].color_r)
        print("id={}, partner_Id={}, wgt={}, sex={}, hntd={}, age={}".format(allFoxes[i].uniqe_id, allFoxes[i].partner_id, allFoxes[i].weight,  allFoxes[i].sex, hunted_,allFoxes[i].age/365))

        #Marking


        #FOX CLEANUP
        if allFoxes[i].is_alive==False:
           allFoxes[i]=None
    #add for detreeting foxes


    #cleanup None Foxes
    while (None in allFoxes):
            for fox_id in range(len(allFoxes)):
                if (allFoxes[fox_id]==None):
                    del allFoxes[fox_id]
                    break

    ##Additioanl 2 Foxes once oper year
    if (gameDate.year%1==0)and(gameDate.month==1)and( gameDate.day==1 or gameDate.day==2 ):
        one_fox=Fox()
        one_fox.x_axis=int(playFileld_x_size/2)
        one_fox.y_axis=int(playFileld_y_size/2)
        allFoxes.append(one_fox)

#dayly cycle
    gameDate=gameDate+timedelta(days=1)

