from tkinter import Tk, Button, Frame
import os
from PIL import Image, ImageTk

global selected_piece, playing_clr, current_pointers, current_capture_pointers

selected_piece = ""
current_pointers = []
current_capture_pointers = []
capture_pieces = []
playing_clr = "w"

board = Tk()
board.title("Chess")
board.geometry("640x640")
board.resizable(False, False)

def draw_board():
    place_x = 0
    place_y = 0
    y_index = 0
    blocks = []
    current_row = []

    for i in range(64):
        white_block = Frame(board,
                            bg="#dbc7a0",
                            height=80,
                            width=80)

        black_block = Frame(board,
                            bg="#8c5331",
                            height=80,
                            width=80)

        if place_x == 560:
            if y_index != 7:
                place_x = 0
                place_y += 80
                y_index += 1
                blocks.append(current_row)
                current_row = []
        elif i != 0:
            place_x += 80

        if y_index % 2 == 0:
            if i % 2 == 0:
                white_block.place(x=place_x, y=place_y)
                current_row.append(white_block)
            else:
                black_block.place(x=place_x, y=place_y)
                current_row.append(black_block)
        else:
            if i % 2 != 0:
                white_block.place(x=place_x, y=place_y)
                current_row.append(white_block)
            else:
                black_block.place(x=place_x, y=place_y)
                current_row.append(black_block)
    blocks.append(current_row)

    return blocks

def load_images():
    image_path = "D:\\Hassan\\Python Projects\\Other Projects\\Games\\Chess\\Chess Images"
    
    pieces = ["white pawn", "white rook", "white bishop", "white knight", "white queen", "white king", 
            "black pawn", "black rook", "black bishop", "black knight", "black queen", "black king", "pointer"]
    
    def load_image(piece_name):
        return ImageTk.PhotoImage(Image.open(os.path.join(image_path, f"{piece_name}.png")))
    
    return {piece: load_image(piece) for piece in pieces}


