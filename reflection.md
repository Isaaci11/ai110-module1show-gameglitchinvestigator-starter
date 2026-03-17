# Reflection: Game Glitch Investigator

1. What was broken when you started?

- What did the game look like the first time you ran it?
  - The application looks like a simple game. The UI isn't as engaging as it could be, and there are definitely major bugs that affect the gameplay.
- List at least two concrete bugs you noticed at the start(for example: "the hints were backwards").
  - Invalid inputs are counted against attempts; depending on the requirements, this could be the intended behavior of the application (image 000)
  - The game does not allow you to get a perfect score, as the first guess is always counted against the final score.
  - Deductions should only apply to wrong answers, not correct ones. If the first guess is correct, the player should receive the maximum score. Additionally, the lowest possible score should be capped at zero rather than going negative, as seen in other screenshots.
  - The game accepts the decimal equivalent of the secret/win value as a correct answer (image 001)
  - Once you win, the game does not allow you to refresh the page — you must press "New Game" instead
  - The history of a previous game's state is retained
  - Even when changing the game difficulty, the previous game's state remains visible (image 002)
  - Contradictory hints are offered: when your guess is too low, it suggests going lower, and when your guess is too high, it suggests going higher (image 003)
  - The application accepts decimal values that, when floored, equal the secret value (image 004)

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Claude Code in the terminal and Antigravity. Antigravity was for tangential questions, such as setting up a Python environment with the necessary libraries. Claude Code was used for thoroughly understanding the codebase and the bugs I had encountered, as well as ones I hadn't noticed yet. I was able to cross-reference my findings from running the game with its knowledge of the codebase to trace the root of various issues.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - Invalid inputs counted against attempts (app.py:148): `st.session_state.attempts += 1` runs before `parse_guess` is called, so even if the input is blank or non-numeric, the attempt counter has already incremented. I was able to verify this by tracing the surrounding code blocks and understanding how that line interacted with the rest of the logic.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - Rather than being outright incorrect, the agent seemed to focus too narrowly on the specific issue and overlooked the broader design of the `parse_guess()` function. This function could be written in a more concise and straightforward way — both for future developers and for easier debugging — as it contains a lot of unnecessary filler code that doesn't meaningfully contribute to the application.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I decided a bug was fixed when it passed the pytest test suite I created and I was able to confirm the behavior by going into the app's UI and playing through it.
- Describe at least one test you ran (manual or using pytest)and what it showed you about your code.
  - The test `test_update_score_win_attempt_1()` was designed to verify that if a player guesses correctly on the first attempt, the score would be 100 (`assert new_score == 100`). Although the test initially passed, it turned out that the updated game logic was not actually being used.
- Did AI help you design or understand any tests? How?
  - I prompted AI to help create tests that I could verify were functional, and used it earlier in the project to identify possible issues. This was helpful because it surfaced bugs that were present in the code but not obvious from an initial read. My existing knowledge of the problem space let me judge which tests were worth pursuing rather than guessing blindly.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - Session state can be thought of as a record of truths and a snapshot of the application. Reruns and page refreshes wipe that record and render the app blank.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
    - I want to write tests for the initial application code based on the requirements first, then work through each failing test to fix the associated functions or statements, rather than going in blind and trying to identify bugs on the fly.
- What is one thing you would do differently next time you work with AI on a coding task?
  - I like refreshing Claude sessions throughout a fix, but it becomes difficult because other sessions don't necessarily have visibility into prior fixes, and tightly coupled code could break without that context. Next time I would consistently use `#codebase` or `#file` to keep sessions grounded.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - The quality of AI-generated code depends heavily on the author's knowledge and skill. It's more of a booster than a full fledged GPS.
