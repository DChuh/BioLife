# BioLife
Modeling of Food chain or biological community

This programm is programm modelling of simple biological community.
Food chain have 3 elements -> Barley -> Mouses -> Foxes
Most of the constants and behavior patterns are based on the real life parameters. (wikipwdia, bilogical scince aricles)
Parameters could be changed in the BioConstants.py or in the classes defenition. Plan is to moove all varible parameters to this file.
Simple tkInter graphic is used

Play field consist of 1ha (100 ar) cells.
gameData is counting every day. Starting from 1 jan 2016.
Every playField cell(1ha) can grows up to 100 entries of Barley
Barley fields are displayed as squares. Size of square depends on number of seeded ar's (1/100 ha) of Barley.
Green square - no corn is produced, grass only
Yellow gradiations - depends on growed corn. (coral color - maximum)

Soil have the following parameters: mineralization, humus percentage, detreet percentage.
It is changed during the game: Barley straw, not used corn, animals droppings, dead animals goes to detreet
Part of detreet turns to humus every eaar (initial plan was to programm every bacteria))))
Part of humus turns to water solvable minerals
Minerals are taken to build the plants (Plan is to describe water cycle and devide minerals to: N-P-K)
Every cell is separate object, containing those parameters, plants slots, animals marks and holes, etc.

Barley have seeds. When it is season for barley(frm april til september), seeds start to grows.
The harvest depends on soil parameters. 
Harvested corn is displayed as transparent circle (size-> mass of corn)
Destributing seeds number depends on harves.

Every mouse familiy is separate object
Mouse Families eat barley corn, became pregnant, grows childrens. Grows and deviding. Dying and prenancy abortaion when starwation
