import argparse
import config as cfg


def parameter_parser():

    """
    A method to parse up command line parameters. By default it gives community detection on the Facebook politicians network.
    The default hyperparameters give a good quality clustering. Default weighting happens by neighborhood overlap.
    """

    parser = argparse.ArgumentParser(description = "Run Label Propagation.")

    parser.add_argument('--input',
                        nargs = '?',
                        #default = './data/politician_edges.csv',
                        #default = './data/soc-sign-epinions.csv',
                        #default = cfg.dataDirecoty+'/compress/Highland-tribes.csv',
                        #default = './data/SNM_INFL.csv',
                        #default = './data/SNM_AFF4.csv',
                        #default = cfg.dataDirecoty+'/basic/usSuprimeADJunw.csv',
                        default = cfg.dataDirecoty+'/compress/soc-sign-bitcoinotc.csv',
                        #default = cfg.dataDirecoty+'/compress/soc-sign-bitcoinalpha.csv',
                        #default = './data/basic/stranke94.csv',
                        #default='./data/edg/bitcoin_alpha.edg_uWuD',
                        #default= cfg.dataDirecoty+'/basic/_uWuD_bitcoin_otc.paj',

                        help = 'Input graph path.')

    parser.add_argument('--assignment-output',
                        nargs = '?',
                        default = './output/politician.json',
	                help = 'Assignment path.')

    parser.add_argument('--weighting',
                        nargs = '?',
                        default = 'overlap',
                        #default = 'min_norm',
                        #default = 'mea_sim',
	                help = 'Overlap weighting.')

    parser.add_argument('--rounds',
                        type = int,
                        default = 30,
	                help = 'Number of iterations. Default is 30.')

    parser.add_argument('--seed',
                        type = int,
                        default = 42,
	                help = 'Random seed. Default is 42.')

    return parser.parse_args()

