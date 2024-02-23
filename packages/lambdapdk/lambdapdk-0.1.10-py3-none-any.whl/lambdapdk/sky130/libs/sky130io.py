import os
import siliconcompiler
from lambdapdk import register_data_source


def setup(chip):
    '''
    Skywater130 I/O library.
    '''
    process = 'skywater130'
    libname = 'sky130io'
    stackup = '5M1LI'

    lib = siliconcompiler.Library(chip, libname, package='lambdapdk')
    register_data_source(lib)

    libdir = os.path.join('lambdapdk', 'sky130', 'libs', libname)

    # pdk
    lib.set('option', 'pdk', process)

    for corner in ['slow', 'typical', 'fast']:
        # Only one corner provided
        lib.set('output', corner, 'nldm', os.path.join(libdir, 'nldm', 'sky130_dummy_io.lib'))
    lib.set('output', stackup, 'lef', os.path.join(libdir, 'lef', 'sky130_ef_io.lef'))

    # Need both GDS files: ef relies on fd one
    lib.add('output', stackup, 'gds', os.path.join(libdir, 'gds', 'sky130_ef_io.gds'))
    lib.add('output', stackup, 'gds', os.path.join(libdir, 'gds', 'sky130_fd_io.gds'))
    lib.add('output', stackup, 'gds', os.path.join(libdir, 'gds',
                                                   'sky130_ef_io__gpiov2_pad_wrapped.gds'))

    lib.set('asic', 'cells', 'filler', ['sky130_ef_io__com_bus_slice_1um',
                                        'sky130_ef_io__com_bus_slice_5um',
                                        'sky130_ef_io__com_bus_slice_10um',
                                        'sky130_ef_io__com_bus_slice_20um'])

    lib.set('output', 'blackbox', 'verilog', os.path.join(libdir, 'bb', 'sky130_io.blackbox.v'))

    return lib


#########################
if __name__ == "__main__":
    lib = setup(siliconcompiler.Chip('<lib>'))
    lib.write_manifest(f'{lib.top()}.json')
