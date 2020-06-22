# ================================================
#             IPv4 to Binary Address
#
#        Run code and enter an IPv4 address
#               to get it in binary!
# ================================================

def binaryOctet(num):
    bin = []
    run_total = 0
    run_total += int(num)
    try:
        if run_total//128 != 0:
            bin.append(str(run_total//128))
            run_total %= 128
        else:
            bin.append('0')
        if run_total // 64 != 0:
            bin.append(str(run_total // 64))
            run_total %= 64
        else:
            bin.append('0')
        if run_total // 32 != 0:
            bin.append(str(run_total // 32))
            run_total %= 32
        else:
            bin.append('0')
        if run_total // 32 != 0:
            bin.append(str(run_total // 32))
            run_total %= 32
        else:
            bin.append('0')
        if run_total // 16 != 0:
            bin.append(str(run_total // 16))
            run_total %= 16
        else:
            bin.append('0')
        if run_total // 8 != 0:
            bin.append(str(run_total // 8))
            run_total %= 8
        else:
            bin.append('0')
        if run_total // 4 != 0:
            bin.append(str(run_total // 4))
            run_total %= 4
        else:
            bin.append('0')
        if run_total // 2 != 0:
            bin.append(str(run_total // 2))
            run_total %= 2
        else:
            bin.append('0')
        if run_total // 1 != 0:
            bin.append(str(run_total // 1))
            run_total %= 1
        else:
            bin.append('0')
    except ZeroDivisionError:
        bin.append('0')
    return bin


def binaryIP(ip_address):
    ip = ip_address.split('.')
    bin_ip = []
    binary_ip = []
    for num in ip:
        bin_ip.append(binaryOctet(num))
    for octet in bin_ip:
        oc = ''.join(octet)
        binary_ip.append(oc)
    print('|',end='')
    for num in binary_ip:
        print(num,end='|')


ip = input('Type IPv4 address to get it in binary > ')
print('\n')
binaryIP(ip)
print('\n\nCool huh?')
