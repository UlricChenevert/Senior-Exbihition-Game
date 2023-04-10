'''
This is the main file for my senior exhibition gamma food insecurity game

Farming simulator with nutrition and poundage outputs
'''
#Imports outside functions
import pygame as pg, random

#Imports local functions
#There is none lol
pg.init()

'''Setting up the display'''
width = 1400
height = 800
screen = pg.display.set_mode((width, height), 0, 32)
pg.display.set_caption("Gamma: Urban Agriculture")
clock = pg.time.Clock()

'''==================================================Colors=================================================='''
#General
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

#UI Colors
slotColor = (100, 100, 100)
nextWeekButtonColor = (198, 45, 22)

#Row Specific Colors
rowColor = (107, 62, 12)
tillColor = (64, 35, 3)
gravelColor = (168, 168, 168)
signColor = (115, 73, 32)
seedColor = (207, 168, 78)
fertilizeColor = (69, 40, 8)

#Vegetable Colors
carrotColor = (217, 117, 17)
tomatoColor = (198, 45, 22)
bellpepperColor = (207, 97, 12)
potatoColor = (150, 96, 14)
cornColor = (214, 165, 17)
onionColor = (207, 200, 180)
broccoliColor = (4, 64, 5)
eggplantColor = (69, 16, 82)
vineColor = (8, 128, 10)

#Staging Colors 
growingStageColor = (12, 71, 20)
readyToHarvestColor = (12, 71, 40)

"""================================================================================MAIN BODY OF CODE================================================================================"""

#Intellectually the rows are a space of 6 ft x 36 ft

#row[0] is coords, row[1] is number of clicks, row[2] is weeks growing, row[3] is which plant
rows = [[(), 0, 0, "Vegetable", [False, False, False, False, False], 0], [(), 0, 0, "Vegetable", [False, False, False, False, False], 0], [(), 0, 0, "Vegetable", [False, False, False, False, False], 0], [(), 0, 0, "Vegetable", [False, False, False, False, False], 0], [(), 0, 0, "Vegetable", [False, False, False, False, False], 0], [(), 0, 0, "Vegetable", [False, False, False, False, False], 0], [(), 0, 0, "Vegetable", [False, False, False, False, False], 0]]

#row[0] is coords, row[1] stored if clicked,
slots = [[(), False, "Tomato"], [(), False, "Bellpepper"], [(), False, "Potato"], [(), False, "Carrot"], [(), False, "Onion"], [(), False, "Corn"], [(), False, "Broccoli"], [(), False, "Eggplant"]]

#Signs 
sign = ["Vegetable", "Vegetable", "Vegetable", "Vegetable",  "Vegetable",   "Vegetable",  "Vegetable",  "Vegetable"]

#In-the-background variables
mouseClicksCount = 0
week = 0
selectedVegetable = "Vegetable"

#Total scores
totalCalories = 0
totalWieght = 0
totalCarbs = 0
totalProtein = 0
totalFat = 0

#In-the-background constants
NUMBER_OF_PLANTS_PER_ROW = 12
TIME_TO_END = 26
ROW_HEIGHT = 745

#Staging constants
FERTILIZE_STAGE = 12
TILL_STAGE = 13
IRRIGATE_STAGE = 14
SEEDING_STAGE_LOWER_LIMIT = 15
HARVEST_STAGE_LOWER_LIMIT = 28
TIME_TO_HARVEST = 13

running = True

'''General Functions'''
class Button:
    def __init__(self, buttonPositionTopLeft, screen, text, textSize, hitboxTopLeft, hitboxLength, hitboxHitWidth, showHitBox = False, showBackground = False, backgroundColor = white):
        '''Display Variables'''
        self.screen = screen
        self.buttonPositionTopLeft = buttonPositionTopLeft
        
        '''Places Text in the Rectangle'''
        self.text = text
        self.textSize = textSize
        self.font = pg.font.Font('freesansbold.ttf', self.textSize)

        if showBackground:
            pg.draw.rect(screen, backgroundColor, pg.Rect(hitboxTopLeft[0], hitboxTopLeft[1], hitboxLength, hitboxHitWidth), 0)
        
        self.img = self.font.render(self.text, True, black)

        ''''Draws the Rectangle'''
        #buttonRect in form (x, y, width, height)
        self.buttonRect = self.img.get_rect()
        self.screen.blit(self.img, self.buttonPositionTopLeft)

        '''Sizes'''
        #Sizes are ints
        self.buttonWidth = self.buttonRect[2]
        self.buttonHeight = self.buttonRect[3]
        #print (self.buttonWidth)

        '''Positions'''
        #Positions will be in forms of (x,y)
        #Top Left aready known
        self.hitboxTopLeft = hitboxTopLeft
        self.hitboxLength = hitboxLength
        self.hitboxHitWidth = hitboxHitWidth

        if showHitBox:
            pg.draw.rect(screen, red, pg.Rect(hitboxTopLeft[0], hitboxTopLeft[1], hitboxLength, hitboxHitWidth), 1)

    def getButtonTopLeft (self):
        return self.buttonPositionTopLeft

    def isMouseInPositionInButton(self):
        return isMouseInPositionOverButton(self.hitboxTopLeft, self.buttonWidth, self.buttonHeight)

