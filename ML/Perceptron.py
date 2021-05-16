import csv
import os
import random
import ML.AElement
from PIL import Image


class Perceptron():
    character_dict = {'A': 'W', 'B': 'F', 'C': '4'}
    A = []
    connectionTable = []
    lambda_a = [list([1] * 400)]
    lambda_b = [list([1] * 400)]
    lambda_c = [list([1] * 400)]
    paths = []

    percentage_of_training = 0

    sumDict = {'A': 0, 'B': 0, 'C': 0}

    def __init__(self):
        self.gen_connection_table()

        for i in range(400):
            self.A.append(ML.AElement.AElement())

    def gen_connection_table(self):
        for i in range(1600):
            self.connectionTable.append(list([0] * 400))
        for i in range(400):
            self.connectionTable[i][i] = random.choice([1, -1])
        for i in range(400, 1600):
            self.connectionTable[i][random.randint(0, 400 - 1)] = random.choice([1, -1])

    def activate_el(self, imag):
        for i in range(400):
            self.A[i].update_status(imag, [r[i] for r in self.connectionTable])

    def sum_el(self):
        self.sumDict['A'] = 0
        self.sumDict['B'] = 0
        self.sumDict['C'] = 0
        for i in range(400):
            self.sumDict['A'] += self.A[i].lambda_a * self.A[i].status
            self.sumDict['B'] += self.A[i].lambda_b * self.A[i].status
            self.sumDict['C'] += self.A[i].lambda_c * self.A[i].status

    def save_lambda(self):
        self.lambda_a.append([el.lambda_a for el in self.A])
        self.lambda_b.append([el.lambda_b for el in self.A])
        self.lambda_c.append([el.lambda_c for el in self.A])

    def update_lambda(self, path_picture):
        for i in range(400):
            if self.A[i].status == 1:
                if 'A' in path_picture:
                    self.A[i].lambda_a += 1
                    self.A[i].lambda_b -= 1
                    self.A[i].lambda_c -= 1
                elif 'B' in path_picture:
                    self.A[i].lambda_a -= 1
                    self.A[i].lambda_b += 1
                    self.A[i].lambda_c -= 1
                elif 'C' in path_picture:
                    self.A[i].lambda_a -= 1
                    self.A[i].lambda_b -= 1
                    self.A[i].lambda_c += 1

    def gen_list_paths(self, directory):
        folder = []
        for files in os.walk(directory):
            folder.append(files)

        for path in folder[0][2]:
            if path != '.DS_Store':
                self.paths.append(directory + '/' + path)

    def percentage_recognition(self, correct_answer, number_of_questions):
        self.percentage_of_training = (correct_answer * 100) / number_of_questions

    def learning(self, path_dataset, recognition_percentage):
        correct_answer = 0
        counter = 0
        self.gen_list_paths(path_dataset)

        while 1:
            random.shuffle(self.paths)
            for j in range(len(self.paths)):
                # активация элементов
                self.activate_el(self.load_image(self.paths[j]))
                # сумматор
                self.sum_el()
                # обновление лямд
                self.update_lambda(self.paths[j])
                # сохраниние лямд в массив
                self.save_lambda()
                key = max(self.sumDict, key=self.sumDict.get)
                print(key, self.sumDict)
                print(self.paths[j])

                if key in self.paths[j]:
                    correct_answer += 1
                counter += 1

            self.percentage_recognition(correct_answer, counter)
            if self.percentage_of_training >= recognition_percentage:
                break
            print(self.percentage_of_training)
        # self.save_network()

    def recognition(self, path_picture):
        self.load_network()
        # активация элементов
        self.activate_el(self.load_image(path_picture))
        # сумматор
        self.sum_el()

        key = max(self.sumDict, key=self.sumDict.get)
        print(self.character_dict[key])
        print(self.sumDict['A'], self.sumDict['B'], self.sumDict['C'])

    def load_image(self, path):
        image = Image.open(path)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()

        table = list()
        min_table = list()
        for i in range(height):
            for j in range(width):
                a = (pix[j, i][0] + pix[j, i][1] + pix[j, i][2]) / 3
                if a > 0:
                    a = 1
                else:
                    a = 0
                min_table.append(a)
            table.append(list(min_table))
            min_table.clear()
        other = []
        for i in range(len(table)):
            other += table[i]
        return other

    def save_network(self):
        # таблица подключений
        with open('TableCSV/baseTable.csv', "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.connectionTable)

        # таблица класса A
        with open('TableCSV/LamdaTableA.csv', "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.lambda_a)

        # таблица класса B
        with open('TableCSV/LamdaTableB.csv', "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.lambda_b)

        # таблица класса С
        with open('TableCSV/LamdaTableC.csv', "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.lambda_c)

    def load_network(self):
        self.lambda_a.clear()
        self.lambda_b.clear()
        self.lambda_c.clear()
        self.connectionTable.clear()
        # таблица подключений
        with open('TableCSV/baseTable.csv', "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                self.connectionTable.append([int(el) for el in row])

        # таблица класса A
        with open('TableCSV/LamdaTableA.csv', "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                self.lambda_a.append([int(el) for el in row])

        # таблица класса B
        with open('TableCSV/LamdaTableB.csv', "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                self.lambda_b.append([int(el) for el in row])

        # таблица класса C
        with open('TableCSV/LamdaTableC.csv', "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                self.lambda_c.append([int(el) for el in row])

    def update_network(self):
        # Инициализация А элементов
        # self.A.clear()
        # for i in range(400):
        #     self.A.append(ML.AElement.AElement())

        for i in range(400):
            self.A[i].lambda_a = self.lambda_a[-1][i]
            self.A[i].lambda_b = self.lambda_b[-1][i]
            self.A[i].lambda_c = self.lambda_c[-1][i]




