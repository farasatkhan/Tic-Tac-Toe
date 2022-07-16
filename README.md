# Tic-Tac-Toe

## Minimax Algorithm:
It is a backtracking algorithm with the primary goal of maximizing utility. It is used for optimal decision-making in game theory. In this algorithm, the two players try to maximize their score and minimize the opponents’ score. It searches game trees, assuming that the players take alternate moves.

## Evaluation Function (Utility Function): 
We use an evaluation function to determine a good move for a particular player. It is unique for every type of game. The basic idea behind this function is to give a high value for a board if max’s turn and a low value for the board if min’s turn.

## Alpha-Beta Pruning:
The time complexity for the minimax algorithm is O(bd), where b is the branching factor (number of legal moves), and d is depth or ply. So, the time complexity increases drastically when we have more possible moves. So, to improve the minimax, Alpha-beta is used. Alpha-beta uses a heuristic and stops evaluating a move when it makes sure that it is worse than the previously examined move. It gives the same result as a simple minimax algorithm, but it prunes branches of the tree that do not affect the final decision, increasing the algorithm's efficiency.

## Alpha-Beta Algorithm:
1.	Alpha = highest-value choice found at any choice point of the path for MAX. 
initially, α = −infinity
2.	Beta = lowest-value choice found at any choice point of the path for MIN. 
initially, β = +infinity
3.	During the search pass down the values of α and β. 
4.	Update values of α and β during the search: 
o	MAX updates α at MAX nodes 
o	MIN updates β at MIN nodes

Prune whenever alpha >= beta (We do so because no matter how large the value of children nodes is, MIN only selects the minimum value, and beta will hold the best MIN value in it so there is no need to search further.) 

Tic Tac Toe Game Tree Size: 
We have 9 legal actions available that can be chosen by one player so if the computer goes first 9! = 362,880 and if the Computer goes second 8! = 40,320   

## Selected Utility Function:
•	-10 if Min wins  
•	0 if it’s a tie
•	10 if Max wins



## How we used Alpha-beta pruning in the code:
We have got two agents here, Min and Max. Max is trying to maximize the utility, and Min is trying to minimize the utility of Max. Both Min and Max play alternatively, and we are assuming that the Min agent (Computer in our case) is playing the game logically and will always try to select the best option possible. The best choice for Min would be the minimum value, thus reducing Max's utility. 
After the definition of our abminimax (Alpha-beta pruning) algorithm, depth is checked. If depth equals zero, the result is returned as all the slots have been filled. (Depth refers to the number of empty places available on the board), or win_status_unrendered method is called to check whether the game is won. Utility value along with the row and col coordinate is returned. The alpha-beta pruning uses the utility function to produce ten if one wins, which is the 'X' player, and returns -10 if -1 wins, which is the 'O' player. We have associated 10 for the human player and -10 for the AI Bot.
The move method is called when the user clicks on one of the nine boxes and convert the pixels into x and y position for the board. We divide the location of the mouse by 430 * 2 to get in the range 0-2 for xPos and yPos. Once the player plays his move, it is AI's move, and the best location is picked using alpha-beta pruning. bestAIMove store the best position for x and y, and at the end, we render the board. AIMoveNone is used to undo the action of the AImove. It is used in the alpha-beta pruning function. We have to undo the steps in the alpha-beta pruning because we have a single 3x3 board.
If we have empty slots available, for loop will run, and Min and Max will select their option alternatively. Alpha-beta pruning is called recursively for each turn of Min and Max until the depth equals zero, meaning no slots left are available on the board. This method has five parameters self, board, alpha, beta, and player. It is used to return the best possible moves for the AI. We continuously call the function until the depth is reached to 0 or either one wins, ' X' or -1, 'O'. We recursively call the function reducing the depth, which is the length of the empty spots available on the 3x3 board. 

We call and AImove function to place the item on the board and undo the action using the AImoveNone. At each recursive call, depth is being decremented, and player value is inversed means player turn changes. If it is Max's turn player, which is one or 'X,' we modify the alpha value if it has a better alternative. Similarly, if it is Min's turn which is the computer's turn, the value of beta also gets updated if it has a better choice.
