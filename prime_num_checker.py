# =================================== #
#     Simple Prime Number Checker     #
# =================================== #

print('Prime Number Checker'.rjust(30,'>')+'\nTrue: is prime\nFalse: not prime\n')
def main():
    num = int(input('Enter a number > '))
    not_prime = 0
    for i in range(2,num):
        if num > 2 and num != 3 and num % i == 0:
            not_prime += 1
    if not_prime > 0 or num == 1 or num == 2:
        print(False)
    else:
        print(True)
    main()
main()