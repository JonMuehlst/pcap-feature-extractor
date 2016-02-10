from utils.general import gen_sni_csv
import sys

if __name__ == '__main__':
    print sys.argv[1]
    gen_sni_csv(sys.argv[1])
