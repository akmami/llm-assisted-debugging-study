class CorrectEditDistance:
    def __init__(self):
        self.word1 = ""
        self.word2 = ""
        self.dp = []

    def __min_dist_top_down_dp(self, m: int, n: int) -> int:
        if m == -1:
            return n + 1
        elif n == -1:
            return m + 1
        elif self.dp[m][n] > -1:
            return self.dp[m][n]
        else:
            if self.word1[m] == self.word2[n]:
                self.dp[m][n] = self.__min_dist_top_down_dp(m - 1, n - 1)
            else:
                insert = self.__min_dist_top_down_dp(m, n - 1)
                delete = self.__min_dist_top_down_dp(m - 1, n)
                replace = self.__min_dist_top_down_dp(m - 1, n - 1)
                self.dp[m][n] = 1 + min(insert, delete, replace)
            return self.dp[m][n]

    def min_dist_top_down(self, word1: str, word2: str) -> int:
        self.word1 = word1
        self.word2 = word2
        self.dp = [[-1 for _ in range(len(word2))] for _ in range(len(word1))]
        return self.__min_dist_top_down_dp(len(word1) - 1, len(word2) - 1)

    def min_dist_bottom_up(self, word1: str, word2: str) -> int:
        self.word1 = word1
        self.word2 = word2
        m = len(word1)
        n = len(word2)
        self.dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    self.dp[i][j] = j
                elif j == 0:
                    self.dp[i][j] = i
                elif word1[i - 1] == word2[j - 1]:
                    self.dp[i][j] = self.dp[i - 1][j - 1]
                else:
                    insert = self.dp[i][j - 1]
                    delete = self.dp[i - 1][j]
                    replace = self.dp[i - 1][j - 1]
                    self.dp[i][j] = 1 + min(insert, delete, replace)
        return self.dp[m][n]


class BuggyEditDistance:
    def __init__(self):
        self.word1 = ''
        self.word2 = ''
        self.dp = []

    def __min_dist_top_down_dp(self, m: int, n: int) -> int:
        if m == -1:
            return n + 1
        elif n == -1:
            return m + 1
        elif self.dp[m][n] > -1:
            return self.dp[m][n]
        else:
            if self.word1[m] == self.word2[n]:
                self.dp[m][n] = self.__min_dist_top_down_dp(m - 1, n - 1)
            else:
                insert = self.__min_dist_top_down_dp(m, n - 1)
                delete = self.__min_dist_top_down_dp(m - 1, n)
                replace = self.__min_dist_top_down_dp(m - 1, n - 1)
                best = 1 + min(insert, delete, replace)

                if (
                    m > 0
                    and n > 0
                    and self.word1[m] == self.word2[n - 1]
                    and self.word1[m - 1] == self.word2[n]
                ):
                    best = min(best, 1 + self.__min_dist_top_down_dp(m - 2, n - 2))

                self.dp[m][n] = best

            return self.dp[m][n]

    def min_dist_top_down(self, word1: str, word2: str) -> int:
        self.word1 = word1
        self.word2 = word2
        self.dp = [[-1 for _ in range(len(word2))] for _ in range(len(word1))]
        return self.__min_dist_top_down_dp(len(word1) - 1, len(word2) - 1)

    def min_dist_bottom_up(self, word1: str, word2: str) -> int:
        self.word1 = word1
        self.word2 = word2
        m = len(word1)
        n = len(word2)
        self.dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    self.dp[i][j] = j
                elif j == 0:
                    self.dp[i][j] = i
                elif word1[i - 1] == word2[j - 1]:
                    self.dp[i][j] = self.dp[i - 1][j - 1]
                else:
                    insert = self.dp[i][j - 1]
                    delete = self.dp[i - 1][j]
                    replace = self.dp[i - 1][j - 1]
                    best = 1 + min(insert, delete, replace)

                    if (
                        i > 1
                        and j > 1
                        and word1[i - 1] == word2[j - 2]
                        and word1[i - 2] == word2[j - 1]
                    ):
                        best = min(best, 1 + self.dp[i - 2][j - 2])

                    self.dp[i][j] = best
        return self.dp[m][n]


def run_test(label, word1, word2):
    for method_name in ["min_dist_top_down", "min_dist_bottom_up"]:
        correct_solver = CorrectEditDistance()
        buggy_solver = BuggyEditDistance()

        expected = getattr(correct_solver, method_name)(word1, word2)
        actual = getattr(buggy_solver, method_name)(word1, word2)

        print(f"{label}_{method_name}")
        if actual != expected:
            print("TEST FAILED")
            print("input:", {"word1": word1, "word2": word2, "method": method_name})
            print("expected:", expected)
            print("got:", actual)
        else:
            print("TEST PASSED")


run_test("TEST_1", "", "")
run_test("TEST_2", "", "abc")
run_test("TEST_3", "abc", "")
run_test("TEST_4", "abc", "abc")
run_test("TEST_5", "abc", "axc")
run_test("TEST_6", "cat", "cut")
run_test("TEST_7", "hello", "yellow")
run_test("TEST_8", "intention", "execution")

run_test("TEST_9", "ab", "ba")
run_test("TEST_10", "ca", "ac")
run_test("TEST_11", "abc", "bac")
run_test("TEST_12", "abcd", "acbd")
run_test("TEST_13", "aab", "aba")
run_test("TEST_14", "abcdef", "abdcef")