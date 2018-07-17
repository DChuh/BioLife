from plantsClasses import *
from collections import Counter
from datetime import date, timedelta
from BioConstants import *

class TerreneCell(object):
    '''Parent class far all types of terrene  1 ha of ground'''
    class_counter=0
    used_coords={(0,-1),}
    #game parameters  and constants
    capasity=100 # 100 cells of 100m2  (100 ar)
    #all field square = 100000 ha = 1000 km^2  In real life, it is minimal square to support reasonable amount of big animals
    #1 cell - 1 ha. It is easy to calculate production per 1 ha.

    minerals_percent_optimal=0.001
    minerals_percent_critical=0.002
    minerals_persent_maximum= 0.005

    detreet_percent_critical=0.03
    detreet_percent_maximum=0.05

    #cell parameters
    plant_citizens=list()
    mouse_mark=list()
    fox_marks=list()
    fox_hole=None
    #slots=
    nick=""
    x_axis=0
    y_axis=0
    #corn is stored once per year or season
    corn_food_stored=0
    #grass is growwing everyday
    grass_food_stored=0
    #corn is detreated, when year or season resicles. Grass is detreated, accordingly to grass parameter
    food_detreeted=0
    seeds_slots=Counter(Barley=0)
    seeds_slots_max=100
    #groung parameters
    basic_productivity=50000000  # gramms/ha = 50t/ha average biomass parametr
    mineral_percent=0
    detreet_percent=0
    humus_percent=0
    water_percent=0
    ph=7
    # detreet gumification  coeficient - 0.15-0.25  should be a function from bacteries, mushrums and detretofags< like worms
    # may by hardcoded as 0.2 of present detreet
    detreet_humification=0.15

    # detreet input should be a function of summ all dead biological items and all food waste
    # e.g.  - forest  -about 30 t/ha

    # humus:  low - 1-2%, typical: 3-5, high:5-10
    # humus mineralization -  1.5 %/ per year    ~ 1t/ha
    humus_mineralization_ratio=0.005

    # productivity should be about 30t/ha for forest, down to 3t/ga savanna
    #

    #concepts
    # environment_types={'air', 'water', 'ground'}
    #   types={'rock', 'hill','humus', 'lake','forest', 'desert', 'ice'}
    #  food_types={'vegetable', 'fruit', 'corn', 'meet', 'organic', 'plancton', 'fish', 'carrion'}
    # climat_types={'cold','moderate' , 'hot' }

    def __init__(self, xaxis=0, yaxis=0 ):
        if ((xaxis,yaxis)not in TerreneCell.used_coords):
            TerreneCell.class_counter+=1
            self.x_axis=xaxis
            self.y_axis=yaxis
            self.mouse_mark=list()
            self.fox_marks=list()
            self.plant_citizens=list()


            TerreneCell.used_coords=TerreneCell.used_coords & set((xaxis,yaxis),)
        else:
            print("incorrect coordinats")

    def minerals_coeficient(self):
        if (0<=self.mineral_percent<self.minerals_percent_optimal):
            #print("low")
            return (self.mineral_percent/self.minerals_percent_optimal)

        elif(self.minerals_percent_optimal<=self.mineral_percent<self.minerals_percent_critical):
            #print("optimal")
            return 1
        elif (self.minerals_percent_critical<=self.mineral_percent<self.minerals_persent_maximum):
            return ((self.minerals_persent_maximum-self.mineral_percent)/(self.minerals_persent_maximum-self.minerals_percent_critical))

        elif(self.mineral_percent>self.minerals_persent_maximum):
            print("critical")
            return 0


    def detreet_coeficient(self):
        if (self.detreet_percent<self.detreet_percent_critical):
            return 1
        elif (self.detreet_percent_critical<self.detreet_percent<self.detreet_percent_maximum):
            return ((self.detreet_percent_maximum-self.detreet_percent)/(self.detreet_percent_maximum-self.detreet_percent_critical))
        elif (self.detreet_percent>self.detreet_percent_maximum):
            print("detreet percent is overheaded, soil_fertility =0")
            return 0
    # producing per 100 m2

    #0.2 of fertility, when no  any humus, and up to 1, when 10% of humus
    def humus_coeficient(self):
        return (0.2+8*self.humus_percent)


    def soil_fertility(self):
        return (self.basic_productivity*(self.humus_coeficient())*self.detreet_coeficient()*self.minerals_coeficient())

    def get_citizen(self, number=0):
        if number<len(self.plant_citizens):
            try:
                citizen_=self.plant_citizens[number]
            except:
                citizen_= Plants()
            return citizen_
        else:
            return None
    def add_citizen(self, some_plant="some_plant"):
        if len(self.plant_citizens)<self.capasity:
            self.plant_citizens.append(some_plant)
            return 1
        else:
            return 0

    def seeds_destribution(self):
        pass


    def year_cycle(self):
        #detreetong grass:
        self.detreet_percent+=(self.grass_food_stored)/mass_of_soil  #+self.corn_food_stored/2
        self.grass_food_stored=0
        #self.corn_food_stored=self.corn_food_stored/2

        #detreet humification
        self.humus_percent+=self.detreet_percent*self.detreet_humification
        self.detreet_percent-=self.detreet_percent*self.detreet_humification*2 # x2 detreet lost in humification

        #humus mineralization
        self.mineral_percent+=self.humus_percent*self.humus_mineralization_ratio
        self.humus_percent-=self.humus_percent*self.humus_mineralization_ratio*10 # 90%lost in mineralization

    def spring_detreeting(self):
        self.detreet_percent+=(self.corn_food_stored/2)/mass_of_soil
        self.corn_food_stored=int(self.corn_food_stored/2)

    #dayly grows all citizens and minerals consumption cycle triggering harvest and dying and cleanup cycle
    def dayly_cycle(self):
        for i in range(len(self.plant_citizens)):
            minerals_consumption=self.plant_citizens[i].dayly_cicle(self.soil_fertility())
            self.mineral_percent-=(self.soil_fertility()*minerals_consumption/mass_of_soil)   #2000000000 - mass of 1 ha 20 cm depth
            if self.plant_citizens[i].age>=self.plant_citizens[i].max_age:
                self.plant_citizens[i].season_cycle()


        #check for harvested plants, replace dead with Nones
        for i in range(len(self.plant_citizens)):
            if self.plant_citizens[i].harvest_ready:
                self.corn_food_stored+=self.plant_citizens[i].harvest["corn"]
                self.grass_food_stored+=self.plant_citizens[i].harvest["biomass"]
                seeds=Counter(Barley=self.plant_citizens[i].harvest["childs"])
                if self.seeds_slots["Barley"]<self.seeds_slots_max:
                    self.seeds_slots+=seeds
                else:
                    self.corn_food_stored+=seeds['Barley']*1500
            #replacing dead enties with None's
            if not(self.plant_citizens[i].is_alive):
                self.plant_citizens[i]=None

        #cleanup None plants
        while (None in self.plant_citizens):
            for i in range(len(self.plant_citizens)):
                if (self.plant_citizens[i]==None):
                    del self.plant_citizens[i]
                    break

class BlackEarth(TerreneCell):
    '''Parent class for black soil'''
    #game parameters
    #groung parameters
    plant_citizens=list()
    basic_productivity=2
    mineral_percent=MINERALS #0.0008  #0.2 m * 10000 m2 * min_percent* density (now=1) = 2 tonn per ha
    detreet_percent=0.0004
    humus_percent=HUMUS #0.01
    water_percent=0.05

    def __init__(self, x_axis=0, y_axis=0):
        super().__init__(x_axis, y_axis)
        self.seeds_slots=Counter(Barley=0)
        self.corn_food_stored=0

#playField initialization==========================================================================

playField=[[BlackEarth(x, y) for y in range(playFileld_y_size)] for x in range(playFileld_x_size)]