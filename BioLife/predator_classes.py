from random import choice, randint,randrange
from BioConstants import *
from landClasses import playField


class Predator(object):

    #status
    is_alive=False
    clock=gameDate
    #constants
    #input
    food_type="meet"
    #output
    weight=0
    age=0
    name="Predator Animal"
    x_axis=0
    y_axis=0

    #biological parameters of specie
    birth_weight=0
    max_weight=0
    max_age=0
    reproductive_age=0
    reproductive_cycle=0
    sex=None

    hole_coords=()
    #resources round trip
    weight_grows_ratio =0
    dayly_meet_consumption=0

    def __init__(self):
        self.weight=self.birth_weight
        self.is_alive=True

    def clock_update(self, clock=gameDate):
        self.clock=clock

    def get_hole_coords(self):
        if self.hole_coords:
            c=self.hole_coords
            return c
        else:
            return None

    def get_x(self):
        x_=self.x_axis
        return x_

    def get_y(self):
        y_=self.y_axis
        return y_

    def set_x(self, set_x=int(playFileld_x_size / 2)):
        correction=True
        if set_x<0:
            set_x=0
        elif set_x>playFileld_x_size-1:
            set_x= playFileld_x_size - 1
        else:
            correction=False
        self.x_axis=set_x
        return set_x

    def set_y(self, set_y=int(playFileld_y_size / 2)):
        correction=True
        if set_y<0:
            set_y=0
        elif set_y>playFileld_y_size -1:
            set_y = playFileld_y_size -1
        else:
            correction=False
        self.y_axis=set_y
        return set_y



    def x_direction(self):
        x_wind=0
        if (self.x_axis!=0)&(self.x_axis!=playFileld_x_size-1):
            x_wind=choice([-1, 0, 1])
        elif self.x_axis==0:
            x_wind=choice([0, 1])
        elif self.x_axis==playFileld_x_size-1:
            x_wind=choice([0, -1])
        return x_wind

    def y_direction(self):
        y_wind=0
        if (self.y_axis!=0)&(self.y_axis!=playFileld_y_size-1):
            y_wind=choice([-1, 0, 1])
        elif self.y_axis==0:
            y_wind=choice([0, 1])
        elif self.y_axis==playFileld_y_size-1:
            y_wind=choice([0, -1])
        return y_wind

    def move_dxy(self, dx=0, dy=0):
        self.x_axis+=dx
        self.y_axis+=dy
        if self.x_axis<0:
            self.x_axis=0
        if self.y_axis<0:
            self.y_axis=0
        if self.x_axis>playFileld_x_size-1:
            self.x_axis=playFileld_x_size-1
        if self.y_axis>playFileld_y_size-1:
            self.y_axis=playFileld_y_size-1

    def move_to_xy(self, to_x=0, to_y=0):
        self.x_axis=to_x
        self.y_axis=to_y
        if self.x_axis<0:
            self.x_axis=0
        if self.y_axis<0:
            self.y_axis=0
        if self.x_axis>playFileld_x_size-1:
            self.x_axis=playFileld_x_size-1
        if self.y_axis>playFileld_y_size-1:
            self.y_axis=playFileld_y_size-1

    def get_size(self):
        size=2+int(10 * self.weight/self.max_weight)
        return size

