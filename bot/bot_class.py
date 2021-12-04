from state_machine import StateMachine


class PizzaBot:
    """Класс для заказа пиццы"""
    def __init__(self):
        self.data = {}

    def get_or_create_state(self, chat_id):
        """Получение или создание состояния"""
        try:
            return self.data[chat_id]['state'].state
        except KeyError:
            self.data.update({
                chat_id: {
                    'state': StateMachine(),
                    'pizza_size': None,
                    'payment_variation': None,
                }
            })
            return self.data[chat_id]['state'].state

    def get_response(self, chat_id, message):
        """Работа с получаемым текстом пользователя"""
        text = message.lower()
        if self.get_or_create_state(chat_id) == 'start_state' and text == '/start':
            self.data[chat_id]['state'].next_state()
            return f"Здравствуйте. Какую вы хотите пиццу? Большую или маленькую?"

        elif text == "/reset":
            self.data[chat_id]['state'].cancel()
            return "Для того, чтобы начать заново, введите команду /start"

        elif self.get_or_create_state(chat_id) == 'food_size':
            if (text == "большую") or (text == "маленькую"):
                self.data[chat_id]['pizza_size'] = text
                self.data[chat_id]['state'].next_state()
                return "Как вы будете платить (наличкой/картой)?"
            else:
                return "Вы не указали размер!\nКакую вы хотите пиццу? Большую или маленькую?"

        elif self.get_or_create_state(chat_id) == "payment_form":
            if text == "наличкой" or text == "картой":
                self.data[chat_id]['payment_variation'] = text
                self.data[chat_id]['state'].next_state()
                return f"Вы хотите {self.data[chat_id]['pizza_size']} пиццу, оплата - " \
                       f"{self.data[chat_id]['payment_variation']}?"
            else:
                return "Вы не указали способ оплаты!\nКак вы будете платить (наличкой/картой)?"

        elif self.get_or_create_state(chat_id) == 'checking':
            if text == "да":
                self.data[chat_id]['state'].next_state()
                return "Спасибо за заказ!"
            elif text == "нет":
                self.data[chat_id]['state'].cancel()
                return "Начните пожалуйста заказ заново. Введите команду /start"
            else:
                return f"Подтвердите пожалуйста заказ.\nВы хотите {self.data[chat_id]['pizza_size']} " \
                       f"пиццу, оплата - {self.data[chat_id]['payment_variation']}?"

        return "Для начала заказа введите: /start"
