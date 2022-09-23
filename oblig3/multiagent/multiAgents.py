# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        # returns the action from min max search
        return self.min_max_search(gameState)

    def min_max_search(self, gameState):
        """
        returns max value with initial depth set to 0
        :param gameState:
        :return:
        """
        return self.max_value(gameState, 0)[1]

    def max_value(self, gameState, depth):
        """
        searches for action giving maximimum value from minmax tree
        :param gameState: current state
        :param depth: current depth
        :return: best
        """
        if self.terminal(gameState, depth):
            # if terminal state, evaluates the state with evaluation function
            return self.evaluationFunction(gameState), None
        # best is initially set to negative inf, every other value will be greater
        best = (float('-inf'), None)
        for action in gameState.getLegalActions(self.index):
            # new state is set by current action
            next_state = gameState.generateSuccessor(self.index, action)
            # action value is set by min value method and current depth
            action_value = self.min_value(next_state, depth, 1)
            # sets new best value if the action value is greater than current best value
            if action_value[0] > best[0]:
                best = (action_value[0], action)
        return best

    def min_value(self, gameState, depth, index):
        """
        searches for action giving minimum value from minmax tree
        :param gameState: current state
        :param depth: current depth
        :param index: index for goast
        :return:
        """
        if self.terminal(gameState, depth):
            return self.evaluationFunction(gameState), None
        # best is set to positive inf, since all other values will be less than
        best = (float('inf'), None)
        for action in gameState.getLegalActions(index):
            next_state = gameState.generateSuccessor(index, action)
            # last index is set to index if it is equal to the number of indexes ( -1 since we start at 0)
            last = index == gameState.getNumAgents() - 1
            if last:
                # if last we find the max value
                action_value = self.max_value(next_state, depth + 1)
            else:
                # if not we continue recursive min search
                action_value = self.min_value(next_state, depth, index + 1)
            if action_value[0] < best[0]:
                # if the action value is less, we set a new best value
                best = (action_value[0], action)
        return best

    def terminal(self, gameState, depth):
        """
        Method to tell if game is ended
        :param gameState: current state
        :param depth: current depth
        :return:
        """
        return gameState.isWin() or gameState.isLose() or depth == self.depth


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alpha_beta_search(gameState)

    def alpha_beta_search(self, gameState):
        """
        returns max value with initial depth set to 0 and alpha -inf and beta inf
        :param gameState:
        :return:
        """
        return self.max_value(gameState, 0, float("-inf"), float("inf"))[1]

    def max_value(self, gameState, depth, alpha, beta):
        """
        :param gameState: current state
        :param depth: current depth
        :param alpha: alpha value
        :param beta: beta value
        :return:
        """
        if self.terminal(gameState, depth):
            return self.evaluationFunction(gameState), None
        best = (float('-inf'), None)
        for action in gameState.getLegalActions(self.index):
            next_state = gameState.generateSuccessor(self.index, action)
            action_value = self.min_value(next_state, depth, 1, alpha, beta)
            if action_value[0] > best[0]:
                best = (action_value[0], action)
            # the new alpha is the maximum value between current alpha and action value
            alpha = max(alpha, action_value[0])
            # if alpha is greater than beta we return best
            if alpha > beta:
                return best
        return best

    def min_value(self, gameState, depth, index, alpha, beta):
        if self.terminal(gameState, depth):
            return self.evaluationFunction(gameState), None
        best = (float('inf'), None)
        n = gameState.getNumAgents()
        for action in gameState.getLegalActions(index):
            next_state = gameState.generateSuccessor(index, action)
            last = index == n - 1
            if last:
                action_value = self.max_value(next_state, depth + 1, alpha, beta)
            else:
                action_value = self.min_value(next_state, depth, index + 1, alpha, beta)
            if action_value[0] < best[0]:
                best = (action_value[0], action)
            # the new beta is the maximum value between current beta and action value
            beta = min(beta, action_value[0])
            if beta < alpha:
                # if beta is greater than beta we return best
                return best
        return best

    def terminal(self, gameState, depth):
        return gameState.isWin() or gameState.isLose() or depth == self.depth

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
