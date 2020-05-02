"""
Security class, stock/bond/currency classes, and forward/option classes. Each class has payoff,
pricing, and arbitrage methods
"""
import datetime, random
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

# alpha vantage
key = input('API key: ')
ts = TimeSeries(key, output_format='pandas')

class Security:
    """
    Security class
    """

    def __init__(self,ticker,rF=.001):

        # pull spot prices
        tick_data, _ = ts.get_monthly_adjusted(symbol=ticker)
        tick_data = tick_data.sort_index()
        S = tick_data.loc[tick_data.index[-3:-1],'5. adjusted close']

        # up/down returns
        rS_up = .1
        rS_dn = -.1

        # TODO: think about other ways to select Su, Sd, K
        Su = (1.+rS_up)*S[0]
        Sd = (1.+rS_dn)*S[0]

class Portfolio:
    """
    Portfolio class
    """
    def __init__(self,securities):
        """
        securities : list (of securities)
            List of security objects
        """
        self.securities = securities

    def plot(self):
        """
        Plots the portfolio in risk-return space
        """
        pass

class TermStructure:
    """
    Yield curve class
    """
    
    def plot(self):
        """
        Plots the yield curve
        """
        pass

    def pricing(self):
        """
        Expectations hypothesis
        """
        pass

class CrossSection:
    """
    Cross-section  class (not sure what I want this to do)
    """
    pass

class Bond(Security):
    """
    Bond class: currently only supports risk-free
    """

    def pricing(self):
        pass

    def arbitrage(self):
        pass

class Stock(Security):
    """
    Stock class
    """

    pass

    def plot(self):
        pass

    def arbitrage(self):
        pass

class Currency(Security):
    """
    Currency class
    """

    def __init__(self):
        pass

    def arbitrage(self,arbtype='timeseries'):
        """
        Parameters
        ----------
        arbtype : str
            Type of arbitrage problem. Default is 'timeseries'. Future release has 'cross-section'
        """

class Forward(Security):
    """
    Forward class
    """
    pass

    def __init__(self):

        K  = random.uniform(Sd,Su)

        # call
        Dc = (Su-K)/(Su-Sd)
        Bc = Dc*Sd/(1.+rF)
        C0 = Dc*S[0]-Bc

        # put 
        Dp = (K-Sd)/(Su-Sd)
        Bp = Dp*Su/(1.+rF)
        P0 = Bp-Dp*S[0]

        self.attr_dict = {
            'tick' : ticker,
            'date' : tick_data.index[-2].isoformat()[:10],
            'S0' : S[0],
            'S1' : S[1],
            'Su' : Su,
            'Sd' : Sd,
            'K'  : K, 
            'rF' : rF,
            'Dc' : Dc,
            'Bc' : Bc, 
            'C0' : C0,
            'Dp' : Dp,
            'Bp' : Bp,
            'P0' : P0,
            'lf' : S[0]-K, # long forward payoff
            'sf' : K-S[0]  # short forward payoff
        }

    def payoffs(self,buy=True,answer=True):
        """
        Returns a forward pricing question

        Parameters
        ----------
        buy : boolean
            If True, then long, else short
        answer : boolean
            If True, then reports the answer
        """


        if call:
            long_payoff = self.attr_dict['lc']
            if buy: # long
                your_payoff = self.attr_dict['lc']
            else: # short
                your_payoff = self.attr_dict['sc']

        lectpath = '/home/jordan/Projects/investments-lectures/L61_OptionsI/'

        setup = '\\noindent On {date}, {tick} traded for {S0} USD. '
        setup += 'Suppose you were {long_short} a {K} USD {call_put} that expired on {date}. '  

        question = 'Was the option in, at, or out-of-the-money? '
        question += 'Was the option exercised? '
        question += 'What was your payoff at expiration?\n\n\\vspace{{9pt}} '

        answer = '\n\n\\textbf{{Solution.}}'
        answer += 'The option was ' + ('in-' if long_payoff > 0 else 'out-of-') + 'the-money, ' 
        answer += 'so it was ' + ('exericed.' if long_payoff > 0 else 'not exercised. ')
        answer += 'Your payoff was ' + str(your_payoff) + ' USD.'

        text = setup + question + answer
        text = text.format(**self.attr_dict)

        filename = 'payoff_{tick}_{long_short}_{call_put}.tex'.format(**self.attr_dict)
        output = open(lectpath + filename,'w')
        output.write(text)
        output.close()

    # TODO: document
    def pricing(self,call=True,buy=True):
        """
        Returns an option pricing question

        Parameters
        ----------
        call : boolean
            If True, then call option, else put option
        buy : boolean
            If True, then long, else short
        answer : boolean
            If True, then reports the answer

        """

    def arbitrage(self):
        """
        Option arbitrage problem
        """
        pass

