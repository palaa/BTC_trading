#!/bin/env python
#encoding=utf-8
# Author: shaolong - shaolong@sogou-inc.com
# Last modified: 2014-08-10 17:55
# Filename: sim_trade.py
# Description: 
import huobi
import sys
import time

hb= huobi.Huobi()
last_bid_cap = None
last_ask_cap = None
golden_ball = 0
is_holding = False
holding_cost = 0

LOG_BUFS = ['', '']
LOG_INDEX = 0


def log(string=''):
    pass
    global LOG_BUFS
    global LOG_INDEX

    log_str = time.strftime("%F %T")
    log_str += '\t'
    log_str += string
    log_str += '\n'
    LOG_BUFS[LOG_INDEX] += log_str
    if len(LOG_BUFS[LOG_INDEX]) > 220:
        LOG_INDEX = 1 - LOG_INDEX
        f = file('log.txt', 'a')
        f.write(LOG_BUFS[1 - LOG_INDEX])
        f.flush()
        f.close()
        LOG_BUFS[1 - LOG_INDEX] = ''


def log_trade(string=''):
    pass
    log_str = time.strftime("%F %T")
    log_str += '\t'
    log_str += string
    log_str += '\n'
    f = file('trade_log.txt', 'a')
    f.write(string)
    f.flush()
    f.close()

def get_current_cap():
    global bc
    ask_cap = 0.0
    bid_cap = 0.0
    hb.get_market_depth()

    # calculating ask cap
    lowest_ask_price = float(hb.market_depth[u'asks'][-1][0])
    
    for item in hb.market_depth[u'asks']:
        price = float(item[0])
        amount = item[1]
        #ask_cap += price * amount
        cap_delta = amount / (price - lowest_ask_price + 1.0)
        ask_cap += cap_delta
        #print 'ask\t%.2f\t%.2f\t%.4f\t%.4f' %(price, amount, cap_delta, ask_cap)

    # calculating bid cap
    highest_bid_price = float(hb.market_depth[u'bids'][0][0])
    for item in hb.market_depth[u'bids']:
        price = float(item[0])
        amount = item[1]
        #bid_cap += price * amount
        cap_delta = amount / (highest_bid_price - price + 1.0)
        bid_cap += cap_delta
        #print 'bid\t%.2f\t%.2f\t%.4f\t%.4f' %(price, amount, cap_delta, bid_cap)

    #sys.exit()
    return (ask_cap, bid_cap, lowest_ask_price, highest_bid_price)



def thread_process():
    pass
    global last_bid_cap
    global last_ask_cap
    global golden_ball
    global is_holding

    ask_cap, bid_cap, ask_price, bid_price = get_current_cap()
    '''
    log("%.2f\t%.2f\t" % (bid_cap, ask_cap) + str(bid_price) + '\t' + str(ask_price) +'\t'+ str(golden_ball))
    #print bid_cap, '\t', ask_cap, '\t', bid_price, '\t', ask_price
    if bid_cap > 2 * ask_cap and False == is_holding:
        log("BUY :\t%.2f" % ask_price)
        log_trade("\nBUY :\t%.2f" % ask_price)
        is_holding = True 
    if bid_cap < ask_cap and True == is_holding:
        log("SELL:\t%.2f" % bid_price)
        log_trade("\nSELL:\t%.2f" % bid_price)
        is_holding = False
    return
    '''

    if last_ask_cap and last_bid_cap:
        pass
        ask_cap_delta = ask_cap - last_ask_cap
        bid_cap_delta = bid_cap - last_bid_cap
        log("bid_cap:%.2f\tdelta:%.2f\task_cap:%.2f\tdelta:%.2f\tBall:%d" \
                % (bid_cap, bid_cap_delta, ask_cap, ask_cap_delta, golden_ball))
        if ask_cap_delta > 0 and bid_cap_delta < 0:
            golden_ball += 1
        elif ask_cap_delta < 0  and bid_cap_delta > 0:
            golden_ball -= 1

        if golden_ball > 7 and False == is_holding:
            #print "BUY :\t", ask_price
            log("BUY :\t%.2f\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" % ask_price)
            is_holding = True
            holding_cost = ask_price
            golden_ball = 0

        if golden_ball < -7 and True == is_holding:
            log("SELL:\t%.2f\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" % bid_price)
            log_trade("BUY:\t%d\tSELL:\t%d\tProfit:%.2f\tPersent:%.4f%%" % ( \
                    holding_cost, bid_price, bid_price - holding_cost,\
                    (bid_price - holding_cost) / holding_cost * 100.0))
            log("BUY:\t%d\tSELL:\t%d\tProfit:%.2f\tPersent:%.4f%%" % ( \
                    holding_cost, bid_price, bid_price - holding_cost,\
                    (bid_price - holding_cost) / holding_cost * 100.0))
            holding_cost = 0
            is_holding = False
            golden_ball = 0

    last_ask_cap = ask_cap
    last_bid_cap = bid_cap

def thread_process_cap_delta():
    # when bid cap regress significantly and ask cap increase in very short time .BUY
    pass
    global last_bid_cap
    global last_ask_cap
    global golden_ball
    global is_holding

    ask_cap, bid_cap, ask_price, bid_price = get_current_cap()

    if last_ask_cap and last_bid_cap:
        pass
        bid_cap_delta = bid_cap - last_bid_cap
        ask_cap_delta = ask_cap - last_ask_cap
        cap_delta = ask_cap_delta - bid_cap_delta
        golden_ball += cap_delta
        log("bid_cap: %.2f\tdelta:  %.2f\task_cap: %.2f\tdelta:  %.2f\tCap_delta:  %.2f\tBall: %.2f\tbid: %.2f\task: %.2f" \
                % (bid_cap, bid_cap_delta, ask_cap, ask_cap_delta, cap_delta, golden_ball, bid_price, ask_price))

        if golden_ball > 200 and False == is_holding:
            #print "BUY :\t", ask_price
            log("BUY :\t%.2f\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" % ask_price)
            is_holding = True
            holding_cost = ask_price
            golden_ball = 0

        if golden_ball < -200 and True == is_holding:
            log("SELL:\t%.2f\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" % bid_price)
            log_trade("BUY:\t%d\tSELL:\t%d\tProfit:%.2f\tPersent:%.4f%%" % ( \
                    holding_cost, bid_price, bid_price - holding_cost,\
                    (bid_price - holding_cost) / holding_cost * 100.0))
            log("BUY:\t%d\tSELL:\t%d\tProfit:%.2f\tPersent:%.4f%%" % ( \
                    holding_cost, bid_price, bid_price - holding_cost,\
                    (bid_price - holding_cost) / holding_cost * 100.0))
            holding_cost = 0
            is_holding = False
            golden_ball = 0

    last_ask_cap = ask_cap
    last_bid_cap = bid_cap
    golden_ball = golden_ball * 0.97




if __name__ == '__main__':
    pass
    print >> sys.stderr, "Starting Algorithm"

    while(True):
        thread_process_cap_delta()
        time.sleep(1)
        #print >> sys.stderr,"golden_ball = ", golden_ball

