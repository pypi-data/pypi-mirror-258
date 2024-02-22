"""
Tests for salt.utils.jinja
"""

import os

import pytest
from jinja2 import Environment, TemplateNotFound, exceptions

# dateutils is needed so that the strftime jinja filter is loaded
import salt.utils.dateutils  # pylint: disable=unused-import
import salt.utils.files  # pylint: disable=unused-import
import salt.utils.json  # pylint: disable=unused-import
import salt.utils.stringutils  # pylint: disable=unused-import
import salt.utils.yaml  # pylint: disable=unused-import
from salt.utils.jinja import SaltCacheLoader
from tests.support.mock import MagicMock, call, patch


@pytest.fixture
def minion_opts(tmp_path, minion_opts):
    minion_opts.update(
        {
            "file_buffer_size": 1048576,
            "cachedir": str(tmp_path),
            "file_roots": {"test": [str(tmp_path / "files" / "test")]},
            "pillar_roots": {"test": [str(tmp_path / "pillar" / "test")]},
            "extension_modules": os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "extmods"
            ),
        }
    )
    return minion_opts


@pytest.fixture
def hello_simple(template_dir):
    contents = """world
"""

    with pytest.helpers.temp_file(
        "hello_simple", directory=template_dir, contents=contents
    ) as hello_simple_filename:
        yield hello_simple_filename


@pytest.fixture
def hello_include(template_dir):
    contents = """{% include 'hello_import' -%}"""

    with pytest.helpers.temp_file(
        "hello_include", directory=template_dir, contents=contents
    ) as hello_include_filename:
        yield hello_include_filename


@pytest.fixture
def relative_dir(template_dir):
    relative_dir = template_dir / "relative"
    relative_dir.mkdir()
    return relative_dir


@pytest.fixture
def relative_rhello(relative_dir):
    contents = """{% from './rmacro' import rmacro with context -%}
{{ rmacro('Hey') ~ rmacro(a|default('a'), b|default('b')) }}
"""

    with pytest.helpers.temp_file(
        "rhello", directory=relative_dir, contents=contents
    ) as relative_rhello:
        yield relative_rhello


@pytest.fixture
def relative_rmacro(relative_dir):
    contents = """{% from '../macro' import mymacro with context %}
{% macro rmacro(greeting, greetee='world') -%}
{{ mymacro(greeting, greetee) }}
{%- endmacro %}
"""

    with pytest.helpers.temp_file(
        "rmacro", directory=relative_dir, contents=contents
    ) as relative_rmacro:
        yield relative_rmacro


@pytest.fixture
def relative_rescape(relative_dir):
    contents = """{% import '../../rescape' as xfail -%}
"""

    with pytest.helpers.temp_file(
        "rescape", directory=relative_dir, contents=contents
    ) as relative_rescape:
        yield relative_rescape


@pytest.fixture
def get_loader(mock_file_client, minion_opts):
    def run_command(opts=None, saltenv="base", **kwargs):
        """
        Now that we instantiate the client in the __init__, we need to mock it
        """
        if opts is None:
            opts = minion_opts
        mock_file_client.opts = opts
        loader = SaltCacheLoader(opts, saltenv, _file_client=mock_file_client, **kwargs)
        # Create a mock file client and attach it to the loader
        return loader

    return run_command


def get_test_saltenv(get_loader):
    """
    Setup a simple jinja test environment
    """
    loader = get_loader(saltenv="test")
    jinja = Environment(loader=loader)
    return loader._file_client, jinja


def test_searchpath(minion_opts, get_loader, tmp_path):
    """
    The searchpath is based on the cachedir option and the saltenv parameter
    """
    saltenv = "test"
    loader = get_loader(opts=minion_opts, saltenv=saltenv)
    assert loader.searchpath == minion_opts["file_roots"][saltenv]


