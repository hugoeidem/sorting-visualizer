TEN_COLORS = [
    "PINK", "GREEN", "YELLOW", "LIGHTBLUE", "BLACK",
    "WHITE", "ORANGE", "RED", "PURPLE", "GREY"
]
BASE_FREQUENCY = 400
PITCH_CHANGE = 400

def delay(n):
    for _ in range(n):
        yield 0,0

def dec_to_hex_str(n):
    a, b = n//16, n%16
    f = lambda x : "0123456789ABCDEF"[x]
    return f(a) + f(b)

def generate_subtree_colors(n):
    colors = []
    span = 1
    val = 255
    while True:
        colors.append("#" + dec_to_hex_str(val) * 3)
        n -= span
        span *= 2
        val -= val // 6
        if span > n:
            break
    return colors

def get_subtree_level(i):
    level = 0
    while i > 2 ** level:
        i -= 2 ** level
        level += 1
    return level - 1
