ENDC                = "\033[0m"

RESET               = "\033[0m"       
BOLD                = "\033[1m"   
FAINT               = "\033[2m"     
ITALIC              = "\033[3m"        
UNDERLINE           = "\033[4m"     
BLINK_SLOW          = "\033[5m"    
BLINK_FAST          = "\033[6m"    
INVERSE             = "\033[7m"    
CONCEAL             = "\033[8m"    
STRIKETHROUGH       = "\033[9m"       

PINK                = "\033[94m"
MAGENTA             = "\033[35m"
CYAN                = "\033[36m"
LIGHT_CYAN          = "\033[96m"
GREEN               = "\033[92m"
DARK_YELLOW         = "\033[33m"
LIGHT_YELLOW        = "\033[93m"
ORANGE              = "\033[38;5;208m"
RED                 = "\033[91m"

WHITE               = "\033[37m"
BLACK               = "\033[30m"
LIGHT_GRAY          = "\033[37m"
DARK_GRAY           = "\033[90m"



ALL_COLORS = [
    PINK         ,        
    MAGENTA      ,        
    CYAN         ,        
    LIGHT_CYAN   ,        
    GREEN        ,        
    DARK_YELLOW  ,        
    LIGHT_YELLOW ,        
    ORANGE       ,
    RED          ,        
    WHITE        ,        
    BLACK        ,        
    LIGHT_GRAY   ,        
    DARK_GRAY
]



def rgb_to_ansi256(r, g, b):

    # First, scale the RGB values to the range [0, 5]
    r = round(r * 5 / 255)
    g = round(g * 5 / 255)
    b = round(b * 5 / 255)

    # Then, compute the color index
    ansi = 16 + (36 * r) + (6 * g) + b
    return f"\033[38;5;{ansi}m"















