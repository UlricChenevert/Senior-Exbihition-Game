'''
This is the main file for my senior exhibition gamma food insecurity game

Farming simulator with nutrition and poundage outputs
'''
#Imports outside functions
import pygame as pg

#Imports local functions
#There is none lol
pg.init()

'''Setting up the display'''
width = 1400
height = 800
screen = pg.display.set_mode((width, height), 0, 32)
pg.display.set_caption("Gamma: Urban Agriculture")
clock = pg.time.Clock()

#Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
rowColor = (107, 62, 12)
tillColor = (64, 35, 3)
gravelColor = (168, 168, 168)
signColor = (115, 73, 32)
seedColor = (207, 168, 78)
fertilizeColor = (69, 40, 8)
tomatoColor = (198, 45, 22)
bellpepperColor = (207, 97, 12)
potatoColor = (250, 183, 27)
vineColor = (8, 128, 10)
slotColor = (100, 100, 100)
nextWeekButtonColor = (198, 45, 22)
growingStageColor = (12, 71, 20)
readyToHarvestColor = (12, 71, 40)


#row[0] is coords, row[1] is number of clicks, row[2] is weeks growing, row[3] is which plant
rows = [[(), 0, 0, "no plant"], [(), 0, 0, "no plant"], [(), 0, 0, "no plant"], [(), 0, 0, "no plant"], [(), 0, 0, "no plant"], [(), 0, 0, "no plant"], [(), 0, 0, "no plant"]]

#row[0] is coords, row[1] stored if clicked,
slots = [[(), False, "Tomato"], [(), False, "Bellpepper"], [(), False, ""], [(), False, "Potato"], [(), False, "Carrot"], [(), False, "Spinach"], [(), False, "Soybeans"], [(), False, "Lettuce"]]

#Signs 
sign = ["no plant", "no plant", "no plant", "no plant",  "no plant",   "no plant",  "no plant",  "no plant"]

mouseClicksCount = 0
week = 0

totalCalories = 0
totalWieght = 0
totalCarbs = 0
totalProtein = 0
totalFat = 0

selectedVegetable = "none"

NUMBER_OF_PLANTS_PER_ROW = 12
TILL_STAGE = 13
IRRIGATE_STAGE = 14
SEEDING_STAGE_LOWER_LIMIT = 15
SEEDING_STAGE_UPPER_LIMIT = 27
HARVEST_STAGE_LOWER_LIMIT = 28
TIME_TO_HARVEST = 13

running = True

'''General Functions'''
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

def drawText (screen, topLeftPosition, text, textSize, drawRect = False, showInfo = False):

    font = pg.font.Font('freesansbold.ttf', int(textSize))
    img = font.render(text, True, black)
    textRectangle = img.get_rect()

    if showInfo:
        print (textRectangle)

    if drawRect:
        pg.draw.rect(screen, white, textRectangle)

    screen.blit(img, topLeftPosition)

def closeWindow():
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

        if rows[row][3] != "no plant":
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

def updateSlots(slot, color):
    pg.draw.rect(screen, color, pg.Rect(slot[0][0], slot[0][1], 50, 50), 5)

def clearRow(clickedOnRow):

    currentRow = rows[clickedOnRow]

    #colors over the plants
    for seedPlace in range(NUMBER_OF_PLANTS_PER_ROW):
        #Max is 50 radius min is 5
        pg.draw.circle(screen, gravelColor, (currentRow[0][0] + 33, currentRow[0][1] + 10 + seedPlace * 63), 53)
        pg.draw.circle(screen, gravelColor, (currentRow[0][0] + 84, currentRow[0][1] + 10 + seedPlace * 63), 53)

    #creates a new row
    pg.draw.rect(screen, rowColor, pg.Rect(currentRow[0][0],  currentRow[0][1], 120, 765), 0)
    
    #Fixes the other rows 
    #If older or equal to 10 then re-draw plant
    #Row to the left
    try:
        rowToTheLeft = rows[clickedOnRow - 1]
        if rowToTheLeft[2] >= 10 and rowToTheLeft[2] < 13:
            exponentialGrowth(rowToTheLeft)
        
        elif rowToTheLeft[2] >= 13:
           readyToHarvest(rowToTheLeft)
    except:
        print ("Error on left side")

    try:
        rowToTheLeft = rows[clickedOnRow + 1]
        if rowToTheLeft[2] >= 10 and rowToTheLeft[2] < 13:
            exponentialGrowth(rowToTheLeft)
        
        elif rowToTheLeft[2] >= 13:
           readyToHarvest(rowToTheLeft)
    except:
        print ("Error on left side")

    #Resets the week counter, the click amount, and the selected vegetable
    currentRow[1] = 0
    currentRow[2] = 0
    currentRow[3] = "no plant"

