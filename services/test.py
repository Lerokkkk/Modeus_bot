import os, datetime
dir = '788497109'
p = os.path.join('..', 'users_data', dir, 'modeus_calendar')
f = os.path.join('..', 'users_data', dir, 'json_calendar', datetime.datetime.now().strftime("%H_%M_%S") + '.json')
if __name__ == '__main__':
    with open(f, 'w', encoding='utf-8') as file:
        file.write(f)
    print(p)
    print(f)
    print(os.path.exists(p))
    print(os.path.abspath(p))