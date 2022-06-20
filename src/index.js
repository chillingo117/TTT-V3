import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import CreateApiInstance from './api';
import {Grid, Box, Stack} from "@mui/material";

function Square(props) {
    return (
        <button className="square" onClick={props.onClick}>
            {props.value}
        </button>
    );
}

class SubBoard extends React.Component {
    renderSquare(squareIndex) {
        return (
            <Square
                value={this.convertToSymbol(this.props.squares[squareIndex])}
                onClick={() => this.props.onClick(squareIndex)}
            />
        );
    }

    convertToSymbol(squareValue) {
        switch (squareValue){
            case 1:
                return "X";
            case -1:
                return "O";
            default:
                return "";
        }
    }
    
    render() {
        let style;
        if(this.props.isCurrent)
            style = { border: 3, borderColor: "Red"};
        else
            style = { border: 3 };
        console.log(this.props.isCurrent)
        return (
            <Box sx={style}>
                <Stack>
                    <Grid item className="board-row">
                        <Stack direction="row">
                            <div>{this.renderSquare(0)}</div>
                            <div>{this.renderSquare(1)}</div>
                            <div>{this.renderSquare(2)}</div>
                        </Stack>
                    </Grid>
                    <Grid item className="board-row">
                        <Stack direction="row">
                            <div>{this.renderSquare(3)}</div>
                            <div>{this.renderSquare(4)}</div>
                            <div>{this.renderSquare(5)}</div>
                        </Stack>
                    </Grid>
                    <Grid item className="board-row">
                        <Stack direction="row">
                            <div>{this.renderSquare(6)}</div>
                            <div>{this.renderSquare(7)}</div>
                            <div>{this.renderSquare(8)}</div>
                        </Stack>
                    </Grid>
                </Stack>
            </Box>
        );
    }
}

class SuperBoard extends React.Component {
    renderSubBoard(subBoardIndex) {
        return (
            <SubBoard
                isCurrent={this.props.currentBoard === subBoardIndex}
                squares={this.props.subBoards[subBoardIndex].squares}
                onClick={squareIndex => this.props.onClick(subBoardIndex, squareIndex)}
            />
        );
    }
    render() {
        return (
            <Stack>
                <Grid item className="super-board-row">
                    <Stack direction="row">
                        <div>{this.renderSubBoard(0)}</div>
                        <div>{this.renderSubBoard(1)}</div>
                        <div>{this.renderSubBoard(2)}</div>
                    </Stack>
                </Grid>
                <Grid item className="super-board-row">
                    <Stack direction="row">
                        <div>{this.renderSubBoard(3)}</div>
                        <div>{this.renderSubBoard(4)}</div>
                        <div>{this.renderSubBoard(5)}</div>
                    </Stack>
                </Grid>
                <Grid item className="super-board-row">
                    <Stack direction="row">
                        <div>{this.renderSubBoard(6)}</div>
                        <div>{this.renderSubBoard(7)}</div>
                        <div>{this.renderSubBoard(8)}</div>
                    </Stack>
                </Grid>
            </Stack>
        );
    }
}

class Game extends React.Component {
    constructor(props) {
        super(props);
        this.loading = true;
        this.state = null;
        this.gameID = null;
        this.api = CreateApiInstance();
        this.newGame();
        this.preparePing();
    }

    preparePing() {
        setTimeout(() => {
            if(this.gameID != null){
                this.api.pingGame(this.gameID).then(() => this.preparePing());
            }
            else
            {
                this.preparePing();
            }
        }, 10000);
    }
    
    newGame(){
        let initialState = {
            history: [],
            currentBoard: 4,
            stepNumber: 0,
            winner: 0
        }
        this.api.createGame()
                .then(gameID => {
                    this.gameID = gameID;
                    return gameID;
                })
                .then(gameID => {
                    return this.api.getGame(gameID);
                })
                .then(state => {
                    initialState.history.push(JSON.stringify(state));
                    this.setState(initialState);
                    this.loading = false;
                });
    }

    handleClick(subBoardIndex, squareIndex) {
        const history = this.state.history.slice(0, this.state.stepNumber + 1);
        const current = JSON.parse(history[history.length - 1]);

        if (current.winner !== 0 
            || subBoardIndex !== current.currentSubBoard
            || current.subBoards[current.currentSubBoard].squares[squareIndex] !== 0) {
            return;
        }

        this.api.playGame(this.gameID, squareIndex)
            .then(response => {
                history.push(JSON.stringify(response));
                this.setState({
                    history: history,
                    currentBoard: response.currentSubBoard,
                    stepNumber: history.length - 1,
                    winner: response.winner
                });
                console.log(this.state)
            })
    }

    jumpTo(step) {
        console.log(this.state);
        let revertedHistory = this.state.history.slice(0, step+1);
        console.log(step)
        console.log(revertedHistory);

        this.setState({
            history: revertedHistory,
            stepNumber: step,
            winner: revertedHistory[step].winner
        });
    }
// <!--
// <ol>{moves}</ol>
// </Stack>
// -->
    render() {
        if(!this.loading)
        {
            const history = this.state.history;
            const current = JSON.parse(history[this.state.stepNumber]);
            const winner = current.winner;
            const moves = history.map((step, move) => {
                const desc = move ?
                    'Go to move #' + move :
                    'Go to game start';
                return (
                    <li key={move}>
                        <button onClick={() => this.jumpTo(move)}>{desc}</button>
                    </li>
                );
            });

            let status;
            if (winner !== 0) {
                status = "Winner: " + winner;
            } else {
                status = "Next player: " + (this.state.currentPlayer === 1 ? "X" : "O");
            }

            return (
                <Box sx={{ flexGrow: 1 }}>
                    <Stack direction="row" className="game" >
                        <SuperBoard
                            currentBoard={this.state.currentBoard}
                            subBoards={current.subBoards}
                            onClick={(subBoardIndex, squareIndex) => this.handleClick(subBoardIndex, squareIndex)}
                        />
                        <Stack>
                            <div className="status">{status}</div>
                        </Stack>

                    </Stack>
                </Box>
            );
        }
        else{
            return(<div>loading</div>);
        }
    }
}

// ========================================

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Game />);

