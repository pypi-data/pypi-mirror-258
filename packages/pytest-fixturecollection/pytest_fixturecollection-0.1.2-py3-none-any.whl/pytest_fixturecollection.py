# -*- coding: utf-8 -*-
import pytest


def pytest_addoption(parser):
    """Add options for pytest to collect tests based on fixtures its using"""
    help_text = '''
        Collects tests based on fixtures used by tests

        Usage: --uses-fixtures [options]

        Options: [ specific_fixture_name | list_of fixture names ]

        Ex: pytest tests/foreman --uses-fixtures target_sat,module_target_sat
    '''
    parser.addoption("--uses-fixtures", nargs='?', help=help_text)


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items, config):

    if not config.getoption('uses_fixtures', False):
        return

    filter_fixtures = config.getvalue('uses_fixtures')
    fixtures_list = filter_fixtures.split(',') if ',' in filter_fixtures else [
        filter_fixtures]
    selected = []
    deselected = []

    for item in items:
        if set(item.fixturenames).intersection(set(fixtures_list)):
            selected.append(item)
        else:
            deselected.append(item)
    config.hook.pytest_deselected(items=deselected)
    items[:] = selected
