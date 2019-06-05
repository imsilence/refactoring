#encoding: utf-8

import json
import math

'''
拆分阶段：计算详细数据+数据渲染模板(中转数据)
    提炼函数
    中转数据
    提炼函数
'''

def statement(invoice, plays):
    return render_text(create_data(invoice, plays))


def create_data(invoice, plays):

    def play_for(performance):
        return plays.get(performance.get('playId', 0), {})

    def enrich_performances(performance):
        rt = performance.copy()
        rt['play'] = play_for(rt)
        rt['amount'] = amount_for(rt)
        rt['credits'] = credits_for(rt)
        return rt

    def amount_for(performance):
        rt_amount = 0
        type_ = performance.get('play').get('type')
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
        if 'comedy' == performance.get('play').get('type'):
            rt_credits += math.floor(performance['audience'] / 5)
        return rt_credits

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