def fertilize(clickedRow, fertilizeIteration):

    pg.draw.rect(screen, fertilizeColor, pg.Rect(rows[clickedRow][0][0], rows[clickedRow][0][1]+ fertilizeIteration * 62, 120, 83), 0)

def till(clickedRow):
    #Draw tilled lines
    pg.draw.rect(screen, tillColor, pg.Rect(rows[clickedRow][0][0] + 31, rows[clickedRow][0][1] + 10, 5, 740), 0)
    pg.draw.rect(screen, tillColor, pg.Rect(rows[clickedRow][0][0] + 82, rows[clickedRow][0][1] + 10, 5, 740), 0)

def irrigate (clickedRow):
    pg.draw.rect(screen, black, pg.Rect(rows[clickedRow][0][0] + 58, rows[clickedRow][0][1] + 10, 5, 740), 0)

def seed(clickedRow, seedIteration = 1):
    #Draw two seeds
    pg.draw.rect(screen, seedColor, pg.Rect(rows[clickedRow][0][0] + 31, rows[clickedRow][0][1] + 10 + seedIteration * 63, 5, 5), 0)
    pg.draw.rect(screen, seedColor, pg.Rect(rows[clickedRow][0][0] + 82, rows[clickedRow][0][1] + 10 + seedIteration * 63, 5, 5), 0)

    #Adds seed stage info to row data (0 means seedling)
    rows[clickedRow][2] = 1

def firstGrowthStage(row):
    for seedPlace in range(NUMBER_OF_PLANTS_PER_ROW):
        pg.draw.rect(screen, growingStageColor, pg.Rect(row[0][0] + 31, row[0][1] + 10 + seedPlace * 63, 5, 5), 0)
        pg.draw.rect(screen, growingStageColor, pg.Rect(row[0][0] + 82, row[0][1] + 10 + seedPlace * 63, 5, 5), 0)

def exponentialGrowth(row):
    week = row[2]

    for seedPlace in range(NUMBER_OF_PLANTS_PER_ROW):
        #Max is 50 radius min is 5
        pg.draw.circle(screen, growingStageColor, (row[0][0] + 33, row[0][1] + 10 + seedPlace * 63), 1.38**week + 5)
        pg.draw.circle(screen, growingStageColor, (row[0][0] + 84, row[0][1] + 10 + seedPlace * 63), 1.38**week + 5)

        #print (1.38**week + 5)

def readyToHarvest(row):
    for seedPlace in range(NUMBER_OF_PLANTS_PER_ROW):
        #Max is 50 radius min is 5
        pg.draw.circle(screen, readyToHarvestColor, (row[0][0] + 33, row[0][1] + 10 + seedPlace * 63), 53)
        pg.draw.circle(screen, readyToHarvestColor, (row[0][0] + 84, row[0][1] + 10 + seedPlace * 63), 53)

def drawTomato (center):

    pg.draw.rect(screen, vineColor, pg.Rect(center[0] - 5, center[1]- 15, 10, 20), 0)
    pg.draw.circle(screen, tomatoColor, center, 10, 0)

def drawBellPepper (topLeft):

    pg.draw.rect(screen, vineColor, pg.Rect(topLeft[0] + 12, topLeft[1], 5, 10), 0)
    pg.draw.rect(screen, bellpepperColor, pg.Rect(topLeft[0], topLeft[1] + 10, 10, 30), 0, border_radius=4)
    pg.draw.rect(screen, bellpepperColor, pg.Rect(topLeft[0] + 10, topLeft[1] + 10, 10, 30), 0, border_radius=4)
    pg.draw.rect(screen, bellpepperColor, pg.Rect(topLeft[0] + 20, topLeft[1] + 10, 10, 30), 0, border_radius=4)