class Fox(Predator):
    class_counter=0
    uniqe_id=0

    reproductive_age=200
    is_child=True
    partner_id=None
    hunting_age=45
    is_hunter=False
    color_D="orange"
    color_r="black"

    hole_coords=()

    pregnance_period=50
    reproductive_cycle=365

    max_age=15*365
    season_gon={2, 3}
    is_pregnant=False
    pregnance_counter=0
    childs_consumers=list()

    child_grows_ratio=1.055   #  150 * (1.055)^45 ~ 1600
    old_grows_ratio=1.003# 1500* 1.005^200 ~ 4000


    food_consumption_coeficient=0.05
    birth_weight=300
    fertility_weight=4*1000
    critical_weight=1.5*1000
    max_weight = 8*1000
    childs=choice([4,4,5,5,5,6,6,7])

    def __init__(self):
        super().__init__()
        Fox.class_counter+=1
        self.uniqe_id=self.class_counter

        self.weight=self.birth_weight
        self.sex=choice(["male", "female"])
        self.childs_consumers=list()
        self.grows_ratio=self.child_grows_ratio
        self.color_D=choice(fox_colors_D)
        self.color_r=choice(fox_colors_r)


    # seek for mouses, avoiding other foxes
    def max_mouses_direction(self, seek_radius=fox_seek_radius, mouse_treshold=1):
        if seek_radius>fox_seek_radius:
            seek_radius=fox_seek_radius
        #print(self.x_axis, "   ", self.y_axis)

        max_marks=len(playField[self.x_axis][self.y_axis].mouse_mark)
        coords=(0,0)
        for x_i in range(self.x_axis-seek_radius, self.x_axis+seek_radius):
            for y_i in range(self.y_axis-seek_radius, self.y_axis+seek_radius):
                if (x_i<0)or(x_i>playFileld_x_size-1)or(y_i<0)or(y_i>playFileld_y_size-1):
                    pass
                else:
                    #avoiding places, used by another for for
                    not_in_use=True
                    #print (x_i, y_i)
                    if playField[x_i][y_i].fox_marks:
                        last_mark=playField[x_i][y_i].fox_marks[-1]
                    else:
                        last_mark=None
                    #maximium food place finding
                    if last_mark:
                        if (self.clock-last_mark["Date"]<re_usage_period)and(last_mark["Id"]!=self.uniqe_id)and(last_mark["Id"]!=self.partner_id):
                            #print(self.clock - last_mark["Date"])
                            not_in_use=False

                    if (len(playField[x_i][y_i].mouse_mark)>max_marks)and not_in_use:
                        max_marks=len(playField[x_i][y_i].mouse_mark)
                        coords=((x_i-self.x_axis), (y_i-self.y_axis))
        #print(max_marks)
        if max_marks<mouse_treshold:
            #need to be reworked.
            dirs=choice(directions_1_step)
            randint
            coords=(dirs[0]*randrange(fox_rush), dirs[1]*randrange(fox_rush))
        return coords

    def fox_hunting(self):
        hunted=0
        coords=self.max_mouses_direction()
        self.move_dxy(coords[0], coords[1])
        target=self.food_per_day()[0]+self.food_per_day()[1]+self.food_per_day()[2]
        #print(allFoxes[i].food_per_day()[0], "   ", allFoxes[i].food_per_day()[1], "    ", allFoxes[i].food_per_day()[2])
        #print("target={}".format(target))
        #availiable mouses
        mouse_list=playField[self.x_axis][self.y_axis].mouse_mark
        # Mouse eating.
        while (hunted<target)and(len(mouse_list)>0):
            if mouse_list:
                prey_id=mouse_list.pop()
                if len(allMouses)>prey_id:
                    while (allMouses[prey_id].old_members>3)and(hunted<target):
                        allMouses[prey_id].old_members-=1
                        hunted+=allMouses[prey_id].mouse_weight
           # except:
            #    break
        return hunted
        #print ("hunted={}".format(hunted))

    def number_by_id(self, id=None):
        for n in range(len (allFoxes)):
            if (allFoxes[n])and (allFoxes[n].uniqe_id==id):
                break
            else:
                pass
        return n



    def follow(self, fox_id ):

        parent_fox=allFoxes[self.number_by_id(fox_id)]
        if parent_fox:
            x=parent_fox.x_axis+choice(directions_1_step)[0]
            y=parent_fox.y_axis+choice(directions_1_step)[1]
            self.move_to_xy(x, y)
            return 1
        else:
            print("where is may daddy!!")
            return 0

    def dayly_lifecycle_check(self):
        self.age+=1
        if self.age==self.hunting_age:
            self.is_hunter=True
            self.is_child=False
            self.grows_ratio=self.old_grows_ratio

        #dying, if weight is less than cricical for reproductive age fox
        if (self.weight<self.critical_weight)and(self.age>self.reproductive_age):
            self.is_alive=False
            if self.partner_id:
                allFoxes[self.number_by_id(self.partner_id)].partner_id=None
            #detreeting fox rests
            playField[self.x_axis][self.y_axis].detreet_percent+=(self.weight/mass_of_soil)

        if self.age>self.max_age:
            self.is_alive=False

