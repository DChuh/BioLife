from datetime import date, timedelta
#start from
year=2016 # 4 seasons, 365 days
day=1  #
month=1 # 91 day
gameDate=date(year, month, day)

#setup playField
playFileld_x_size=65
playFileld_y_size=40
map_ratio=20

# soil parameters. fine tune for qualified agronoms Minerals optimal - 0.001-0.002)
MINERALS=0.00063
HUMUS=0.01
mass_of_soil=2000000000#2000000000 - mass of 1 ha 20 cm depth

#mouses parameters
mouse_seek_radius=10
mouse_move_radius=1
mouse_rush=3
allMouses=list()
#corn could be eaten per day of availiable on the cell
food_consumption_coeficient=1/100

directions_1_step=[(-1, -1), (-1, 0),(-1, 1), (0, -1), (0, 1),(1, -1), (1, 0),(1, 1)]

#fox Parameters
fox_seek_radius=14
fox_rush=18
fox_colors_D=["Orange","Orange1","Orange2","Orange3","Orange4",
            "dark orange","DarkOrange1","DarkOrange2","DarkOrange3","DarkOrange4",
            "LightGoldenrod2", "AntiqueWhite1","white"]

fox_colors_r=["dim gray", "gray38", "wheat4", "gray30","black" ]


allFoxes=list()

fox_marks_duration=timedelta(days=15)
re_usage_period=timedelta(days=5)
hole_re_usage_period=timedelta(days=14)



class FoxHole(object):
    '''Fox Hole appears first, when fox  '''
    size=0
    foundator=None
    in_use=False
    users=()
    active=False
    foundation_date=gameDate
    not_used_counter=0
    max_not_used_counter=300
    couple_use=False

    def __init__(self, size=1, fox_id=None):
        self.in_use=True
        self.couple_use=False
        self.size=size
        self.foundator=fox_id
        #self.user=fox_id
        self.foundation_date=gameDate
        self.not_used_counter=0

    def reset_counter(self):
        self.not_used_counter=0
    def inc_counter(self):
        self.not_used_counter+=1

    def reset_in_use(self):
        self.in_use=False
        self.couple_use=False

    def add_user(self, id=None):
        self.users.append(id)

    def clear_users(self):
        self.users.clear()