def drawPotato (topLeft):

    pg.draw.rect(screen, potatoColor, pg.Rect(topLeft[0], topLeft[1], 25, 40), 0, border_radius=13)

def drawPlantsSwitch (plant, clickedRow):

    if plant == "Tomato":
        drawTomato((rows[clickedRow][0][0] + 60, rows[clickedRow][0][1] + 690))
    elif plant == "Bellpepper":
        drawBellPepper((rows[clickedRow][0][0] + 40, rows[clickedRow][0][1] + 670))
    else: 
        print ("Error!")

#Ordered: quanitity per plant, wieght per item (grams), carbs per item (grams), protein per item(grams), fat per item(grams), calories per item
vegetableNutrientInfoDictionary = {
"none": [0, 0, 0, 0, 0, 0], "Bellpepper":  [7, 400, 24, 4, 1.2, 124], "Tomato" : [16, 900, 35.1, 8.1, 1.8, 162]
}

def drawSelectedVegetableOptions(vegetable = "none"):

    nutritionalFacts = vegetableNutrientInfoDictionary[vegetable]
    #Draws title
    drawText(screen, (1000, 100), "Vegetable Nutrients", 40)
    
    #First Row of Info
    drawText(screen, (1000, 140), "Calories: " + str(nutritionalFacts[5]) + "g" , 20)
    drawText(screen, (1150, 140), "Weight: " + str(nutritionalFacts[1]) + "g", 20)

    #Second Row of Info
    drawText(screen, (1000, 170), "Carbs: " + str(nutritionalFacts[2]) + "g" , 20)
    drawText(screen, (1150, 170), "Protein: " + str(nutritionalFacts[3]) + "g", 20)
    drawText(screen, (1300, 170), "Fat: " + str(nutritionalFacts[4]) + "g", 20)

def drawTotalImpact(vegetable = "none"):
    global totalCalories, totalWieght, totalCarbs, totalProtein, totalFat

    nutritionalFacts = vegetableNutrientInfoDictionary[vegetable]
    
    totalCalories = round((totalCalories + nutritionalFacts[5]) * NUMBER_OF_PLANTS_PER_ROW, 2)
    totalWieght = round((totalWieght + nutritionalFacts[1]) * NUMBER_OF_PLANTS_PER_ROW, 2)
    totalCarbs = round((totalCarbs + nutritionalFacts[2]) * NUMBER_OF_PLANTS_PER_ROW, 2)
    totalProtein = round((totalProtein + nutritionalFacts[3]) * NUMBER_OF_PLANTS_PER_ROW, 2)
    totalFat = round((totalFat + nutritionalFacts[4]) * NUMBER_OF_PLANTS_PER_ROW, 2)

    #Draws title
    drawText(screen, (1000, 200), "Total Impact", 40)
    
    #First Row of Info
    drawText(screen, (1000, 250), "Calories: " + str(totalCalories) + "g" , 20)
    drawText(screen, (1000, 270), "Weight: " + str(totalWieght) + "g", 20)

    #Second Row of Info
    drawText(screen, (1000, 290), "Carbs: " + str(totalCarbs) + "g" , 20)
    drawText(screen, (1000, 310), "Protein: " + str(totalProtein) + "g", 20)
    drawText(screen, (1000, 330), "Fat: " + str(totalFat) + "g", 20)

#Creates the background
screen.fill(gravelColor)
createRows()
createSlots ()
drawTomato((1025, 65))
drawBellPepper((1060, 45))

#Draws UI
drawText(screen, (1000, 0), "Vegetable Options", 40)
drawSelectedVegetableOptions()
drawTotalImpact()

drawPotato((500, 500))

nextWeekButton = Button((1000, 700), screen, "Next Week", 40, (995, 695), 215, 50, showBackground = True, backgroundColor = nextWeekButtonColor)
drawText (screen, (1215, 700), "Week: " + str(week), 40) #screen, topLeftPosition, text, textSize

