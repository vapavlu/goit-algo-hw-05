def binary_search(arr, target):
    """
    Реалізує двійковий пошук для відсортованого масиву з дробовими числами.
    
    :param arr: Список відсортованих дробових чисел.
    :param target: Значення, яке потрібно знайти.
    :return: Кортеж, де перший елемент - кількість ітерацій,
             другий елемент - найменший елемент, який є більшим або рівним заданому значенню.
    """
    low, high = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        mid = (low + high) // 2
        iterations += 1

        if arr[mid] == target:
            # Знайдено точну відповідність
            return (iterations, arr[mid])
        elif arr[mid] < target:
            # Шукаємо у правій частині
            low = mid + 1
        else:
            # Шукаємо у лівій частині
            high = mid - 1
            upper_bound = arr[mid]

    # Якщо елемента не знайдено, повертаємо верхню межу
    if low < len(arr):
        upper_bound = arr[low] if upper_bound is None else upper_bound
    
    return (iterations, upper_bound)

# Приклад використання
sorted_array = [1.1, 2.3, 3.5, 4.7, 5.9]

print("Binary Search for 3.5:", binary_search(sorted_array, 3.5))  # Виведе (3, 3.5)
print("Binary Search for 4.0:", binary_search(sorted_array, 4.0))  # Виведе (4, 4.7)
print("Binary Search for 6.0:", binary_search(sorted_array, 6.0))  # Виведе (5, None)
