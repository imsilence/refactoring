#encoding: utf-8

import json
import math

'''
提炼函数
'''

def statement(invoice, plays):
    total = 0
    credits = 0

    print("Statement for: {0}".format(invoice['customer']))

    def play_for(performance):
        return plays.get(performance.get('playId', 0), {})

    def amount_for(performance):
        rt_amount = 0
        type_ = play_for(performance).get('type')
        if type_ == 'tragedy':
            rt_amount = 40000
            if performance['audience'] > 30:
                rt_amount += 1000 * (performance['audience'] - 30)
        elif type_ == 'comedy':
            rt_amount = 30000 + 300 * performance['audience']
            if performance['audience'] > 20:
                rt_amount += 10000 + 500 * (performance['audience'] - 20)
        else:
            print("error type: {0}", type_)
        return rt_amount

    def credits_for(performance):
        rt_credits = max(performance['audience'] - 30, 0)
        if 'comedy' ==  play_for(performance).get('type'):
            rt_credits += math.floor(performance['audience'] / 5)
        return rt_credits

    def rmb(amount):
        return amount / 100

    for performance in invoice['performances']:
        credits += credits_for(performance)
        total += amount_for(performance)
        print("\t{0}: {1} ({2} seats)".format(play_for(performance).get('name'), rmb(amount_for(performance)), performance['audience']))

    print("total: {0}".format(rmb(total)))
    print("credits: {0}".format(credits))
    return total, credits



if __name__ == '__main__':
    invoices = []
    with open("invoices.json", "rt", encoding="utf-8") as cxt:
        invoices = json.loads(cxt.read())

    plays = {}
    with open("plays.json", "rt", encoding="utf-8") as cxt:
        plays = json.loads(cxt.read())

    for invoice in invoices:
        statement(invoice, plays)