import unittest
from bot_class import PizzaBot
from state_machine import StateMachine


class TestBot(unittest.TestCase):
    """Класс для тестирования бота"""

    def setUp(self):
        self.handler = PizzaBot()
        self.chat_id = '1385'
        self.handler.get_or_create_state(self.chat_id)
        self.data = self.handler.data

    def test_for_start(self):
        self.data[self.chat_id]['state'] = StateMachine('start_state')
        self.assertEqual(self.handler.get_response(self.chat_id, '/start'),
                         "Здравствуйте. Какую вы хотите пиццу? Большую или маленькую?")

    def test_for_wrong_food_size(self):
        self.data[self.chat_id]['state'] = StateMachine('food_size')
        self.assertEqual(self.handler.get_response(self.chat_id, "Неправильный текст"),
                         "Вы не указали размер!\nКакую вы хотите пиццу? Большую или маленькую?")

    def test_for_correct_food_size(self):
        self.data[self.chat_id]['state'] = StateMachine('food_size')
        self.assertEqual(self.handler.get_response(self.chat_id, "Большую"),
                         "Как вы будете платить (наличкой/картой)?")

    def test_for_wrong_payment_form(self):
        self.data[self.chat_id]['state'] = StateMachine('payment_form')
        self.assertEqual(self.handler.get_response(self.chat_id, "2"),
                         "Вы не указали способ оплаты!\nКак вы будете платить (наличкой/картой)?")

    def test_for_correct_payment_form(self):
        self.data[self.chat_id]['state'] = StateMachine('payment_form')
        self.data[self.chat_id]['pizza_size'] = "большую"
        self.assertEqual(self.handler.get_response(self.chat_id, "Наличкой"),
                         f"Вы хотите {self.data[self.chat_id]['pizza_size']} пиццу, оплата - "
                         f"{self.data[self.chat_id]['payment_variation']}?")

    def test_for_wrong_checking(self):
        self.data[self.chat_id]['state'] = StateMachine('checking')
        self.assertEqual(self.handler.get_response(self.chat_id, "Куда"),
                         f"Подтвердите пожалуйста заказ.\nВы хотите {self.data[self.chat_id]['pizza_size']} "
                         f"пиццу, оплата - {self.data[self.chat_id]['payment_variation']}?"
                         )

    def test_for_negative_checking(self):
        self.data[self.chat_id]['state'] = StateMachine('checking')
        self.assertEqual(
            self.handler.get_response(self.chat_id, 'нет'),
            'Начните пожалуйста заказ заново. Введите команду /start'
        )

    def test_for_positive_checking(self):
        self.data[self.chat_id]['state'] = StateMachine('checking')
        self.assertEqual(
            self.handler.get_response(self.chat_id, 'да'),
            'Спасибо за заказ!'
        )

    def test_for_reset(self):
        self.assertEqual(
            self.handler.get_response(self.chat_id, '/reset'),
            'Для того, чтобы начать заново, введите команду /start'
        )

    def test_for_default_answer(self):
        self.data[self.chat_id]['state'] = StateMachine('start_state')
        self.assertEqual(
            self.handler.get_response(self.chat_id, 'Привет!'),
            'Для начала заказа введите: /start'
        )


if __name__ == "__main__":
    unittest.main()