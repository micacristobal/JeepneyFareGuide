mobile app name: jeepney fare guide

tech stack: 
  front end/UI: kivy
  back end: python 
  data storage: javascript(json file)

features:
1. display the fare of the commuters once the buttons for the starting point and ending point were clicked. name those better. for example: when the starting point and the ending point are both clicked, then this is where the fare is displayed.

2. calculate the fare if the payment is for multiple commuters. for example: there are two or many commuters in a single payment, there are 3 commuters in 100 pesos. they could drop off to different destination or places, but they get in at the same time. there should be plus button for the calculation to work.

3. there should be 2 pages in the app. the first page should include the name of the app and there is a button below named start.

logic part of the app or system
1. there are less than 17 places in the route of the jeepney, from 0 km to 10 km. the minimum first four kms is a regular fare which is 13 pesos. in the succeeding kms, there should be additional 1 peso. 

2. discounts for students, seniors, disabled varies per km. in the minimum first four kms, their fare is 11. in the succeeding kms = additional 1 peso.

3. the places are: 

from SM San Mateo(starting point) to San Jose (ending point)

0km- "SM San Mateo" - 13 pesos
1km- "Ampid" - 13 pesos
2km- "Paraiso" - 13 pesos
3km- "Guitnang Bayan" - 13 pesos
4km- "Dulong Bayan", "Patiis" - 13 pesos
5km- "Guinayang" - 14 pesos
6km- "Maly", "Gold River" - 15 pesos
7km- "Inares" - 16 pesos
8km- "Montana" - 17 pesos
9km- "Burgos" - 18 pesos
10km- "Manggahan" - 19 pesos
11km- "Highway" - 20 pesos
12km- "San Jose"  - 22 pesos


then,

from San Jose(starting point) to SM San Mateo (ending point)

0km- "San Jose" - 13 pesos
1km- "Highway" - 13 pesos
2km- "Manggahan" - 13 pesos
3km- "Burgos" - 13 pesos
4km- "Maly", "Guinayang" - 13 pesos
5km- "Malanday" - 14 pesos
6km- "Patiis" - 15 pesos
7km- "Dulong Bayan" - 16 pesos
8km- "Guitnang Bayan" - 17 pesos
9km- "Plaza" - 18 pesos
10km- "Paraiso", "Tulay" - 19 pesos
11km- "Ampid" - 20 pesos
12km- "SM San Mateo"  - 22 pesos

4. once the conductor is done with the fare of the commuter that pays their fare, then there should be a reset button to calculate another fare.

UI of the app
1. the color scheme should be light colors or peach. solid and gradient in a single app.

2. the places are inside the buttons. the buttons are in the shape of square with 25% rounded edges. the color of the buttons are peach with darker peach border 1px. the name of the places are in separate buttons, without the km and its price. the font size in the buttons are semi big and the font is clear to read. the color of teh font for the places are black only, and are in uppercases. 

