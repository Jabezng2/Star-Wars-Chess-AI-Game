# ♟️Star-Wars-Chess-AI-Game♟️ 

## Content Page

- [About](#about)
- [Interfaces](#interfaces)
- [Pieces](#pieces)
- [Controls](#controls)
- [NegaMax w Alpha-Beta Pruning](#negamax-w-alpha-beta-pruning)
- [Improvments](#improvements)
- [Image Sources](#image-sources)

## About

This game was implemented using Python and was inspired by Eddie Sharick's tutorial series. The repository involves added user interface features and the chess game has been created with the *STAR WARS* theme in mind. In this implementation, *NegaMax* with *Alpha-Beta Pruning* optimisation algorithm is utilized. 

Link to [Eddie's Chess Series](https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_)

## Interfaces

<table>
  <tr>
    <th align="center">Main Menu</th>
     <th align="center">Credit Menu</th>
  </tr>
  <tr>
    <td valign="top"><img src="https://github.com/Jabezng2/Star-Wars-Chess-AI-Game/blob/main/interfaces/mainmenu.png"></td>
    <td valign="top"><img src="https://github.com/Jabezng2/Star-Wars-Chess-AI-Game/blob/main/interfaces/creditspage.png"></td>
  </tr>
 </table>
<table>
  <tr>
    <th align="center">Start State</th>
     <th align="center">Game State</th>
  </tr>
  <tr>
    <td valign="top"><img src="https://github.com/Jabezng2/Star-Wars-Chess-AI-Game/blob/main/interfaces/gameStart.png"></td>
    <td valign="top"><img src="https://github.com/Jabezng2/Star-Wars-Chess-AI-Game/blob/main/interfaces/gameCurrent.png"></td>
  </tr>
 </table>

Font used is [8-BIT WONDER](https://github.com/Jabezng2/Star-Wars-Chess-AI-Game/blob/main/8-BIT%20WONDER.TTF) and has been uploaded.

## Pieces

A brief description of the pieces in this *STAR WARS* themed game is as follows:

### *Light Side*
1. `Pawn` : R2D2
2. `Rook` : *Millennium Falcon*
3. `Knight` : C3P0
4. `Bishop` : Chewbacca
5. `Queen` : Padme Amidala (Naboo)
6. `King` : Anakin Skywalker

### *Dark Side*
1. `Pawn` : Stormtrooper
2. `Rook` : *TIE* Fighter
3. `Knight` : Captain Phasma
4. `Bishop` : Boba Fett
5. `Queen` : Kylo Ren
6. `King` : Darth Vader

## Controls

- When `Credits` button is pressed, CREDIT_DISPLAY will be loaded. `MOUSECLICK` will return user back to MAIN_MENU.  
- Press <kbd>Z</kbd> to undo the move
- Press <kbd>R</kbd> to reset the game

## NegaMax w Alpha-Beta Pruning

The *NegaMax* algorithm is similar to the *MiniMax* algorithm just that it is slightly less complex. Instead of using two functions a *minimizing* and *maximizing* function, it ***ONLY*** utilizes a *maximizing* function. (i.e to say that it always selects the maximum value out of possible values) Furthermore, it negates the selected value / multiply value by -1. In addition to using *NegaMax*, *Alpha-Beta Pruning* is also incoportated to further optimize the alogrithm. *Alpha-Beta Pruning* allows us to remove unnecessary game states which improves the speed of the algorithm. In *Alpha-Beta Pruning*, a *depth-first* transversal is being used. We will have 2 variables, namely &alpha; and &beta; which are initialized to -&infin; and +&infin; respectively. It is crucial to note that the pruning condition is that &alpha; &#8805; &beta;. When that condition is fufilled, we prune and do not bother exploring that node. *GIF* below illustrates the concept.

<p align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/f/ff/Negamax_AlphaBeta.gif"></p>

## Improvements

1. Definitely, `ChessAI` can be improved for greater speed and accuracy. Was thinking of `Stockfish's Search Algorithm` which is popular for chess.
2. Board flip when `Dark Side` is selected, although AI plays using the `Light Side` pieces.

## Image Sources

1. [MainMenu](https://www.pinterest.com/pin/256212666287753305/)
2. [CreditMenu](https://www.pinterest.com/pin/86694361568238849/)
3. [ChessPieces](https://www.pinterest.com/pin/4574037102111760/)