def isMouseInPositionOverButton(buttonPositionTopLeft, width, height):
        #Get postion of bottom-right limits in (x, y) format
        buttonPositionBottomRight  = (buttonPositionTopLeft[0] + width, buttonPositionTopLeft[1] + height)
        
        #Gets x, y cords of mouse
        mouseX = pg.mouse.get_pos()[0]
        mouseY = pg.mouse.get_pos()[1]
        
        #if mouse is outside X-coords
        if mouseX > buttonPositionBottomRight[0] or mouseX < buttonPositionTopLeft[0]:
            return False

        #if mouse is outside Y-coords
        if mouseY > buttonPositionBottomRight[1] or mouseY < buttonPositionTopLeft[1]:
            return False

        #print ("Mouse over button!")
        return True

def drawText (screen, topLeftPosition, text, textSize, drawRect = False, showInfo = False):

    font = pg.font.Font('freesansbold.ttf', int(textSize))
    img = font.render(text, True, black)
    textRectangle = img.get_rect()

    if showInfo:
        print (textRectangle)

    if drawRect:
        pg.draw.rect(screen, white, textRectangle)

    screen.blit(img, topLeftPosition)

def readableText(rawText, convertgTokg=False):

    if convertgTokg:
        rawText = int(rawText / 1000)
    
    #splits up the list
    textList = list(str(rawText))

    #Goes from the back of the number to front, adding a comma every 3rd place
    for characterIndex in range(len(textList)-3, 0, -3):
        textList.insert(characterIndex, ',')

    finalText = ""

    #joins the list back together again
    for character in textList:
        finalText = finalText + character

    return finalText

def closeWindow():
    global running

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            quit()

'''-----------------------------------Graphics-----------------------------------'''

def createRows ():
    rowWidth = int((width-420)/len(rows))

    for rowIteration in range(len(rows)):
        #Crop Row
        coordsOfRow = (int(rowWidth*rowIteration) + 20, 20)
        # dimensionsOfRow is width is 120 and height is 760

        pg.draw.rect(screen, rowColor, pg.Rect(coordsOfRow[0], coordsOfRow[1], 120, 765), 0)

        rows[rowIteration][0] = coordsOfRow

def returnRowNumber ():
    mousePosititon = pg.mouse.get_pos()
    print (mousePosititon)
    #if mouse is in a row and check all rows
    for rowIteration in range(len(rows)):
        # dimensionsOfRow is width is 120 and height is 960

        #if mousePosititon is less than the left-most value of the row or row is greater than the right-most value of the row
        if mousePosititon[0] < rows[rowIteration][0][0] or mousePosititon[0] > rows[rowIteration][0][0] + 120:
            continue
        
        #if mousePosititon is less than the top-most value of the row or row is greater than the bottom-most value of the row
        if mousePosititon[1] < rows[rowIteration][0][1] or mousePosititon[1] > rows[rowIteration][0][1] + 980:
            continue

        return rowIteration
    
    #if the player clicked on none of the rows
    return -1

def createSigns ():
    for row in range(len(rows)):
        # dimensionsOfRow is width is 120 and height is 760
        #Sign 
        pg.draw.rect(screen, signColor, pg.Rect(rows[row][0][0] + 20, 680, 80, 60), 0)
        pg.draw.rect(screen, signColor, pg.Rect(rows[row][0][0] + 55, 740, 10, 40), 0)

        if rows[row][3] != "Vegetable":
            drawPlantsSwitch(rows[row][3], row) 

def createSlots ():
    NUMBER_OF_SLOTS = 8

    #slots are 50 by 50 squares
    #slots are under the vegetable options heading (x: 1000 - 1400, y: 0-40)

    for slot in range(NUMBER_OF_SLOTS):
        #Stores position data
        topLeftPosition = (slot*50 + 1000, 40)
        slots[slot][0] = topLeftPosition

        pg.draw.rect(screen, slotColor, pg.Rect(topLeftPosition[0], topLeftPosition[1], 50, 50), 5)

