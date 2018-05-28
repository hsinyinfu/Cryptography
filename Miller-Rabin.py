#!/usr/bin/python3
import random

def isPrime( target, faultRateDenominator ):
    """ Test if the "target" is prime or composite.

    Args:
        target: The number to be tested if it is a prime.
        faultRateDenominator: if input is x, then the fault rate is 1/x.

    Return:
        A tuple.
        witnesses: number to test if target is a prime
            by Miller-Rabin Test in each round. One round of the test
            uses one witness.
        results: a list of "True"/"False", each one is the result of
            one Miller-Rabin Test.
        rounds: How many rounds of Miller-Rabin Test be performed.
            The rounds is determined by the fault rate.

    """

    witnesses = []
    results = []
    rounds = computeRounds( faultRateDenominator )

    for i in range( rounds ):
        witness = random.randint( 3, target-1 )

        # Prevent witness is duplicate.
        while witness in witnesses:
            witness = random.randint( 3, target-1 )
        witnesses.append(witness)

        results.append( Miller_Rabin_Test( target, witness ) )
    return( witnesses, results, rounds )
        
def Miller_Rabin_Test( target , base ):
    """ Test whether the target is prime or composite by base.

    Args:
        target: The number to be tested if it is a prime or not.
        base: A Miller-Rabin witness or nonwitness for target
    Return:
        True: target "may" be a prime, and "base" is the nonwitness for target.
        False: target is definetely a composite number, and "base" is the witness
            for the target.

    """

    # Compute (s, d) such that " target-1 = 2^s * d (d is an odd number)".
    s, d = 0, target-1
    while d  % 2 == 0:
        s += 1
        d = d // 2
    #print('s: {}'.format(s))
    #print('d: {}'.format(d))

    # Check if (base^d) is +1 or target-1.
    squareRoot = faster_mod( base, d, target )
    if squareRoot in (1,target-1):
        return True
    #print('(witness^d): {}', squareRoot)

    # Check if any one of ( base^(2^1*d), base^(2^2*d),...,base^(2^(s-1)*d) )
    # is (target-1).
    for i in range( 1 , s ):
        squareRoot = faster_mod( squareRoot, 2, target )
        if  squareRoot == (target-1):
                return True
        #print('(witness^(2^{0}*d): {1}'.format(i, squareRoot))
    return False

def computeRounds( faultRateDenominator ):
    """ Compute how many rounds of Miller-Rabin Test should be performed.

    Args:
        faultRateDenominator: The denominator of fault Rate, positive integer.
            e.g., if input is 100, then the fault rate is 1/100.

    Return:
        r is an positive integer that satisfy (1/4)^r < 1/faultRateDenominator.

    """

    r = 0
    while ( 4 ** r) < faultRateDenominator :
        r += 1
    return r

def faster_mod( x, n, m):
    """Compute x^n mod m

    Args:
        x: base, positive integer
        n: power, positive integer
        m: modulo, positive integer

    Return:
        integer, answer of x^n mod m

    """

    ans, base = 1, x
    while n != 0:
        if n & 1 == 1:  # the last bit of n in binary is 1
            ans = (ans * base) % m
        base = (base ** 2) % m
        n >>= 1
    return ans

def generatePrime( faultRateDenominator ):
    """ Generate a 512-bits prime number with specified fault rate.

    Args:
        faultRateDenominator: The denominator of fault Rate, positive integer.
            e.g., if input is 100, then the fault rate is 1/100.

    Return:
        A 512-bits prime tested by Miller-Rabin Test with specified fault rate.

    """

    while True:
        # Generate an odd number
        prime = random.randrange( 2**512+1, 2**513-1, 2)

        # Test if the number is really a prime.
        _, results, _ = isPrime( prime, faultRateDenominator )

        # If every result of Miller-Rabin Test is False( which means
        # it "may" be a prime), then return the number.
        # If there are one or more result of Miller-Rabin Test is True
        # (which means it "absolutely" is a composite number),
        # re-generate a prime again.
        if not False in results:
            return prime


if __name__ == '__main__':
    print('\n' + \
        '###############################################\n' + \
        '# 0: Verify if a number is prime or not.      #\n' + \
        '# 1: Generate a 512-bits prime.               #\n' + \
        '# exit: shut down this program.               #\n' + \
        '###############################################\n\n' \
        )

    while True:
        mode = input('Please select a mode: ')

        if mode == '0':
            print('[ Start to verify a number ]')
            target = int(input('< Enter a number to be tested if it is a prime or not: >\n'))
            denominator = int(input('< Enter the denominator of fault rate: >\n'))
        
            if target % 2 == 0:
                print('This is an even number, so it must be a composite number.')
        
            else:
                witnesses, results, rounds = isPrime( target, denominator )
                for i in range(rounds):
                    print('The {0} round: result is \"{1}\", {2} is {3}'.format(i,\
                        results[i], "nonwitness" if results[i] else "witness", witnesses[i]))
                    print('----------')
                print('To sum up, the number you input is a {} number.'\
                        .format('composite' if False in results else 'prime'))

        elif mode == '1':
            print('[ Start to generate a prime ]')
            denominator = int(input('< Enter the denominator of fault rate: >\n'))
            prime = generatePrime( denominator )
            print('The 512-btis prime generated for you is:\n{}'.format(prime))

        elif mode == 'exit':
            print('[ The program is going to be shut down ]')
            exit()

        else:
            print('[ Wrong input! ]')

