from flask import *
from TicTacToe import TTTInstance
from Constants import *
import ErrorHandlers


class App:

    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["DEBUG"] = True

        self.Instances = []
        self.ClosedIDs = []

        @self.app.route("/game/create", methods=["GET"])
        def createGame():
            passed, error = validatePrettyBoards(request.args)
            if not passed:
                return error

            if request.args["pretty"] == "True":
                prettyBoards = True
            else:
                prettyBoards = False

            if len(self.ClosedIDs) != 0:
                instanceID = self.ClosedIDs.pop()
                self.Instances[instanceID] = TTTInstance(prettyBoards)
            else:
                if len(self.Instances) >= MAX_GAMES:
                    ErrorHandlers.insufficient_resources(
                        "Max number of concurrent game has been hit. Try play again later.")
                    return
                else:
                    self.Instances.append(TTTInstance(prettyBoards))
                    instanceID = len(self.Instances) - 1

            print("Game created with ID: " + str(instanceID))
            return str(instanceID)

        @self.app.route("/game/close", methods=["GET"])
        def closeGame():
            passed, error = validateIDInput(request.args)
            if not passed:
                return error
            instanceID = int(request.args["id"])
            self.Instances[instanceID].close()

        @self.app.route("/game/play", methods=["GET"])
        def playGame():
            passed, error = validateIDInput(request.args)
            if not passed:
                return error
            passed, error = validateXYInput(request.args)
            if not passed:
                return error

            instanceID = int(request.args["id"])
            x = int(request.args["x"])
            y = int(request.args["y"])
            instance = self.Instances[instanceID]

            passed, error = validatePlay(instance, x, y)
            if not passed:
                return error

            instance.play(x, y)
            return instance.getBoard()

        @self.app.route("/game", methods=["GET"])
        def getGame():
            passed, error = validateIDInput(request.args)
            if not passed:
                return error

            instanceID = int(request.args["id"])
            return self.Instances[instanceID].getBoard()

        def validateIDInput(args):
            if "id" not in args:
                return False, ErrorHandlers.bad_request("Please provide the game ID")
            try:
                instanceID = int(args["id"])
            except ValueError:
                return False, ErrorHandlers.bad_request("Game ID provided was not a number")

            if instanceID < 0 or instanceID >= len(self.Instances) or instanceID in self.ClosedIDs:
                return False, ErrorHandlers.not_found("Ongoing game with ID " + str(instanceID) + " was not found.")

            return True, None

        def validateXYInput(args):
            if "x" not in args or "y" not in args:
                return False, ErrorHandlers.bad_request("Please provide the X and Y of the intended play.")
            try:
                x = int(args["x"])
                y = int(args["y"])
            except ValueError:
                return False, ErrorHandlers.bad_request("X and/or Y provided not number")

            if x < 0 or x > 2 or y < 0 or y > 2:
                return False, ErrorHandlers.bad_request("X and/or Y provided was out of bounds")

            return True, None

        def validatePlay(instance, x, y):
            gameEnded, winner = instance.hasGameBeenWon()
            if gameEnded:
                return False, ErrorHandlers.bad_request("Game has already been won by " + winner)

            if not instance.isCurrentSubBoardCellBlank(x, y) and not instance.isCurrentSubBoardFull():
                return False, ErrorHandlers.bad_request("Chosen cell has already been played in!")

            return True, None

        def validatePrettyBoards(args):
            if "pretty" not in args:
                return False, ErrorHandlers.bad_request("Please provide args for pretty board.")
            if args["pretty"] == "False" or args["pretty"] == "True":
                return True, None
            else:
                return False, ErrorHandlers.bad_request("Please enter 'False' or 'True' for arg 'pretty'.")

    def run(self):
        self.app.run()
