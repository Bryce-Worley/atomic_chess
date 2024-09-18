# 2-Player Command Line Atomic Chess

A 2-play game of the chess variation, [Atomic Chess.](https://en.wikipedia.org/wiki/Atomic_chess)

## Description

Created as part of the portfolio project for Oregon State University's CS162 Introduction to Computer Science, this app allows for users to play Atomic Chess in the command line.

The starting position for the game is the normal starting position for standard chess. You will need to keep track of which player's turn it is. As in standard chess, white moves first. Pieces move and capture the same as in standard chess, except that **there is no check or checkmate, and there is no castling, en passant, or pawn promotion**. As in standard chess, each pawn should be able to move two spaces forward on its first move (but not on subsequent moves). 

If a player's king is captured or blown up, the game ends, and that player loses. 

Locations on the board will be specified using "algebraic notation", with columns labeled a-h and rows labeled 1-8

Special rules for this variant of chess:

In Atomic Chess, whenever a piece is captured, an "explosion" occurs at the 8 squares immediately surrounding the captured piece in all the directions. This explosion kills all of the pieces in its range except for **pawns**. Different from regular chess, where only the captured piece is taken off the board, in Atomic Chess, every capture is suicidal. Even the capturing piece is affected by the explosion and must be taken off the board. As a result, a pawn can only be removed from the board when directly involved in a capture. If that is the case, both capturing and captured pawns must be removed from the board. Because every capture causes an explosion that affects not only the victim but also the capturing piece itself, **the king is not allowed to make captures**. Also, a player **cannot blow up both kings at the same time**. In other words, the move that would kill both kings in one step is not allowed. Blowing up a king has the same effect as capturing it, which will end the game.
[(https://www.chess.com/terms/atomic-chess#captures-and-explosions)](https://www.chess.com/terms/atomic-chess#captures-and-explosions)

## Getting Started

Download the program, and run in the command line.

### Dependencies

Board uses utf-8 characters to represent the various chess pieces in the command line.  If the symbols are not appearing after each move, check to see if the terminal allows for utf-8 character encoding.

## Authors

Bryce Worley
[@Bryce-Worley](https://github.com/Bryce-Worley)

## Version History
* 0.1
    * Initial Development Release 

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Portfolio Project assignment created by Tim Alcon, Luyao Zhang, and Brian Baker for Oregon State University CS162 Intro to Computer Science II course.