class Option(Security):
    """Option class"""

    def __init__(self):

        K  = random.uniform(Sd,Su)

        # call
        Dc = (Su-K)/(Su-Sd)
        Bc = Dc*Sd/(1.+rF)
        C0 = Dc*S[0]-Bc

        # put 
        Dp = (K-Sd)/(Su-Sd)
        Bp = Dp*Su/(1.+rF)
        P0 = Bp-Dp*S[0]

        self.attr_dict = {
            'tick' : ticker,
            'date' : tick_data.index[-2].isoformat()[:10],
            'S0' : S[0],
            'S1' : S[1],
            'Su' : Su,
            'Sd' : Sd,
            'K'  : K, 
            'rF' : rF,
            'Dc' : Dc,
            'Bc' : Bc, 
            'C0' : C0,
            'Dp' : Dp,
            'Bp' : Bp,
            'P0' : P0,
            'lc' : max(S[0]-K,0), # long call payoff
            'sc' : min(K-S[0],0), # short call payoff
            'lp' : max(K-S[0],0), # long put payoff
            'sp' : min(S[0]-K,0)  # short put payoff
        }

    # TODO: document
    def payoffs(self,call=True,buy=True,answer=True):
        """
        Returns an option pricing question

        Parameters
        ----------
        call : boolean
            If True, then call option, else put option
        buy : boolean
            If True, then long, else short
        answer : boolean
            If True, then reports the answer
        """

        self.attr_dict['long_short'] = 'long' if buy else 'short'
        self.attr_dict['short_long'] = 'short' if buy else 'long'
        self.attr_dict['call_put'] = 'call' if call else 'put'

        if call:
            long_payoff = self.attr_dict['lc']
            if buy: # long
                your_payoff = self.attr_dict['lc']
            else: # short
                your_payoff = self.attr_dict['sc']
        else: # if put
            long_payoff = self.attr_dict['lp']
            if buy: # long
                your_payoff = self.attr_dict['lp']
            else: # short
                your_payoff = self.attr_dict['sp']
                
        lectpath = '/home/jordan/Projects/investments-lectures/L61_OptionsI/'

        setup = '\\noindent On {date}, {tick} traded for {S0} USD. '
        setup += 'Suppose you were {long_short} a {K} USD {call_put} that expired on {date}. '  

        question = 'Was the option in, at, or out-of-the-money? '
        question += 'Was the option exercised? '
        question += 'What was your payoff at expiration?\n\n\\vspace{{9pt}} '

        answer = '\n\n\\textbf{{Solution.}}'
        answer += 'The option was ' + ('in-' if long_payoff > 0 else 'out-of-') + 'the-money, ' 
        answer += 'so it was ' + ('exericed.' if long_payoff > 0 else 'not exercised. ')
        answer += 'Your payoff was ' + str(your_payoff) + ' USD.'

        text = setup + question + answer
        text = text.format(**self.attr_dict)

        return text

    # TODO: document
    def pricing(self,call=True,buy=True):
        """
        Returns an option pricing question

        Parameters
        ----------
        call : boolean
            If True, then call option, else put option
        buy : boolean
            If True, then long, else short
        answer : boolean
            If True, then reports the answer

        """

        self.attr_dict['long_short'] = 'long' if buy else 'short'
        self.attr_dict['short_long'] = 'short' if buy else 'long'
        self.attr_dict['call_put'] = 'call' if call else 'put'

        lectpath = '/home/jordan/Projects/investments-lectures/L62_OptionsII/'

        setup = '\\noindent On {date}, {tick} traded for {S0} USD. '
        setup += 'In one month, {tick} can either go up to {Su} USD or down to {Sd} USD. '
        setup += 'Suppose that on {date}, you went {long_short} a {K} USD {call_put}. '

        question = 'What was the option premium that you paid or received? '
        question += 'How would you hedge your position?\n\n\\vspace{{9pt}}'

        D = self.attr_dict['Dc'] if call else self.attr_dict['Dp']
        B = self.attr_dict['Bc'] if call else self.attr_dict['Bp']

        answer = '\n\n\\noindent\\textbf{{Solution.}} '
        sub = '_{{c}}' if call else '_{{p}}'
        answer += '$\\Delta' + sub + '$ is ' + str(D) + ', '
        answer += '$B' + sub + '$ is ' + str(B) + ' USD, and so '

        if call:
            answer += '$C_{{0}}$ is ' + str(self.attr_dict['C0']) + ' USD. '
        else: # if put
            answer += '$P_{{0}}$ is ' + str(self.attr_dict['P0']) + ' USD. '

        answer += 'To hedge your position, '
        if call:
            answer += 'you should go {short_long} ' + str(D) + ' shares of {tick} and '  
            answer += '{long_short} ' + str(B) + ' USD in the risk-free asset.' 
        else:
            answer += 'you should go {long_short} ' + str(D) + ' shares of {tick} and '  
            answer += '{short_long} ' + str(B) + ' USD in the risk-free asset.' 

        text = setup + question + answer
        text = text.format(**self.attr_dict)

        return text

    def arbitrage(self):
        """
        Option arbitrage problem
        """
        pass

    def plot(self):
        pass
