"""Training of the agent

Author: YANG, Austin Liu
Created Date: Feb. 26, 2017
Modified Date: Mar. 6 2017
"""


import pytz
from datetime import datetime
from zipline.api import (
    order,
    symbol,
    get_datetime)
import random
from global_values import (
    directory_log,
    TP_matrixs,
    mu, portfolio_prev,
    epsilon, gama, action_set, date_prev, action_prev, Q_function)
import pdb


def initialize_train(context):
    # AAPL
    context.security = symbol('AAPL')

    print(directory_log)


def handle_data_train(context, data):
    pdb.set_trace()

    # Get current date
    now = str(get_datetime('US/Eastern'))[0:11] + "00:00:00+0000"

    # Get current state
    state = TP_matrixs.ix(now)

    # Epsilon-greedy Algorithm
    # Choose an action to execute according to current state
    probab = random.random()
    if probab <= epsilon:
        # Epsilon
        # Take random action
        action = action_set[random.randint(0, 2)]
    else:
        # 1 - epsilon
        # Take the action of the highest Q-Value
        action_values = [Q_function(state, action_set[0]),
                         Q_function(state, action_set[1]),
                         Q_function(state, action_set[2])]
        action = action_set[action_values.index(max(action_values))]

    # Execute chosen action
    if action == action_set[0]:
        # Sell
        order(context.security, -mu)
    elif action == action_set[1]:
        # Buy
        order(context.security, mu)
    elif action == action_set[2]:
        # Hold
        pass

    # Produce training data
    global date_prev, action_prev, portfolio_prev
    y = context.portfolio.portfolio_value - \
        portfolio_prev + gama * Q_function(state, action)
    if action_prev == 'sell':
        # Previous taken action is "sell"
        global data_train_sell
        data_train_sell.addSample((state_prev[:]), (y))
    elif action_prev == 'buy':
        # Previous taken action is "buy"
        global data_train_buy
        data_train_buy.addSample((state_prev[:]), (y))
    elif action_prev == 'hold':
        # Previous taken action is "hold"
        global data_train_hold
        data_train_hold.addSample((state_prev[:]), (y))

    # Update saved previous information
    state_prev = state[:]
    action_prev = action
    portfolio_prev = context.portfolio.portfolio_value
