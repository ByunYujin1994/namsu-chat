import os
import json
from pprint import pprint
import sqlite3


class ChatBot:
    def __init__(self):
        self.bot_path = os.path.join(os.path.dirname(__file__), 'bots')  # 봇들이 저장된 경로
        self.bots = [os.path.splitext(b)[0] for b in os.listdir(self.bot_path)]  # 봇들 리스트
        self.brain_path = os.path.join(os.path.dirname(__file__), 'brain')  # brain들이 저장된 경로
        self.topics = [os.path.splitext(t)[0] for t in os.listdir(self.brain_path)]  # brain들 리스트
        print(self.bot_path)
        print(self.brain_path)
        self.brain = {}  # 메모리상의 brain
        self._history = {'input': [], 'reply': []}

        self.bot_list = []
        for bot in self.bots:
            path = os.path.join(self.bot_path, bot)
            with open(path + '.json', 'r', encoding='utf-8') as file:
                j = json.load(file)
                # print(j, type(j))
                self.bot_list.append(j)

    def select_bot(self):
        print('-----아래 봇 중 채팅할 봇을 선택하세요.-----\n')
        for idx, bot in enumerate(self.bot_list):
                print(f'{idx+1}. {bot["BotName"]}: {bot["Description"]}')

        print('\n=======================================')
        selected_bot = input('선택: ')
        if selected_bot in self.bots:
            self.brain['BotName'] = selected_bot
            return True
        else:
            return False

    def load_brain(self):
        print('---start loading brain---')
        br = {}
        for t in self.topics:
            path = os.path.join(self.brain_path, t)
            with open(path + '.json', 'r', encoding='utf-8') as t_file:
                topic = json.load(t_file)
                br[topic['TopicName']] = topic['Data']

        self.brain['Data'] = br
        return

    def search(self, input_message):
        self._history['input'].insert(0, input_message)
        self._history['input'] = self._history['input'][:10]
        for topic, content in self.brain['Data'].items():
            for cont in content:
                if input_message == cont['question']:
                    print(f'{topic} 토픽에서 발견!!')
                    self._history['reply'].insert(0, cont['response'])
                    self._history['reply'] = self._history['reply'][:10]
                    return cont['response']


    # def create_chat_bot_db(self):
    #     conn = sqlite3.connect('chatbot.db')
    #     curs = conn.cursor()
    #     curs.execute('CREATE TABLE IF NOT EXISTS bots('
    #                  'botid text primary key,'
    #                  'description text)')
    #     curs.execute('CREATE TABLE IF NOT EXISTS topics('
    #                  'topicid text primary key,'
    #                  'description text)')
    #     insert_data = [(bot['BotName'], bot['Description']) for bot in self.bot_list]
    #     # print(insert_data)
    #     curs.executemany('insert into bots values (?, ?)', insert_data)
    #     conn.commit()
    #     conn.close()


if __name__ == '__main__':
    print('[[[namsu-chat started]]]')
    chat_bot = ChatBot()
    # chat_bot.create_chat_bot_db()

    while(True):
        if chat_bot.select_bot():
            chat_bot.load_brain()
            break
        else:
            print('올바르지 않은 봇입니다.')
            continue

    # print(chat_bot.brain)

    print('채팅을 시작합니다.')

    while(True):
        user_input = input('입력: ')
        if user_input == 'quit':
            break
        pprint(chat_bot.search(user_input), indent=4)
        print(chat_bot._history['input'])
        print(chat_bot._history['reply'])
