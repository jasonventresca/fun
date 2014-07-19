#!/usr/bin/env python

DEBUG = 1

def logs_in_triangle(n):
    if n == 0:
        return 0

    return n + logs_in_triangle(n - 1)


def min_triangle_iteration(n):
    """ returns the smallest triangle with at least n logs """
    for i in xrange(n + 2):
        if logs_in_triangle(i) >= n:
            return i


def _get_triangle_with_height(n):
    # grid length is 2n-1 (i.e. n cells + n-1 in-between cells)

    # draw the triangle bottom up
    def bottom_up(n):
        row = ' '.join(['*',] * n)
        for i in xrange(n):
            yield row
            row = row.replace('*', ' ', 1)
            row = row[1:] + ' '

    for line in reversed(tuple(bottom_up(n))):
        yield line


def capacity_of_height(height):
    def inner(n):
        if n == 1: return 1

        return n + inner(n - 1)

    return inner(height)


def get_height_of_logs(n_logs):
    if n_logs == 0:
        return 0

    if n_logs < 0:
        raise Exception("get_height_of_logs() does not support negative numbers")

    fun = [x for x in xrange(1, n_logs+1) if capacity_of_height(x) >= n_logs]
    if DEBUG >= 2:
        print fun
    return min(fun)


def _get_carved_triangle(perfect_triangle, logs_to_carve_out):
    for n_rows_down in xrange(1, get_height_of_logs(logs_to_carve_out)+1):
        if logs_to_carve_out >= n_rows_down:
            logs_to_carve_out -= n_rows_down
            yield next(perfect_triangle).replace("*", " ", n_rows_down)
        else:
            yield next(perfect_triangle).replace("*", " ", logs_to_carve_out)
            logs_to_carve_out = 0

    for line in perfect_triangle:
        yield line


def _get_logs_to_carve_out(n_logs):
    return capacity_of_height(get_height_of_logs(n_logs)) - n_logs


def get_triangle_with_logs(n_logs):
    min_perfect_triangle = _get_triangle_with_height(get_height_of_logs(n_logs))

    if DEBUG >= 2:
        min_perfect_triangle = tuple(min_perfect_triangle)
        for line in min_perfect_triangle:
            print line
        min_perfect_triangle = (x for x in min_perfect_triangle)

    carved_triangle = _get_carved_triangle(min_perfect_triangle, _get_logs_to_carve_out(n_logs))
    for line in carved_triangle:
        yield line


def draw_triangle_with_logs(n_logs):
    for line in get_triangle_with_logs(n_logs):
        print line + ']'


def run_tests():
    EXPECTED_RESULTS = {
        1:  ("*",),

        2:  ("   ",
             "* *",),

        11: ("         ",
             "         ",
             "    * *  ",
             " * * * * ",
             "* * * * *",),

        64: ("                     ",
             "           *         ",
             "        * * *        ",
             "       * * * *       ",
             "      * * * * *      ",
             "     * * * * * *     ",
             "    * * * * * * *    ",
             "   * * * * * * * *   ",
             "  * * * * * * * * *  ",
             " * * * * * * * * * * ",
             "* * * * * * * * * * *",),
    }

    for key, value in sorted(EXPECTED_RESULTS.iteritems()):
        observed = tuple(get_triangle_with_logs(key))
        assert observed == value
        if DEBUG >= 1:
            print "num_logs = {}".format(key)
            for line in observed:
                print line
            print "=============================="


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--height', '-H', type=int, help='number of logs')
    parser.add_argument('--logs', '-L', type=int, help='number of logs')
    parser.add_argument('--test', '-T', action='store_true', help='run unit tests')

    args = parser.parse_args()

    if DEBUG >= 3:
        for i in xrange(1, 11):
            print "{}\t=>\t{}".format(i, get_height_of_logs(i))

    if args.test:
        run_tests()

    elif args.height and DEBUG >= 2:
        for line in _get_triangle_with_height(args.height):
            print line

    elif args.logs:
        draw_triangle_with_logs(args.logs)