class Pieces:
    def __init__(self, x, y, image, color):
        self.x = x
        self.y = y
        self.color = color
        self.image = image
        self.bg, self.abg = self.get_backgrounds(self.x, self.y)

        self.opp_x = 7 - self.x
        self.opp_y = 7 - self.y
        self.flipped = False
        self.opp_bg, self.opp_abg = self.get_backgrounds(self.opp_x, self.opp_y)

        self.create_button()

    def get_coordinates(self, selected_piece):
        for y, row in enumerate(blocks):
            for x, block in enumerate(row):
                if str(block) == selected_piece:
                    return y, x

    def unselect_piece(self, selected, change_piece=False):
        if not selected and not change_piece: 
            self.remove_selected_piece()
            self.selected_piece_color_change(False)    
        
        else:
            self.selected_piece_color_change(False, True)
            self.remove_selected_piece()
            self.select_piece()

    def selected_piece_color_change(self, selected, change_piece=False):
        if not change_piece:
            if selected:
                if self.flipped:
                    self.opp_button.config(bg="#8ab3ff")
                    self.opp_button.config(activebackground="#3273ed")
                else:
                    self.button.config(bg="#8ab3ff")
                    self.button.config(activebackground="#3273ed")
            
            else:
                if self.flipped:
                    self.opp_button.config(bg=self.opp_bg)
                    self.opp_button.config(activebackground=self.opp_abg)
                else:
                    self.button.config(bg=self.bg)
                    self.button.config(activebackground=self.abg)
        else:
            current_y, current_x = self.get_coordinates(selected_piece)
            if self.flipped:
                piece = self.get_piece_at_location(7 - current_x, 7 - current_y, all_pieces)
            else:
                piece = self.get_piece_at_location(current_x, current_y, all_pieces)
            
            piece.selected_piece_color_change(False)

    def delete_piece(self, moving_piece):
        global all_pieces
        if hasattr(self, 'button'):
            self.button.destroy()

            if hasattr(self, "opp_button"):
                self.opp_button.destroy()

        elif hasattr(self, "opp_button"):
            self.opp_button.destroy()

        board.update_idletasks()

        for key, piece_list in all_pieces.items():
            if isinstance(piece_list, list):
                if self in piece_list:
                    piece_list.remove(self)
                    break
            else:
                if self == piece_list:
                    del all_pieces[key]
                    break

        if moving_piece.flipped:
            moving_piece.move_piece(7 - self.x, 7 - self.y)
        else:
            moving_piece.move_piece(self.x, self.y)

        del self
        
    def remove_selected_piece(self):
        global selected_piece, current_pointers, current_capture_pointers
        selected_piece = ""

        def remove_pointers(pointers, capture_pointers):
            global current_pointers, current_capture_pointers

            for pointer in pointers:
                pointer.destroy()
            
            if capture_pointers:

                for pointer in capture_pointers:
                    child_piece_values = pointer[0].children.values()
                    
                    if not child_piece_values:
                        continue
                    
                    capture_block = list(child_piece_values)[0]
                    capture_block["bg"] = pointer[1]
                    capture_block["activebackground"] = pointer[2]

            pointers = []
            capture_pointers = []

            current_pointers = []
            current_capture_pointers = []

            return pointers, capture_pointers

        if current_pointers != [] or current_capture_pointers != []:
            remove_pointers(current_pointers, current_capture_pointers)
            self.pointers, self.capture_pointers = remove_pointers(self.pointers, self.capture_pointers)

    def move_piece(self, new_x, new_y):
        self.button.destroy()

        if self.flipped == False:
            self.update_coordinates(new_x, new_y)

            self.bg, self.abg = self.get_backgrounds(self.x, self.y)
            self.opp_bg, self.opp_abg = self.get_backgrounds(self.opp_x, self.opp_y)
        else:
            self.opp_x = new_x
            self.opp_y = new_y

            self.update_coordinates(7 - self.opp_x, 7 - self.opp_y)
            self.opp_bg, self.opp_abg = self.get_backgrounds(self.opp_x, self.opp_y)
            self.bg, self.abg = self.get_backgrounds(self.x, self.y)
        
        self.remove_selected_piece()
        self.create_button(command=self.select_piece)
        self.flip_board()

    def get_capture_block(self, x, y, color):
        if self.flipped:
            capture_piece = self.get_piece_at_location(7 - x, 7 - y, all_pieces)
            capture_piece_color = self.get_piece_color(capture_piece)
        else:
            capture_piece = self.get_piece_at_location(x, y, all_pieces)
            capture_piece_color = self.get_piece_color(capture_piece)

        if capture_piece_color:
            if color == capture_piece_color:
                return None
            else:
                capture_block = blocks[y][x]
                capture_piece = list(capture_block.children.values())[0]

                original_bg = capture_piece["bg"]
                original_abg = capture_piece["activebackground"]
                
                if self.flipped:
                    current_capture_piece = self.get_piece_at_location(7 - x , 7 - y, all_pieces)
                else: 
                    current_capture_piece = self.get_piece_at_location(x, y, all_pieces)
                capture_piece.config(command=lambda: current_capture_piece.delete_piece(self))

                capture_piece["bg"] = "red"     
                capture_piece["activebackground"] = "dark red"

                current_capture_pointers.append((capture_block, original_bg, original_abg))
                return (capture_block, original_bg, original_abg)
    
    def get_piece_at_location(self, x, y, all_pieces):
        for piece_type, Pieces in all_pieces.items():
            if isinstance(Pieces, list):
                for piece in Pieces:
                    px = piece.x
                    py = piece.y
                    if px == x and py == y:
                        return piece
            else:
                px = Pieces.x
                py = Pieces.y
                if px == x and py == y:
                    return Pieces
        return None

    def get_piece_color(self, piece):
        if piece.flipped == True:
            if piece.color == "w":
                return "w"
            else:
                return "b"
        else:
            return piece.color

    def place_pointer(self, x, y):
        bg, abg = self.get_backgrounds(x, y)
        move_button = Button(blocks[y][x], 
                            bg=bg, 
                            activebackground=abg, 
                            relief="flat", 
                            image=images["pointer"],
                            command=lambda: self.move_piece(x, y))
        move_button.place(x=0, y=0)
        current_pointers.append(move_button)
        return move_button

    def flip_board(self):
        global playing_clr
        playing_clr = "b" if playing_clr == "w" else "w"

        for piece_type, pieces in all_pieces.items():
            if isinstance(pieces, list):
                for piece in pieces:
                    piece.flip_piece(piece.select_piece if piece.color == playing_clr else None)
            else:
                pieces.flip_piece(pieces.select_piece if pieces.color == playing_clr else None)

    def flip_piece(self, command=None):
        self.button.destroy()
        if self.flipped ==  False:
            self.create_opp_button(command)
        
        else:
            self.opp_button.destroy()
            
            if self.color == playing_clr:
                self.create_button(self.select_piece)
            else:
                self.create_button()
                
        self.flipped = not self.flipped
    
    def create_button(self, command=None):
        self.button = Button(blocks[self.y][self.x], 
                            image=self.image, 
                            bg=self.bg, 
                            activebackground=self.abg, 
                            relief="flat",
                            command=command)
        self.button.place(x=0, y=0)

    def create_opp_button(self, command=None):
        self.opp_button = Button(blocks[self.opp_y][self.opp_x], 
                                 image=self.image, 
                                 bg=self.opp_bg, 
                                 activebackground=self.opp_abg, 
                                 relief="flat",
                                 command=command)
        self.opp_button.place(x=0, y=0)

    def update_coordinates(self, x, y):
        self.x = x
        self.y = y
        self.opp_x = 7 - self.x
        self.opp_y = 7 - self.y

    def get_backgrounds(self, x, y):
        def check_active_background(bg):
            if bg == "#dbc7a0":
                return "#a18a5d"
            elif bg == "#8c5331":
                return "#61351a"
        
        bg = blocks[y][x]["bg"]
        abg = check_active_background(bg)

        return bg, abg

    def append_pointers(self, moves, knight=False):
        if not knight:
            for move in moves:
                current_x = move[0]
                current_y = move[1]

                if (8 > current_x >= 0) and (8 > current_y >= 0) and (not blocks[current_y][current_x].children):
                    self.pointers.append(self.place_pointer(current_x, current_y))
        
        else:
            for move in moves:
                current_x = move[0]
                current_y = move[1] 

                if (8 > current_x >= 0) and (8 > current_y >= 0) and (not blocks[current_y][current_x].children):
                    self.pointers.append(self.place_pointer(current_x, current_y))

                elif (8 > current_x >= 0) and (8 > current_y >= 0) and (blocks[current_y][current_x].children):
                    capture_block = self.get_capture_block(current_x, current_y, self.color)
                    if capture_block is not None:
                        self.capture_pointers.append(capture_block)

        self.selected_piece_color_change(True)