def startup():
    global nextWeekButton, week, selectedVegetable, totalCalories, totalWieght, totalCarbs, totalProtein, totalFat, rows

    #resets variables
    week = 0
    selectedVegetable = "Vegetable"
    totalCalories = 0
    totalWieght = 0
    totalCarbs = 0
    totalProtein = 0
    totalFat = 0

    rows = [[(), 0, 0, "Vegetable", [False, False, False, False, False], 0], [(), 0, 0, "Vegetable", [False, False, False, False, False], 0], [(), 0, 0, "Vegetable", [False, False, False, False, False], 0], [(), 0, 0, "Vegetable", [False, False, False, False, False], 0], [(), 0, 0, "Vegetable", [False, False, False, False, False], 0], [(), 0, 0, "Vegetable", [False, False, False, False, False], 0], [(), 0, 0, "Vegetable", [False, False, False, False, False], 0]]

    #Creates the background
    screen.fill(gravelColor)
    createRows()
    createSlots ()
    drawTomato((1025, 65))
    drawBellPepper((1060, 45))
    drawPotato((1112, 45))
    drawCarrot ((1152, 35))
    drawOnion((1225, 65))
    drawCorn((1265, 45))
    drawBroccoli((1300, 45))
    drawEggplant((1373, 60))

    #Draws UI
    drawText(screen, (1000, 0), "Vegetable Options", 40)
    drawSelectedVegetableOptions()
    drawTotalImpact()

    nextWeekButtonCoords = (1100, 735)
    nextWeekButton = Button(nextWeekButtonCoords, screen, "Next Week", 40, (nextWeekButtonCoords[0] - 5, nextWeekButtonCoords[1] - 5), 215, 50, showBackground = True, backgroundColor = nextWeekButtonColor)
    drawText (screen, (1045, 690), "Season End: " + str(TIME_TO_END - week) + " weeks", 30) #screen, topLeftPosition, text, textSize

def endScreen():
    global running

    screen.fill(gravelColor)
    drawText(screen, (400, 200), "Thank You for Playing!", 60)
    playAgainButton = Button((500, 350), screen, "Play Again", 30, (495, 345), 170, 40, showBackground = True, backgroundColor = white)
    quitButton = Button((850, 350), screen, "Quit", 30, (845, 345), 75, 40, showBackground = True, backgroundColor = white)

    if pg.mouse.get_pressed(3)[0] and playAgainButton.isMouseInPositionInButton():
        startup()

    if pg.mouse.get_pressed(3)[0] and quitButton.isMouseInPositionInButton():
        running = False
        quit()

def updateSlots(slot, color):
    pg.draw.rect(screen, color, pg.Rect(slot[0][0], slot[0][1], 50, 50), 5)

def clearRow(clickedOnRow):

    currentRow = rows[clickedOnRow]

    isSpecial = vegetableInfoDictionary[currentRow[3]][9]

    #colors over the plants
    readyToHarvest(currentRow, gravelColor, True)

    pg.draw.rect(screen, gravelColor, pg.Rect(currentRow[0][0],  currentRow[0][1] - 10, 120, 10), 0)

    #creates a new row
    pg.draw.rect(screen, rowColor, pg.Rect(currentRow[0][0],  currentRow[0][1], 120, 765), 0)
    
    #Fixes the other rows 
    #If older or equal to 10 then re-draw plant
    #Row to the left
    try:
        rowToTheLeft = rows[clickedOnRow - 1]
        if rowToTheLeft[2] >= 10 and rowToTheLeft[2] < 13 and not isSpecial:
            bushyPlantGrowth(rowToTheLeft)

        elif rowToTheLeft[2] >= 10 and rowToTheLeft[2] < 13 and isSpecial:
            stalkyPlantGrowth(rowToTheLeft)
        
        elif rowToTheLeft[2] >= 13:
           readyToHarvest(rowToTheLeft)
    except:
        print ("Error on left side")

    try:
        rowToTheRight = rows[clickedOnRow + 1]
        if rowToTheRight[2] >= 10 and rowToTheRight[2] < 13 and not isSpecial:
            bushyPlantGrowth(rowToTheRight)

        elif rowToTheRight[2] >= 10 and rowToTheRight[2] < 13 and isSpecial:
            stalkyPlantGrowth(rowToTheRight)
        
        elif rowToTheLeft[2] >= 13:
           readyToHarvest(rowToTheRight)
    except:
        print ("Error on right side")

    #Resets the week counter, the click amount, and the selected vegetable
    currentRow[1] = 0
    currentRow[2] = 0
    currentRow[3] = "Vegetable"
    currentRow[4] = [False, False, False, False, False]

