import pytest

from pymarsys.sync.base_endpoint import BaseEndpoint


class TestBaseEndpoint:
    def test_init(self):
        with pytest.raises(TypeError) as excinfo:
            BaseEndpoint()
        assert "Can't instantiate abstract class BaseEndpoint with abstract " \
               "methods __init__" in str(excinfo.value)
