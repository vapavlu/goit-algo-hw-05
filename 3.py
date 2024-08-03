import requests
import timeit

# Алгоритм Боєра-Мура
def bm_search(text, pattern):
    def preprocess(pattern):
        bad_char = {}
        length = len(pattern)
        for i in range(length):
            bad_char[pattern[i]] = length - i - 1
        return bad_char

    def search(text, pattern):
        bad_char = preprocess(pattern)
        m = len(pattern)
        n = len(text)
        s = 0
        while s <= n - m:
            j = m - 1
            while j >= 0 and pattern[j] == text[s + j]:
                j -= 1
            if j < 0:
                return s
            s += bad_char.get(text[s + m - 1], m)
        return -1

    return search(text, pattern)

# Алгоритм Кнута-Морріса-Пратта
def kmp_search(text, pattern):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
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
        return lps

    def search(text, pattern):
        lps = compute_lps(pattern)
        i = 0
        j = 0
        while i < len(text):
            if pattern[j] == text[i]:
                i += 1
                j += 1
            if j == len(pattern):
                return i - j
            elif i < len(text) and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        return -1

    return search(text, pattern)

# Алгоритм Рабіна-Карпа
def rabin_karp_search(text, pattern):
    def hash_function(s, prime=101):
        hash_val = 0
        for char in s:
            hash_val = (hash_val * 256 + ord(char)) % prime
        return hash_val

    def search(text, pattern):
        m = len(pattern)
        n = len(text)
        prime = 101
        pattern_hash = hash_function(pattern, prime)
        text_hash = hash_function(text[:m], prime)
        for i in range(n - m + 1):
            if pattern_hash == text_hash and text[i:i + m] == pattern:
                return i
            if i < n - m:
                text_hash = (256 * (text_hash - ord(text[i]) * pow(256, m - 1)) + ord(text[i + m])) % prime
                if text_hash < 0:
                    text_hash += prime
        return -1

    return search(text, pattern)

# Вимірювання часу виконання алгоритмів
def time_search(algorithm, text, pattern):
    return timeit.timeit(lambda: algorithm(text, pattern), number=1)

# Завантаження текстів з URL
def load_text_from_url(url):
    response = requests.get(url)
    return response.text

# URL текстів 
url1 = 'https://drive.google.com/uc?id=18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh'  # Стаття 1
url2 = 'https://drive.google.com/uc?id=13hSt4JkJc11nckZZz2yoFHYL89a4XkMZ'  # Стаття 2

text1 = load_text_from_url(url1)
text2 = load_text_from_url(url2)

# Вибрані підрядки для тестування
existing_substring1 = "return"  # Існуючий підрядок для Статті 1
nonexistent_substring1 = "ІАФВАФІАФ"   # Вигаданий підрядок для Статті 1

existing_substring2 = "Graph"      # Існуючий підрядок для Статті 2
nonexistent_substring2 = "ІАФВАФІАФ"    # Вигаданий підрядок для Статті 2

# Вимірювання часу для кожної статті і підрядка
def measure_time(text, substring):
    print(f"Тестування для підрядка: {substring}")
    bm_time = time_search(lambda text, pattern: bm_search(text, pattern), text, substring)
    kmp_time = time_search(lambda text, pattern: kmp_search(text, pattern), text, substring)
    rabin_karp_time = time_search(lambda text, pattern: rabin_karp_search(text, pattern), text, substring)
    return {
        'Boyer-Moore': bm_time,
        'KMP': kmp_time,
        'Rabin-Karp': rabin_karp_time
    }

# Виведення результатів
def print_results(text_id, text, existing_substring, nonexistent_substring):
    print(f"\nТестування для {text_id}:")
    print("Підрядок, що існує:")
    times_existing = measure_time(text, existing_substring)
    for algo, time in times_existing.items():
        print(f"  {algo}: {time:.6f} секунд")
    
    print("Вигаданий підрядок:")
    times_nonexistent = measure_time(text, nonexistent_substring)
    for algo, time in times_nonexistent.items():
        print(f"  {algo}: {time:.6f} секунд")

print_results("Стаття 1", text1, existing_substring1, nonexistent_substring1)
print_results("Стаття 2", text2, existing_substring2, nonexistent_substring2)
