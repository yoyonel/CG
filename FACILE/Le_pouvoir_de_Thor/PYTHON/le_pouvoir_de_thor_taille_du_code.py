# url: http://codegolf.stackexchange.com/questions/49772/how-could-i-reduce-the-length-of-this-code

a, b, x, y = map(int, raw_input().split())
while 1: c, d = (y > b) - (y < b), (x > a) - (x < a);print((' NS'[c] + ' WE'[d]).strip());y -= c;x -= d

a, b, x, y = map(int, raw_input().split())
while 1: c, d = cmp(y, b), cmp(x, a);print(' NS'[c] + ' WE'[d]).strip();y -= c;x -= d