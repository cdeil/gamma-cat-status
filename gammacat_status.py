"""
Print data entry status for gamma-cat.
"""
import os
from astropy.table import Table


class GammaCatStatus:
    def __init__(self):
        folder = os.environ['GAMMA_CAT']
        filename = os.path.join(folder, 'docs/data/gammacat.fits.gz')
        print('Reading {}'.format(filename))
        self.table = Table.read(filename)

    def make(self):
        self.make_cat_table_summary()
        self.make_cat_table_printout()

    def print(self):
        print('Number of sources: {}'.format(len(self.table)))

    def make_cat_table_summary(self):
        table = self.table.info('stats', out=None)

        # import IPython; IPython.embed()
        filename = 'cat_table_summary.csv'
        print('Writing {}'.format(filename))
        table.write(filename, format='ascii.fixed_width', delimiter=',', overwrite=True)

    def make_cat_table_printout(self):
        cols = ['source_id', 'common_name', 'where', 'classes', 'reference_id', 'morph_type', 'spec_type']
        table = self.table[cols].copy()
        table.sort(['where', 'source_id'])

        filename = 'cat_table_printout.csv'
        print('Writing {}'.format(filename))
        table.write(filename, format='ascii.fixed_width', delimiter=',', overwrite=True)


if __name__ == '__main__':
    status = GammaCatStatus()
    status.make()
