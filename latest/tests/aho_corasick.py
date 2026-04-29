from __future__ import annotations

from collections import deque


class CorrectAutomaton:
    def __init__(self, keywords: list[str]):
        self.adlist: list[dict] = []
        self.adlist.append(
            {"value": "", "next_states": [], "fail_state": 0, "output": []}
        )

        for keyword in keywords:
            self.add_keyword(keyword)
        self.set_fail_transitions()

    def find_next_state(self, current_state: int, char: str) -> int | None:
        for state in self.adlist[current_state]["next_states"]:
            if char == self.adlist[state]["value"]:
                return state
        return None

    def add_keyword(self, keyword: str) -> None:
        current_state = 0
        for character in keyword:
            next_state = self.find_next_state(current_state, character)
            if next_state is None:
                self.adlist.append(
                    {
                        "value": character,
                        "next_states": [],
                        "fail_state": 0,
                        "output": [],
                    }
                )
                self.adlist[current_state]["next_states"].append(len(self.adlist) - 1)
                current_state = len(self.adlist) - 1
            else:
                current_state = next_state
        self.adlist[current_state]["output"].append(keyword)

    def set_fail_transitions(self) -> None:
        q: deque = deque()
        for node in self.adlist[0]["next_states"]:
            q.append(node)
            self.adlist[node]["fail_state"] = 0
        while q:
            r = q.popleft()
            for child in self.adlist[r]["next_states"]:
                q.append(child)
                state = self.adlist[r]["fail_state"]
                while (
                    self.find_next_state(state, self.adlist[child]["value"]) is None
                    and state != 0
                ):
                    state = self.adlist[state]["fail_state"]
                self.adlist[child]["fail_state"] = self.find_next_state(
                    state, self.adlist[child]["value"]
                )
                if self.adlist[child]["fail_state"] is None:
                    self.adlist[child]["fail_state"] = 0
                self.adlist[child]["output"] = (
                    self.adlist[child]["output"]
                    + self.adlist[self.adlist[child]["fail_state"]]["output"]
                )

    def search_in(self, string: str) -> dict[str, list[int]]:
        result: dict = {}
        current_state = 0
        for i in range(len(string)):
            while (
                self.find_next_state(current_state, string[i]) is None
                and current_state != 0
            ):
                current_state = self.adlist[current_state]["fail_state"]
            next_state = self.find_next_state(current_state, string[i])
            if next_state is None:
                current_state = 0
            else:
                current_state = next_state
                for key in self.adlist[current_state]["output"]:
                    if key not in result:
                        result[key] = []
                    result[key].append(i - len(key) + 1)
        return result


class BuggyAutomaton:
    def __init__(self, keywords: list[str]):
        self.adlist: list[dict] = []
        self.adlist.append(
            {"value": "", "next_states": [], "fail_state": 0, "output": []}
        )

        for keyword in keywords:
            self.add_keyword(keyword)
        self.set_fail_transitions()

    def find_next_state(self, current_state: int, char: str) -> int | None:
        for state in self.adlist[current_state]["next_states"]:
            if char == self.adlist[state]["value"]:
                return state
        return None

    def add_keyword(self, keyword: str) -> None:
        current_state = 0
        for character in keyword:
            next_state = self.find_next_state(current_state, character)
            if next_state is None:
                self.adlist.append(
                    {
                        "value": character,
                        "next_states": [],
                        "fail_state": 0,
                        "output": [],
                    }
                )
                self.adlist[current_state]["next_states"].append(len(self.adlist) - 1)
                current_state = len(self.adlist) - 1
            else:
                current_state = next_state
        self.adlist[current_state]["output"].append(keyword)

    def set_fail_transitions(self) -> None:
        q: deque = deque()
        for node in self.adlist[0]["next_states"]:
            q.append(node)
            self.adlist[node]["fail_state"] = 0
        while q:
            r = q.popleft()
            for child in self.adlist[r]["next_states"]:
                q.append(child)
                state = self.adlist[r]["fail_state"]
                while (
                    self.find_next_state(state, self.adlist[child]["value"]) is None
                    and state != 0
                ):
                    state = self.adlist[state]["fail_state"]
                self.adlist[child]["fail_state"] = self.find_next_state(
                    state, self.adlist[child]["value"]
                )
                if self.adlist[child]["fail_state"] is None:
                    self.adlist[child]["fail_state"] = 0

    def search_in(self, string: str) -> dict[str, list[int]]:
        result: dict = {}
        current_state = 0
        for i in range(len(string)):
            while (
                self.find_next_state(current_state, string[i]) is None
                and current_state != 0
            ):
                current_state = self.adlist[current_state]["fail_state"]
            next_state = self.find_next_state(current_state, string[i])
            if next_state is None:
                current_state = 0
            else:
                current_state = next_state
                matched_states = [current_state]
                fail_state = self.adlist[current_state]["fail_state"]
                if fail_state != 0:
                    matched_states.append(fail_state)
                for state in matched_states:
                    for key in self.adlist[state]["output"]:
                        if key not in result:
                            result[key] = []
                        result[key].append(i - len(key) + 1)
        return result


def run_test(label, keywords, text):
    print(label)
    expected = CorrectAutomaton(keywords).search_in(text)
    actual = BuggyAutomaton(keywords).search_in(text)
    if actual != expected:
        print("TEST FAILED")
        print("input:", {"keywords": keywords, "text": text})
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")


run_test(
    "TEST_1",
    ["what", "hat", "ver", "er"],
    "whatever, err ... , wherever",
)

run_test(
    "TEST_2",
    ["cat", "dog"],
    "my cat chases dog and another cat",
)

run_test(
    "TEST_3",
    ["ab", "b"],
    "zab",
)

run_test(
    "TEST_4",
    ["abcd", "bcd"],
    "xxabcdyyabcd",
)

run_test(
    "TEST_5",
    [],
    "anything goes here",
)

run_test(
    "TEST_6",
    ["a", "ab"],
    "",
)

run_test(
    "TEST_7",
    ["abc", "bc", "c"],
    "abc",
)

run_test(
    "TEST_8",
    ["abcd", "bcd", "cd", "d"],
    "xabcd",
)

run_test(
    "TEST_9",
    ["aaaa", "aaa", "aa", "a"],
    "aaaa",
)

run_test(
    "TEST_10",
    ["abc", "bc", "c"],
    "zabcabc",
)

run_test(
    "TEST_11",
    ["xabc", "abc", "bc", "c"],
    "xabc",
)

run_test(
    "TEST_12",
    ["miss", "iss", "ss", "s"],
    "mississippi",
)