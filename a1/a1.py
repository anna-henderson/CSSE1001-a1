from typing import Optional
from support import *

ROW_DICT = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8}
ROW_DICT_LETTER = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H",
    8: "I",
}
INTEGERS_AS_STRINGS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def num_hours() -> float:
    """Returns the number of hours that spent on the assignment

    Parameters:

    Returns:
        Float number of hours spent on assignment
    """
    return 4


def create_empty_board(board_size: int) -> list[str]:
    """Returns and empty board of size board_size

    Parameters:
        board_size: size of the board

    Returns:
        Empty board.
    """
    row = EMPTY_SQUARE * board_size
    board = []
    for i in range(board_size):
        board.append(row)
    return board


def get_square(board: list[str], position: tuple[int, int]) -> str:
    """Returns the character present at the given (row, column) position within the given board.

    Parameters:
        board: game board
        position: position we want to get of the board, (row,column)

    Returns:
        The square in the specified position on the board
    """
    row, col = position
    return board[row][col]


def change_square(board: list[str], position: tuple[int, int], new_square: str) -> None:
    """Replaces the character at the given (row, column) position with new square.

    Parameters:
        board: game board
        position: position we want to get of the board, (row,column)
        new_square: new square to go in position on the board

    Returns:
        Returns nothing
    """
    row, col = position
    new_row = ""
    for idx, square in enumerate(board[row]):
        if idx != col:
            new_row += square
        else:
            new_row += new_square
    board[row] = new_row


def coordinate_to_position(coordinate: str) -> tuple[int, int]:
    """Returns the (row, column) position tuple corresponding to the given coordinate.

    Parameters:
        coordinates: string coordinate entered by user

    Returns:
        Returns tuple of row, column coordinates
    """
    row, column = coordinate[0], coordinate[1]
    column_calc = int(column) - 1
    return (column_calc, ROW_DICT[row])


def can_place_ship(board: list[str], ship: list[tuple[int, int]]) -> bool:
    """Returns True if the ship can be placed on the board, and False otherwise.

    Parameters:
        board: game board
        shift: ship to place on board

    Returns:
        Returns boolean if ship can be placed on board
    """
    for row, col in ship:
        if board[row][col] != EMPTY_SQUARE:
            return False
    return True


def place_ship(board: list[str], ship: list[tuple[int, int]]) -> None:
    """Places the ship on the board by changing all positions from the ship to the ACTIVE SHIP SQUARE.

    Parameters:
        board: game board
        shift: ship to place on board

    Returns:
        Returns None
    """
    for position in ship:
        change_square(board, position, ACTIVE_SHIP_SQUARE)


def attack(board: list[str], position: tuple[int, int]) -> None:
    """Attempts to attack the cell at the (row, column) position within the board.

    Parameters:
        board: game board
        position: position we want to get of the board, (row,column)

    Returns:
        Returns None
    """
    row, col = position
    if board[row][col] == ACTIVE_SHIP_SQUARE:
        change_square(board, position, DEAD_SHIP_SQUARE)
    elif board[row][col] == EMPTY_SQUARE:
        change_square(board, position, MISS_SQUARE)


def display_board(board: list[str], show_ships: bool) -> None:
    """Prints the board in a human-readable format.

    Parameters:
        board: game board
        show_ships: boolean of whether to show ships

    Returns:
        Returns None
    """
    header = HEADER_SEPARATOR
    for i, _ in enumerate(board):
        header += ROW_DICT_LETTER[i]
    print(header)

    for idx, row in enumerate(board):
        row_to_print = f"{idx+1}" + ROW_SEPARATOR
        for j in row:
            if not show_ships and j == ACTIVE_SHIP_SQUARE:
                row_to_print += EMPTY_SQUARE
            else:
                row_to_print += j
        print(row_to_print)


def get_player_hp(board: list[str]) -> int:
    """Returns the play hp, equivalent to active ship squares on board.

    Parameters:
        board: game board

    Returns:
        Returns integer of player hp
    """
    hp = 0
    for row in board:
        for square in row:
            if square == ACTIVE_SHIP_SQUARE:
                hp += 1
    return hp


def display_game(p1_board: list[str], p2_board: list[str], show_ships: bool) -> None:
    """Prints the overall game state. The game state consists of player 1's health and board state,
        followed by player 2's health and board state.

    Parameters:
        p1_board: game board of player 1
        p2_board: game board of player 2
        show_ships: bool of whether to show ships

    Returns:
        Returns None but displays game board
    """
    for board, player in [(p1_board, PLAYER_ONE), (p2_board, PLAYER_TWO)]:
        player_hp = get_player_hp(board)
        if player_hp == 1:
            l_remaining = "life remaining"
        else:
            l_remaining = "lives remaining"
        print(f"{player}: {player_hp} {l_remaining}")
        display_board(board, show_ships)


def is_valid_coordinate(coordinate: str, board_size: int) -> tuple[bool, str]:
    """Checks if the provided coordinate represents a valid coordinate string.

    Parameters:
        coordinate: Coordinate as a string
        board_size: size of the board

    Returns:
        Returns tuple of boolean and a string describing the issue if any
    """
    if len(coordinate) != 2:  # TODO fix if can't use len
        return (False, INVALID_COORDINATE_LENGTH)
    elif ROW_DICT.get(coordinate[0]) is None or board_size <= ROW_DICT.get(
        coordinate[0]
    ):  # TODO Fix this guy
        return (False, INVALID_COORDINATE_LETTER)
    elif coordinate[1] not in INTEGERS_AS_STRINGS or board_size < int(coordinate[1]):
        return (False, INVALID_COORDINATE_NUMBER)
    else:
        return (True, "")


