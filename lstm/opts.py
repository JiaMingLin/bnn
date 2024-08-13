import argparse
parser = argparse.ArgumentParser(description="Extreme quantization of RNN-based models")
parser.add_argument('dataset', type=str, default='emg', choices=['mnist', 'emg', 'ecg'])
parser.add_argument('-b', '--batch', type=int, default='50')
parser.add_argument('-e', '--epoch', type=int, default='50')
parser.add_argument('-hs', '--hidden', type=int, default='128')
parser.add_argument('-ls', '--num_layers', type=int, default='1')

parser.add_argument('-lr', '--learning_rate', type=float, default=0.00025)

parser.add_argument('-q', '--quant', action='store_true')
parser.add_argument('-no_brevitas', '--no_brevitas', action='store_true')
parser.add_argument('-wb', '--w_bit', type=int, default='8')
parser.add_argument('-ab', '--a_bit', type=int, default='8')
parser.add_argument('-ib', '--i_bit', type=int, default='8')
parser.add_argument('-ob', '--o_bit', type=int, default='8')
parser.add_argument('-rb', '--r_bit', type=int, default='8')

# parser.add_argument('--settings', nargs='+')
