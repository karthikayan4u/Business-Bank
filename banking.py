import random
import sqlite3
conn = sqlite3.connect("card.s3db")
cur = conn.cursor()


def drop_table():
    cur.execute('delete from card')


try:
    customer_inf = [i for i in cur.execute('select id from card')][-1][0]
except IndexError:
    customer_inf = []
customer_info_id = customer_inf if customer_inf else 0


def check_sum_calculator(customer_account_number):
    return sum([int(i) - 9 if int(i) > 9 else int(i) for i in [customer_account_number[i] if i % 2 != 0
                    else str(int(customer_account_number[i]) * 2) for i in range(15)]])


def exe_commit(number, pin='0', i_d=0, balance=0, drop=False, ret=False, commit=False):
    if drop:
        cur.execute(f'delete from card where number = {number}')
        conn.commit()
    if ret:
        if pin == '0':
            return [i for i in cur.execute(f'select id, number, pin, balance from card where number = {number};')]
        else:
            return [i for i in cur.execute(f'select id, number, pin, balance '
                                           f'from card where number = {number} and pin = {pin};')]
    if commit:
        cur.execute(f'insert into card (id, number, pin, balance) values ({i_d}, '
                    f'{number}, {pin}, {balance});')
        conn.commit()


def create_account():
    global customer_info_id
    customer_account_number = '400000' + ''.join(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                                                               9))
    check_sum_calc = check_sum_calculator(customer_account_number)
    check_sum = (10 - (check_sum_calc % 10)) % 10
    customer_pin = ''.join(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4))
    customer_info_id += 1
    exe_commit(customer_account_number + str(check_sum), customer_pin, customer_info_id, commit=True)
    print(f'\nYour card has been created\nYour card number:\n{customer_account_number + str(check_sum)}'
          f'\nYour card PIN:\n{customer_pin}\n')


def log_in():
    customer_account_number = input("\nEnter your card number:\n>")
    customer_pin = input("Enter your PIN:\n>")
    check_sum = check_sum_calculator(customer_account_number[:-1]) + int(customer_account_number[-1])
    if check_sum % 10 != 0:
        print("\nWrong card number or PIN!\n")
        main()
    customer_det = exe_commit(customer_account_number, customer_pin, ret=True)
    if customer_det:
        print("\nYou have successfully logged in!\n")
    else:
        print("\nWrong card number or PIN!\n")
        main()
    customer_login_option = -1
    while customer_login_option != 0:
        customer_login_option = \
            input('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n>')
        customer_det = exe_commit(customer_account_number, customer_pin, ret=True)
        if customer_login_option == '1':
            print(f"\nBalance: {customer_det[-1][-1]}\n")
            continue
        elif customer_login_option == '2':
            income = int(input("\nEnter income:\n>"))
            exe_commit(customer_account_number, customer_pin, customer_det[-1][0], customer_det[-1][-1] + income,
                       drop=True, commit=True)
            print("Income was added!\n")
        elif customer_login_option == '3':
            print("\nTransfer")
            recipient_number = input("Enter card number:\n>")
            recipient_info = exe_commit(recipient_number, ret=True)
            check_sum_res = check_sum_calculator(recipient_number[:-1]) + int(recipient_number[-1])
            if check_sum_res % 10 != 0:
                print("Probably you made mistake in the card number. Please try again!\n")
                continue
            elif recipient_number == customer_account_number:
                print("You can't transfer money to the same account!")
                continue
            elif not recipient_info:
                print("Such a card does not exist.\n")
                continue
            amount_to_transfer = int(input("\nEnter how much money you want to transfer:\n>"))
            if amount_to_transfer > customer_det[-1][-1]:
                print("Not enough money!\n")
            else:
                exe_commit(recipient_number, recipient_info[-1][2], recipient_info[-1][0],
                           recipient_info[-1][-1] + amount_to_transfer, drop=True, commit=True)
                exe_commit(customer_account_number, customer_pin, customer_det[-1][0],
                           customer_det[-1][-1] - amount_to_transfer, drop=True, commit=True)
                print("Success!\n")
        elif customer_login_option == '4':
            exe_commit(customer_account_number, drop=True)
            print("\nThe account has been closed!")
            main()
        elif customer_login_option == '5':
            print('\nYou have successfully logged out!\n')
            break
        elif customer_login_option == '0':
            print("\nBye!")
            exit()
        else:
            print("\nNo such option!\n")


def main():
    option = -1
    while option != '0':
        option_dict = {1: "Create an account", 2: "Log into account", 0: "Exit"}
        option = input(f"\nPlease select an option below\n1. {option_dict[1]}\n2. {option_dict[2]}\n0. {option_dict[0]}\n>").strip()
        if option == '1':
            create_account()
        elif option == '2':
            log_in()
        elif option == '0':
            print("\nBye!")
            exit()
        else:
            print("\nNo such option! Try Again!\n")


if __name__ == '__main__':
    print("Welcome to Business Bank\nPlease select an option below\n")
    choice = input("1. Start a New Game\n2. Continue with the previous game\n0. Exit\n>")
    if choice == '1':
        drop_table()
        main()
    elif choice == '2':
        main()
    elif choice == '0':
        print("\nBye!!")
        exit()
    else:
        print("\nNo such option! Try Again!\n")