def is_valid_coordinate_sequence(
    coordinate_sequence: str, ship_length: int, board_size: int
) -> tuple[bool, str]:  # TODO do we need to test this?
    """Checks if the provided coordinate sequence represents a sequence of exactly ship length comma-separated valid coordinate strings.

    Parameters:
        coordinate_sequence: Coordinates as a string separated by ","
        ship_length: length of the ship
        board_size: size of the board

    Returns:
        This function should return a tuple containing a boolean (which is True if there are exactly ship length coordinates
        which are all valid, and False otherwise), and a string containing a message to describe the issue (if any)
        with the coordinate sequence.
    """
    coords = coordinate_sequence.split(",")  # TODO remove split
    for coord in coords:
        if len(coords) != ship_length:
            return (False, INVALID_COORDINATE_SEQUENCE_LENGTH)
        if is_valid_coordinate(coord, board_size)[0] == False:
            return is_valid_coordinate(coord, board_size)
    return (True, "")


def build_ship(coordinate_sequence: str) -> list[tuple[int, int]]:
    """Returns the list of (row, column) positions corresponding to the coordinate sequence.

    Parameters:
        coordinate_sequence: Coordinates as a string separated by ","

    Returns:
        Returns the list of (row, column) positions corresponding to the coordinate sequence.
    """
    coords = coordinate_sequence.split(",")  # TODO remove split
    coordinates = []
    for coord in coords:
        coordinates.append(coordinate_to_position(coord))
    return coordinates


def setup_board(board_size: int, ship_sizes: list[int]) -> list[str]:
    """Allows the user to set up a new board by placing ships.

    Parameters:
        board_size: integer board size
        ship_sizes: list of ship sizes as integers

    Returns:
        Returns the setup board
    """
    board = create_empty_board(board_size)
    for ship_length in ship_sizes:
        ship_placed = False
        while ship_placed == False:
            display_board(board, True)
            ship_coords_sequence = input(prompt_for_ship_coordinates(ship_length))
            if is_valid_coordinate_sequence(
                ship_coords_sequence, ship_length, board_size
            )[0]:
                ship = []
                ship_coords_list = ship_coords_sequence.split(",")
                for coord in ship_coords_list:
                    ship.append(coordinate_to_position(coord))
                if can_place_ship(board, ship):
                    place_ship(board, ship)
                    ship_placed = True
                else:
                    print(INVALID_SHIP_PLACEMENT)
            else:
                print(
                    is_valid_coordinate_sequence(
                        ship_coords_sequence, ship_length, board_size
                    )[1]
                )
    return board


def get_winner(p1_board: list[str], p2_board: list[str]) -> Optional[str]:
    """Returns whihc player has won, if any

    Parameters:
        p1_board: player 1 game board
        p2_board: player 2 game board

    Returns:
        Returns string of player that has won, or None if no player has won
    """
    for board, opponent in [(p1_board, PLAYER_TWO), (p2_board, PLAYER_ONE)]:
        if get_player_hp(board) == 0:
            return opponent
    return None


def make_attack(target_board: list[str]) -> None:
    """Performs a single turn against the target board.

    Parameters:
        target_board: target game board

    Returns:
        Returns None
    """
    has_not_attacked = True
    while has_not_attacked:
        attack_coord = input(TURN_INPUT_MESSAGE)
        if is_valid_coordinate(attack_coord, len(target_board))[0]:
            position = coordinate_to_position(attack_coord)
            attack(target_board, position)
            has_not_attacked = False
        else:
            print(is_valid_coordinate(attack_coord, len(target_board))[1])


def play_game() -> None:
    """Coordinates gameplay of a single game of Battleships from start to finish according to section 3.

    Parameters:

    Returns:
        Returns None
    """
    board_size = int(input("Enter board size: "))
    ship_sizes_str = input("Enter ships sizes: ")
    print(DIVIDER_MESSAGE)
    ship_sizes_list = ship_sizes_str.split(",")
    ship_sizes = []
    for ship_size in ship_sizes_list:
        ship_sizes.append(int(ship_size))

    print(P1_PLACEMENT_MESSAGE)
    p1_board = setup_board(board_size, ship_sizes)
    print(P2_PLACEMENT_MESSAGE)
    p2_board = setup_board(board_size, ship_sizes)

    turn = 1
    # if no player has won
    while get_winner(p1_board, p2_board) == None:
        print(NEXT_TURN_GRAPHIC)
        # TODO can we make out own little functions to display both boards?

        display_game(p1_board, p2_board, False)
        if turn % 2 != 0:
            print(f"\n{PLAYER_ONE}'s turn!")
            make_attack(p2_board)
        else:
            print(f"\n{PLAYER_TWO}'s turn!")
            make_attack(p1_board)
        turn += 1
    print(GAME_OVER_GRAPHIC)
    print(f"{get_winner(p1_board,p2_board)} won!")
    display_game(p1_board, p2_board, True)


if __name__ == "__main__":
    play_game()