def fertilize(clickedRow, fertilizeIteration):
    
    pg.draw.rect(screen, fertilizeColor, pg.Rect(rows[clickedRow][0][0], rows[clickedRow][0][1]+ fertilizeIteration * 62, 120, 83), 0)

    if rows[clickedRow][1] == FERTILIZE_STAGE:
        rows[clickedRow][4] = [True, False, False, False, False]

def till(clickedRow):
    #Draw tilled lines
    pg.draw.rect(screen, tillColor, pg.Rect(rows[clickedRow][0][0] + 31, rows[clickedRow][0][1] + 10, 5, 740), 0)
    pg.draw.rect(screen, tillColor, pg.Rect(rows[clickedRow][0][0] + 82, rows[clickedRow][0][1] + 10, 5, 740), 0)

    if rows[clickedRow][1] == TILL_STAGE:
        rows[clickedRow][4] = [True, True, False, False, False]

def irrigate (clickedRow):
    pg.draw.rect(screen, black, pg.Rect(rows[clickedRow][0][0] + 58, rows[clickedRow][0][1] + 10, 5, 740), 0)

    if rows[clickedRow][1] == IRRIGATE_STAGE:
        rows[clickedRow][4] = [True, True, True, False, False]

def seed(clickedRow, selectedVegetable, seedIteration = 1):
    currentRow = rows[clickedRow]

    numberOfSeeds = vegetableInfoDictionary[selectedVegetable][7]
    spacing = ROW_HEIGHT / numberOfSeeds

    #The number of clicks it takes to grow the vegetable
    seedingStageUpperLimit = numberOfSeeds + SEEDING_STAGE_LOWER_LIMIT
    
    seedPlacementY = int(currentRow[0][1] + seedIteration * spacing + 10) #The row starts at y: 20 and ends at 785 #convert to int to undershoot the placement

    #Draw two seeds
    pg.draw.rect(screen, seedColor, pg.Rect(currentRow[0][0] + 31, seedPlacementY, 5, 5), 0)
    pg.draw.rect(screen, seedColor, pg.Rect(currentRow[0][0] + 82, seedPlacementY, 5, 5), 0)

    if  currentRow[1] == seedingStageUpperLimit:

        currentRow[4] = [True, True, True, True, False]
        #Adds seed stage info to row data (0 means seedling)
        currentRow[2] = 1

def sprout(row):

    vegetable = row[3]
    numberOfPlantsPerRow = vegetableInfoDictionary[vegetable][7]
    spacing = (ROW_HEIGHT) / numberOfPlantsPerRow

    for plant in range(numberOfPlantsPerRow):

        seedPlacementY = int(row[0][1] + plant * spacing + 10) #The row starts at y: 20 and ends at 765

        pg.draw.rect(screen, growingStageColor, pg.Rect(row[0][0] + 31, seedPlacementY, 5, 5), 0)
        pg.draw.rect(screen, growingStageColor, pg.Rect(row[0][0] + 82, seedPlacementY, 5, 5), 0)
    
def bushyPlantGrowth(row):
    week = row[2]

    numberOfWeeksOfGrowth = vegetableInfoDictionary[row[3]][6]

    numberOfPlantsPerRow = vegetableInfoDictionary[row[3]][7]
    spacing = ROW_HEIGHT / numberOfPlantsPerRow

    #print(numberOfWeeksOfGrowth)

    growthRate = 50/numberOfWeeksOfGrowth

    for plant in range(numberOfPlantsPerRow):

        seedPlacementY = int(row[0][1] + plant * spacing + 10) #The row starts at y: 20 and ends at 765

        #Max is 50 radius min is 5
        pg.draw.circle(screen, growingStageColor, (row[0][0] + 33, seedPlacementY), round(growthRate*(week-1)))
        pg.draw.circle(screen, growingStageColor, (row[0][0] + 84, seedPlacementY), round(growthRate*(week-1)))

