# rep1
tic-tac-toe game
The game with minimax algorithm
What is Minimax?
Max is moving first and turns are changing until the game is over. Points are awarded to the winner 
player and penalties to the lost one. A game can be formally defined as a kind of a search problem 
with the following elements:
The initial sate – how game condition looks like at the start.
Player – defines which player has the move in a state
Action – returns the set of a legal moves in a state
Result – the transition model that defines the result of a move
Terminal-test – a terminal test, that is true when the game is over and false when it’s in process. 
States where game is ended is called terminal state.
Utility – an utility function that is also called an objective function, defines the final numeric value 
for a game that ends with a terminal state s for a player p.
This game containes mini max algorithm for playing with computer and random choice algorithm. It also has a function to play with other player without computer participation.