def test_searchpath_pillar_rend(minion_opts, get_loader):
    """
    The searchpath is based on the pillar_rend if it is True
    """
    saltenv = "test"
    loader = get_loader(opts=minion_opts, saltenv=saltenv, pillar_rend=True)
    assert loader.searchpath == minion_opts["pillar_roots"][saltenv]


def test_searchpath_bad_pillar_rend(minion_opts, get_loader):
    """
    The searchpath is based on the pillar_rend if it is True
    """
    saltenv = "bad_env"
    loader = get_loader(opts=minion_opts, saltenv=saltenv, pillar_rend=True)
    assert loader.searchpath == []


def test_mockclient(minion_opts, template_dir, hello_simple, get_loader):
    """
    A MockFileClient is used that records all file requests normally sent
    to the master.
    """
    loader = get_loader(opts=minion_opts, saltenv="test")
    res = loader.get_source(None, "hello_simple")
    assert len(res) == 3
    # res[0] on Windows is unicode and use os.linesep so it works cross OS
    assert str(res[0]) == "world" + os.linesep
    assert res[1] == str(hello_simple)
    assert res[2](), "Template up to date?"
    assert loader._file_client.requests
    assert loader._file_client.requests[0]["path"] == "salt://hello_simple"


def test_import(get_loader, hello_import):
    """
    You can import and use macros from other files
    """
    fc, jinja = get_test_saltenv(get_loader)
    result = jinja.get_template("hello_import").render()
    assert result == "Hey world !a b !"
    assert len(fc.requests) == 2
    assert fc.requests[0]["path"] == "salt://hello_import"
    assert fc.requests[1]["path"] == "salt://macro"


def test_relative_import(
    get_loader, relative_rhello, relative_rmacro, relative_rescape, macro_template
):
    """
    You can import using relative paths
    issue-13889
    """
    fc, jinja = get_test_saltenv(get_loader)
    tmpl = jinja.get_template(os.path.join("relative", "rhello"))
    result = tmpl.render()
    assert result == "Hey world !a b !"
    assert len(fc.requests) == 3
    assert fc.requests[0]["path"] == "salt://relative/rhello"
    assert fc.requests[1]["path"] == "salt://relative/rmacro"
    assert fc.requests[2]["path"] == "salt://macro"
    # This must fail when rendered: attempts to import from outside file root
    template = jinja.get_template("relative/rescape")
    pytest.raises(exceptions.TemplateNotFound, template.render)


def test_include(get_loader, hello_include, hello_import):
    """
    You can also include a template that imports and uses macros
    """
    fc, jinja = get_test_saltenv(get_loader)
    result = jinja.get_template("hello_include").render()
    assert result == "Hey world !a b !"
    assert len(fc.requests) == 3
    assert fc.requests[0]["path"] == "salt://hello_include"
    assert fc.requests[1]["path"] == "salt://hello_import"
    assert fc.requests[2]["path"] == "salt://macro"


def test_include_context(get_loader, hello_include, hello_import):
    """
    Context variables are passes to the included template by default.
    """
    _, jinja = get_test_saltenv(get_loader)
    result = jinja.get_template("hello_include").render(a="Hi", b="Salt")
    assert result == "Hey world !Hi Salt !"


def test_cached_file_client(get_loader, minion_opts):
    """
    Multiple instantiations of SaltCacheLoader use the cached file client
    """
    with patch("salt.channel.client.ReqChannel.factory", MagicMock()):
        loader_a = SaltCacheLoader(minion_opts)
        loader_b = SaltCacheLoader(minion_opts)
    assert loader_a._file_client is loader_b._file_client


def test_file_client_kwarg(minion_opts, mock_file_client):
    """
    A file client can be passed to SaltCacheLoader overriding the any
    cached file client
    """
    mock_file_client.opts = minion_opts
    loader = SaltCacheLoader(minion_opts, _file_client=mock_file_client)
    assert loader._file_client is mock_file_client


