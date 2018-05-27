#!/usr/bin/python3
import random
import sys

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
    print('s: {}'.format(s))
    print('d: {}'.format(d))

    # Check if (base^d) is +1 or -1.
    squareRoot = faster_mod( base, d, target )
    if squareRoot in (1,-1):
        return True
    print('(witness^d): {}', squareRoot)

    # Check if any one of ( base^(2^1*d), base^(2^2*d),...,base^(2^(s-1)*d) )
    # is -1.
    for i in range( 1 , s ):
        squareRoot = faster_mod( squareRoot, 2, target )
        if  squareRoot == -1:
                return True
        print('(witness^(2^{0}*d): {1}'.format(i, squareRoot))
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
            ans *= base
        base = (base ** 2) % m
        n >>= 1
    return ans

if __name__ == '__main__':
    target = int(input('Enter a number to be tested if it is a prime or not.\n'))
    denominator = int(input('Enter the denominator of fault rate.\n'))

    if target % 2 == 0:
        print('This is an even number, so it must be a composite number.')

    else:
        witnesses, results, rounds = isPrime( target, denominator )
        for i in range(rounds):
            print('The {0} round: result is \"{1}\", {2} is {3}'.format(i,\
                results[i], "nonwitness" if results[i] else "witness", witnesses[i]))
            print('----------')
        if False in results:
            print('To sum up, the number you input is a composite number.')
        else:
            print('To sum up, the number you input is a prime number.')
