import random
import string
import sys

def word_generator(word_size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(word_size))

def random_generator(string_size):
    st = []
    for i in range(string_size):
        st.append(word_generator(random.randint(1,15)))
    return ' '.join(st) + '. ' + '\n'

def string_generator(word_size, string_size):
    st = []
    for i in range(string_size):
        st.append(word_generator(word_size))
    return ' '.join(st) + '. ' + '\n'

def main():    
    txtfile = 'random_text.txt'
    if len(sys.argv) <= 2:
        inputs = input('Enter N, K, L (or N, K) through the SPACE button: ').split()
    elif len(sys.argv) <= 3:
        inputs = [int(sys.argv[1]), int(sys.argv[2])]
    else:
        inputs = [int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])]
    text_size, string_size = map(int, inputs[:2])
    with open(txtfile, 'w') as f:    
        for line in range(text_size):
            if len(inputs) == 3:
                st = string_generator(int(inputs[2]), string_size)
            else:
                st = random_generator(string_size)
            f.write(st)

if __name__ == "__main__":
    main()