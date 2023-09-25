
import os
import random
import time

from const import *

def terminal_size():
    import subprocess
    rows, columns = subprocess.check_output(['tput', 'lines']), subprocess.check_output(['tput', 'cols'])
    return int(rows), int(columns)

def map(x, a, b, c, d):
    return c + (x - a) * (d - c) / (b - a)

def getTime():
    T = time.time()
    local_time = time.localtime(T)
    return time.strftime("%H:%M:%S", local_time)

VARIABLES = []

class Variable:
    def __init__(self, **kwargs):
        self.key, self.value = list(kwargs.items())[0]
        self.color = kwargs.get("color") if "color" in kwargs else ""

        VARIABLES.append(self)

    def setValue(self, new_value):
        self.value = new_value

    def __name__(self):
        return self.key

    def __call__(self):
        return self.value
    
    def __str__(self):
        return str(self.color) + str(self.key) + " : " + str(self.value) + ENDC
    
    def __repr__(self):
        return str(self.color) + str(self.key) + " : " + str(self.value) + ENDC
    
    def setPrintColor(self, color = ""):
        self.color = color

    def cut(self):
        VARIABLES.remove(self)
        del self

    # def __del__(self):
    #     print(f"{self} is being deallocated")
    #     VARIABLES.remove(self)


