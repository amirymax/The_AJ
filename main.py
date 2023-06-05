from nltk.stem.lancaster import LancasterStemmer
import json
import pickle
from tensorflow.python.framework import ops
import logging

logging.getLogger('tensorflow').disabled = True

import tflearn
import numpy
from nltk import word_tokenize
from brain import get_json
from brain.right_hemisphere import GAFD
from brain import right_hemisphere as right
import random
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
stemmer = LancasterStemmer()


class AJ:
    def __init__(self):
        self.database = None
        self.yes = None
        self.model = None
        self.data = None
        self.output = None
        self.training = None
        self.labels = None
        self.words = None
        self.name = 'AJ'
        self.options = {1: 'self.db_all()', 2: 'self.db_filter()', 3: 'self.db_by_day()'}

    def load_data(self):
        with open("brain/all_data/intents.json", encoding='utf-8') as file:
            self.data = json.load(file)

    def load_model_data(self):
        with open("brain/all_data/data.pickle", "r") as f:
            self.words, self.labels, self.training, self.output = pickle.load(f)

    def retrain(self):
        from brain.train_again import training, words, output
        self.training = training
        self.words = words
        self.output = output

    def train(self):
        ops.reset_default_graph()
        net = tflearn.input_data(shape=[None, len(self.training[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(self.output[0]), activation="softmax")
        net = tflearn.regression(net)

        self.model = tflearn.DNN(net)

    def load_model(self):
        self.model.load("brain/all_data/model.tflearn")

    def save_model(self):
        self.train()
        self.model.fit(self.training, self.output, n_epoch=1000, batch_size=8, show_metric=True)
        self.model.save("brain/all_data/model.tflearn")

    def bag_of_words(self, s: str):
        bag = [0 for _ in range(len(self.words))]

        s_words = word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(self.words):
                if w == se:
                    bag[i] = 1

        return numpy.array(bag)

    def chat(self):
        labels = get_json.list_of_tags()
        print("Бот запустить шид ")
        last_saying = 'оли хичи нагуфтай'
        answer_not_printed = True
        while True:
            inp = input("::::\n\t")
            if inp.lower() == 'стоп':

                f = self.data['intents']
                for i in range(len(f)):
                    print(f'Tag {i + 1}:', f[i]['tag'])

                number_of_tag: int = int(input('чандм тег? '))
                get_json.update(last_saying, number_of_tag)

            last_saying: str = inp
            results = self.model.predict([self.bag_of_words(inp)])

            results_index = numpy.argmax(results)

            tag = labels[results_index]
            if tag == 'stop': print('Давай радной');break

            answer = random.choice(self.data['intents'][results_index]['responses'])

            if tag == 'db':
                print(answer)
                answer_not_printed = False
                self.answer_yes_no()
                if self.yes:
                    text = input('Ку гап за брат чи гап шид?\n')
                    date = input('Кай шид и гап?\n')
                    right.write_daybook(text, date)
                    print("Навиштм, тамом")
                else:
                    print(f'Хай чи агане?\n')

            elif tag == 'from_db':
                self.answer_yes_no()
                answer_not_printed = False

                if self.yes:
                    self.from_db()
                else:
                    print(f'Хай чи агане?\n')
            elif tag=='google':
                self.answer_yes_no(answer)
                answer_not_printed=False
                if self.yes:
                    right.search_on_google()

            if answer_not_printed: print(answer)

    def answer_yes_no(self, confirmation=''):
        print(confirmation)
        while True:
            try:
                self.yes = int(input('0 - нея\n1 - ова\n::::\n\t'))
                if self.yes != 0 and self.yes != 1:
                    raise ValueError
                break
            except ValueError:
                print('абача 1 ё 0 бнавис')

    def from_db(self):
        self.database = GAFD()
        print('ЧхелӢ бброрм?\n1. Ҳамаша\n2. ай кай то кай\n3. рузқати\n4. ягонташ, гапа хато фаҲмидӢ\n::::')
        while True:
            try:
                option = int(input('\t'))
                break
            except ValueError:
                print('Рақамша навис')
        eval(self.options[option])

    def db_all(self):
        self.answer_yes_no('Ҳамаи записора нишон бтм?')
        if self.yes:
            self.database.print_all()
            print("Ҳаамаи записое, ки да БД навиштай")
        else:
            self.from_db()

    def db_filter(self):
        self.answer_yes_no('Ай як вақт то я вақта нишон бтм?')
        if self.yes:
            days = self.database.get_all()[0]
            for i in range(len(days)):
                print(f'{i + 1}', days[i])
            index1 = self.try_get_int('Ай кай?', 'Рақамша ай списоки боло навис')
            index2 = self.try_get_int('То кай?', 'Рақамша ай списоки боло навис')
            date1, date2 = days[index1 - 1], days[index2 - 1]
            self.database.get_by_date(date1, date2)
        else:
            self.from_db()

    def db_by_day(self):
        self.answer_yes_no('Ягон рузи аниқа нишон бтм?')
        if self.yes:
            days, times, speeches = self.database.get_all()
            print("Кадом руз?")
            for i in range(len(days)):
                print(f'{i + 1} - {days[i]}')
            while True:
                try:
                    day = int(input('::::\n\t'))
                    print(days[day - 1], times[day - 1], speeches[day - 1])
                    break
                except ValueError:
                    print('Рақамша навис')
        else:
            self.from_db()

    def try_get_int(self, input_text: str, error_text: str) -> int:
        while True:
            try:
                number = int(input(input_text + '\n::::\n\t'))
                break
            except ValueError:
                print(error_text)
        return number

    def start(self):
        self.load_data()
        try:
            self.load_model_data()
        except:
            self.retrain()
        self.train()
        try:

            self.load_model()
        except:
            print('Сохранит кадестам...')
            self.save_model()
        self.chat()


he = AJ()
he.start()
