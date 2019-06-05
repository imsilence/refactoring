#encoding: utf-8

import abc
import json
import math

'''
多态取代条件表达式
'''

class PerformanceCalculator(abc.ABC):

    def __init__(self, performance, play):
        self.__performance = performance
        self.__play = play

    @property
    def play(self):
        return self.__play

    @property
    def performance(self):
        return self.__performance

    @abc.abstractmethod
    def amount(self):
        pass

    @abc.abstractmethod
    def credits(self):
        pass


class TragedyPerformanceCalculator(PerformanceCalculator):

    def amount(self):
        rt_amount = 40000
        if self.performance['audience'] > 30:
            rt_amount += 1000 * (self.performance['audience'] - 30)
        return rt_amount

    def credits(self):
        return max(self.performance['audience'] - 30, 0)


class ComedyPerformanceCalculator(PerformanceCalculator):

    def amount(self):
        rt_amount = 30000 + 300  * self.performance['audience']
        if self.performance['audience'] > 20:
            rt_amount += 10000 + 500 * (self.performance['audience'] - 20)
        return rt_amount

    def credits(self):
        return max(self.performance['audience'] - 30, 0) + math.floor(self.performance['audience'] / 5)


def create_performance_calculator(performance, play):
    calculators = {
        'tragedy' : TragedyPerformanceCalculator,
        'comedy' : ComedyPerformanceCalculator,
    }

    calculator = calculators.get(play.get('type'))
    if calculator is None:
        raise Exception("not found calculator: {0}".format(play.get('type')))
    return calculator(performance, play)


def statement(invoice, plays):
    return render_text(create_data(invoice, plays))


def create_data(invoice, plays):

    def play_for(performance):
        return plays.get(performance.get('playId', 0), {})

    def enrich_performances(performance):
        calculator = create_performance_calculator(performance, play_for(performance))
        rt = performance.copy()
        rt['play'] = calculator.play
        rt['amount'] = calculator.amount()
        rt['credits'] = calculator.credits()
        return rt

    def total_amount(data):
        rt_amount = 0
        for performance in data['performances']:
            rt_amount += performance.get('amount')
        return rt_amount


    def total_credits(data):
        rt_credits = 0
        for performance in data['performances']:
            rt_credits += performance.get('credits')
        return rt_credits

    data = {}
    data['customer'] = invoice.get('customer')
    data['performances'] = [enrich_performances(p) for p in invoice.get('performances')]
    data['total_amount'] = total_amount(data)
    data['total_credits'] = total_credits(data)
    return data


def rmb(amount):
    return amount / 100


def render_text(data):
    print("Statement for: {0}".format(data['customer']))
    for performance in data['performances']:
        print("\t{0}: {1} ({2} seats)".format(performance.get('play').get('name'), rmb(performance['amount']), performance['audience']))

    print("total: {0}".format(rmb(data['total_amount'])))
    print("credits: {0}".format(data['total_credits']))
    return data['total_amount'], data['total_credits']


if __name__ == '__main__':
    invoices = []
    with open("invoices.json", "rt", encoding="utf-8") as cxt:
        invoices = json.loads(cxt.read())

    plays = {}
    with open("plays.json", "rt", encoding="utf-8") as cxt:
        plays = json.loads(cxt.read())

    for invoice in invoices:
        statement(invoice, plays)