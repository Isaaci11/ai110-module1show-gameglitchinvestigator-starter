import sys
sys.path.append("../")  #logic_utils is not in the same directory as test_game_logic.py, need to add it to the path
from logic_utils import check_guess, update_score

# --- check_guess: outcome and hint message ---

def test_winning_guess():
    # Guess matches secret → Win with correct message
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_guess_too_high():
    # Guess above secret → Too High outcome
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message is not None  # hint is returned


def test_guess_too_low():
    # Guess below secret → Too Low outcome
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message is not None  # hint is returned


# --- Bug regression: even-attempt string cast (app.py FIXME) ---
# On even attempts, app.py passed secret as a string instead of int.
# check_guess must still return the correct outcome in that case.

def test_check_guess_with_string_secret_win():
    # Regression: secret accidentally cast to str on even attempts
    outcome, message = check_guess(50, "50")
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_check_guess_with_string_secret_too_high():
    # Regression: guess int vs secret str should still identify Too High
    outcome, _ = check_guess(60, "50")
    assert outcome == "Too High"


def test_check_guess_with_string_secret_too_low():
    # Regression: guess int vs secret str should still identify Too Low
    outcome, _ = check_guess(40, "50")
    assert outcome == "Too Low"


# --- update_score: points by attempt number ---
# Bug fixed: old formula 100 - 10*(attempt+1) gave wrong values.
# New code uses POINTS_BY_ATTEMPT lookup table.

def test_update_score_win_attempt_1():
    # Attempt 1 win should award 100 points (max bonus)
    new_score = update_score(0, "Win", 1)
    assert new_score == 100


def test_update_score_win_attempt_5():
    # Attempt 5 win should award 60 points per POINTS_BY_ATTEMPT table
    new_score = update_score(0, "Win", 5)
    assert new_score == 60


def test_update_score_win_attempt_10():
    # Attempt 10 win should award 10 points (minimum in table)
    new_score = update_score(0, "Win", 10)
    assert new_score == 10


def test_update_score_win_beyond_table():
    # Attempt beyond table (>10) should award 0 points
    new_score = update_score(50, "Win", 11)
    assert new_score == 50


# --- Integration: simulate app's increment-then-score pattern ---
# app.py does: attempts += 1, then calls update_score(attempts).
# Tests above call update_score directly and can pass even if the app
# initializes attempts to 1 (making the first real attempt number 2).

def test_first_guess_scores_100_after_increment():
    # Mirrors app.py: start at 0, increment, then score.
    attempts = 0
    attempts += 1  # as app.py does on submit
    new_score = update_score(0, "Win", attempts)
    assert new_score == 100, f"Expected 100 but got {new_score} — attempts was {attempts}"


def test_second_guess_scores_90_after_increment():
    # Second guess should yield 90, not be mistaken for attempt 1.
    attempts = 1
    attempts += 1
    new_score = update_score(0, "Win", attempts)
    assert new_score == 90, f"Expected 90 but got {new_score} — attempts was {attempts}"


if __name__ == "__main__":
    tests = [
        test_winning_guess,
        test_guess_too_high,
        test_guess_too_low,
        test_check_guess_with_string_secret_win,
        test_check_guess_with_string_secret_too_high,
        test_check_guess_with_string_secret_too_low,
        test_update_score_win_attempt_1,
        test_update_score_win_attempt_5,
        test_update_score_win_attempt_10,
        test_update_score_win_beyond_table,
        test_first_guess_scores_100_after_increment,
        test_second_guess_scores_90_after_increment,
    ]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {test.__name__} — {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
