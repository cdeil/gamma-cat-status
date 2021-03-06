"""
Dump gamma-cat to plots and printouts
"""
import os
import json
from pprint import pprint
import logging
import astropy.units as u
from gammapy.catalog import SourceCatalogGammaCat
from gammapy.catalog.gammacat import NoDataAvailableError

import matplotlib

matplotlib.use('agg')

import matplotlib.pyplot as plt

log = logging.getLogger(__name__)


class GammaCatDump:
    def __init__(self, row_idxs=None):
        folder = os.environ['GAMMA_CAT']
        filename = os.path.join(folder, 'output/gammacat.fits.gz')
        log.info('Reading {}'.format(filename))
        self.cat = SourceCatalogGammaCat(filename)

        all_row_idxs = list(range(len(self.cat.table)))
        if row_idxs:
            row_idxs = sorted(set(row_idxs) & set(all_row_idxs))
        else:
            row_idxs = all_row_idxs

        self.row_idxs = row_idxs

    def make_txt_all(self):
        if not os.path.isdir('txt'):
            os.makedirs('txt')

        for row_idx in self.row_idxs:
            self.make_txt_one(row_idx)

    def make_json_all(self):
        if not os.path.isdir('json'):
            os.makedirs('json')

        for row_idx in self.row_idxs:
            self.make_json_one(row_idx)

    def make_sed_png_all(self):
        if not os.path.isdir('sed_png'):
            os.makedirs('sed_png')

        for row_idx in self.row_idxs:
            self.make_sed_png_one(row_idx)

    def make_txt_one(self, row_idx):
        source = self.cat[row_idx]
        source_id = source.data['source_id']
        text = str(source)

        filename = 'txt/source_{:06d}.txt'.format(source_id)
        log.info('Writing {}'.format(filename))
        with open(filename, 'w') as fh:
            fh.write(text)
            fh.write('\n===\n\n')
            pprint(source.data, stream=fh)
            fh.write('\n===\n\n')
            try:
                lines = source.flux_points.table.pformat(-1)
                fh.write('\n'.join(lines))
            except NoDataAvailableError:
                fh.write('No flux points available.')
            # TODO: fix!
            except ValueError:
                log.error('Invalid SED for: source_id={}'.format(source_id))

    def make_json_one(self, row_idx):
        source = self.cat[row_idx]
        source_id = source.data['source_id']
        text = json.dumps(source.data, indent=4)

        filename = 'json/source_{:06d}.json'.format(source_id)
        log.info('Writing {}'.format(filename))
        with open(filename, 'w') as fh:
            fh.write(text)

    def make_sed_png_one(self, row_idx):
        source = self.cat[row_idx]
        source_id = source.data['source_id']
        common_name = source.data['common_name']
        title = 'row_idx: {:03d}, source_id: {:03d}, common_name: {}'.format(row_idx, source_id, common_name)

        plt.clf()

        # TODO: read range from source by default (not clear how yet)
        energy_range = [0.2, 50] * u.TeV
        energy_power = 2

        opts = dict(energy_power=energy_power, flux_unit='erg-1 cm-2 s-1', color='k')

        if source.data['spec_type'] != 'none':
            source.spectral_model.plot_error(energy_range=energy_range, alpha=0.2, **opts)
            source.spectral_model.plot(energy_range=energy_range, alpha=0.5, **opts)
        else:
            log.debug('No spectral model: {}'.format(title))

        try:
            source.flux_points.plot(**opts)
        except NoDataAvailableError:
            log.debug('No SED points: {}'.format(title))
        # TODO: figure out why this occurs!? Is shouldn't, right?
        except ValueError:
            log.error('Invalid SED points: source_id={}'.format(source_id))

        plt.title(title)
        plt.grid()

        filename = 'sed_png/source_{:06d}.png'.format(source_id)
        log.info('Writing {}'.format(filename))
        plt.savefig(filename)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # row_idxs = [42, 24, 99]
    # row_idxs = list(range(30))
    row_idxs = None
    # row_idxs = [93]
    dump = GammaCatDump(row_idxs=row_idxs)
    dump.make_txt_all()
    # JSON serialisation doesn't work at the moment
    # dump.make_json_all()
    dump.make_sed_png_all()