def test_cache_loader_passed_file_client(minion_opts, mock_file_client):
    """
    The shudown method can be called without raising an exception when the
    file_client does not have a destroy method
    """
    # Test SaltCacheLoader creating and destroying the file client created
    file_client = MagicMock()
    with patch("salt.fileclient.get_file_client", return_value=file_client):
        loader = SaltCacheLoader(minion_opts)
        assert loader._file_client is None
        with loader:
            assert loader._file_client is file_client
        assert loader._file_client is None
        assert file_client.mock_calls == [call.destroy()]

    # Test SaltCacheLoader reusing the file client passed
    file_client = MagicMock()
    file_client.opts = {"file_roots": minion_opts["file_roots"]}
    with patch("salt.fileclient.get_file_client", return_value=MagicMock()):
        loader = SaltCacheLoader(minion_opts, _file_client=file_client)
        assert loader._file_client is file_client
        with loader:
            assert loader._file_client is file_client
        assert loader._file_client is file_client
        assert file_client.mock_calls == []

    # Test SaltCacheLoader creating a client even though a file client was
    # passed because the "file_roots" option is different, and, as such,
    # the destroy method on the new file client is called, but not on the
    # file client passed in.
    file_client = MagicMock()
    file_client.opts = {"file_roots": ""}
    new_file_client = MagicMock()
    with patch("salt.fileclient.get_file_client", return_value=new_file_client):
        loader = SaltCacheLoader(minion_opts, _file_client=file_client)
        assert loader._file_client is file_client
        with loader:
            assert loader._file_client is not file_client
            assert loader._file_client is new_file_client
        assert loader._file_client is None
        assert file_client.mock_calls == []
        assert new_file_client.mock_calls == [call.destroy()]


def test_check_cache_miss(get_loader, minion_opts, hello_simple):
    saltenv = "test"
    loader = get_loader(opts=minion_opts, saltenv=saltenv)
    with patch.object(loader, "cached", []):
        with patch.object(loader, "cache_file") as cache_mock:
            loader.check_cache(str(hello_simple))
            cache_mock.assert_called_once()


def test_check_cache_hit(get_loader, minion_opts, hello_simple):
    saltenv = "test"
    loader = get_loader(opts=minion_opts, saltenv=saltenv)
    with patch.object(loader, "cached", [str(hello_simple)]):
        with patch.object(loader, "cache_file") as cache_mock:
            loader.check_cache(str(hello_simple))
            cache_mock.assert_not_called()


def test_get_source_no_environment(
    get_loader, minion_opts, relative_rhello, relative_dir
):
    saltenv = "test"
    loader = get_loader(opts=minion_opts, saltenv=saltenv)
    with pytest.raises(TemplateNotFound):
        loader.get_source(None, str(".." / relative_rhello.relative_to(relative_dir)))


def test_get_source_relative_no_tpldir(
    get_loader, minion_opts, relative_rhello, relative_dir
):
    saltenv = "test"
    loader = get_loader(opts=minion_opts, saltenv=saltenv)
    with pytest.raises(TemplateNotFound):
        loader.get_source(
            MagicMock(globals={}), str(".." / relative_rhello.relative_to(relative_dir))
        )


def test_get_source_template_doesnt_exist(get_loader, minion_opts):
    saltenv = "test"
    fake_path = "fake_path"
    loader = get_loader(opts=minion_opts, saltenv=saltenv)
    with pytest.raises(TemplateNotFound):
        loader.get_source(None, fake_path)


def test_get_source_template_removed(get_loader, minion_opts, hello_simple):
    saltenv = "test"
    loader = get_loader(opts=minion_opts, saltenv=saltenv)
    contents, filepath, uptodate = loader.get_source(None, str(hello_simple))
    hello_simple.unlink()
    assert uptodate() is False


def test_no_destroy_method_on_file_client(get_loader, minion_opts):
    saltenv = "test"
    loader = get_loader(opts=minion_opts, saltenv=saltenv)
    loader._close_file_client = True
    # This should fail silently, thus no error catching
    loader.destroy()
