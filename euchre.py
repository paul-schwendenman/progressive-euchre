import argparse
import logging



rounds7 = [
    [
        [[1, 2], [3, 4]],
        [[5, 6], [7, 8]],
    ],
    [
        [[2, 4], [5, 7]],
        [[6, 8], [1, 3]],
    ],
    [
        [[5, 8], [6, 7]],
        [[1, 4], [2, 3]],
    ],
    [
        [[4, 8], [1, 5]],
        [[2, 6], [3, 7]],
    ],
    [
        [[1, 6], [2, 5]],
        [[3, 8], [4, 7]],
    ],
    [
        [[2, 8], [3, 5]],
        [[4, 6], [1, 7]],
    ],
    [
        [[3, 6], [4, 5]],
        [[1, 8], [2, 7]],
    ],
]

rounds11 = [
    [
        [[1, 2], [3, 4]],
        [[5, 6], [7, 8]],
        [[9, 10], [11, 12]],
    ],
    [
        [[3, 6], [7, 10]],
        [[1, 4], [9, 12]],
        [[2, 11], [5, 8]],
    ],
    [
        [[4, 11], [7, 12]],
        [[2, 9], [3, 8]],
        [[1, 6], [5, 10]],
    ],
    [
        [[3, 10], [5, 12]],
        [[1, 8], [2, 7]],
        [[4, 9], [6, 11]],
    ],
    [
        [[1, 10], [8, 11]],
        [[3, 12], [6, 9]],
        [[2, 5], [4, 7]],
    ],
    [
        [[1, 12], [6, 7]],
        [[4, 5], [10, 11]],
        [[2, 3], [8, 9]],
    ],
    [
        [[2, 6], [3, 11]],
        [[7, 9], [8, 10]],
        [[1, 5], [4, 12]],
    ],
    [
        [[2, 12], [5, 9]],
        [[3, 7], [4, 8]],
        [[1, 11], [6, 10]],
    ],
    [
        [[1, 7], [4, 10]],
        [[3, 9], [5, 11]],
        [[2, 8], [6, 12]],
    ],
    [
        [[6, 8], [9, 11]],
        [[2, 4], [10, 12]],
        [[1, 3], [5, 7]],
    ],
    [
        [[1, 9], [7, 11]],
        [[2, 10], [3, 5]],
        [[4, 6], [8, 12]],
    ],
]

scores = [
    [7, 5, 5, 5, 2, 7, 6, 1, 7, 4, 8],
    [7, 6, 2, 5, 6, 5, 5, 7, 5, 8, 6],
    [7, 7, 7, 8, 5, 5, 5, 5, 7, 4, 3],
    [7, 5, 5, 8, 6, 5, 4, 6, 4, 8, 5],
    [10, 7, 5, 7, 6, 5, 6, 7, 6, 9, 3],
    [10, 7, 5, 3, 7, 6, 5, 12, 11, 6, 5],
    [5, 6, 8, 5, 6, 6, 9, 5, 7, 9, 10],
    [5, 7, 7, 5, 10, 5, 3, 6, 5, 6, 4],
    [5, 5, 2, 8, 7, 5, 9, 7, 7, 3, 8],
    [5, 6, 5, 8, 2, 5, 3, 12, 4, 3, 6],
    [5, 6, 5, 3, 10, 5, 5, 1, 6, 3, 10],
    [5, 5, 8, 7, 5, 7, 4, 7, 11, 3, 4],
]

mine = [5, 6, 5, 8, 5, 7, 5, 1, 5, 3, 4]

def setup_logging(lvl):
    logger = logging.getLogger('')
    ch = logging.StreamHandler()
    ch.setLevel(lvl)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    
    logger.addHandler(ch)
    logger.setLevel(lvl)
    return logger
    
def get_args():
    parser = argparse.ArgumentParser(description='Check your progressive euchre charts.')
    parser.add_argument('--players', default=12, type=int,
        help='specify 8 or 12 players (default: 12)')
    parser.add_argument('--verbose', '-v', dest='verbosity', action='store_const',
        const=logging.INFO, default=logging.DEBUG,
        help='Set verbosity')
    args = parser.parse_args()
    
    print args.verbosity
    
    return args.players, args.verbosity


def main(players, logger):
    if players == 8:
        rounds = rounds7
    elif players == 12:
        rounds = rounds11

    print len(rounds)

    for n, score in enumerate(scores):
        print "%d: %d" % (n + 1, sum(score))

    for roundno, tables in enumerate(rounds):
        for table in tables:
            for team in table:
                score = scores[team[0] - 1][roundno], scores[team[1] - 1][roundno]
                if not score[0] == score[1]:
                    logger.debug("Players %d and %d differ on round %d scores of %d and %d", team[0], team[1], roundno + 1, score[0], score[1])
                else:
                    logger.info("Players %d and %d agree on round %d score of %d", team[0], team[1], roundno + 1, score[0])

    print list(reversed([a[0] + 1 for a in sorted(enumerate([sum(n) for n in scores]), key=lambda a: a[1])]))

    for n, tables in enumerate(rounds):
        for table in tables:
            if 6 in table[0]:
                assert scores[table[1][0] - 1][n] == mine[n]
            if 6 in table[1]:
                assert scores[table[0][0] - 1][n] == mine[n]


if __name__ == '__main__':
    players, lvl = get_args()
    logger = setup_logging(lvl)

    main(players, logger)
