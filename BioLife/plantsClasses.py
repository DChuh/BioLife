from BioConstants import *

class Plants(object):
    '''Parent class for all Biological entitys'''
    #monitoring parameters
    is_alive=False
    harvest_ready=False
    weight=0
    age=0
    name="Plants"
    #biological parameters of specie
    birth_weight=0
    max_weight=0
    max_age=0
    reproductive_age=0
    reproductive_cycle=0
    food_cycle=0
    #Iput-output parameters
    is_producer=True

    #resources round trip
    weight_grows_ratio =0
    corn_weight=0
    dayly_minerals_consumption_ratio=0.045

    def __init__(self):
        self.weight=self.birth_weight
        self.is_alive=True
    def season_cycle(self):
        #propagation
        if self.corn_weight>=20000:
            self.harvest['childs']=3
            self.corn_weight-=4500
        elif self.corn_weight>=10000:
            self.harvest['childs']=2
            self.corn_weight-=3000
        elif self.corn_weight>=5000:
            self.harvest['childs']=1
            self.corn_weight-=1500
        else:
            self.harvest['childs']=0
        #corn harwest
        self.harvest['corn']=self.corn_weight
        self.corn_weight=0

        #biomass harvest
        self.harvest['biomass']=self.biomass_weight
        self.biomass_weight=0

        #diying and harvest flag
        self.harvest_ready=True
        self.is_alive=False

        return self.harvest

    def dayly_cicle(self, soil_fertility=0):
        '''1) mineral consumption, water consumption in the future\
           2) biomass production (grass for Barley, wood for trees, etc. returns to redtreet at the end of instance life)
           3) food (corn, storage root) production
           4)
        '''

        if self.age<self.corn_production_start_day:
            self.biomass_weight+=soil_fertility*(self.biomass_productivity/(self.corn_production_start_day))
        elif self.corn_production_start_day<=self.age<self.vegetable_period:
            self.corn_weight+=soil_fertility*(self.corn_productivity/(self.vegetable_period-self.corn_production_start_day))
        elif self.vegetable_period<self.age<self.max_age:
            #post=production
            #self.biomass_weight+=landObject.soil_fertility()*(self.biomass_productivity/(self.corn_production_start_day))
            pass

        #1) 100m2 of barley consume:
        #   100 kg per tonn of corn. 50kg of corn (100m2 product) consume 5kg of minerals per season, o it is 55g per day

        delta_weight=self.biomass_weight+self.corn_weight-self.weight
        self.weight=self.biomass_weight+self.corn_weight
        self.age+=1

        return (self.dayly_minerals_consumption_ratio*delta_weight)

class Barley(Plants):
    '''100 m2 of Barley. Starting from 1500 gramms of corn up to 50000 g/100m2 (5t/ha) of corn, and 250000 g/100m2 of detreet. Once in season
        1 Terrian cell can contain up to it's capacity (100) of Barley items
    season cicle:
    1) cycle starting from 1500g
    2)
    Propagation:
    '''
    birth_weight=1500
    max_weight=5000000+4000000
    max_age=90
    reproductive_cycle=1
    seasons={4, 5, 6, 7, 8}

    food_cycle=1
    #Iput-output parameters
    is_producer=True

    #resources round trip
    weight_grows_ratio =0
    dayly_minerals_consumption_ratio=0.05    #

    biomass_productivity=40*1000  #dry mass
    corn_productivity= 60*1000

    harvest={'corn':0, 'biomass':0, 'childs':0}
    biomass_weight=1500
    corn_weight=0
    vegetable_period=90 #days
    corn_production_start_day=40
    period=365  #once per year
    season_start_day=80  # March, 20

    def __init__(self):
        super().__init__()
