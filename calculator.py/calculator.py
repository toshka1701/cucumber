from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

# Определяем состояния для ConversationHandler
CHOOSING, NUM1, NUM2 = range(3)

# Функции калькулятора
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

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> int:
    keyboard = [["Сложение", "Вычитание"], ["Умножение", "Деление"], ["История", "Выход"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Выберите операцию:",
        reply_markup=reply_markup,
    )
    return CHOOSING

# Обработчик выбора операции
async def choose_operation(update: Update, context: CallbackContext) -> int:
    user_choice = update.message.text
    context.user_data['operation'] = user_choice

    if user_choice == "История":
        history = context.user_data.get('history', [])
        if not history:
            await update.message.reply_text("История операций пуста.")
        else:
            await update.message.reply_text("\nИстория операций:\n" + "\n".join(history))
        return CHOOSING
    elif user_choice == "Выход":
        await update.message.reply_text("Выход из программы.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Введите первое число:")
        return NUM1

# Обработчик ввода первого числа
async def num1(update: Update, context: CallbackContext) -> int:
    try:
        num1 = float(update.message.text)
        context.user_data['num1'] = num1
        await update.message.reply_text("Введите второе число:")
        return NUM2
    except ValueError:
        await update.message.reply_text("Ошибка: введите числовое значение.")
        return NUM1

# Обработчик ввода второго числа и выполнения операции
async def num2(update: Update, context: CallbackContext) -> int:
    try:
        num2 = float(update.message.text)
        num1 = context.user_data['num1']
        operation = context.user_data['operation']

        result = None
        operation_str = ""

        if operation == "Сложение":
            result = add(num1, num2)
            operation_str = f"{num1} + {num2} = {result}"
        elif operation == "Вычитание":
            result = subtract(num1, num2)
            operation_str = f"{num1} - {num2} = {result}"
        elif operation == "Умножение":
            result = multiply(num1, num2)
            operation_str = f"{num1} * {num2} = {result}"
        elif operation == "Деление":
            result = divide(num1, num2)
            operation_str = f"{num1} / {num2} = {result}"

        if result is not None:
            await update.message.reply_text(f"Результат: {result}")
            # Сохраняем операцию в историю
            if 'history' not in context.user_data:
                context.user_data['history'] = []
            context.user_data['history'].append(operation_str)
    except ValueError:
        await update.message.reply_text("Ошибка: введите числовое значение.")
        return NUM2

    return CHOOSING

# Обработчик команды /cancel
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Операция отменена.")
    return ConversationHandler.END

# Основная функция
def main() -> None:
    # Вставьте сюда ваш токен
    token = "7834035155:AAE_W3PyMqGLjsa-hFS603XQ7ZqeSralVGA"

    # Создаем приложение и передаем токен
    application = Application.builder().token(token).build()

    # Определяем ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, choose_operation)
            ],
            NUM1: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, num1)
            ],
            NUM2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, num2)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем ConversationHandler в приложение
    application.add_handler(conv_handler)

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()