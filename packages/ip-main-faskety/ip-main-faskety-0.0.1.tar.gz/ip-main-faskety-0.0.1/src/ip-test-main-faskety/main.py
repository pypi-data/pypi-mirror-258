import requests


def add_one(number):

    return number + 1

def get_your_ip():
    response = requests.get('https://httpbin.org/ip')

    print('Your IP is {0}'.format(response.json()['origin']))
