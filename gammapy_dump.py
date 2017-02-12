"""
Dump gamma-cat to plots and printouts
"""
import os
from gammapy.catalog import SourceCatalogGammaCat


class GammaCatDump:
    def __init__(self, source_ids=None):
        folder = os.environ['GAMMA_CAT']
        filename = os.path.join(folder, 'docs/data/gammacat.fits.gz')
        print('Reading {}'.format(filename))
        self.cat = SourceCatalogGammaCat(filename)

        if not source_ids:
            source_ids = list(self.cat['source_id'])

        self.source_ids = source_ids

    def make_txt_all(self):
        if not os.path.isdir('txt'):
            os.makedirs('txt')

        for source_id in self.source_ids:
            self.make_txt_one(source_id)

    def make_txt_one(self, source_id):
        source = self.cat[source_id]
        text = str(source)

        filename = 'txt/source_{:06d}.txt'.format(source_id)
        print('Writing {}'.format(filename))
        with open(filename, 'w') as fh:
            fh.write(text)


if __name__ == '__main__':
    source_ids = [42, 24, 99]
    dump = GammaCatDump(source_ids=source_ids)
    dump.make_txt_all()
