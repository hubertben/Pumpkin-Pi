
import pumpkin as PI
import random
import time

from const import *


pi = PI.PumpkinPi()

# pi.main_section.setString("Hello, World!", 3, 4, color = PINK)
# pi.main_section.setString("Hello, World!", 5, 4, reverse = True)

# pi.main_section.setString("Hello, World!", 10, 4, drawVertical = True)
# pi.main_section.setString("Hello, World!", 10, 6, drawVertical = True, cutoff = 8, reverse = True)

import string

def random_string(L):
    # Define characters: uppercase, lowercase, digits, and common punctuation symbols
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(L))

X = PI.NumericVariable(This_is_a_very_very_very_very_very_very_very_very_long_label = 0, color = PINK)
Y = PI.NumericVariable(Y = 0, color = LIGHT_CYAN)

while(X() <= 5):
    X.incValue()
    Y.incValue(int(((round(random.random()) * 2) - 1) * random.random() * 50))
    pi.main_section.step(buffer_seconds_ = 1)
    
X.cut()
Y.cut()

# V = []
# for i in range(pi.num_rows - 6):
#     Z = PI.Variable(String = "", color = ORANGE)
#     V.append(Z)

# while(True):
#     pi.main_section.step(buffer_seconds_ = 0.25)
    
#     for v in V:
#         v.setValue(random_string(150))