####love is here
        if self.partner_id==None:
            if self.sex=='male':
                if (self.clock.month in self.season_gon)&(self.partner_id==None):
                    leady_x_y=self.fox_male_estrus()
                    self.move_to_xy(leady_x_y[0], leady_x_y[1])
            elif self.sex=='female':
                if (self.clock.month in self.season_gon)&(self.partner_id==None):
                    fox_Id=self.fox_female_choise()
                    if (allFoxes[self.number_by_id(fox_Id)].partner_id==None)and (allFoxes[self.number_by_id(fox_Id)].partner_id!=self.uniqe_id):
                        self.partner_id=fox_Id
                        allFoxes[self.number_by_id(fox_Id)].partner_id=self.uniqe_id

        elif self.partner_id:


            #is_alive

            #try to pregn  droww some love signs

            #do some love picture and draw
            pass


        #Look for the hole
        # 1) partners hole
        # 2) current hole
        # 3) look for hole
        # 4) dig hole

        partner_hole=None
        look=self.look_for_hole()


        if (self.partner_id)and(allFoxes[self.number_by_id(self.partner_id)].get_hole_coords()):
            partner_hole=allFoxes[self.number_by_id(self.partner_id)].get_hole_coords()
            #print(partner_hole)
            if (playField[partner_hole[0]][partner_hole[1]].fox_hole != None):
                if ((partner_hole[0]-self.x_axis)+abs(partner_hole[1]-self.y_axis)<fox_seek_radius)and(playField[partner_hole[0]][partner_hole[1]].fox_hole.size>=self.get_size()):
                    playField[partner_hole[0]][partner_hole[1]].fox_hole.in_use=True
                    playField[partner_hole[0]][partner_hole[1]].fox_hole.couple_use=True
                    self.hole_coords=partner_hole



        elif self.hole_coords and (playField[self.hole_coords[0]][self.hole_coords[1]].fox_hole):
            if (abs(self.hole_coords[0]-self.x_axis)+abs(self.hole_coords[1]-self.y_axis)<fox_seek_radius)and(playField[self.hole_coords[0]][self.hole_coords[1]].fox_hole.size>=self.get_size()):
                # hole exists and in use
                playField[self.hole_coords[0]][self.hole_coords[1]].fox_hole.in_use=True
            else:
                playField[self.hole_coords[0]][self.hole_coords[1]].fox_hole.in_use=False
                if (look["Result"])and(look["HoleSize"]>=self.get_size()):
                    playField[look["Coordinates"][0]][look["Coordinates"][1]].fox_hole.in_use=True
                    self.hole_coords=look["Coordinates"]
                else:
                    self.hole_coords=self.hole_digging()

        elif (look["Result"])and(look["HoleSize"]>=self.get_size()):
                playField[look["Coordinates"][0]][look["Coordinates"][1]].fox_hole.in_use=True
                self.hole_coords=look["Coordinates"]
        else:
                self.hole_coords=self.hole_digging()