class Royal(Pieces):
    def try_moves(self, dx, dy, try_x, try_y, moves, king=False):
        try_x += dx
        try_y += dy

        while (0 <= try_x < 8) and (0 <= try_y < 8):
            current_block = blocks[try_y][try_x]

            if not current_block.children:
                moves.append((try_x, try_y))
                if not king:
                    try_x += dx
                    try_y += dy
                else:
                    if not current_block.children:
                        moves.append((try_x, try_y))
                        break
                    
                    else:
                        capture_block = self.get_capture_block(try_x, try_y, self.color)
                        if capture_block is not None:
                            self.capture_pointers.append(capture_block)
                        break
            
            else:
                capture_block = self.get_capture_block(try_x, try_y, self.color)
                if capture_block is not None:
                    self.capture_pointers.append(capture_block)
                break


class Pawns(Pieces):
    def __init__(self, x, y, image, color):
        super().__init__(x, y, image, color)
        if self.color == playing_clr:
            self.button.config(command=self.select_piece)
        
        self.pointers = []
        self.capture_pointers = []
        
    def select_piece(self):
        global selected_piece, current_pointers, current_capture_pointers

        current_x = self.opp_x if self.flipped else self.x
        current_y = self.opp_y if self.flipped else self.y
        
        if selected_piece == "":
                
            selected_piece = str(blocks[current_y][current_x])
            moves = []
            
            if (0 <= current_y - 1 < 8) and (not blocks[current_y - 1][current_x].children):
                moves.append((current_x, current_y - 1))

                if current_y == 6 and not blocks[current_y - 2][current_x].children:
                    moves.append((current_x, current_y - 2))

            if (0 <= current_y - 1 < 8) and (0 <= current_x + 1 < 8) and (blocks[current_y - 1][current_x + 1].children):
                capture_block = self.get_capture_block(current_x + 1, current_y - 1, self.color)
                if capture_block is not None:
                    self.capture_pointers.append(capture_block)

            if (0 <= current_y - 1 < 8) and (0 <= current_x - 1 < 8) and (blocks[current_y - 1][current_x - 1].children):
                capture_block = self.get_capture_block(current_x - 1, current_y - 1, self.color)
                if capture_block is not None:
                    self.capture_pointers.append(capture_block)

            self.append_pointers(moves)

        elif selected_piece == str(blocks[current_y][current_x]):
            self.unselect_piece(False)

        else:
            self.unselect_piece(False, True)
    

