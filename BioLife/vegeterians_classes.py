from random import choice
from BioConstants import *

class Vegeterian(object):
    #status
    is_alive=False
    #constants
    #input
    food_type=""
    #output
    weight=0
    age=0
    name="Vegeterian Animal"
    x_axis=int(playFileld_x_size/2)
    y_axis=int(playFileld_y_size/2)
    #biological parameters of specie

    is_pregnant=False
    pregnance_counter=0
    childs_age=0
    childs_members=0


    birth_weight=0


    max_weight=0
    max_age=0
    reproductive_age=0
    reproductive_cycle=0

    #resources round trip
    weight_grows_ratio =0
    dayly_corn_consumption=0

    def __init__(self):
        self.weight=self.birth_weight
        self.is_alive=True

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

    def move_dxy(self, dx=110, dy=110):
        new_x=self.x_axis+dx
        new_y=self.y_axis+dy
        if new_x<0:
            new_x=0
            print("x to zerro")
        elif new_x>playFileld_x_size-1:
            self.x_axis=playFileld_x_size-1
            print("x to pf-1")
        if new_y<0:
            new_y=0
            print("y to zerro")
        elif new_y>playFileld_y_size-1:
            new_y=playFileld_y_size-1
            print("y to pf-1")
        self.x_axis=new_x
        self.y_axis=new_y
        assert (new_x>0, new_y>0, new_x<playFileld_x_size, new_y>playFileld_y_size)



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

# 1 mouse family, up to 100 old mouses
class MouseFamily(Vegeterian):
    class_counter=0
    uniqe_id=0

    reproductive_age=25
    reproductive_cycle=30
    max_age=365*1.5
    childs_members=0
    childs=choice([4,4,5,5,5,6,7])
    chuild_weight=5

    mouse_weight=25
    old_members=2
    birth_weight=mouse_weight*old_members
    max_number=100
    dayly_food_per_mouse=50
    dayly_food_per_child=10

    dayly_corn_consumption=dayly_food_per_mouse*old_members+childs_members*dayly_food_per_child

    moove=1 #1 cell per day
    food_type = "corn"



    def __init__(self,x_axis=playFileld_x_size/2, y_axis=playFileld_y_size/2):
        super().__init__()
        MouseFamily.class_counter+=1
        self.uniqe_id=self.class_counter

        self.is_alive=True
        self.x_axis=x_axis
        self.y_axis=y_axis

    #devide family, when it have 100 members and food enough
    def deviding(self):
        self.old_members=int(self.old_members/2)

        new_family=MouseFamily(self.x_axis+self.x_direction(), self.y_axis+self.y_direction())
        new_family.move_dxy(0,0)
        new_family.old_members=10
        self.age=self.age/2
        return new_family


    def grows(self):
        if self.old_members<self.max_number:
            #childs to old
            if (self.childs_age>=self.reproductive_age)&(self.childs_members!=0):
                self.old_members+=self.childs_members
                self.childs_members=0
                self.childs_age=0
            else:
                self.childs_age+=1
            #pregnance
            if self.pregnance_counter>=self.reproductive_cycle:
                self.childs_members=self.childs*(1+int(self.old_members/8))

                self.pregnance_counter=0
                self.is_pregnant=False
            else:
                self.pregnance_counter+=1
            #became pregnant, if is not, and counter inverase, when is
            if self.is_pregnant==False:
                self.is_pregnant=True
            else:
                self.pregnance_counter+=1
            new_family=None

        elif self.old_members>=self.max_number:
            new_family=self.deviding()
        return new_family

    def stagnation(self):
        self.is_pregnant=False
        self.pregnance_counter=0

    def starwation(self):
        self.is_pregnant=False
        self.pregnance_counter=0
        if self.childs_members>0:
            self.childs_members-=1
            detreeted=self.chuild_weight
        else:
            self.old_members-=1
            detreeted=self.mouse_weight
            self.childs_age=0
        return detreeted

    #MOUSE food consumption switch
    def food_consume(self, food_availiable):
        corn_consumed=0
        new_family=None
        move_flag=False
        detreeted_=0
        #childs food1
        if self.childs_members==0:
            self.childs_age=0
        food_needed=self.dayly_food_per_mouse*self.old_members+self.childs_members*self.dayly_food_per_child
        if food_availiable>=food_needed:
            corn_consumed=food_needed
            new_family=self.grows()
        elif (food_needed>food_availiable>=food_needed/2):
            corn_consumed=food_availiable
            self.stagnation
        elif (food_needed/4<=food_availiable<=food_needed/2):
            corn_consumed=food_availiable
            detreeted_=self.starwation()
            move_flag=True
        elif food_needed/4>food_availiable:
            corn_consumed=food_availiable
            detreeted=self.starwation()
            self.old_members-=1
            detreeted_+=self.mouse_weight
            move_flag=True
        return (corn_consumed, new_family, move_flag, detreeted_, food_needed)
