"""
Dump gamma-cat to plots and printouts
"""
import os
import json
from pprint import pprint

import sys
gammacat_path = os.environ['GAMMA_CAT']
sys.path.append(gammacat_path)

from gammacat.utils import write_json
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

    def make_json_all(self):
        if not os.path.isdir('json'):
            os.makedirs('json')

        for source_id in self.source_ids:
            self.make_json_one(source_id)

    def make_txt_one(self, source_id):
        source = self.cat[source_id]
        text = str(source)

        filename = 'txt/source_{:06d}.txt'.format(source_id)
        print('Writing {}'.format(filename))
        with open(filename, 'w') as fh:
            fh.write(text)
            fh.write('\n===\n\n')
            pprint(source.data, stream=fh)

    def make_json_one(self, source_id):
        source = self.cat[source_id]
        text = json.dumps(source.data, indent=4)

        filename = 'json/source_{:06d}.json'.format(source_id)
        print('Writing {}'.format(filename))
        with open(filename, 'w') as fh:
            fh.write(text)

        # write_json(source.data, filename)


if __name__ == '__main__':
    source_ids = [42, 24, 99]
    dump = GammaCatDump(source_ids=source_ids)
    dump.make_txt_all()
    # JSON serialisation doesn't work at the moment
    # dump.make_json_all()