#print (rows)

'''main game loop'''
while running:

    '''Quit Condition'''
    closeWindow()

    '''Handles mouse events'''
    if pg.mouse.get_pressed(3)[0]:
        clickedOnRow = returnRowNumber()

        #If the player clicks on a row....
        if not clickedOnRow == -1:
            
            currentRow = rows[clickedOnRow]

            print (currentRow)

            #Adds the number of "clicks" to the row information
            currentRow[1] = currentRow[1] + 1

            #print (rows[clickedOnRow])

            '''
            These are in drawing order not stage order
            Stage 1 (Fertilize): 1-12
            Stage 2 (Till): 13
            Stage 3 (Irrigate): 14
            Stage 4 (Seed): 26 - 38
            '''
            #First Stage - Fertilizes the seeds 
            if currentRow[1] <= NUMBER_OF_PLANTS_PER_ROW:
                for fertilizedPlaces in range (currentRow[1]):
                    #Seeds the area in stages
                    fertilize(clickedOnRow, fertilizedPlaces)

            #Second Stage - Tills the land
            elif currentRow[1] == TILL_STAGE:
                till(clickedOnRow)

            #Third Stage - Irrigate the row
            elif currentRow[1] == IRRIGATE_STAGE:
                irrigate (clickedOnRow)
            
            #Fourth Stage - Plants the seeds
            elif not selectedVegetable == "none" and currentRow[1] >= SEEDING_STAGE_LOWER_LIMIT and currentRow[1] <= SEEDING_STAGE_UPPER_LIMIT:

                #Seeds the area in stages

                for seedPlaces in range (currentRow[1]):
                    seed(clickedOnRow, seedPlaces - SEEDING_STAGE_LOWER_LIMIT)
                
                currentRow[3] = selectedVegetable

            #Fifth Stage - Harvest the row

            elif currentRow[2] >= TIME_TO_HARVEST and currentRow[1] >= HARVEST_STAGE_LOWER_LIMIT:
                
                temp = currentRow[3]

                #Clears the row
                clearRow(clickedOnRow)

                #Clears SelectedVegetableOptions and draws a new set
                pg.draw.rect(screen, gravelColor, [1000, 200, 400, 350])
                print (currentRow)
                drawTotalImpact(temp)

            #Refunds the click
            else:
                currentRow[1] = currentRow[1] - 1

        #If the player clicked on one of the slots
        elif isMouseInPositionOverButton((1000, 40), 400, 50):
            #print (slots) 
            # # [[(1000, 40), False, 'Tomato'], [(1050, 40), False, 'Bellpepper'], [(1100, 40), False, ''], [(1150, 40), False, 'Potato'], [(1200, 40), False, 'Carrot'], [(1250, 40), False, 'Spinach'], [(1300, 40), False, 'Soybeans'], [(1350, 40), False, 'Lettuce']]
            for slot in slots:
                #checks each slot
                if isMouseInPositionOverButton(slot[0], 50, 50):
                    slot[1] = True
                    updateSlots(slot, red)
                    selectedVegetable = slot[2]

                    #Clears SelectedVegetableOptions and draws a new set
                    pg.draw.rect(screen, gravelColor, [1000, 130, 400, 60])
                    drawSelectedVegetableOptions(selectedVegetable)

                else:
                    #This ensures there aren't any other red slots
                    slot[1] = False
                    updateSlots(slot, slotColor)

        # If nextWeekButton is pressed
        elif nextWeekButton.isMouseInPositionInButton():
            
            #increments week display
            week = week + 1
            pg.draw.rect(screen, gravelColor, pg.Rect(1215, 700, 215, 40), 0)

            drawText (screen, (1215, 700), "Week: " + str(week), 40) #screen, topLeftPosition, text, textSize
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
                if row[2] == 2:
                    firstGrowthStage(row)

                elif row[2] > 2 and row[2] < 13:
                    exponentialGrowth(row)
                
                elif row[2] >= TIME_TO_HARVEST:
                    readyToHarvest(row)

    #print(pg.mouse.get_pos())

    createSigns ()

    '''Updates the window'''
    pg.display.flip()
    clock.tick(20)