def stalkyPlantGrowth(row, color = growingStageColor):
    week = row[2]
    vegetable = row[3]
    numberOfWeeksOfGrowth = vegetableInfoDictionary[vegetable][6]
    numberOfPlantsPerRow = vegetableInfoDictionary[vegetable][7]

    spacing = ROW_HEIGHT / numberOfPlantsPerRow


    if vegetable == "Onion":

        growthRate = 12/numberOfWeeksOfGrowth

        for plant in range(numberOfPlantsPerRow):

            seedPlacementY = int(row[0][1] + plant * spacing + 10) #The row starts at y: 20 and ends at 765

            #Max is 50 radius min is 5
            pg.draw.circle(screen, color, (row[0][0] + 33, seedPlacementY), round(growthRate*(week-1)))
            pg.draw.circle(screen, color, (row[0][0] + 84, seedPlacementY), round(growthRate*(week-1)))

            #print (round(growthRate*(week-1)))

    elif vegetable == "Corn":

        growthRate = 36/numberOfWeeksOfGrowth

        for plant in range(numberOfPlantsPerRow):

            seedPlacementY = int(row[0][1] + plant * spacing - 5) #The row starts at y: 20 and ends at 765
            
            pg.draw.ellipse(screen, color, [row[0][0] + 33 - round(growthRate*(week-1) * 1/2), seedPlacementY, round(growthRate*(week-1)), (growthRate*(week-1) * 3/4)])
            pg.draw.ellipse(screen, color, [row[0][0] + 84 - round(growthRate*(week-1) * 1/2), seedPlacementY, round(growthRate*(week-1)), (growthRate*(week-1) * 3/4)])

            '''
            #Max is 50 radius min is 5
            pg.draw.circle(screen, color, (row[0][0] + 33, seedPlacementY), round(growthRate*(week-1)))
            pg.draw.circle(screen, color, (row[0][0] + 84, seedPlacementY), round(growthRate*(week-1)))
            
            '''
            
def readyToHarvest(row, bushColor = readyToHarvestColor, clear = False):

    plantInfo = vegetableInfoDictionary[row[3]]
    numberOfPlantsPerRow = plantInfo[7]
    
    spacing = (ROW_HEIGHT) / numberOfPlantsPerRow

    producesFruit = plantInfo[8]
    isSpecial = plantInfo[9]
    vegetable = row[3]

    if producesFruit:
        
        fruitColor = plantInfo[10]

        #Draws a layer of "plant"
        for plant in range(numberOfPlantsPerRow):

            plantPlacementY = int(row[0][1] + plant * spacing + 10) #The row starts at y: 20 and ends at 765

            #Max is 50 radius min is 5
            pg.draw.circle(screen, bushColor, (row[0][0] + 33, plantPlacementY), 52)
            pg.draw.circle(screen, bushColor, (row[0][0] + 84, plantPlacementY), 52)

        #Then Draws a layer of "Fruit"

        for plant in range(numberOfPlantsPerRow):

            if clear:
                break

            plantPlacementY = int(row[0][1] + plant * spacing + 10) #The row starts at y: 20 and ends at 765
            numberOfFruitInSection = random.randint(1, 3)

            distanceBetweenFruits = int(120/numberOfFruitInSection)

            for fruit in range(numberOfFruitInSection):

                fruitPlacementX = row[0][0] + random.randint(distanceBetweenFruits * fruit, distanceBetweenFruits * (fruit + 1))

                pg.draw.circle(screen, fruitColor, (fruitPlacementX, plantPlacementY), 8)

    elif isSpecial:
        
        for plant in range(numberOfPlantsPerRow):

            plantPlacementY = int(row[0][1] + plant * spacing + 10) #The row starts at y: 20 and ends at 765

            if vegetable == "Onion":

                stalkyPlantGrowth(row, readyToHarvestColor)

            elif vegetable == "Corn":
                print (plantPlacementY)

                stalkyPlantGrowth(row, readyToHarvestColor)

                for plant in range(numberOfPlantsPerRow):

                    plantPlacementY = int(row[0][1] + plant * spacing + 10) #The row starts at y: 20 and ends at 765

                    pg.draw.circle(screen, cornColor, (row[0][0] + 33, plantPlacementY), 7)
                    pg.draw.circle(screen, cornColor, (row[0][0] + 84, plantPlacementY), 7)

    else: #Bush

        for plant in range(numberOfPlantsPerRow):

            plantPlacementY = int(row[0][1] + plant * spacing + 10) #The row starts at y: 20 and ends at 765

            #Max is 50 radius min is 5
            pg.draw.circle(screen, bushColor, (row[0][0] + 33, plantPlacementY), 53)
            pg.draw.circle(screen, bushColor, (row[0][0] + 84, plantPlacementY), 53)

def drawTomato (center):

    pg.draw.rect(screen, vineColor, pg.Rect(center[0] - 3, center[1]- 15, 6, 20), 0)
    pg.draw.circle(screen, tomatoColor, center, 10, 0)

