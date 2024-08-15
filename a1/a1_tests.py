from a1 import *


def test_create_empty_board():
    expected = ["~~", "~~"]
    results = create_empty_board(2)

    assert expected == results
    assert type(expected) == type(results)
    print("Passed create_empty_board")


test_create_empty_board()


def test_get_square():
    expected = [
        ACTIVE_SHIP_SQUARE,
        DEAD_SHIP_SQUARE,
        MISS_SQUARE,
        EMPTY_SQUARE,
        ACTIVE_SHIP_SQUARE,
        DEAD_SHIP_SQUARE,
        ACTIVE_SHIP_SQUARE,
        MISS_SQUARE,
        EMPTY_SQUARE,
    ]
    results = []
    positions = [(i, j) for i in range(0, 3) for j in range(0, 3)]
    board = ["OX!", "~OX", "O!~"]
    for position in positions:
        results.append(get_square(board, position))
    assert results == expected
    print("Passed get_square test 1")

    board = ["~~~!", "!O~~", "~~~~", "~~~~"]

    assert get_square(board, (1, 0)) == MISS_SQUARE
    assert get_square(board, (0, 1)) == EMPTY_SQUARE
    print("Passed get_square test 2")

    board = ["abc", "de"]
    assert get_square(board, (1, 1)) == "e"
    print("Passed get_square test 3")


test_get_square()


def test_change_square():
    expected_board = ["~~~~~", "~~~~~", "~~~!~", "~~~~~", "~~~~~"]
    board = create_empty_board(5)
    change_square(board, (2, 3), MISS_SQUARE)
    assert board == expected_board
    print("Passed change_square test 1")

    expected_board = ["abc", "dh"]
    board = ["abc", "de"]
    change_square(board, (1, 1), "h")
    assert board == expected_board
    print("Passed change_square test 2")


test_change_square()


def test_coordinate_to_position():
    assert coordinate_to_position("A1") == (0, 0)
    assert coordinate_to_position("B3") == (2, 1)
    assert coordinate_to_position("G8") == (7, 6)
    print("Passed coordinate_to_position test 1")


test_coordinate_to_position()


def test_can_place_ship():
    board = ["~~~~", "OO~~", "~~~~", "~~~~"]
    assert can_place_ship(board, [(0, 0), (0, 1)]) == True
    assert can_place_ship(board, [(0, 0), (1, 0)]) == False
    print("Passed can_place_ship test 1")


test_can_place_ship()


def test_place_ship():
    expected_board = ["OO~~", "OO~~", "~~~~", "~~~~"]
    board = ["~~~~", "OO~~", "~~~~", "~~~~"]
    place_ship(board, [(0, 0), (0, 1)])
    assert board == expected_board
    print("Passed place_ship test 1")


test_place_ship()


def test_attack():
    expected_board = ["X!~~", "O~~~", "~~~~", "~~~~"]
    board = ["O~~~", "O~~~", "~~~~", "~~~~"]
    attack(board, (0, 0))
    attack(board, (0, 1))
    attack(board, (0, 0))
    assert expected_board == board
    print("Passed attack test 1")


test_attack()


def test_display_board():
    board = create_empty_board(4)
    place_ship(board, [(0, 0), (1, 0)])
    attack(board, (0, 0))
    assert board[0][0] == DEAD_SHIP_SQUARE
    print("Passed display_board test 1")


test_display_board()


def test_get_player_hp():
    board = ["O~~~", "O~~~", "~~~~", "~~~~"]
    assert get_player_hp(board) == 2
    print("Passed get_player_hp test 1")
    attack(board, (0, 0))
    assert get_player_hp(board) == 1
    print("Passed get_player_hp test 2")


test_get_player_hp()


def test_display_game():
    player_1_board = ["O~~~", "O~~~", "~~~~", "~~~~"]
    player_2_board = ["~~~~", "~~~~", "OO~~", "~~~~"]
    attack(player_1_board, (0, 0))
    attack(player_2_board, (0, 0))
    # display_game(player_1_board, player_2_board, True)
    # display_game(player_1_board, player_2_board, False)


test_display_game()


def test_is_valid_coordinate():
    assert is_valid_coordinate("A3", 4) == (True, "")
    print("Passed is_valid_coordinate test 1")
    assert is_valid_coordinate("A4", 3) == (False, "Invalid coordinate number.")
    print("Passed is_valid_coordinate test 2")
    assert is_valid_coordinate("abcd", 4) == (
        False,
        "Coordinates should be 2 characters long.",
    )
    print("Passed is_valid_coordinate test 3")
    assert is_valid_coordinate("AA", 4) == (False, "Invalid coordinate number.")
    print("Passed is_valid_coordinate test 4")
    assert is_valid_coordinate("H3", 5) == (False, "Invalid coordinate letter.")
    print("Passed is_valid_coordinate test 5")


test_is_valid_coordinate()


def test_is_valid_coordinate_sequence():
    assert is_valid_coordinate_sequence("A1,B2,C3", 3, 4) == (True, "")
    print("Passed is_valid_coordinate_sequence test 1")
    assert is_valid_coordinate_sequence("A1,B2,C3", 3, 2) == (
        False,
        "Invalid coordinate letter.",
    )
    print("Passed is_valid_coordinate_sequence test 2")
    assert is_valid_coordinate_sequence("A1,B2,C3", 2, 2) == (
        False,
        "Invalid coordinate sequence length.",
    )
    print("Passed is_valid_coordinate_sequence test 3")
    assert is_valid_coordinate_sequence("A1,B2,ABCD", 3, 4) == (
        False,
        "Coordinates should be 2 characters long.",
    )
    print("Passed is_valid_coordinate_sequence test 4")
    assert is_valid_coordinate_sequence("E8,B2,ABCD", 3, 4) == (
        False,
        "Invalid coordinate letter.",
    )
    print("Passed is_valid_coordinate_sequence test 5")


test_is_valid_coordinate_sequence()


def test_build_ship():
    assert build_ship("A1,A2,A3") == [(0, 0), (1, 0), (2, 0)]
    print("Passed build_ship test 1")
    assert build_ship("G4,G5,G6,G7,G8") == [(3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
    print("Passed build_ship test 2")


test_build_ship()


def test_play():
    # board = setup_board(4, [2, 3])
    # assert board ==['OOOO', 'O~~~', '~~~~', '~~~~']
    pass


test_play()


def test_get_winner():
    p1_board = ["OOOO", "O~~~", "~~~~", "~~~~"]
    p2_board = ["XX~~", "!~~~", "XXX~", "!!!!"]
    assert get_winner(p1_board, p2_board) == "PLAYER 1"
    print("Passed get_winner test 1")
    assert get_winner(p2_board, p1_board) == "PLAYER 2"
    print("Passed get_winner test 2")


test_get_winner()


def test_make_attack():
    # board = ['OOOO', 'O~~~', '~~~~', '~~~~']
    # make_attack(board)
    # assert board == ['XOOO', 'O~~~', '~~~~', '~~~~']
    # print("Passed make_attack test 1")
    # make_attack(board)
    # assert board == ['XOOO', 'O~~~', '~~~~', '~~~~']
    # print("Passed make_attack test 1")
    pass


test_make_attack()
