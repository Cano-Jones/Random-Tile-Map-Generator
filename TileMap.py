#!/usr/bin/env python
"""
TileMap.py

This program generates a randomized Tile Map from a set of tiles and a predefined set of rules.
The input needed is a set of 'TileName.png' images contained in a 'TileSet' and a 'MapRules.txt' file, that specifies for each Tile the posible 
tiles that can be adjacent to it. The format of the 'MapRules.txt' goes as follows:

>FirstTale
#NE,FirstTale,OtherTale,AnotherTale
#E,FirstTale,AnotherTale
#SE,FirstTale
#S,OtherTale,AnotherTale
>OtherTale
#NE,FirstTale,AnotherTale
#E,FirstTale
#SE,FirstTale,AnotherTale
#S,OtherTale
>,AnotherTale
#NE,...
...

The meaning of the # variables is
#NE-> North East
#E-> East
#SE-> South East
#S-> South

meaning that a specific tile can be placed at the upper-right, right, lower-right or below the >Tile. It is only necesary to specify this rules, as the program
starts placing tiles from the top left, continues on that column and passes to the next.

After placing at random the tiles, the program can erase 'lonely' tiles (tiles with no direct contact with a tile equal to it), so the result looks cleaner.
The final tile map is saved as 'Map.png'

:Author: Cano Jones, Alejandro
:Date: March 2023
:LinkedIn: https://www.linkedin.com/in/alejandro-cano-jones-5b20a7136/
:GitHub: https://github.com/Cano-Jones
"""

#Used libraries
from random import sample
import pygame
from pygame.locals import *
import os

pygame.init() #Necessary for the use of the pygame library
tile_size=16 #Size of the elementary tile
Rows=60 #Number of tiles for each column
Columns=60 #Number of tiles for each row
screen_width= tile_size*Rows #Width of the final map
screen_height=tile_size*Columns #Height of the final map
screen=pygame.display.set_mode((screen_width, screen_height)) #Pygame definition of the map



class World():
    """
    World Class
    Describes the tile placement of the map in a language that pygame can interpret. The data class of the Wold is a tile list 'tile_list' in which
    each element is a tuple, stating the image to be placed, and its coordinates on the map. The input 'data' is a matrix, where its elements determine the tile 
    on each relative position.

    The inner function 'Draw()' uses the pygame library to draw each tile in its place to create the complete map.
    """
    def __init__(self, data):
            """Definition of the World Class"""
            self.tile_list=[] #The list that will contain the information on each tile is created

            row_count=0 #Row counter
            for row in data: #Loop on each row
                col_count=0 #Column counter
                for tile in row: #Loop on each element of the row
                    img=pygame.transform.scale(pygame.image.load('TileSet/'+tile+'.png'), (tile_size, tile_size)) #The image relating to the tile is stored
                    img_rect=img.get_rect() #Definition of the position of the tile
                    img_rect.y=col_count*tile_size #Y coordinate of the image
                    img_rect.x=row_count*tile_size #X position of the image
                    self.tile_list.append((img, img_rect)) #The information of the tile is added to the tile_list
                    col_count+=1 #The column counter is updated 
                row_count+=1 #The row counter is updated

    def Draw(self):
        """Function that draws each tile on its position to create the tale map"""
        for tile in self.tile_list: #Loop on each tile information
            screen.blit(tile[0], tile[1]) #The tile is placed on its proper location

class TileRule():
    """TileRule Class 
        Class used to better organice the tile placement rules, storing the name of a tile and in a dictionary, the direction as a key and a list of tiles
        that can be placed on that direction
    """
    def __init__(self, name, ok_dic):
        self.name=name #Name of the tile
        self.ok_dic=ok_dic #Dictionary containing the direction and list of tiles that can be placed on that direction


def CreateMapRules():
    """
    CreateMapTules()
    This function reads the 'MapRules.txt' file containing the information on the tile that can be placed on each configuration. Returns a 
    list of TileRule classes.
    """
    file = open('MapRules.txt',mode='r') #The file 'MapRules.txt' is open on read mode
    Text = file.read() #The text contanied by the file is readed and saved on 'Text' variable
    file.close() #file is closed
    Text=Text.split('>') #The text is divided on a list, where each element contains the information on different tiles
    Rules=[] #The list that will contain the rules is created
    del Text[0] #The first elemet of 'Text' contains nothing, and therefore must be eliminated
    for Tile_type in Text: #Loop on each tile type
        Tile_type=Tile_type.split('\n') #The information of each tile is divided in rows
        name=Tile_type[0] #The first row contains only the name of the tile
        del Tile_type[0] #Once it is saved, it is eliminated from the text for simpler usage
        dic={} #The dictionary that will contain the compatibility between tiles and direction is created
        for direction in Tile_type: #Loop on each direction
            direction=direction.split(',') #The remaining text is divided: Direction,Tile1,Tile2,Tile3,...
            dir=direction[0].replace('#','') #The direction is stored separetly, it will be the key of the dictionary 
            del direction[0] #That information is deleted from the text form simpler usage, the remaining information is a list of compatible tiles
            dic.update({dir:direction}) #The dictionary is updated with this new information
        Rules.append(TileRule(name, dic)) #The Rules list is updated with the dictionary
    return Rules #The Rules list is returned

        

