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

    def amount_for(performance, play):
        rt_amount = 0
        if play['type'] == 'tragedy':
            rt_amount = 40000
            if performance['audience'] > 30:
                rt_amount += 1000 * (performance['audience'] - 30)
        elif play['type'] == 'comedy':
            rt_amount = 30000 + 300 * performance['audience']
            if performance['audience'] > 20:
                rt_amount += 10000 + 500 * (performance['audience'] - 20)
        else:
            print("error type: {0}", play['type'])
        return rt_amount

    for performance in invoice['performances']:
        play = plays.get(performance['playId'])
        if not play:
            print("error playId: {0}".format(performance['playId']))
            continue

        amount = amount_for(performance, play)

        credits += max(performance['audience'] - 30, 0)
        if 'comedy' == play['type']:
            credits += math.floor(performance['audience'] / 5)

        total += amount
        print("\t{0}: {1} ({2} seats)".format(play['name'], amount / 100, performance['audience']))

    print("total: {0}".format(total / 100))
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