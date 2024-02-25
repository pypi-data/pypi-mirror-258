# **Monopoly MCTS AI**

Monopoly MCTS AI is a Python package that implements the Monte Carlo Tree Search (MCTS) algorithm for decision-making in simulated Monopoly games. It utilizes neural networks for strategy optimization and state evaluation, providing a framework for researching AI-driven decision-making in board games.

## **Features**

- Implementation of the Monte Carlo Tree Search (MCTS) algorithm.
- Use of neural networks (NN) for evaluating game states and making decisions.
- Simulation of Monopoly game dynamics including properties, stations, utilities, and player interactions.
- Customizable strategies for AI players.

## **Installation**
### **Option 1**
Clone this repository to your local machine:

```bash
bashCopy code
git clone https://github.com/catherineannie13/Capstone-Optimising-Monopoly-Gameplay-Strategies.git
cd monopoly-mcts-ai

```

Ensure you have Python 3.8 or later installed. It's recommended to use a virtual environment:

```bash
bashCopy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

```

Install the required dependencies:

```bash
bashCopy code
pip install -r requirements.txt

```

### **Option 2**
Run pip install -i https://pypi.org/simple/ mcts-catherineannie13==0.0.1

## **Usage**

To run a simulation of the Monopoly game with the MCTS AI, execute the following command in the root directory of the project:

```bash
bashCopy code
python -m MonopolyBoardMCTS

```

You can customize the simulation parameters within the **`MonopolyBoardMCTS.py`** script or by modifying the command-line interface (if implemented) to adjust the number of games, AI strategies, and other settings.

## **Contributing**

Contributions to the Monopoly MCTS AI project are welcome. Please follow the standard fork-and-pull request workflow on GitHub. Ensure you write or update tests as necessary.

## **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## **Acknowledgments**

- This project is inspired by the classic board game Monopoly.
- Monte Carlo Tree Search algorithm for strategic decision-making.
- Neural network implementation for state evaluation.