#dayly food consumption calculations
    def food_per_day(self):
        if self.weight<self.max_weight:
            food_for_grows=5*self.weight*(self.grows_ratio-1)
        else:
            food_for_grows=0

        life_support=self.weight * self.food_consumption_coeficient
        childs_food=0
        for child in self.childs_consumers:
            childs_food+=child.food_per_day
        if self.is_pregnant:
            childs_food+= self.food_consumption_coeficient*(self.childs*self.birth_weight/self.pregnance_period)*self.pregnance_counter
        # (return Child's food [0], life_support_food[1], food_for_grows)
        return (childs_food, life_support, food_for_grows)

    # 1 - childrens, life support, grows. Weight changfes are here too
    def hunt_redistribution(self, hunted=0):
        hunted_temp=hunted
        trash=0
        needs=self.food_per_day()

        #childs feeding
        if self.childs_consumers:
            for consumer in self.childs_consumers:
                one_child_food=consumer.food_per_day[1]+consumer.food_per_day[2]
                consumer.hunt_redistribution(one_child_food)
                hunted_temp-=one_child_food

        #trash produecd by parent fox
        trash=hunted_temp
        if hunted_temp>=needs[1]:
            hunted_temp-=needs[1]
        else:
            self.weight-=3*self.food_consumption_coeficient*(needs[1]-hunted_temp)
            hunted_temp=0

        if (hunted_temp>needs[2])and(self.weight<self.max_weight):  # or (self.uniqe_id%3==0)
            self.weight=self.weight * self.grows_ratio
        elif (10<hunted_temp<needs[2])and(self.weight<self.max_weight):
            self.weight=self.weight + self.weight*(1- self.grows_ratio)*(hunted_temp/needs[2])

        return trash
    #  def look_for_hole(self):
    def look_for_hole(self, *user_id):
        max_size=0
        coords=(0,0)
        result=False
        for x_i in range(self.x_axis-fox_seek_radius, self.x_axis+fox_seek_radius):
            for y_i in range(self.y_axis-fox_seek_radius, self.y_axis+fox_seek_radius):
                if (x_i<0)or(x_i>playFileld_x_size-1)or(y_i<0)or(y_i>playFileld_y_size-1):
                    pass
                else:
                    #avoiding places, used by another fox for 20 days
                    not_used_lately=True
                    if playField[x_i][y_i].fox_marks:
                        last_mark=playField[x_i][y_i].fox_marks[-1]
                    else:
                        last_mark=None
                    #maximium food place finding
                    if last_mark:
                        if (self.clock-last_mark["Date"]<hole_re_usage_period)and(last_mark["Id"]!=self.uniqe_id)and(last_mark["Id"]!=self.partner_id):
                            #print(self.clock - last_mark["Date"])
                             not_used_lately=False

                    if (playField[x_i][y_i].fox_hole!=None)and not_used_lately:
                        if (playField[x_i][y_i].fox_hole.size>max_size)and(playField[x_i][y_i].fox_hole.in_use==False):
                            max_size=playField[x_i][y_i].fox_hole.size
                            coords=(x_i, y_i)
        if max_size>0:
            result=True
        return {"Result":result,"Coordinates": coords, "HoleSize": max_size}
    #
    def hole_digging(self):
        x_y=[self.x_axis+randrange(-3,3),self.y_axis+randrange(-3,3), ]
        if x_y[0]<0:
            x_y[0]=0
        elif x_y[0]>playFileld_x_size-1:
            x_y[0]=playFileld_x_size-1
        if x_y[1]<0:
            x_y[1]=0
        elif x_y[1]>playFileld_y_size-1:
            x_y[1]=playFileld_y_size-1

        playField[x_y[0]][x_y[1]].fox_hole=FoxHole(2+int(10 * self.weight/self.max_weight), self.uniqe_id)
        return x_y

    # I'll try to describe a Fox love