def drawBellPepper (topLeft):

    pg.draw.rect(screen, vineColor, pg.Rect(topLeft[0] + 12, topLeft[1], 5, 10), 0)
    pg.draw.rect(screen, bellpepperColor, pg.Rect(topLeft[0], topLeft[1] + 10, 10, 30), 0, border_radius=4)
    pg.draw.rect(screen, bellpepperColor, pg.Rect(topLeft[0] + 10, topLeft[1] + 10, 10, 30), 0, border_radius=4)
    pg.draw.rect(screen, bellpepperColor, pg.Rect(topLeft[0] + 20, topLeft[1] + 10, 10, 30), 0, border_radius=4)

def drawPotato (topLeft):

    pg.draw.rect(screen, potatoColor, pg.Rect(topLeft[0], topLeft[1], 25, 40), 0, border_radius=13)

def drawCarrot(topLeft):
    pg.draw.polygon(screen, vineColor, [(topLeft[0] + 15, topLeft[1] + 10), (topLeft[0] + 30, topLeft[1] + 10), (topLeft[0] + 25, topLeft[1] + 30)])
    pg.draw.polygon(screen, carrotColor, [(topLeft[0] + 10, topLeft[1] + 20), (topLeft[0] + 35, topLeft[1] + 20), (topLeft[0] + 23, topLeft[1] + 50)])

def drawCorn (topLeft):
    pg.draw.rect(screen, cornColor, pg.Rect(topLeft[0], topLeft[1], 20, 40), 0, border_radius=13)
    
    pg.draw.polygon(screen, vineColor, [(topLeft[0] - 5, topLeft[1] + 15), (topLeft[0] - 5, topLeft[1] + 40), (topLeft[0] + 12, topLeft[1] + 40)])
    pg.draw.polygon(screen, vineColor, [(topLeft[0] + 25, topLeft[1] + 15), (topLeft[0] + 25, topLeft[1] + 40), (topLeft[0] + 8, topLeft[1] + 40)])

def drawOnion (center):

    pg.draw.circle(screen, onionColor, center, 10, 0)
    pg.draw.polygon(screen, onionColor, [(center[0] - 9, center[1]), (center[0] + 8, center[1]), (center[0], center[1] - 17)])
    #pg.draw.polygon(screen, onionColor, [(center[0] - 8, center[1]), (center[0] + 8, center[1]), (center[0] - 5, center[1] - 15)])

def drawBroccoli(topLeft):
    pg.draw.rect(screen, vineColor, [topLeft[0] + 20, topLeft[1] + 20, 10, 15])
    pg.draw.rect(screen, broccoliColor, [topLeft[0] + 10, topLeft[1] + 10, 30, 15], border_radius=10)

def drawEggplant(center):

    pg.draw.rect(screen, broccoliColor, [center[0] - 3, center[1] - 13, 5, 10])
    pg.draw.circle(screen, eggplantColor, (center[0], center[1] + 10), 12, 0)
    pg.draw.circle(screen, eggplantColor, center, 9, 0)

def drawPlantsSwitch (plant, clickedRow):
    
    if plant == "Tomato":
        drawTomato((rows[clickedRow][0][0] + 60, rows[clickedRow][0][1] + 690))
    elif plant == "Bellpepper":
        drawBellPepper((rows[clickedRow][0][0] + 40, rows[clickedRow][0][1] + 670))
    elif plant == "Potato":
        drawPotato((rows[clickedRow][0][0] + 47, rows[clickedRow][0][1] + 670))
    elif plant == "Carrot":
        drawCarrot((rows[clickedRow][0][0] + 35, rows[clickedRow][0][1] + 660))
    elif plant == "Corn":
        drawCorn((rows[clickedRow][0][0] + 50, rows[clickedRow][0][1] + 670))
    elif plant == "Onion":
        drawOnion((rows[clickedRow][0][0] + 60, rows[clickedRow][0][1] + 690))
    elif plant == "Broccoli":
        drawBroccoli((rows[clickedRow][0][0] + 38, rows[clickedRow][0][1] + 665))
    elif plant == "Eggplant":
        drawEggplant((rows[clickedRow][0][0] + 59, rows[clickedRow][0][1] + 682))
    else: 
        print ("Error!")