class Knights(Pieces):
    def __init__(self, x, y, image, color):
        super().__init__(x, y, image, color)
        if self.color == playing_clr:
            self.button.config(command=self.select_piece)
        
        self.pointers = []
        self.capture_pointers = []
 
    def select_piece(self):
        global selected_piece, current_pointers, current_capture_pointers

        current_x = self.opp_x if self.flipped else self.x
        current_y = self.opp_y if self.flipped else self.y

        if selected_piece == "":
            selected_piece = str(blocks[current_y][current_x])
            
            moves =  [(current_x + 1, current_y + 2),
                      (current_x - 1, current_y + 2),
                      (current_x + 1, current_y - 2),
                      (current_x - 1, current_y - 2),
                      (current_x + 2, current_y + 1),
                      (current_x - 2, current_y + 1),
                      (current_x + 2, current_y - 1),
                      (current_x - 2, current_y - 1)]
        
            self.append_pointers(moves, True)

        elif selected_piece == str(blocks[current_y][current_x]):
            self.unselect_piece(False)

        else:
            self.unselect_piece(False, True)


class Bishops(Royal):
    def __init__(self, x, y, image, color):
        super().__init__(x, y, image, color)
        if self.color == playing_clr:
            self.button.config(command=self.select_piece)

        self.pointers = []
        self.capture_pointers = []
        
    def select_piece(self):
        global selected_piece, current_pointers, current_capture_pointers

        current_x = self.opp_x if self.flipped else self.x
        current_y = self.opp_y if self.flipped else self.y

        if selected_piece == "":
            selected_piece = str(blocks[current_y][current_x])
            moves = []
            
            self.try_moves(-1, -1, current_x, current_y, moves) # Top left
            self.try_moves(1, -1, current_x, current_y, moves) # Top right
            self.try_moves(-1, 1, current_x, current_y, moves) # Bottom left
            self.try_moves(1, 1, current_x, current_y, moves) # Bottom right
        
            self.append_pointers(moves)

        elif selected_piece == str(blocks[current_y][current_x]):
            self.unselect_piece(False)

        else:
            self.unselect_piece(False, True)

     
class Rooks(Royal):
    def __init__(self, x, y, image, color):
        super().__init__(x, y, image, color)
        if self.color == playing_clr:
            self.button.config(command=self.select_piece)

        self.pointers = []
        self.capture_pointers = []
    
    def select_piece(self):
        global selected_piece, current_pointers, current_capture_pointers

        current_x = self.opp_x if self.flipped else self.x
        current_y = self.opp_y if self.flipped else self.y

        if selected_piece == "":
            selected_piece = str(blocks[current_y][current_x])
            moves = []
            
            self.try_moves(0, -1, current_x, current_y, moves) # Top 
            self.try_moves(0, 1, current_x, current_y, moves) # Bottom
            self.try_moves(1, 0, current_x, current_y, moves) # Right
            self.try_moves(-1, 0, current_x, current_y, moves) # Left
        
            self.append_pointers(moves)

        elif selected_piece == str(blocks[current_y][current_x]):
            self.unselect_piece(False)

        else:
            self.unselect_piece(False, True)


