from typing import Optional
from support import *

LETTER_TO_INDEX = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
}
ROW_INDEX_TO_LETTER = {
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


def num_hours() -> float:
    """Returns the number of hours that spent on the assignment

    Parameters:

    Returns:
        Float number of hours spent on assignment
    """
    return 6.0


def create_empty_board(board_size: int) -> list[str]:
    """Returns and empty board of size board_size

    Parameters:
        board_size: The size of the board

    Returns:
        Empty board

    Pre-condition:
        board_size must be between 3 and 9
    """
    return [EMPTY_SQUARE * board_size] * board_size


def get_square(board: list[str], position: tuple[int, int]) -> str:
    """Returns the character present at the given (row, column) position within the given board.

    Parameters:
        board: The game board
        position: The position we want to get of the board as (row,column)

    Returns:
        The square in the specified position on the board as a string

    Pre-condition:
        Position must exist on the board
    """
    row, col = position
    return board[row][col]


def change_square(board: list[str], position: tuple[int, int], new_square: str) -> None:
    """Replaces the character at the given (row, column) position with new string.

    Parameters:
        board: The game board
        position: The position we want to get of the board as (row,column)
        new_square: The new square string to go in position on the board

    Pre-condition:
        Position must exist on the board
    """
    row, col = position
    # Take parts of the string around the position and adds new_square in between
    board[row] = board[row][:col] + new_square + board[row][col + 1 :]


def coordinate_to_position(coordinate: str) -> tuple[int, int]:
    """Returns the (row, column) position tuple corresponding to the given coordinate.

    Parameters:
        coordinate: The coordinate in the format of "A1"

    Returns:
        Tuple of row, column coordinates

    Pre-condition:
        Coordinate must consist of two characters where the first is a capital letter from "A" to "I" and the second is a single digit character

    """
    column, row = coordinate

    # Input value - 1 as lists are 0 indexed
    row_value = int(row) - 1
    # Dictionary lookup to get column index
    column_value = LETTER_TO_INDEX[column]
    return row_value, column_value


def can_place_ship(board: list[str], ship: list[tuple[int, int]]) -> bool:
    """Returns True if the ship can be placed on the board, and False otherwise.

    Parameters:
        board: The game board
        ship: The ship to be placed on the board

    Returns:
        Returns boolean if the ship can be placed on the board

    Pre-condition:
        All positions in ship must exist on the board
    """
    for row, col in ship:
        if board[row][col] != EMPTY_SQUARE:
            return False
    return True


def place_ship(board: list[str], ship: list[tuple[int, int]]) -> None:
    """Places the ship on the board by changing all positions from the ship to "O".

    Parameters:
        board: The game board
        shift: The ship to be placed on the board

    Pre-condition:
        ship should be able to be placed on the board according to can_place_ship.
    """
    for position in ship:
        change_square(board, position, ACTIVE_SHIP_SQUARE)


def attack(board: list[str], position: tuple[int, int]) -> None:
    """Attempts to attack the cell at the (row, column) position within the board and places result of attack on the board.

    Parameters:
        board: The game board
        position: The position we want to get of the board as (row,column)

    Pre-condition:
        position must exist on board
    """
    row, col = position
    if board[row][col] == ACTIVE_SHIP_SQUARE:
        change_square(board, position, DEAD_SHIP_SQUARE)
    elif board[row][col] == EMPTY_SQUARE:
        change_square(board, position, MISS_SQUARE)


def display_board(board: list[str], show_ships: bool) -> None:
    """Prints the board in a human-readable format. Ff show_ships is False, the board will print active ship squares as empty squares.

    Parameters:
        board: The game board
        show_ships: Boolean of whether to show ships or not
    """
    header = HEADER_SEPARATOR
    for i in range(len(board)):
        header += ROW_INDEX_TO_LETTER[i]
    print(header)

    # Loop over rows and print each row with or without ships and with row label
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
        board: The game board

    Returns:
        Returns integer of player hp
    """
    hp = 0
    for row in board:
        hp += row.count(ACTIVE_SHIP_SQUARE)
    return hp


def display_game(p1_board: list[str], p2_board: list[str], show_ships: bool) -> None:
    """Prints the overall game state. The game state consists of player 1's health and board state,
        followed by player 2's health and board state.

    Parameters:
        p1_board: The game board of player 1
        p2_board: The game board of player 2
        show_ships: Boolean of whether to show ships or not
    """
    # Loops over each player's board and print the board and hp remaining
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
        coordinate: The coordinate as a string
        board_size: The size of the board

    Returns:
        Returns tuple of boolean and a string describing the issue if any
    """
    if len(coordinate) != 2:
        return (False, INVALID_COORDINATE_LENGTH)
    # Check if the first digit does not correlate to a valid letter
    elif LETTER_TO_INDEX.get(coordinate[0]) is None:
        return (False, INVALID_COORDINATE_LETTER)
    # Check if the first digit is a valid letter but is our of range for the board
    elif board_size <= LETTER_TO_INDEX.get(coordinate[0]):
        return (False, INVALID_COORDINATE_LETTER)
    # Check if the second digit is not a valid integer or is out of range
    elif not coordinate[1].isdigit() or int(coordinate[1]) not in range(
        1, board_size + 1
    ):
        return (False, INVALID_COORDINATE_NUMBER)
    else:
        return (True, "")


def is_valid_coordinate_sequence(
    coordinate_sequence: str, ship_length: int, board_size: int
) -> tuple[bool, str]:
    """Checks if the provided coordinate sequence represents a sequence of exactly ship length comma-separated valid coordinate strings.

    Parameters:
        coordinate_sequence: The coordinates as a string separated by ","
        ship_length: The length of the ship
        board_size: The size of the board

    Returns:
        A tuple containing a boolean (which is True if there are exactly ship length coordinates
        which are all valid, and False otherwise), and a string containing a message to describe the issue (if any)
        with the coordinate sequence.
    """
    coords = coordinate_sequence.split(",")
    # Loops through all coordinates and only returns (True, "") if all coordinates are valid
    for coord in coords:
        # Check the right number of coordinates were given
        if len(coords) != ship_length:
            return (False, INVALID_COORDINATE_SEQUENCE_LENGTH)
        # Checks coordinate is valid
        elif is_valid_coordinate(coord, board_size)[0] == False:
            return is_valid_coordinate(coord, board_size)
    return (True, "")


def build_ship(coordinate_sequence: str) -> list[tuple[int, int]]:
    """Returns the list of (row, column) positions corresponding to the coordinate sequence.

    Parameters:
        coordinate_sequence: The coordinates as a string separated by ","

    Returns:
        Returns the list of (row, column) positions corresponding to the coordinate sequence.

    Pre-condition:
        coordinate_sequence must represent a valid coordinate sequence
    """
    coords = coordinate_sequence.split(",")
    coordinates = []
    for coord in coords:
        coordinates.append(coordinate_to_position(coord))
    return coordinates


def setup_board(board_size: int, ship_sizes: list[int]) -> list[str]:
    """Allows the user to setup a new board by getting user inputs to place the ships.

    Parameters:
        board_size: The integer board size
        ship_sizes: The list of ship sizes as integers

    Returns:
        Returns the setup board
    """
    board = create_empty_board(board_size)
    for ship_length in ship_sizes:
        ship_placed = False
        # Repeats until valid coordinates are input and a ship is placed
        while ship_placed == False:
            display_board(board, True)
            ship_coords_sequence = input(prompt_for_ship_coordinates(ship_length))

            # If valid coordinate sequence construct a ship
            if is_valid_coordinate_sequence(
                ship_coords_sequence, ship_length, board_size
            )[0]:
                ship = []
                ship_coords_list = ship_coords_sequence.split(",")
                for coord in ship_coords_list:
                    ship.append(coordinate_to_position(coord))

                # Check the ship can be placed at the coordinates
                if can_place_ship(board, ship):
                    place_ship(board, ship)
                    ship_placed = True
                else:
                    print(INVALID_SHIP_PLACEMENT)

            # If not a valid sequcence print the reason
            else:
                print(
                    is_valid_coordinate_sequence(
                        ship_coords_sequence, ship_length, board_size
                    )[1]
                )
    return board


def get_winner(p1_board: list[str], p2_board: list[str]) -> Optional[str]:
    """Returns which player has won, if any

    Parameters:
        p1_board: Player 1's game board
        p2_board: Player 2's game board

    Returns:
        Returns string of player that has won, or None if no player has won
    """
    # Check if a player has any hp, if not return the opponents name
    for board, opponent in [(p1_board, PLAYER_TWO), (p2_board, PLAYER_ONE)]:
        if get_player_hp(board) == 0:
            return opponent
    return None


def make_attack(target_board: list[str]) -> None:
    """Performs a single turn against the target board.

    Parameters:
        target_board: The target game board
    """
    has_not_attacked = True
    # Repeat until a valid move has been made
    while has_not_attacked:
        attack_coord = input(TURN_INPUT_MESSAGE)

        # If a valid coordinate is input, place it on the board
        if is_valid_coordinate(attack_coord, len(target_board))[0]:
            position = coordinate_to_position(attack_coord)
            attack(target_board, position)
            has_not_attacked = False
        # If not valid print the reason why the move is invalid
        else:
            print(is_valid_coordinate(attack_coord, len(target_board))[1])


def play_game() -> None:
    """Coordinates gameplay of a single game of Battleships from start to finish according to section 3."""
    board_size = int(input("Enter board size: "))
    ship_sizes_str = input("Enter ships sizes: ")

    print(DIVIDER_MESSAGE)

    ship_sizes_list = ship_sizes_str.split(",")
    ship_sizes = []
    for ship_size in ship_sizes_list:
        ship_sizes.append(int(ship_size))

    # Display board and prompt each player to setup their board
    print(P1_PLACEMENT_MESSAGE)
    p1_board = setup_board(board_size, ship_sizes)
    print(P2_PLACEMENT_MESSAGE)
    p2_board = setup_board(board_size, ship_sizes)

    turn = 0
    # Repeat until there is a winner
    while get_winner(p1_board, p2_board) == None:
        turn += 1
        print(NEXT_TURN_GRAPHIC)
        display_game(p1_board, p2_board, False)

        # If player 1's turn
        if turn % 2 != 0:
            print(f"\n{PLAYER_ONE}'s turn!")
            make_attack(p2_board)
        # If player 2's turn
        else:
            print(f"\n{PLAYER_TWO}'s turn!")
            make_attack(p1_board)

    print(GAME_OVER_GRAPHIC)
    print(f"{get_winner(p1_board,p2_board)} won!")
    display_game(p1_board, p2_board, True)


if __name__ == "__main__":
    play_game()
    pass


# def run_tests():
# TEST 1
#     board_size = 3
#     breakpoint()
#     board = setup_board(board_size,[3,4])
#     print(board)


# run_tests()
