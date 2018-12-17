"""
    lml.loader
    ~~~~~~~~~~~~~~~~~~~

    Auto discover avaiable plugins

    :copyright: (c) 2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import pkgutil
import logging
from itertools import chain
from lml.utils import do_import


log = logging.getLogger(__name__)


def scan_plugins(prefix, path, black_list=None, white_list=None):
    """
    Discover plugins via pkgutil and pyinstaller path
    """
    if black_list is None:
        black_list = []

    if white_list is None:
        white_list = []

    # scan pkgutil.iter_modules
    module_names = (module_info[1] for module_info in pkgutil.iter_modules()
                    if module_info[2] and module_info[1].startswith(prefix))
    import pdb; pdb.set_trace()
    # scan pyinstaller
    module_names_from_pyinstaller = scan_from_pyinstaller(prefix, path)

    all_modules = chain(module_names,
                        module_names_from_pyinstaller,
                        white_list)
    # loop through modules and find our plug ins
    for module_name in all_modules:
        log.debug(module_name)

        if module_name in black_list:
            log.debug("ignored " + module_name)
            continue

        try:
            do_import(module_name)
        except ImportError as e:
            log.debug(module_name)
            log.debug(e)
            continue


# load modules to work based with and without pyinstaller
# from: https://github.com/webcomics/dosage/blob/master/dosagelib/loader.py
# see: https://github.com/pyinstaller/pyinstaller/issues/1905
# load modules using iter_modules()
# (should find all plug ins in normal build, but not pyinstaller)
def scan_from_pyinstaller(prefix, path):
    """
    Discover plugins from pyinstaller
    """
    table_of_content = set()
    for a_toc in (importer.toc for importer in map(pkgutil.get_importer, path)
                  if hasattr(importer, 'toc')):
        table_of_content |= a_toc

    for module_name in table_of_content:
        if module_name.startswith(prefix) and '.' not in module_name:
            yield module_name