class NumericVariable(Variable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def incValue(self, inc = 1):
        self.value += inc



class PumpkinPi:

    def __init__(self, clear = True,):
        if(clear):
            print("\033[2J\033[H\n")
        
        self.height, self.width = terminal_size()
        
        self.num_rows = self.height
        self.num_cols = self.width
        
        self.main_section = Section(0, 0, self.width, self.height, draw_border = True, draw_logo = True, multi_pass = False, label = "main")



class Section:

    def __init__(self, start_row, start_col, width, height, draw_border = True, draw_logo = False, multi_pass = False, label = ""):
        
        self.start_row = start_row
        self.start_col = start_col
        self.num_rows = height
        self.num_cols = width

        self.draw_logo = draw_logo

        self.dependencies = []

        if(not multi_pass):
            self.num_rows -= 1

        self.print_matrix = [[" " for _ in range(self.num_cols)] for _ in range(self.num_rows)]

        if(draw_border):
            self.drawFullBorder()

        self.label = label


    def __repr__(self):
        return self.label
    

    def __str__(self):
        return self.label
    
    def setPrintLayer(self, layer):
        self.print_layer = layer
    

    def requestChanges(self, overwriteBorder = True):
        if(not hasattr(self, "print_layer")):
            self.print_layer = float('inf')

        Payload = []

        if(overwriteBorder):
            self.drawFullBorder()
        
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                char = self.print_matrix[row][col]
                Payload.append({"row": self.start_row + row, "col": self.start_col + col, "char": char, "layer": self.print_layer})

        return Payload
    

    # def computeDependants(self, parent = None):
        
    #     if(len(self.dependencies) == 0):
    #         Payload = self.requestChanges()
    #         changes = []
    #         for package in Payload:
    #             changes.append({
    #                 "row": (package.get("row") + parent.start_row),
    #                 "col": (package.get("col") + parent.start_col),
    #                 "char": package.get("char"),
    #                 "layer": package.get("layer")
    #             })

    #         return changes

    #     changes = self.requestChanges()
        
    #     for dep in self.dependencies:
    #         changes.extend(dep.computeDependants(self))

    #     return changes
    

    # def getChanges(self):

    #     changes = self.computeDependants()
        
    #     aggregate = [["[NONE]" for _ in range(self.num_cols)] for _ in range(self.num_rows)]
    #     push = []

    #     for change in changes:
    #         row = change.get("row")
    #         col = change.get("col")
    #         char = change.get("char")
    #         layer = change.get("layer")
            
    #         if(aggregate[row][col] == "[NONE]"):
    #             aggregate[row][col] = {"row": row, "col": col, "char": char, "layer": layer}

    #         else:
    #             if(layer <= aggregate[row][col].get("layer")):
    #                 aggregate[row][col] = {"row": row, "col": col, "char": char, "layer": layer}

    #     for row in range(self.num_rows):
    #         for col in range(self.num_cols):
    #             if(aggregate[row][col] != "[NONE]"):
    #                 push.append(aggregate[row][col])

    #     return push

    def writeVariables(self, start_row, start_col):
        current_row = start_row
        header = "[ VARIABLES ]"
        self.setString(header, current_row, start_col)
        current_row += 1

        if(len(VARIABLES) == 0):
            return

        max_key_length = max(len(header) - 2, (max(len(str(V.key)) for V in VARIABLES) + 2)) # +2 for brackets
        # max_val_length = max(len(str(V.value)) for V in VARIABLES)

        self.setString("=" + ("-" * max_key_length) + "=", current_row, start_col)
        current_row += 1
        
        for var in VARIABLES:
            color = var.color
            key = var.key
            value = var.value

            pre = "[" + str(key) + "]"
            preL = len(pre)
            preS = " " * (max_key_length - preL)

            post = str(value)
            # postL = len(post)
            # postS = " " * (max_val_length - postL)
            
            string = pre + preS + " : " + post
            self.setString(string, current_row, start_col, None, False, False, color)

            current_row += 1


    def update(self):
        self.print_matrix = [[" " for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        self.drawFullBorder()
        self.writeVariables(2, 4)
        

    def step(self, buffer_ = True, buffer_seconds_ = 0.1, final_ = False):
        self.update()
        self.setString(getTime(), 0, 3, color = LIGHT_GRAY)
        
        self.writeFrame(buffer = buffer_, buffer_seconds = buffer_seconds_, final = final_)


    def stop(self):
        self.step(final_ = True)


    def __del__(self):
        self.step(final_ = True)


    def writeFrame(self, buffer = True, buffer_seconds = 0.1, final = False):
        
        if(buffer):
            time.sleep(buffer_seconds)
        
        def print_overwrite(lines, final = False):
            
            print(f'\033[{len(lines)}A', end='')
            for line in lines:
                print(f'\r{line: <{self.num_cols}}')

            if(not final):
                print(f'\033[{len(lines)}A', end='')

        lines = []

        for row in self.print_matrix:
            temp_line = ""
            for col in row:
                temp_line += str(col)
            lines.append(temp_line)

        print_overwrite(lines, final)
        return

        


    def checkBounds(self, row = 0, col = 0):
        return row >= 0 and row < self.num_rows and col >= 0 and col < self.num_cols


    def convertChanges(self):

        changes = self.getChanges()

        for change in changes:
            row = change.get("row")
            col = change.get("col")
            char = change.get("char")

            self.setChar(char, row, col)


    def setChar(self, char, row, col, color = ""):
        if(self.checkBounds(row, col)):
            self.print_matrix[row][col] = color + char + ENDC


    def setRow(self, char, row, start_col = None, end_col = None, color = ""):
        if(self.checkBounds(row = row)):

            if(start_col == None): start_col = 0
            if(end_col == None): end_col = self.num_cols

            for col in range(start_col, end_col):
                self.setChar(char, row, col, color)


    def setCol(self, char, col, start_row = None, end_row = None, color = ""):
        if(self.checkBounds(col = col)):

            if(start_row == None): start_row = 0
            if(end_row == None): end_row = self.num_rows
            
            for row in range(start_row, end_row):
                self.setChar(char, row, col, color)


    def placeLogo(self, color = ""):
        
        if(hasattr(self, "logo_config")):
            return

        # try:
        #     if(self.logo_config):
        #         return
        # except Exception as e:
        #     pass

        LOGO = f" Pi. v0.1 r:{self.num_rows}, c:{self.num_cols}"

        config = {
            "LOGO": LOGO,
            "color": color
        }
        
        row = -1
        col = -1
        drawVertical = False

        if(round(random.random()) == 1):
            row = int( map( random.random(), 0, 1, 1, (self.num_rows - len(LOGO) - 1) ) )
            col = round(random.random()) * (self.num_cols - 1)
            drawVertical = True
        else:
            col = int( map( random.random(), 0, 1, int(self.num_cols / 3), (self.num_cols - len(LOGO) - 1) ) )
            row = round(random.random()) * (self.num_rows - 1)
            drawVertical = False

        config["row"] = row
        config["col"] = col
        config["drawVertical"] = drawVertical
        
        self.logo_config = config


    def drawFullBorder(self):
        self.drawBorder(0, 0, "full", "full", DARK_GRAY)

        if(self.draw_logo):
            self.placeLogo(ORANGE)
            
            LOGO =              self.logo_config.get("LOGO")
            row =               self.logo_config.get("row")
            col =               self.logo_config.get("col")
            drawVertical =      self.logo_config.get("drawVertical")
            color =             self.logo_config.get("color")

            self.setString(LOGO, row, col, drawVertical = drawVertical, color = color)

            
    def computeEndRowCol(self, start_row, start_col, width, height):

        end_row = 0
        end_col = 0

        if(str(width).lower() == "full"):
            width = self.num_cols - start_col - 1

        if(str(height).lower() == "full"):
            height = self.num_rows - start_row - 1

        if(width >= 0):
            end_col = (start_col + width)
        else:
            end_col = (self.num_cols + width) - 1

        if(height >= 0):
            end_row = (start_row + height)
        else:
            end_row = (self.num_rows + height) - 1

        return end_row, end_col

    
    def drawBorder(self, start_row, start_col, width, height, color = ""):
        
        end_row, end_col = self.computeEndRowCol(start_row, start_col, width, height)

        self.setRow("-", start_row,         start_col = start_col, end_col = end_col, color = color)
        self.setRow("-", end_row,           start_col = start_col, end_col = end_col, color = color)
        self.setCol("|", start_col,         start_row = start_row, end_row = end_row, color = color)
        self.setCol("|", end_col,           start_row = start_row, end_row = end_row, color = color)

        self.setChar("+", start_row, start_col, color)
        self.setChar("+", end_row, start_col, color)
        self.setChar("+", start_row, end_col, color)
        self.setChar("+", end_row, end_col, color)



    def setString(self, string, start_row, start_col, cutoff = None, drawVertical = False, reverse = False, color = ""):
        
        if(self.checkBounds(start_row, start_col)):

            if(reverse):
                string = string[::-1]
            
            distance = min(cutoff, len(string)) if(cutoff != None) else len(string)

            for index in range(distance):
                char = string[index]
                if(drawVertical):
                    self.setChar(char, start_row + index, start_col, color = color)
                else:
                    self.setChar(char, start_row, start_col + index, color = color)









# class Section:

#     def __init__(self, start_row, start_col, width, height, draw_border = True, draw_logo = False, multi_pass = False, label = ""):
        
#         self.num_rows = height
#         self.num_cols = width

#         self.start_row = start_row
#         self.start_col = start_col
#         self.width = width
#         self.height = height

#         self.dependencies = []
#         self.print_matrix = [[" " for _ in range(self.num_cols)] for _ in range(self.num_rows)]

#         if(not multi_pass):
#             self.num_rows -= 1

#         if(draw_border):
#             self.drawFullBorder(draw_logo)

#         self.label = label


#     def __repr__(self):
#         return self.label
    

#     def __str__(self):
#         return self.label


#     def setPrintLayer(self, layer):
#         self.print_layer = layer
    

#     def requestChanges(self):
#         if(not hasattr(self, "print_layer")):
#             self.print_layer = float('inf')

#         Payload = []
#         for row in range(self.num_rows):
#             for col in range(self.num_cols):
#                 char = self.print_matrix[row][col]
#                 Payload.append({"row": self.start_row + row, "col": self.start_col + col, "char": char, "layer": self.print_layer})

#         return Payload
    

#     def computeDependants(self, parent = None):
        
#         if(len(self.dependencies) == 0):
#             Payload = self.requestChanges()
#             changes = []
#             for package in Payload:
#                 changes.append({
#                     "row": (package.get("row") + parent.start_row),
#                     "col": (package.get("col") + parent.start_col),
#                     "char": package.get("char"),
#                     "layer": package.get("layer")
#                 })

#             return changes

#         changes = self.requestChanges()
        
#         for dep in self.dependencies:
#             changes.extend(dep.computeDependants(self))

#         return changes
    

#     def getChanges(self):

#         changes = self.computeDependants()
        
#         aggregate = [["[NONE]" for _ in range(self.num_cols)] for _ in range(self.num_rows)]
#         push = []

#         for change in changes:
#             row = change.get("row")
#             col = change.get("col")
#             char = change.get("char")
#             layer = change.get("layer")
            
#             if(aggregate[row][col] == "[NONE]"):
#                 aggregate[row][col] = {"row": row, "col": col, "char": char, "layer": layer}

#             else:
#                 if(layer <= aggregate[row][col].get("layer")):
#                     aggregate[row][col] = {"row": row, "col": col, "char": char, "layer": layer}

#         for row in range(self.num_rows):
#             for col in range(self.num_cols):
#                 if(aggregate[row][col] != "[NONE]"):
#                     push.append(aggregate[row][col])

#         return push


#     def printSection(self):
#         for row in range(self.num_rows):
#             for col in range(self.num_cols):
#                 print(self.print_matrix[row][col], end = "")
#             print()


#     def checkBounds(self, row = 0, col = 0):
#         return row >= 0 and row < self.num_rows and col >= 0 and col < self.num_cols


#     def convertChanges(self):

#         changes = self.getChanges()

#         for change in changes:
#             row = change.get("row")
#             col = change.get("col")
#             char = change.get("char")

#             self.setChar(char, row, col)


#     def setChar(self, char, row, col, color = ""):
#         if(self.checkBounds(row, col)):
#             self.print_matrix[row][col] = color + char + ENDC


#     def setRow(self, char, row, start_col = None, end_col = None, color = ""):
#         if(self.checkBounds(row = row)):

#             if(start_col == None): start_col = 0
#             if(end_col == None): end_col = self.num_cols

#             for col in range(start_col, end_col):
#                 self.setChar(char, row, col, color)


#     def setCol(self, char, col, start_row = None, end_row = None, color = ""):
#         if(self.checkBounds(col = col)):

#             if(start_row == None): start_row = 0
#             if(end_row == None): end_row = self.num_rows
            
#             for row in range(start_row, end_row):
#                 self.setChar(char, row, col, color)


#     def placeLogo(self, color = ""):
        
#         if(hasattr(self, "logo_config")):
#             return

#         # try:
#         #     if(self.logo_config):
#         #         return
#         # except Exception as e:
#         #     pass

#         LOGO = f" Pi. v0.1 r:{self.num_rows}, c:{self.num_cols}"

#         config = {
#             "LOGO": LOGO,
#             "color": color
#         }
        
#         row = -1
#         col = -1
#         drawVertical = False

#         if(round(random.random()) == 1):
#             row = int( map( random.random(), 0, 1, 1, (self.num_rows - len(LOGO) - 1) ) )
#             col = round(random.random()) * (self.num_cols - 1)
#             drawVertical = True
#         else:
#             col = int( map( random.random(), 0, 1, 1, (self.num_cols - len(LOGO) - 1) ) )
#             row = round(random.random()) * (self.num_rows - 1)
#             drawVertical = False

#         config["row"] = row
#         config["col"] = col
#         config["drawVertical"] = drawVertical
#         self.logo_config = config


#     def drawFullBorder(self, logo = True):
#         self.drawBorder(0, 0, "full", "full", DARK_GRAY)

#         if(logo):
#             self.placeLogo(ORANGE)
            
#             LOGO =              self.logo_config.get("LOGO")
#             row =               self.logo_config.get("row")
#             col =               self.logo_config.get("col")
#             drawVertical =      self.logo_config.get("drawVertical")
#             color =             self.logo_config.get("color")

#             self.setString(LOGO, row, col, drawVertical = drawVertical, color = color)

            
#     def computeEndRowCol(self, start_row, start_col, width, height):

#         end_row = 0
#         end_col = 0

#         if(str(width).lower() == "full"):
#             width = self.num_cols - start_col - 1

#         if(str(height).lower() == "full"):
#             height = self.num_rows - start_row - 1

#         if(width >= 0):
#             end_col = (start_col + width)
#         else:
#             end_col = (self.num_cols + width) - 1

#         if(height >= 0):
#             end_row = (start_row + height)
#         else:
#             end_row = (self.num_rows + height) - 1

#         return end_row, end_col

    
#     def drawBorder(self, start_row, start_col, width, height, color = ""):
        
#         end_row, end_col = self.computeEndRowCol(start_row, start_col, width, height)

#         self.setRow("-", start_row,         start_col = start_col, end_col = end_col, color = color)
#         self.setRow("-", end_row,           start_col = start_col, end_col = end_col, color = color)
#         self.setCol("|", start_col,         start_row = start_row, end_row = end_row, color = color)
#         self.setCol("|", end_col,           start_row = start_row, end_row = end_row, color = color)

#         self.setChar("+", start_row, start_col, color)
#         self.setChar("+", end_row, start_col, color)
#         self.setChar("+", start_row, end_col, color)
#         self.setChar("+", end_row, end_col, color)


#     def setString(self, string, start_row, start_col, cutoff = None, drawVertical = False, reverse = False, color = ""):
        
#         if(self.checkBounds(start_row, start_col)):

#             if(reverse):
#                 string = string[::-1]
            
#             distance = min(cutoff, len(string)) if(cutoff != None) else len(string)

#             for index in range(distance):
#                 char = string[index]
#                 if(drawVertical):
#                     self.setChar(char, start_row + index, start_col, color = color)
#                 else:
#                     self.setChar(char, start_row, start_col + index, color = color)



