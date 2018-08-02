import os
import json


class ChatBot:
    def __init__(self):
        self.bot_path = os.path.join(os.path.dirname(__file__), 'bots')
        print(self.bot_path)
        self.bots = os.listdir(self.bot_path)
        # print(bot_list)

    def select_bot(self):
        print('아래 봇 중 채팅할 봇을 선택하세요.')
        bot_list = []
        for idx, bot in enumerate(self.bots):
            path = os.path.join(self.bot_path, bot)
            with open(path, 'r', encoding='utf-8') as file:
                j = json.load(file)
                # print(j, type(j))
                bot_list.append(j)
                print(f'{idx+1}. BotName: {j["BotName"]}, Description: {j["Description"]}')
                # lines = file.readlines()
                # for line in lines:
                #     print(line)
        selected_bot = input('선택: ')
        return selected_bot


if __name__ == '__main__':
    print('[[[namsu-chat started]]]')
    chat_bot = ChatBot()
    sel_bot = chat_bot.select_bot()
    print(sel_bot)
