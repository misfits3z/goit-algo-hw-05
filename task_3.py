import timeit
from tabulate import tabulate

with open('article_1.txt', 'rb') as file:
    article_1 = file.read()

with open('article_2.txt', 'rb') as file:
    article_2 = file.read()

def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1



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

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено



def rabin_karp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    if n < m:
         return -1 
    prime = 101  # Просте число для обчислення хешу
    base = 256   # Кількість можливих символів ASCII
    p_hash = 0   # Хеш підрядка
    t_hash = 0   # Хеш відрізка тексту
    h = 1        # Множник для вирахування хешу

    # Обчислюємо h = (base ** (m-1)) % prime для подальшого використання
    for i in range(m - 1):
        h = (h * base) % prime

    # Обчислюємо початковий хеш для підрядка і першого відрізка тексту
    for i in range(m):
        p_hash = (base * p_hash + ord(pattern[i])) % prime
        t_hash = (base * t_hash + ord(text[i])) % prime

    # Пошук підрядка у тексті
    for i in range(n - m + 1):
        if p_hash == t_hash:  # Якщо хеші співпадають, перевіряємо підрядок додатково
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                return i  # Повертаємо індекс початку збігу
        if i < n - m:  # Обчислюємо хеш для наступного відрізка тексту
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            if t_hash < 0:  # Враховуємо від'ємні значення хешу
                t_hash += prime
    return -1  # Якщо не знайдено входження підрядка, повертаємо -1

article_1 = ""
article_2 = ""

real_pattern = "формули інтерполяції"  
fictional_pattern = "кризисна"  

#стаття 1
results_article_1 = []
results_article_1.append(["Real pattern", "Boyer-Moore", timeit.timeit(lambda: boyer_moore_search(article_1, real_pattern), number=100)])
results_article_1.append(["Real pattern", "Knuth-Morris-Pratt", timeit.timeit(lambda: kmp_search(article_1, real_pattern), number=100)])
results_article_1.append(["Real pattern", "Rabin-Karp", timeit.timeit(lambda: rabin_karp_search(article_1, real_pattern), number=100)])
results_article_1.append(["Fictional pattern", "Boyer-Moore", timeit.timeit(lambda: boyer_moore_search(article_1, fictional_pattern), number=100)])
results_article_1.append(["Fictional pattern", "Knuth-Morris-Pratt", timeit.timeit(lambda: kmp_search(article_1, fictional_pattern), number=100)])
results_article_1.append(["Fictional pattern", "Rabin-Karp", timeit.timeit(lambda: rabin_karp_search(article_1, fictional_pattern), number=100)])

#стаття 2
results_article_2 = []
results_article_2.append(["Real pattern", "Boyer-Moore", timeit.timeit(lambda: boyer_moore_search(article_2, real_pattern), number=100)])
results_article_2.append(["Real pattern", "Knuth-Morris-Pratt", timeit.timeit(lambda: kmp_search(article_2, real_pattern), number=100)])
results_article_2.append(["Real pattern", "Rabin-Karp", timeit.timeit(lambda: rabin_karp_search(article_2, real_pattern), number=100)])
results_article_2.append(["Fictional pattern", "Boyer-Moore", timeit.timeit(lambda: boyer_moore_search(article_2, fictional_pattern), number=100)])
results_article_2.append(["Fictional pattern", "Knuth-Morris-Pratt", timeit.timeit(lambda: kmp_search(article_2, fictional_pattern), number=100)])
results_article_2.append(["Fictional pattern", "Rabin-Karp", timeit.timeit(lambda: rabin_karp_search(article_2, fictional_pattern), number=100)])

# Print the results in tabular format
print("Results for Article 1:")
print(tabulate(results_article_1, headers=["Pattern Type", "Algorithm", "Execution Time"]))
print("\nResults for Article 2:")
print(tabulate(results_article_2, headers=["Pattern Type", "Algorithm", "Execution Time"]))