def WorldData(Rules):
    """
    WorldData(Rules)
    This function creates a random matrix which elements are the posible tiles. The relative position between elements determine the relative position between
    tiles in the final map. The elements are choosen randomly but acording to the rules stores in the 'Rules' list, whose elements are TileRule class elements.
    """
    world=[['X' for i in range(Columns)] for j in range(Rows)] #The matrix is defined with 'X' on each element
    Tile_set=set() #An empty set is defined, it will store the Posible tiles
    for i in Rules:  Tile_set.add(i.name) #A loop is used to extract the names of all posible tiles, and they are stored on the Tile_set set

    for i in range(Columns): #A loop on each column of the matrix
        for j in range(Rows): #Loop on each rof of the matrix
            if i==0 and j==0: #If the matrix element is at (0,0) coordinates, there are no restrictions for the tiles
                world[i][j]=sample(Tile_set,1)[0] #A random tile is choosen 
            elif i==0: #If the matrix element is on the first column, it needs to check if the tile above it allows the random tile selected
                while True: #A loop that will run until a tile is choosen
                    aux=sample(Tile_set,1)[0] #A random tile is generated
                    for r in Rules: #All rules are checked
                        if r.name==world[i][j-1]: set_pos=r.ok_dic #A set of posible tiles that can be choosen is created
                    if aux in set_pos['S']: #If the choosen tile is on that set
                        world[i][j]=aux #The tile is saved
                        break #And the loop is stopped
            elif j==0: #Similar case as above, this time with the first row, it needs to check the tile at its left and the tile below that one
                while True:
                    aux=sample(Tile_set,1)[0]
                    for r in Rules:
                        if r.name==world[i-1][j]: set_pos_W=r.ok_dic
                        if r.name==world[i-1][j+1]: set_pos_SW=r.ok_dic
                    if (aux in set_pos_W['E']) and (aux in set_pos_SW['NE']):
                        world[i][j]=aux
                        break
            elif (i==Columns-1) and (j==Rows-1): #Similar case as the first one, The lower left tile, needs to check the tile above, the tile at its left, an
                                                     #the tile above that one
                while True:
                    aux=sample(Tile_set,1)[0]
                    for r in Rules:
                        if r.name==world[i][j-1]: set_pos_N=r.ok_dic
                        if r.name==world[i-1][j]: set_pos_W=r.ok_dic
                        if r.name==world[i-1][j-1]: set_pos_NW=r.ok_dic
                    if (aux in set_pos_N['S']) and (aux in set_pos_W['E']) and (aux in set_pos_NW['SE']):
                        world[i][j]=aux
                        break

            elif i==Columns-1: #The last column, it needs to check the tiles above, left, above left and below left.
                while True:
                    aux=sample(Tile_set,1)[0]
                    for r in Rules:
                        if r.name==world[i][j-1]: set_pos_N=r.ok_dic
                        if r.name==world[i-1][j]: set_pos_W=r.ok_dic
                        if r.name==world[i-1][j-1]: set_pos_NW=r.ok_dic
                        if r.name==world[i-1][j+1]: set_pos_SW=r.ok_dic
                    if (aux in set_pos_N['S']) and (aux in set_pos_W['E']) and (aux in set_pos_NW['SE']) and (aux in set_pos_SW['NE']):
                        world[i][j]=aux
                        break
            elif j==Rows-1: #The last row needs to check the tiles above, left and above left.
                while True:
                    aux=sample(Tile_set,1)[0]
                    for r in Rules:
                        if r.name==world[i][j-1]: set_pos_N=r.ok_dic
                        if r.name==world[i-1][j]: set_pos_W=r.ok_dic
                        if r.name==world[i-1][j-1]: set_pos_NW=r.ok_dic
                    if (aux in set_pos_N['S']) and (aux in set_pos_W['E']) and (aux in set_pos_NW['SE']):
                        world[i][j]=aux
                        break

            else:  #The rest of the tiles need to check above, left, above left, below left
                while True:
                    aux=sample(Tile_set,1)[0]
                    for r in Rules:
                        if r.name==world[i-1][j]: set_pos_W=r.ok_dic
                        if r.name==world[i][j-1]: set_pos_N=r.ok_dic
                        if r.name==world[i-1][j-1]: set_pos_NW=r.ok_dic
                        if r.name==world[i-1][j+1]: set_pos_SW=r.ok_dic

                    if (aux in set_pos_W['E']) and (aux in set_pos_N['S']) and (aux in set_pos_NW['SE']) and (aux in set_pos_SW['NE']):
                        world[i][j]=aux
                        break
    """
    #Next, the program checks if a tile is a 'lonely' tile (it does not touch anothe tile equal to it). If thats the case, it is changed
    for i in range(1,Columns-1):
        for j in range(1,Rows-1):
            if world[i][j] not in [world[i][j-1],world[i+1][j],world[i][j+1],world[i-1][j]]: world[i][j]=world[i-1][j]
    """
    
    return world #The world matrix is returned
    


def Main():
    """
    Main function of the program. It creates the world Matrix, then creates the World class and draws the final map. It saves the image on 'Map.png'
    """
    world_data=WorldData(CreateMapRules()) #World matrix is created
    world=World(world_data) #World class is created
    world.Draw() #Map is drawed
    pygame.image.save(screen, "Map.png") #The image is saved as 'Map.pn'
    pygame.quit() #The pygame library stops
    clear = lambda: os.system('clear') #During the program, some terminal comands apperars, this function clears the terminal
    clear() #The terminal is cleared


if __name__ == "__main__":
        Main()
    











