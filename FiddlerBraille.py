# This entirely unoptimized brute force solution counts all of the possible
# subsets of patterns of pips on a grid that are distinct from one another
# under translation.

# Formulas in the comments will refer to number of columns as c and number of
# rows as r.

# The strategy here is to express each pattern as a binary number with number
# of digits = cr. The top left pip is the most significant digit, and the
# bottom right is least significant.

# A pattern can be translated right if and only if there are no ones in the
# rightmost column. To translate a pattern to the right, it is simply bit
# shifted right by one place.

# A pattern can similarly be shifted down only if there are no ones in the
# bottom row. To translate down, the pattern is shifted right by the number of
# columns.

columns = 4
rows = 6

# Create bitmasks for the rightmost column and the bottom row. These will be
# used to test if a pattern can be translated using logical and.

# Right column has (# of rows) ones, spaced (# of columns) apart. This is
# equal to the sum of 2^(ck) for k = 0..(r - 1). This works out to be
# (2^(cr) - 1) / (2^c - 1), expressed here using bit shift instead of
# exponentiation (1 << n is equivalent to 2^n).

# The bottom row is simply (# of columns) ones in the least significant
# positions. This is equal to 2^c - 1.

# The integer division operator (//) is necessary here.
right_column = ((1 << (columns * rows)) - 1) // ((1 << columns) - 1)
bottom_row = (1 << columns) - 1

# Create boolean array to track patterns that have been tested.
n = 1 << (columns * rows)
tested = [0] * n

# Initialize results. We're counting the empty grid as its own subset.
subsets = [[0]]

# Top left is the most significant bit, and we're moving right and down, so
# start with all ones and decrement to ensure we're searching starting with
# the top leftmost translation of a particular pattern. To ensure nothing was
# counted more than once, we'll count the total number of results.
current = n - 1
while (current > 0):
    if (tested[current] == 0):
        # If it hasn't been tested yet, then it's a new subset.
        subset = [current]
        moving_right = current
        while (moving_right & right_column == 0):
            # If there are (still) no ones in the right column, then:
            moving_down = moving_right
            while (moving_down & bottom_row == 0):
                # If there are (still) no ones in the bottom row, then move
                # down, append the translation to the current subset, and mark
                # it as tested.
                moving_down = moving_down >> columns
                subset.append(moving_down)
                tested[moving_down] = 1
            # Move right, append the translation to the current subset, and
            # mark it as tested.
            moving_right = moving_right >> 1
            subset.append(moving_right)
            tested[moving_right] = 1
        # Move the rightmost translation down if possible, add translations to
        # the current subset, and mark them as tested, just as in the inner
        # loop above.
        moving_down = moving_right
        while (moving_down & bottom_row == 0):
            moving_down = moving_down >> columns
            subset.append(moving_down)
            tested[moving_down] = 1
        # Append the subset to the results.
        subsets.append(subset)
    current -= 1

# Print all subsets in binary. Count results to ensure nothing was counted
# more than once. There should be 2^(cr) results.
results = 0
for subset in subsets:
    results += len(subset)
#   Or maybe don't print all of them if there are 2^24. It takes a while.
#    print([format(number, 'b') for number in subset])

# Total subsets is the final answer to the puzzle.
print("Total subsets: ", len(subsets))
print("Results: ", results)

# Verify bitmasks for bottom row and right column are correct.
print("bottom_row", format(bottom_row, 'b'))
print("right_column", format(right_column, 'b'))