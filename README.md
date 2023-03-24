<p align="center">
  <img src="Banner.gif" />
</p>

Program that creates a random tilemap from a set of tiles and some predefined rules.

Using a set of .png images (tiles) storaged in a directory named 'TileSet' and a set of rules specified on a 'MapRules.txt' file on the main directory, the program generates a image (named 'Map.png') formed by a grid of tiles from the TileSet directory. The final result is a randomized TileMap.

```
>Tile1
#NE,TileX,TileY,TileZ,...
#E,TileX,TileY,TileZ,...
#SE,TileX,TileY,TileZ,...
#S,TileX,TileY,TileZ,...
>Tile2
#NE,TileX,TileY,TileZ,...
#E,TileX,TileY,TileZ,...
#SE,TileX,TileY,TileZ,...
#S,TileX,TileY,TileZ,...
>Tile3
#NE,TileX,TileY,TileZ,...
...
```

<div align="center">
    <table >
     <tr>
        <td><b>Tile Set</b></td>
        <td><b>Results</b></td>
     </tr>
     <tr>
       <td>
            <img align="left" src="TileSet/TileSet_2.png" width="260"/>
      </td>
       <td>
            <img align="left" src="OutputExamples/MoreExamples.gif" width="260"/>
      </td>
     </tr>
     <tr>
     <td>
            <img align="left" src="TileSet/TileSet.png" width="260"/>
      </td>
       <td>
            <img align="left" src="OutputExamples/MapExamples.gif" width="260"/>
      </td>
       





