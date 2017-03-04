#!/usr/bin/env python
# coding: utf-8
''' Module encapsulating main work for this project.
'''
import argparse

import lastpass_pwned_checker.credentials
import lastpass_pwned_checker.check

def check(args):
    ''' Default function for parser: check sites against account
    '''
    credentials = (lastpass_pwned_checker
                   .credentials
                   .Credentials(args.credentials).get())
    checker = (lastpass_pwned_checker
               .check
               .Checker.safe_open(*credentials))
    with open(args.list_of_pwned) as data:
        lines = [line.strip() for line in data.readlines()]
        sites = checker.compare_pwned(lines)
    print 'You should consider updating your information on these sites:'
    print '\n'.join(sites)

def main():
    ''' Main function
    '''
    parser = argparse.ArgumentParser('Check your LastPass account for pwned \
sites')
    parser.add_argument('-c', '--credentials',
                        help='Path to JSON file holding LastPass credentials',
                        default='credentials.json')
    parser.add_argument('-l', '--list_of_pwned',
                        help='Path to list of sitenames suspected to be pwned',
                        default='pwned.txt')
    parser.set_defaults(func=check)
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