#    def fox_coupling(self):
#       if self.partner_id==0:

    # male fox behavior during wedding time
    def fox_male_estrus(self, seek_radius=fox_seek_radius):
        if seek_radius>fox_seek_radius:
            seek_radius=fox_seek_radius
        best_foxy_points=0
        coords=(self.x_axis, self.y_axis)
        for x_i in range(self.x_axis-seek_radius, self.x_axis+seek_radius):
            for y_i in range(self.y_axis-seek_radius, self.y_axis+seek_radius):
                if (x_i<0)or(x_i>playFileld_x_size-1)or(y_i<0)or(y_i>playFileld_y_size-1):
                    pass
                else:
                    for i_f in range(len(playField[x_i][y_i].fox_marks)):
                        mark=playField[x_i][y_i].fox_marks[i_f]
                        points=(15-int(mark["Age"]/365)) + 15*(mark["Weight"]/self.max_weight)

                        #print(mark["Date"], self.clock, points)
                        if (points>best_foxy_points)&(self.clock-timedelta(days=3)<mark["Date"])&(mark['Sex']=="female")&(mark["Hole"]==False):
                            print("WOW")
                            best_foxy_points=points
                            coords=[x_i, y_i]
        #print(max_marks)
        # if best_foxy_points==0:
        #     #need to be reworked.
        #     dirs=choice(directions_1_step)
        #     randint
        #     coords=[dirs[0]*randrange(fox_rush), dirs[1]*randrange(fox_rush)]
        return coords
# female fox choose the best fox to make a couple. Couple is stable until one of fox dying

    def fox_female_choise(self, seek_radius=int(fox_seek_radius/2)):
        best_fox_points=0
        choise_Id=None
        for x_i in range(self.x_axis-seek_radius, self.x_axis+seek_radius):
            for y_i in range(self.y_axis-seek_radius, self.y_axis+seek_radius):
                if (x_i<0)or(x_i>playFileld_x_size-1)or(y_i<0)or(y_i>playFileld_y_size-1):
                    pass
                else:
                    for i_f in range(len(playField[x_i][y_i].fox_marks)):
                        mark=playField[x_i][y_i].fox_marks[i_f]
                        #print(mark)
                        if (mark['Sex']=="male")and(int(mark["Age"]/365)<=5)and not(mark["Partner_Id"]):
                            points=int(mark["Age"]/365)+10*(mark["Weight"]/self.max_weight)
                        elif (mark['Sex']=="male")and(int(mark["Age"]/365)>5)and not(mark["Partner_Id"]) :
                            points=(10-int(mark["Age"]/365)) + 10*(mark["Weight"]/self.max_weight)
                        else:
                            points=0
                        #print(mark["Date"], self.clock, points)
                        if (points>best_fox_points)&(self.clock-timedelta(days=2)<mark["Date"])&(mark['Sex']=="male")&(mark["Hole"]==False):
                            print("Fem_WOW", mark)
                            best_fox_points=points
                            choise_Id=mark["Id"]
        #print(max_marks)
        # if best_foxy_points==0:
        #     #need to be reworked.
        #     dirs=choice(directions_1_step)
        #     randint
        #     coords=[dirs[0]*randrange(fox_rush), dirs[1]*randrange(fox_rush)]
        return choise_Id



    # Making marks
    def fox_marking(self):
        #marking with parameters: self id, age, weight, partner weight(if availiable)
        fox_mark_={"Id":self.uniqe_id, "Sex": self.sex, "Age":self.age, "Weight":self.weight,"Partner_Id": self.partner_id, "Date":self.clock, "Hole":False}
        #print("Id:", self.uniqe_id, "  Sex:", self.sex, "  Age:", self.age, " Weight:", self.weight,"  Partner_Id:", self.partner_id, " Date: ", self.clock)
        x_=self.x_axis
        y_=self.y_axis
        playField[x_][y_].fox_marks.append(fox_mark_)

        if self.hole_coords:
            x_=self.hole_coords[0]
            y_=self.hole_coords[1]
            fox_mark_={"Id":self.uniqe_id, "Sex": self.sex, "Age":self.age, "Weight":self.weight,"Partner_Id": self.partner_id, "Date":self.clock, "Hole":True}
            playField[x_][y_].fox_marks.append(fox_mark_)
