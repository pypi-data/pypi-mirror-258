from typing import Any, Union

from fused.utils._impl._udf_ops_impl import get_step_config_from_server
from fused.utils._udf_ops import AttrDict, ExecutableUdf


class _Public:
    def __init__(self, cache_key: Any = None):
        self._cache_key = cache_key

    def __getattribute__(self, key: str) -> Union[Any, AttrDict]:
        try:
            return super().__getattribute__(key)
        except AttributeError:
            try:
                return self[key]
            # Note that we need to raise an AttributeError, **not a KeyError** so that
            # IPython's _repr_html_ works here
            except KeyError:
                raise AttributeError(
                    f"object of type {type(self).__name__} has no attribute {key}"
                ) from None

    def __getitem__(self, key: str) -> AttrDict:
        step_config = get_step_config_from_server(
            email=None,
            slug=key,
            cache_key=self._cache_key,
            _is_public=True,
        )

        return ExecutableUdf(step_config=step_config).utils


public = _Public()
