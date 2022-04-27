# Import list
from os import name, system
from random import choice, random
from time import sleep

''' Starting Stuff '''
# Rule class
class Rule ():
    # Initialize object (using birth / survive notation; cell options, # for next stage, probability of birth / survive / next)
    def __init__(self, b, s, c, n = [0, 1], pb = 1, ps = 0, pn = 1):
        self.birth = b
        self.survive = s
        self.next = n
        self.options = c
        self.prob_b = pb
        self.prob_s = ps
        self.prob_n = pn
        pass
    pass

# Clear function
def clear():
    # If Windows, else for Mac and Linux
    if name == 'nt': _ = system('cls')
    else: _ = system('clear')
    pass

# Random state generator (dimenions, cell options)
def rsg (side, cellopt = [0, 1]):
    state = []
    for i in range(side):
        state.append([])
        for j in range(side): state[i].append(choice(cellopt))
    return state

# Parser
def parser (ls, speed, symopt, cellopt):
    # Determine the speed
    if speed != 0: speed **= -1

    # Output
    out = ''

    # For every row in the list,
    for row in ls:
        # For every value in the row,
        for value in row:
            # For every option,
            for o in range(len(cellopt)):
                # Substitute the corresponding symbol
                if value == cellopt[o]: out += symopt[o]
                pass
            # Add a space
            out += ' '
            pass
        # Add a new line
        out += '\n'
        pass

    # Clear screen, print the state, and wait.
    clear()
    print(out)
    sleep(speed)
    pass

''' CA Methods '''
# CA (size of strip, generations, Wolfram rule, cell options)
def ca (size, gen, rule, speed = 0, symbs = [':', '#']):
    # Youngest and oldest states
    jungest = rule.options[0]
    oldest = rule.options[-1]

    # The initial state is random
    state = rsg(size, rule.options)

    # Parse the initial state and wait two seconds
    parser(state, 0.5, symbs, rule.options)

    # Every generation...
    for g in range(gen):
        # Redefine the new state
        newstate = []

        # For row index in the state
        for rinx in range(len(state)):
            # Add a row onto the new state
            newstate.append([])

            # For every value index in each row,
            for vinx in range(len(state[0])):
                # Current position
                pos = state[rinx][vinx]

                # Alive cells per neighbourhood
                alive = 0

                # Define its neighbourhood
                neigh = [state[rinx - 1][vinx - 1], state[rinx - 1][vinx], state[rinx - 1][(vinx + 1) % len(state[0])], state[rinx][vinx - 1],
                        state[rinx][(vinx + 1) % len(state[0])], state[(rinx + 1) % len(state[0])][vinx - 1], state[(rinx + 1) % len(state[0])][vinx],
                        state[(rinx + 1) % len(state[0])][(vinx + 1) % len(state[0])]]
                
                # Count the number of alive cells in its neighbourhood
                for cell in neigh:
                    if cell != jungest: alive += 1
                    pass

                # Evolve according to the rule
                if pos == jungest and alive in rule.birth and random() <= rule.prob_b: pos += 1
                elif pos == oldest and alive not in rule.survive and random() >= rule.prob_s: pos = jungest
                elif pos != jungest and pos != oldest and random() <= rule.prob_n: pos += 1

                # Add the position to the state's row
                newstate[rinx].append(pos)
                pass
            pass
        # Set the current state and parse it
        state = newstate
        parser(state, speed, symbs, rule.options)
        pass
    return None

''' Debug Tools '''
# List printing
def lprint (l):
    for i in l: print(i)
    pass

''' Important Stuff '''
# Main method
if __name__ == '__main__':
    # Default settings
    gridsize = 20
    gen = 100
    speed = 20
    rule = None

    # User input
    uin = ''

    # While the user wishes not to quit
    while uin != '3':
        # Reset the symbol set
        symbols = ['.', '#']

        # Clear screen
        clear()

        # User menu
        print('Menu:' + '\n' +
                '(1) Change Settings\n' +
                '(2) Select a Preset\n' +
                '(3) Quit\n' +
                '-- Settings: --\n' +
                'Grid size: %g\nGenerations: %g\nSpeed: %g ms [%g]\n' %(gridsize, gen, round(1000 / speed, 2), speed) +
                '--')
        uin = input('Please select an option: ')

        # Response validation
        # Settings
        if uin == '1':
            gridsize = int(input('How big should the grid be? (side length): '))
            gen = int(input('How many generations should be simulated? '))
            speed = int(input('How quickly should it go? (the larger, the faster; but 0 is fastest): '))
            input('Your settings have been applied. Press enter to continue.')
            pass
        # Presets
        elif uin == '2':
            # While the response is invalid
            while uin not in ['A', 'B', 'C', 'D']:
                # Clear screen
                clear()

                # Preset menu
                print('Presets: \
                \n(A) Conway\'s Game of Life \
                \n(B) Fluid Conway \
                \n(C) Day & Night (1977, N. Thompson & D. Bell) \
                \n(D) Basic Wildfire')
                uin = input('--\nPlease select an option: ')

                # Input validation
                # Conway's Game of Life and Day & Night
                if uin == 'A': rule = Rule([3], [2, 3], [0, 1])
                elif uin == 'C': rule = Rule([3, 6, 7, 8], [3, 4, 6, 7, 8], [0, 1])
                # Fluid Conway
                elif uin == 'B':
                    rule = Rule([3], [2, 3], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
                    symbols = [':', '!', '?', '$', '#']
                    pass
                # Basic Wildfire
                elif uin == 'D':
                    rule = Rule([0, 1, 2, 3, 4, 5, 6, 7, 8], [], [0, 1, 2], [1, 2, 3, 4, 5, 6, 7, 8], 0.5, 0.1, 0.6)
                    symbols = [':', 'T', '#']
                    pass
                # Call the automata
                ca(gridsize, gen, rule, speed, symbols)
                input('Press enter to continue. ')
            pass
        # Quit
        elif uin == '3':
            break
    pass