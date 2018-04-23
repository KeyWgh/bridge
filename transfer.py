# Author: Ganghua Wang.
# Version: 0.1
# Copyright 2018. All Rights Reserved.
# ==============================================================================

'''Transfer a string form of BBO play to a txt form.
   Notify Chinese character is not supported by BBO, hence unsupported by this program either.
'''
import re
import datetime
import argparse
import sys
import os

# length of cards
LENGTH = 15
# max length of name
MAX_NAME = 15
# parameters from argparse
FLAG = None


def trans_to_txt(str, save_file=None):
    '''
    :param str: the page url, which contains all the information needed.
    :param save_file: The name of the file to save the transferred txt.
    :return: None
    '''
    def check_none(card_str):
        '''
        If this suit is void then add '-' to it.
        :param card_str: string of a suit of one player
        :return: str
        '''
        if len(card_str) == 1:
            return card_str+'-'
        else:
            return card_str

    def write_ns(card_str):
        '''write the cards of N and S to the file.'''
        # first three suit, spade, heart, diamond
        for sign in suit[1:]:
            ind = card_str.index(sign)
            f.write(' '*LENGTH+check_none(card_str[:ind])+'\n')
            card_str = card_str[ind:]
        # club
        f.write(' '*LENGTH+check_none(card_str)+'\n')

    def write_ew(s1, s2):
        '''write the cards of W and E to the file.'''
        # position of each player
        fill = dict(zip(suit, map(lambda s: list(s), [' ' * LENGTH] * 4)))
        fill['H'][LENGTH // 2] = 'N'
        fill['C'][LENGTH // 2] = 'S'
        fill['D'][LENGTH // 4] = 'W'
        fill['D'][-LENGTH // 4] = 'E'

        for key, val in fill.items():
            fill[key] = ''.join(val)

        for sign in suit[1:]:
            ind1 = s1.index(sign)
            ind2 = s2.index(sign)
            f.write('%-*s' % (LENGTH, check_none(s1[:ind1])) + fill[sign] + '%-*s' % (LENGTH, check_none(s2[:ind2]))+'\n')
            s1, s2 = s1[ind1:], s2[ind2:]
        f.write('%-*s' % (LENGTH, check_none(s1)) + ' '*LENGTH + '%-*s' % (LENGTH, check_none(s2))+'\n')

    def write_bid(s):
        '''write the bidding process to the file'''
        f.write('\n')
        # order of biding
        for p in pos:
            f.write('%-*s' % (MAX_NAME, p))
        f.write('\n')
        # find the dealer and start with him
        for p in pos:
            f.write('%-*s' % (MAX_NAME, name_dic[p]))
        f.write('\n')
        start = pos.index(new_lst[0][2].upper())
        f.write(' '*MAX_NAME*start)

        # extract all the bidding, leave the explanation to the last part.
        pattern = re.compile('([1-7]?[SHDCPN]|R)(\([^\)]*\))?')
        com_lst, k = [], 1
        for bid, com in re.findall(pattern, s):
            # if this bidding is accompanied with a explanation, then record it
            if com:
                com_lst.append(com)
                bid += '(%d)' % k
                k += 1
            f.write('%-*s' % (MAX_NAME, bid))
            start += 1
            # newline
            if start == 4:
                f.write('\n')
                start = 0

        # the explanations
        f.write('\n')
        for i in range(k-1):
            f.write('%d' % (i+1) + ': ' + com_lst[i] + '\n')

    # preprocession
    # reserve the useful information, which is after '?'
    str = str[str.index('?')+1:]
    # divide the string to several parts, representing different info
    lst = str.split('&')
    # writing order of players, in order to get name_dic
    pos = ['S', 'W', 'N', 'E']
    # representation of suits
    suit = ['S', 'H', 'D', 'C']
    # vulnerability
    vul = {'o': 'None',
           'b': 'Both',
           'n': 'NS',
           'e': 'EW',
           's': 'NS',
           'w': 'EW'}
    # name of each players
    name_dic = dict(zip(pos, map(lambda s: s[3:MAX_NAME], lst[:8:2])))
    # In order to adjust to custom
    pos = ['W', 'N', 'E', 'S']
    # name of the saved file
    if save_file:
        fn = save_file
    else:
        fn = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'.txt'

    # transfer information to the file
    with open(fn, 'w') as f:
        new_lst = lst[8:]
        f.write('Dealer: '+new_lst[0][2].upper()+'\n')
        f.write('Vul: ' + vul[new_lst[1][2]]+'\n')
        f.write('Num: ' + new_lst[2][2]+'\n')

        write_ns(lst[5][2:])
        write_ew(lst[3][2:], lst[7][2:])
        write_ns(lst[1][2:])

        write_bid(lst[11])


def main():
    # Note:
    # I want to use command line directly,
    # however "&" seems is a special character and cannot be contained in the input.
    # Therefore I use input file as the compromise.
    if FLAG.string:
        s = FLAG.string.strip().replace('%20', ' ')
    else:
        s = ''
        with open(FLAG.input) as f:
            s += f.readline()
        s.strip()
        # correctly recognize space
        s = s.replace('%20', ' ')
    trans_to_txt(s, FLAG.filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--string',
        type=str,
        default='',
        help='The string to transfer.'
    )
    parser.add_argument(
        '-in',
        '--input',
        type=str,
        default='input.txt',
        help='The string to transfer.'
    )
    parser.add_argument(
        '-fn',
        '--filename',
        type=str,
        default='output.txt',
        help='The name of the file saved.'
    )

    FLAG, unparsed = parser.parse_known_args()
    main()
