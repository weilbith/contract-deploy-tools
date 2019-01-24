import pytest
from deploy_tools.plugin import CONTRACTS_FOLDER_OPTION


@pytest.fixture()
def contract(deploy_contract):
    return deploy_contract('TestContract', constructor_args=(4,))


@pytest.fixture()
def go_to_root_testdir_conftest(testdir):
    """gives access to the go_to_root_dir fixture to testdir tests"""

    testdir.makeconftest(
        """
        import pytest
        import os
        from pathlib import Path


        @pytest.fixture()
        def go_to_root_dir():
            current_path = os.getcwd()
            os.chdir(Path(__file__).parent.parent)
            yield
            os.chdir(current_path)
        """)


def test_call(contract):
    assert contract.functions.testFunction(3).call() == 7


@pytest.mark.usefixtures('go_to_root_testdir_conftest')
def test_get_contracts_folder(testdir):
    """This tests that get_contracts_folder returns a relative path when the option
    CONTRACTS_FOLDER_OPTION is set"""

    testdir.makepyfile(
        """
        import pytest
        from deploy_tools.plugin import get_contracts_folder
        
        
        def test_get_contracts_folder(pytestconfig):
            assert get_contracts_folder(pytestconfig) == 'test/dir'
        
        
        @pytest.mark.usefixtures('go_to_root_dir')
        def test_get_contracts_folder_from_root_dir(pytestconfig):
            assert get_contracts_folder(pytestconfig) == 'test/dir'
        """)

    result = testdir.runpytest(CONTRACTS_FOLDER_OPTION + "=test/dir")
    result.assert_outcomes(passed=2)


@pytest.mark.usefixtures('go_to_root_testdir_conftest')
def test_get_contracts_default_folder(testdir):
    """This tests that get_contracts_folder returns the path of rootdir/contracts when no
    CONTRACTS_FOLDER_OPTION is set"""

    testdir.makepyfile(
        """
        import pytest
        from pathlib import Path
        from deploy_tools.plugin import get_contracts_folder


        def test_get_contracts_default_folder(pytestconfig):
            assert get_contracts_folder(pytestconfig) == Path(pytestconfig.rootdir / '/contracts')
        
        
        @pytest.mark.usefixtures('go_to_root_dir')
        def test_get_contracts_default_folder_from_root_dir(pytestconfig):
            assert get_contracts_folder(pytestconfig) == Path(pytestconfig.rootdir / '/contracts')
        """)

    result = testdir.runpytest()
    result.assert_outcomes(passed=2)
