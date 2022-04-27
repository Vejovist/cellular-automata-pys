# Import list
import turtle

''' Simple Conversion '''
# Decimal to Binary
def dec_bin (n, b = 8):
    # Basic replacement
    binary = bin(n).replace('0b', '')

    # Convert to b-bit
    while len(binary) < b: binary = '0' + binary

    # Return result
    return binary

''' Turtle Methods '''
# Turtle Settings
def set_turtle (tup):
    turtle.up()
    turtle.setx(tup[0])
    turtle.sety(tup[1])
    turtle.setheading(tup[2])
    turtle.down()
    pass

# Drawing a square (with or without fill, colour)
def square (side, wfill = False, c = (0, 0, 0)):
    # Colour
    if wfill: turtle.fillcolor(c)
    turtle.color(c)

    # If it can be filled, start filling
    if wfill: turtle.begin_fill()

    # Actual drawing part
    for i in range(4):
        turtle.fd(side)
        turtle.right(90)
        pass

    # If it can be filled, stop
    if wfill: turtle.end_fill()
    pass

''' CA Methods '''
# Default initial state for CAs
def middle (size) -> str: return dec_bin(2 ** (size // 2), size)

# CA (size of strip, generations, Wolfram rule, initial condition)
def ca (size, gen, rule, init = None) -> list:
    # Invalid rules
    if rule > 255 or rule < 0: return None

    # Master list of states
    masterl = []

    # Ruleset
    ruleset = [['111', ''], ['110', ''], ['101', ''], ['100', ''], ['011', ''], ['010', ''], ['001', ''], ['000', '']]

    # Fill in the ruleset according to the Wolfram rule
    for bitx in range(len(ruleset)): ruleset[bitx][1] = dec_bin(rule)[bitx]

    # If the initial condition isn't given, default
    if init == None: init = middle(size)

    # Put the state in its initial first
    state = init

    # Add the initial state
    masterl.append(state)

    # Every generation...
    for g in range(gen):
        # Redefine the new state
        newstate = ''

        # For every position in the state,
        for p in range(len(state)):
            # Define the neighbourhood (with wrap-around)
            neigh = state[p - 1] + state[p] + state[(p + 1) % len(state)]
            
            # For every rule in the ruleset,
            for r in ruleset:
                # Does the neighbourhood match? If so, add the corresponding bit to the new state.
                if neigh == r[0]: newstate += r[1]
                pass
            pass
        # Set the current state and put it in the master list
        state = newstate
        masterl.append(state)
        pass
    # Return the master list
    return masterl

# Binary to picture (list of strings, square size)
def bin_pic (binlist, sq = 30):
    # Window Set-up (don't ask, it's complicated)
    w = len(binlist[0]) * sq
    h = len(binlist) * sq
    turtle.setup(width = w, height = h, startx = 0, starty = 0)
    inx = -turtle.window_width() / 2
    iny = turtle.window_height() / 2
    set_turtle((inx, iny, 0))
    turtle.setup(width = w * 1.5, height = h * 1.5, startx = 0, starty = 0)

    # For every state,
    for state in binlist:
        # For every bit in the state
        for bit in state:
            # Draw a square [filled if 1, not if 0]
            if bit == '1': square(sq, True)
            else: square(sq)

            # Move the pen over [pick it up, move, then put back down]
            turtle.up()
            turtle.fd(sq)
            turtle.down()
            pass
        # Move down to the next row
        turtle.up()
        iny -= sq
        set_turtle((inx, iny, 0))
        turtle.down()
        pass
    pass

''' Important Stuff '''
# Main method
if __name__ == '__main__':
    # Basic turtle things
    turtle.speed(0)
    turtle.shape('turtle')

    # Produce a picture
    bin_pic(ca(31, 60, 30), 10)

    # Finishing steps
    turtle.hideturtle()
    input('Press enter to close. ')
    pass