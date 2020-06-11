from pinyin_core_function import *
from time import time
import sys

if __name__ == '__main__':
    print('Welcome to pinyin input method created by Ren Yi!')
    print('loading words prob dict')
    start_time = time()
    # return a dict with unigram and bigram as the key, occurrence count as the value
    words_dict = np.load('./words_dict_small_more.npy', allow_pickle=True).item()
    print('words prob dict load complete, time cost = %.2fs\n' % (time() - start_time))

    # a dict with pinyin as the key and character list corresponding to the pinyin as value
    pinyin_dict = get_pinyin_dict()

    # initializing the data structure for viterbi algorithm
    Layer.words_dict = words_dict
    Layer.vocabulary_size = 0
    for words in pinyin_dict.values():
        Layer.vocabulary_size += len(words)

    # len(argv) == 3, file mode
    if len(sys.argv) == 3:
        print('File mode, read from %s, write to %s' % (sys.argv[1], sys.argv[2]))
        with open(sys.argv[1], 'r') as f:
            input_commands = f.readlines()
        result = ''
        for line in input_commands:
            result += viterbi(process_seq(line), words_dict, pinyin_dict) + '\n'
        with open(sys.argv[2], 'w') as f:
            f.write(result)
    
    # another test mode, input files should be like https://docs.qq.com/doc/DYmZVbURWZWhzc0lH
    elif len(sys.argv) == 2:
        test(sys.argv[1], words_dict, pinyin_dict)
    
    # len(argv) != 3, input mode, requires input manually
    else:
        print('Input mode, input pinyin with one space and enter, or input exit to quit')
        try:
            while True:
                seq = input().strip()
                if seq.lower() == 'exit':
                    print('You have exit the input.')
                    break
                if seq == '':
                    continue
                result = viterbi(process_seq(seq), words_dict, pinyin_dict)
                print(result, '\n')
        except KeyboardInterrupt:
            print('Keyboard interrupted, input terminated.\n')

        # # Test the dataset collected by classmates on https://docs.qq.com/doc/DYmZVbURWZWhzc0lH
        # test('../data/TestSet.txt', words_dict, pinyin_dict)