#Ordered: quanitity per plant, wieght per item (grams), carbs per item (grams), protein per item(grams), fat per item(grams), calories per item
#weeks until grown, seeds per row, is it a fruit plant, is it a special plant?
vegetableInfoDictionary = {
"Vegetable": [0, 0, 0, 0, 0, 0, 0, 0, False, False, growingStageColor], "Bellpepper":  [7, 400, 24, 4, 1.2, 124, 13, 24, True, False, bellpepperColor], "Tomato" : [16, 900, 35.1, 8.1, 1.8, 162, 10, 24, True, False, tomatoColor], 
"Potato" : [6, 200, 40.1, 3.8, 0.2, 174, 13, 36, False, False, potatoColor], "Carrot" : [1, 61, 5.856, 0.549, 0.122, 25, 10, 100, False, False, carrotColor], "Onion" : [1, 110, 10, 1.2, 0.1, 44, 14, 36, False, True, onionColor], 
"Corn" : [4, 90, 17, 2.9, 1.1, 77, 10, 54, False, True, cornColor], "Broccoli" : [3, 221, 15.47, 6.19, 0.884, 75.14, 10, 12, False, False, broccoliColor], "Eggplant" : [5, 548, 32, 5, 1, 136, 10, 54, True, False, eggplantColor]
}

def drawSelectedVegetableOptions(vegetable = "Vegetable"):

    #print (vegetable)

    nutritionalFacts = vegetableInfoDictionary[vegetable]
    #Draws title
    drawText(screen, (1000, 100), vegetable + " Nutrients", 35)
    
    #First Row of Info
    drawText(screen, (1000, 140), "Calories: " + str(round(nutritionalFacts[5], 1)), 20) 
    drawText(screen, (1150, 140), "Weight: " + str(round(nutritionalFacts[1], 1)) + "g", 20)

    #Second Row of Info
    drawText(screen, (1000, 170), "Carbs: " + str(round(nutritionalFacts[2], 1)) + "g" , 20)
    drawText(screen, (1150, 170), "Protein: " + str(round(nutritionalFacts[3], 1)) + "g", 20)
    drawText(screen, (1300, 170), "Fat: " + str(round(nutritionalFacts[4], 1)) + "g", 20)

def drawTotalImpact(vegetable = "Vegetable"):
    global totalCalories, totalWieght, totalCarbs, totalProtein, totalFat

    nutritionalFacts = vegetableInfoDictionary[vegetable]
    
    totalCalories = totalCalories + nutritionalFacts[5] * NUMBER_OF_PLANTS_PER_ROW
    totalWieght = totalWieght + nutritionalFacts[1] * NUMBER_OF_PLANTS_PER_ROW
    totalCarbs = totalCarbs + nutritionalFacts[2] * NUMBER_OF_PLANTS_PER_ROW
    totalProtein = totalProtein + nutritionalFacts[3] * NUMBER_OF_PLANTS_PER_ROW
    totalFat = totalFat + nutritionalFacts[4]* NUMBER_OF_PLANTS_PER_ROW
    
    
    displayTotalCalories = readableText(int(totalCalories))

    if len(str(int(totalWieght))) > 3:
        displayTotalWieght = readableText(int(totalWieght), True) + "kg"
    else:
        displayTotalWieght = readableText(int(totalWieght)) + "g"

    if len(str(int(totalCarbs))) > 3:
        displayTotalCarbs = readableText(int(totalCarbs), True) + "kg"
    else:
        displayTotalCarbs = readableText(int(totalCarbs)) + "g"

    if len(str(int(totalProtein))) > 3:
        displayTotalProtein = readableText(int(totalProtein), True) + "kg"
    else:
        displayTotalProtein = readableText(int(totalProtein)) + "g"

    if len(str(int(totalProtein))) > 3:
        displayTotalFat = readableText(int(totalFat), True) + "kg"
    else:
        displayTotalFat = readableText(int(totalFat))  + "g"

    #Draws title
    drawText(screen, (1000, 200), "Total Impact", 35)
    
    #First Row of Info
    drawText(screen, (1000, 250), "Calories: " + displayTotalCalories, 20)
    drawText(screen, (1000, 270), "Weight: " + displayTotalWieght, 20)

    #Second Row of Info
    drawText(screen, (1000, 290), "Carbs: " + displayTotalCarbs, 20)
    drawText(screen, (1000, 310), "Protein: " + displayTotalProtein, 20)
    drawText(screen, (1000, 330), "Fat: " + displayTotalFat, 20)

startup()

