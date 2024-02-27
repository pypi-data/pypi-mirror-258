from faker import Faker
from random import random, choice
from sub_classes import *


class AA:
    def __init__(self, neuron_one, neuron_two):
        self.neurons = [neuron_one, neuron_two]
    
    def generate_random_fucking_project(self):
        fake = Faker('ru_RU')
        return Project(hash(random()), fake.name())
    
    def generate_answer(self):
        return choice(["Да", "Нет", "Забыл"])
    
    def is_go_to_lessons(self):
        return random() < 0.1
