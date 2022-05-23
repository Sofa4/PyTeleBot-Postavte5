import requests

# -----------------------------------------------------------------------
# вместо того, что бы делать еще один класс, обойдёмся без него - подумайте, почему и как
activeGames = {}  # Тут будем накапливать все активные игры. У пользователя может быть только одна активная игра


def newGame(chatID, newGame):
    activeGames.update({chatID: newGame})
    return newGame


def getGame(chatID):
    return activeGames.get(chatID)


def stopGame(chatID):
    activeGames.pop(chatID)


# -----------------------------------------------------------------------
class GameRPS:
    values = ["Камень", "Ножницы", "Бумага"]
    games_results = {}

    name = 'кнб'

    @classmethod
    def __init__(cls, chat_id):
        cls.computerChoice = cls.getRandomChoice()

    @classmethod
    def newGame(cls, chat_id, message_id):
        cls.computerChoice = cls.getRandomChoice()

        round_text = '⠀⠀⠀⠀<b>Игровой⠀раунд</b>' + '\n\n' + \
                     'Игрок:    <b>???</b>' + '\n' + \
                     'Компьютер:    <b>???</b>'

        cls.games_results[str(chat_id)] = {}
        cls.games_results[str(chat_id)][str(message_id)] = round_text

    @classmethod
    def editGameResult(cls, chat_id, message_id, result_text):
        cls.games_results[str(chat_id)][str(message_id)] = result_text

    @classmethod
    def getRandomChoice(cls):
        import random

        lenValues = len(cls.values)
        rndInd = random.randint(0, lenValues-1)
        return cls.values[rndInd]

    def playerChoice(self, player1Choice):
        code = player1Choice[0] + self.computerChoice[0]
        if player1Choice == self.computerChoice:
            winner = "Ничья!"
        elif code == "КН" or code == "БК" or code == "НБ":
            winner = "Игрок выиграл!"
        else:
            winner = "Компьютер выиграл!"

        return f"{player1Choice} vs {self.computerChoice} => " + winner


# -----------------------------------------------------------------------
class gameTicTacToe:
    fields = {}
    games_results = {}

    name = 'ттт'

    @classmethod
    def __init__(cls, chat_id):
        cls.fields[str(chat_id)] = {}
        cls.games_results[str(chat_id)] = {}

    @classmethod
    def newGame(cls, chat_id, message_id):
        field = [0 for i in range(9)]

        cls.fields[str(chat_id)][str(message_id)] = field
        cls.games_results[str(chat_id)][str(message_id)] = "❌ Игрок\n" + \
                                                           "⭕ Компьютер"
    @classmethod
    def editGameResult(cls, chat_id, message_id, result_text):
        cls.games_results[str(chat_id)][str(message_id)] = result_text

    @classmethod
    def getField(cls, chat_id, message_id):
        return cls.fields[str(chat_id)][str(message_id)]

    @classmethod
    def computerChoice(cls, chat_id, message_id):
        import random

        field = cls.getField(chat_id, message_id)

        x = random.randint(0, 2)
        y = random.randint(0, 2)

        while field[x + y * 3] != 0:
            x = random.randint(0, 2)
            y = random.randint(0, 2)

        # Ход компьютера
        field[x + y * 3] = 2

        cls.fields[str(chat_id)][str(message_id)] = field

    @classmethod
    def gameEndCheck(cls, chat_id, message_id):
        # Проверка на пообеду крестиков
        if cls.winnerCheck(chat_id, message_id, 1):
            return 1

        # Проверка на пообеду ноликов
        elif cls.winnerCheck(chat_id, message_id, 2):
            return 2

        # Проверка на ничью
        elif 0 not in cls.fields[str(chat_id)][str(message_id)]:
            return 3

        # Игра не завершена
        return 0

    @classmethod
    def winnerCheck(cls, chat_id, message_id, winner_check):
        field = cls.getField(chat_id, message_id)

        cond_list = []

        # Проверка заполнены ли строки одинаковыми символами
        for i in range(3):
            cond_list.append(field[0 + 3 * i:3 + 3 * i].count(winner_check) == 3)

        # Проверка заполнены ли столбцы одинаковыми символами
        for i in range(3):
            cond_list.append([field[0 + i], field[3 + i], field[6 + i]].count(winner_check) == 3)

        # Проверка заполнены ли диагонали одинаковыми символами
        cond_list.append([field[0], field[4], field[8]].count(winner_check) == 3)
        cond_list.append([field[2], field[4], field[6]].count(winner_check) == 3)

        return True in cond_list

    @classmethod
    def playerChoice(cls, chat_id, message_id, field_number):
        cls.fields[str(chat_id)][str(message_id)][field_number] = 1


# -----------------------------------------------------------------------
if __name__ == "__main__":
    print("Этот код должен использоваться ТОЛЬКО в качестве модуля!")