'''====================================main game loop===================================='''
while running:

    '''Quit Condition'''
    closeWindow()

    '''Handles mouse events'''
    if pg.mouse.get_pressed(3)[0]:
        clickedOnRow = returnRowNumber()

        #print(rows)

        #If the player clicks on a row....
        if not clickedOnRow == -1:
            
            currentRow = rows[clickedOnRow]

            print (currentRow)

            #Adds the number of "clicks" to the row information
            currentRow[1] = currentRow[1] + 1

            '''
            These are in drawing order not stage order
            Stage 1 (Fertilize): 1-12
            Stage 2 (Till): 13
            Stage 3 (Irrigate): 14
            Stage 4 (Seed): 26 - 38
            '''

            #print (currentRow[4])

            #First Stage - Fertilizes the seeds 
            if currentRow[4] == [False, False, False, False, False]:

                #Fertilizes for every click upto 12
                for fertilizedPlaces in range (currentRow[1]):
                    fertilize(clickedOnRow, fertilizedPlaces)
            
            #Second Stage - Tills the land
            elif currentRow[4] == [True, False, False, False, False]:
                till(clickedOnRow)

            #Third Stage - Irrigate the row
            elif currentRow[4] == [True, True, False, False, False]:
                irrigate (clickedOnRow)
            
            #Fourth Stage - Plants the seeds
            elif currentRow[4] == [True, True, True, False, False] and not selectedVegetable == "Vegetable":
                
                #Sets the row vegetable
                currentRow[3] = selectedVegetable

                #Seeds the area in stages
                for seedPlaces in range (currentRow[1] - SEEDING_STAGE_LOWER_LIMIT):
                    seed(clickedOnRow, selectedVegetable, seedPlaces)
                
            #Fifth Stage - Harvest the row

            elif currentRow[2] >= 2 and currentRow[4] == [True, True, True, True, False] :
                
                temp = currentRow[3]

                #Clears the row
                clearRow(clickedOnRow)

                #Clears SelectedVegetableOptions and draws a new set
                pg.draw.rect(screen, gravelColor, [1000, 200, 400, 350])
                #print (currentRow)
                drawTotalImpact(temp)

            #Refunds the click
            else:
                currentRow[1] = currentRow[1] - 1

        #If the player clicked on one of the slots
        elif isMouseInPositionOverButton((1000, 40), 400, 50):
            #print (slots) 

            #clears all slots
            for slot in slots:
                updateSlots(slot, slotColor)
                slot[1] = False

            #Draws the red slot
            for slot in slots:
                #checks each slot
                if isMouseInPositionOverButton(slot[0], 50, 50):

                    #Changes slot to red
                    slot[1] = True
                    updateSlots(slot, red)

                    selectedVegetable = slot[2]

                    #Clears SelectedVegetableOptions and draws a new set
                    pg.draw.rect(screen, gravelColor, [1000, 100, 400, 100])
                    drawSelectedVegetableOptions(selectedVegetable)

        # If nextWeekButton is pressed
        elif nextWeekButton.isMouseInPositionInButton():
            
            #increments weeks 
            week = week + 1
            pg.draw.rect(screen, gravelColor, pg.Rect(990, 690, 500, 30), 0)
            drawText (screen, (1045, 690), "Season End: " + str(TIME_TO_END - week) + " weeks", 30) #screen, topLeftPosition, text, textSize

            if TIME_TO_END - week == 1:
                pg.draw.rect(screen, gravelColor, pg.Rect(990, 690, 500, 30), 0)
                drawText (screen, (1045, 690), "Season End: " + str(TIME_TO_END - week) + " week", 30) #screen, topLeftPosition, text, textSize


            #print (rows)
            
            '''
            unseeded - 0
            seeded - 1 week
            first growth stage - 2 week
            second growth stage - 3 - 12 weeks
            Ready to havest - after 13 weeks
            '''
            #increment all seeded plots if seeded
            for row in rows:
                if not row[2] == 0:
                    row[2] = row[2] + 1
            
            '''Handles time increments changes'''
            for row in rows:
                plantInfo = vegetableInfoDictionary[row[3]]

                weeksUntilPlantIsGrown = plantInfo[6] + 2
                isSpecial = plantInfo[9]
                
                if row[2] == 2:
                    
                    seedingStageUpperLimit = row[5]
                    

                    #Brute-force fix for a bug
                    if row[1] <= seedingStageUpperLimit:
                        row[1] = seedingStageUpperLimit

                    sprout(row)

                elif row[2] > 2 and row[2] < weeksUntilPlantIsGrown and not isSpecial:

                    bushyPlantGrowth(row)
                
                elif row[2] > 2 and row[2] < weeksUntilPlantIsGrown and isSpecial:

                    stalkyPlantGrowth(row)

                elif row[2] == weeksUntilPlantIsGrown:
                    
                    readyToHarvest(row)

    #print(pg.mouse.get_pos())

    createSigns ()

    '''End Condition And End Screen'''
    if week >= TIME_TO_END:
        endScreen()

    '''Updates the window'''
    pg.display.flip()
    clock.tick(20)