class Queens(Royal):
    def __init__(self, x, y, image, color):
        super().__init__(x, y, image, color)
        if self.color == playing_clr:
            self.button.config(command=self.select_piece)

        self.pointers = []
        self.capture_pointers = []
    
    def select_piece(self):
        global selected_piece, current_pointers, current_capture_pointers
        
        current_x = self.opp_x if self.flipped else self.x
        current_y = self.opp_y if self.flipped else self.y

        if selected_piece == "":
            selected_piece = str(blocks[current_y][current_x])
            moves = []
            
            self.try_moves(0, -1, current_x, current_y, moves) # Top 
            self.try_moves(0, 1, current_x, current_y, moves) # Bottom
            self.try_moves(1, 0, current_x, current_y, moves) # Right
            self.try_moves(-1, 0, current_x, current_y, moves) # Left

            self.try_moves(-1, -1, current_x, current_y, moves) # Top left
            self.try_moves(1, -1, current_x, current_y, moves) # Top right
            self.try_moves(-1, 1, current_x, current_y, moves) # Bottom left
            self.try_moves(1, 1, current_x, current_y, moves) # Bottom right
        
            self.append_pointers(moves)

        elif selected_piece == str(blocks[current_y][current_x]):
            self.unselect_piece(False)

        else:
            self.unselect_piece(False, True)


class Kings(Royal):
    def __init__(self, x, y, image, color):
        super().__init__(x, y, image, color)
        if self.color == playing_clr:
            self.button.config(command=self.select_piece)
        self.pointers = []
        self.capture_pointers = []
    
    def select_piece(self):
        global selected_piece, current_pointers, current_capture_pointers

        current_x = self.opp_x if self.flipped else self.x
        current_y = self.opp_y if self.flipped else self.y

        if selected_piece == "":
            selected_piece = str(blocks[current_y][current_x])
            moves = []
            
            self.try_moves(0, -1, current_x, current_y, moves, True) # Top
            self.try_moves(0, 1, current_x, current_y, moves, True) # Bottom
            self.try_moves(1, 0, current_x, current_y, moves, True) # Right
            self.try_moves(-1, 0, current_x, current_y, moves, True) # Left

            self.try_moves(-1, -1, current_x, current_y, moves, True) # Top left
            self.try_moves(1, -1, current_x, current_y, moves, True) # Top right
            self.try_moves(-1, 1, current_x, current_y, moves, True) # Bottom left
            self.try_moves(1, 1, current_x, current_y, moves, True) # Bottom right
        
            self.append_pointers(moves)

        elif selected_piece == str(blocks[current_y][current_x]):
            self.unselect_piece(False)

        else:
            self.unselect_piece(False, True)
    

def setup():
    white_pawns = []
    black_pawns = []

    for i in range(8):
        white_pawns.append(Pawns(i, 6, images["white pawn"], "w"))
        black_pawns.append(Pawns(i, 1, images["black pawn"], "b"))

    white_rooks = [Rooks(0, 7, images["white rook"], "w"), 
                   Rooks(7, 7, images["white rook"], "w")]
    
    white_knights = [Knights(1, 7, images["white knight"], "w"), 
                     Knights(6, 7, images["white knight"], "w")]
    
    white_bishops = [Bishops(2, 7, images["white bishop"], "w"), 
                     Bishops(5, 7, images["white bishop"], "w")]
    
    white_queen = Queens(3, 7, images["white queen"], "w")
    white_king = Kings(4, 7, images["white king"], "w")

    black_rooks = [Rooks(0, 0, images["black rook"], "b"), 
                   Rooks(7, 0, images["black rook"], "b")]
    
    black_knights = [Knights(1, 0, images["black knight"], "b"), 
                     Knights(6, 0, images["black knight"], "b")]
    
    black_bishops = [Bishops(2, 0, images["black bishop"], "b"), 
                     Bishops(5, 0, images["black bishop"], "b")]
    
    black_queen = Queens(3, 0, images["black queen"], "b")
    black_king = Kings(4, 0, images["black king"], "b")

    return {"white_pawns": white_pawns,
            "black_pawns": black_pawns,
            "white_rooks": white_rooks,
            "white_knights": white_knights,
            "white_bishops": white_bishops,
            "white_queen": white_queen,
            "white_king": white_king,
            "black_rooks": black_rooks,
            "black_knights": black_knights,
            "black_bishops": black_bishops,
            "black_queen": black_queen,
            "black_king": black_king,}
    
blocks = draw_board()
images = load_images()
all_pieces = setup()

board.mainloop()