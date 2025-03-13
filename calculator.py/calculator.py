def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Ошибка: деление на ноль!"
    return x / y

def calculator():
    history = []  # Список для хранения истории операций

    while True:
        print("\nВыберите операцию:")
        print("1. Сложение")
        print("2. Вычитание")
        print("3. Умножение")
        print("4. Деление")
        print("5. Показать историю операций")
        print("6. Выход")

        choice = input("Введите номер операции (1/2/3/4/5/6): ")

        if choice == '6':
            print("Выход из программы.")
            break

        if choice == '5':
            if not history:
                print("История операций пуста.")
            else:
                print("\nИстория операций:")
                for operation in history:
                    print(operation)
            continue

        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Введите первое число: "))
                num2 = float(input("Введите второе число: "))
            except ValueError:
                print("Ошибка: введите числовое значение.")
                continue

            result = None
            operation_str = ""

            if choice == '1':
                result = add(num1, num2)
                operation_str = f"{num1} + {num2} = {result}"
            elif choice == '2':
                result = subtract(num1, num2)
                operation_str = f"{num1} - {num2} = {result}"
            elif choice == '3':
                result = multiply(num1, num2)
                operation_str = f"{num1} * {num2} = {result}"
            elif choice == '4':
                result = divide(num1, num2)
                operation_str = f"{num1} / {num2} = {result}"

            if result is not None:
                print(f"Результат: {result}")
                history.append(operation_str)  # Добавляем операцию в историю
        else:
            print("Неверный ввод")

if __name__ == "__main__":
    calculator()