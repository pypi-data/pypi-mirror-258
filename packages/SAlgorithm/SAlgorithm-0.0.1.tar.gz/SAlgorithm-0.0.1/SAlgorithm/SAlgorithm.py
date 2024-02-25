class Algorithm:
    @staticmethod
    def bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    @staticmethod
    def selection_sort(arr):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    @staticmethod
    def insertion_sort(arr):
        n = len(arr)
        for i in range(1, n):
            key = arr[i]
            j = i-1
            while j >= 0 and arr[j] > key:
                arr[j+1] = arr[j]
                j -= 1
            arr[j+1] = key
        return arr

    @staticmethod
    def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        left = Algorithm.merge_sort(left)
        right = Algorithm.merge_sort(right)
        return Algorithm.merge(left, right)

    @staticmethod
    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    @staticmethod
    def quick_sort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return Algorithm.quick_sort(left) + middle + Algorithm.quick_sort(right)

    @staticmethod
    def heap_sort(arr):
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            Algorithm.heapify(arr, n, i)
        for i in range(n-1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            Algorithm.heapify(arr, i, 0)
        return arr

    @staticmethod
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[i] < arr[left]:
            largest = left
        if right < n and arr[largest] < arr[right]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            Algorithm.heapify(arr, n, largest)

    @staticmethod
    def binary_search(arr, target):
        low = 0
        high = len(arr) - 1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    @staticmethod
    def dfs(graph, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        print(start, end=' ')
        for neighbor in graph[start]:
            if neighbor not in visited:
                Algorithm.dfs(graph, neighbor, visited)

    @staticmethod
    def bfs(graph, start):
        visited = set()
        queue = [start]
        visited.add(start)
        while queue:
            vertex = queue.pop(0)
            print(vertex, end=' ')
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)

    @staticmethod
    def knapsack_problem(weights, values, capacity):
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(1, capacity + 1):
                if weights[i - 1] <= j:
                    dp[i][j] = max(values[i - 1] + dp[i - 1][j - weights[i - 1]], dp[i - 1][j])
                else:
                    dp[i][j] = dp[i - 1][j]
        return dp[n][capacity]

    @staticmethod
    def longest_common_subsequence(s1, s2):
        m = len(s1)
        n = len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]

    @staticmethod
    def shortest_path(graph, start, end):
        distances = {vertex: float('inf') for vertex in graph}
        distances[start] = 0
        queue = [start]
        while queue:
            vertex = queue.pop(0)
            for neighbor in graph[vertex]:
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = distances[vertex] + 1
                    queue.append(neighbor)
        return distances[end]

    @staticmethod
    def minimum_spanning_tree(graph):
        n = len(graph)
        parent = [-1] * n
        key = [float('inf')] * n
        mst_set = [False] * n
        key[0] = 0
        for _ in range(n):
            min_key = float('inf')
            min_index = -1
            for i in range(n):
                if not mst_set[i] and key[i] < min_key:
                    min_key = key[i]
                    min_index = i
            mst_set[min_index] = True
            for j in range(n):
                if (
                    graph[min_index][j] != 0 and
                    not mst_set[j] and
                    graph[min_index][j] < key[j]
                ):
                    parent[j] = min_index
                    key[j] = graph[min_index][j]
        return parent

    @staticmethod
    def topological_sort(graph):
        n = len(graph)
        visited = [False] * n
        stack = []
        for i in range(n):
            if not visited[i]:
                Algorithm.topological_sort_util(graph, i, visited, stack)
        return stack[::-1]

    @staticmethod
    def topological_sort_util(graph, vertex, visited, stack):
        visited[vertex] = True
        for neighbor in graph[vertex]:
            if not visited[neighbor]:
                Algorithm.topological_sort_util(graph, neighbor, visited, stack)
        stack.append(vertex)

    @staticmethod
    def kmp_algorithm(text, pattern):
        m = len(pattern)
        n = len(text)
        lps = [0] * m
        Algorithm.compute_lps_array(pattern, m, lps)
        i = j = 0
        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1
            if j == m:
                print("Pattern found at index", i - j)
                j = lps[j - 1]
            elif i < n and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1

    @staticmethod
    def compute_lps_array(pattern, m, lps):
        length = 0
        i = 1
        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

    @staticmethod
    def boyer_moore_algorithm(text, pattern):
        m = len(pattern)
        n = len(text)
        last = Algorithm.bad_character_heuristic(pattern, m)
        i = 0
        while i <= n - m:
            j = m - 1
            while j >= 0 and pattern[j] == text[i + j]:
                j -= 1
            if j < 0:
                print("Pattern found at index", i)
                if i + m < n:
                    i += m - last[ord(text[i + m])]
                else:
                    i += 1
            else:
                i += max(1, j - last[ord(text[i + j])])

    @staticmethod
    def bad_character_heuristic(pattern, m):
        last = [-1] * 256
        for i in range(m):
            last[ord(pattern[i])] = i
        return last

    @staticmethod
    def rabin_karp_algorithm(text, pattern, q):
        d = 256
        m = len(pattern)
        n = len(text)
        p = h = 0
        t = []
        for i in range(m):
            p = (d * p + ord(pattern[i])) % q
            h = (d * h + ord(text[i])) % q
        for i in range(n - m + 1):
            if p == h:
                for j in range(m):
                    if text[i + j] != pattern[j]:
                        break
                if j == m - 1:
                    print("Pattern found at index", i)
            if i < n - m:
                h = (d * (h - ord(text[i]) * pow(d, m - 1, q)) + ord(text[i + m])) % q
                if h < 0:
                    h += q

    @staticmethod
    def prime_number_algorithm(n):
        primes = []
        is_prime = [True] * (n + 1)
        p = 2
        while p * p <= n:
            if is_prime[p]:
                for i in range(p * p, n + 1, p):
                    is_prime[i] = False
            p += 1
        for p in range(2, n + 1):
            if is_prime[p]:
                primes.append(p)
        return primes

    @staticmethod
    def gcd_algorithm(a, b):
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def lcm_algorithm(a, b):
        return (a * b) // Algorithm.gcd_algorithm(a, b)

    @staticmethod
    def timeit(func):
        import time

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"Execution time: {end_time - start_time} seconds")
            return result

        return wrapper

    @staticmethod
    def memoize(func):
        cache = {}

        def wrapper(*args, **kwargs):
            key = (args, tuple(kwargs.items()))
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]

        return wrapper

    @staticmethod
    def decimal_to_binary(n):
        return bin(n)[2:]

    @staticmethod
    def decimal_to_octal(n):
        return oct(n)[2:]

    @staticmethod
    def decimal_to_hexadecimal(n):
        return hex(n)[2:]

    @staticmethod
    def binary_to_decimal(n):
        return int(n, 2)

    @staticmethod
    def octal_to_decimal(n):
        return int(n, 8)

    @staticmethod
    def hexadecimal_to_decimal(n):
        return int(n, 16)

    @staticmethod
    def convert_number_system(number, from_base, to_base):
        if from_base == 10:
            if to_base == 2:
                return Algorithm.decimal_to_binary(number)
            elif to_base == 8:
                return Algorithm.decimal_to_octal(number)
            elif to_base == 16:
                return Algorithm.decimal_to_hexadecimal(number)
        elif from_base == 2:
            decimal_number = Algorithm.binary_to_decimal(number)
            if to_base == 10:
                return decimal_number
            elif to_base == 8:
                return Algorithm.decimal_to_octal(decimal_number)
            elif to_base == 16:
                return Algorithm.decimal_to_hexadecimal(decimal_number)
        elif from_base == 8:
            decimal_number = Algorithm.octal_to_decimal(number)
            if to_base == 10:
                return decimal_number
            elif to_base == 2:
                return Algorithm.decimal_to_binary(decimal_number)
            elif to_base == 16:
                return Algorithm.decimal_to_hexadecimal(decimal_number)
        elif from_base == 16:
            decimal_number = Algorithm.hexadecimal_to_decimal(number)
            if to_base == 10:
                return decimal_number
            elif to_base == 2:
                return Algorithm.decimal_to_binary(decimal_number)
            elif to_base == 8:
                return Algorithm.decimal_to_octal(decimal_number)
        return None

# 创建 Algorithm 类的实例
algorithm = Algorithm()
