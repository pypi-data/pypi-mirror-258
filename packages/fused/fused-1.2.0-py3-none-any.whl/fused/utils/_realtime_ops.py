from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import Optional

import aiohttp
import geopandas as gpd
import pandas as pd
import pyarrow.parquet as pq
import requests
import xarray as xr
import yarl
from PIL import Image

from ._impl._context_impl import context_get_auth_token, context_get_user_email
from ._impl._realtime_ops_impl import (
    get_recursion_factor,
    make_realtime_url,
    make_shared_realtime_url,
)

DEFAULT_DTYPE_VECTOR = "parquet"
DEFAULT_DTYPE_RASTER = "tiff"


def _parse_realtime_response(r: requests.Response, content_type: str):
    if content_type == "application/octet-stream":  # parquet
        r_bio = BytesIO(r.content)
        right_metadata = pq.read_metadata(r_bio)
        if b"geo" in right_metadata.metadata:
            return gpd.read_parquet(r_bio)
        else:
            return pd.read_parquet(r_bio)
    elif content_type == "image/png":
        image = Image.open(BytesIO(r.content))
        width, height = image.size
        if len(image.getbands()) == 1:
            image_data = list(image.getdata())
            image_data = [
                image_data[i : i + width] for i in range(0, len(image_data), width)
            ]
            data_array = xr.DataArray(image_data, dims=["y", "x"])
        else:
            image_data = []
            for band in range(len(image.getbands())):
                band_data = list(image.getdata(band=band))
                band_data = [
                    band_data[i : i + width] for i in range(0, len(band_data), width)
                ]
                image_data.append(band_data)
            data_array = xr.DataArray(image_data, dims=["band", "y", "x"])

        # Create the dataset with image, latitude, and longitude data
        dataset = xr.Dataset({"image": data_array})

        return dataset
    elif content_type == "image/tiff":
        import rioxarray

        with NamedTemporaryFile(prefix="udf_result", suffix=".tiff") as ntmp:
            with open(ntmp.name, "wb") as f:
                f.write(r.content)
            rda = rioxarray.open_rasterio(
                ntmp.name,
                masked=True,
            )
            dataset = xr.Dataset({"image": rda})
            return dataset

    return r.content  # TODO


async def _parse_realtime_response_async(r: aiohttp.ClientResponse, content_type: str):
    content = await r.read()
    if content_type == "application/octet-stream":  # parquet
        r_bio = BytesIO(content)
        right_metadata = pq.read_metadata(r_bio)
        if b"geo" in right_metadata.metadata:
            return gpd.read_parquet(r_bio)
        else:
            return pd.read_parquet(r_bio)
    elif content_type == "image/png":
        image = Image.open(BytesIO(content))
        width, height = image.size
        if len(image.getbands()) == 1:
            image_data = list(image.getdata())
            image_data = [
                image_data[i : i + width] for i in range(0, len(image_data), width)
            ]
            data_array = xr.DataArray(image_data, dims=["y", "x"])
        else:
            image_data = []
            for band in range(len(image.getbands())):
                band_data = list(image.getdata(band=band))
                band_data = [
                    band_data[i : i + width] for i in range(0, len(band_data), width)
                ]
                image_data.append(band_data)
            data_array = xr.DataArray(image_data, dims=["band", "y", "x"])

        # Create the dataset with image, latitude, and longitude data
        dataset = xr.Dataset({"image": data_array})

        return dataset
    elif content_type == "image/tiff":
        import rioxarray

        with NamedTemporaryFile(prefix="udf_result", suffix=".tiff") as ntmp:
            with open(ntmp.name, "wb") as f:
                f.write(content)
            rda = rioxarray.open_rasterio(
                ntmp.name,
                masked=True,
            )
            dataset = xr.Dataset({"image": rda})
            return dataset

    return content  # TODO


def _realtime_raise_for_status(r: requests.Response):
    if r.status_code >= 400 and "x-fused-error" in r.headers:
        msg = str(r.headers["x-fused-error"])
        raise requests.HTTPError(msg, response=r)
    if r.status_code >= 400 and "x-fused-metadata" in r.headers:
        # TODO: Format this
        msg = str(r.headers["x-fused-metadata"])
        raise requests.HTTPError(msg, response=r)
    r.raise_for_status()


def _realtime_raise_for_status_async(r: aiohttp.ClientResponse):
    if r.status >= 400 and "x-fused-error" in r.headers:
        msg = str(r.headers["x-fused-error"])
        raise requests.HTTPError(msg, response=r)
    if r.status >= 400 and "x-fused-metadata" in r.headers:
        # TODO: Format this
        msg = str(r.headers["x-fused-metadata"])
        raise requests.HTTPError(msg, response=r)
    r.raise_for_status()


async def _realtime_follow_redirect_async(
    *, session: aiohttp.ClientSession, r: aiohttp.ClientResponse
):
    if r.status >= 300 and r.status < 400 and "location" in r.headers:
        # Per this link, aiohttp will mangle the redirect URL
        # https://stackoverflow.com/questions/77319421/aiohttp-showing-403-forbidden-error-but-requests-get-giving-200-ok-response
        url = yarl.URL(r.headers["location"], encoded=True)
        return await session.get(url)
    return r


def _run_tile(
    url: str,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    **params,
):
    access_token = context_get_auth_token()
    recursion_factor = get_recursion_factor()

    req_params = {
        # TODO...
        "dtype_out_vector": _dtype_out_vector,
        "dtype_out_raster": _dtype_out_raster,
        **(params if params is not None else {}),
    }

    r = requests.get(
        url=url,
        params=req_params,
        headers={
            **({"Authorization": f"Bearer {access_token}"} if access_token else {}),
            "Fused-Recursion": f"{recursion_factor}",
        },
    )
    _realtime_raise_for_status(r)

    return _parse_realtime_response(r, content_type=r.headers["content-type"])


def run_tile(
    email: str,
    id: Optional[str] = None,
    *,
    x: int,
    y: int,
    z: int,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    _client_id: Optional[str] = None,
    **params,
):
    if id is None:
        id = email
        email = context_get_user_email()

    url = f"{make_realtime_url(_client_id)}/api/v1/run/udf/saved/{email}/{id}/tiles/{z}/{x}/{y}"
    return _run_tile(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        **params,
    )


def run_shared_tile(
    token: str,
    *,
    x: int,
    y: int,
    z: int,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    _client_id: Optional[str] = None,
    **params,
):
    url = f"{make_shared_realtime_url(token)}/run/tiles/{z}/{x}/{y}"
    return _run_tile(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        _client_id=_client_id,
        **params,
    )


def _run_file(
    url: str,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    **params,
):
    access_token = context_get_auth_token()
    recursion_factor = get_recursion_factor()

    req_params = {
        # TODO...
        "dtype_out_vector": _dtype_out_vector,
        "dtype_out_raster": _dtype_out_raster,
        **(params if params is not None else {}),
    }

    r = requests.get(
        url=url,
        params=req_params,
        headers={
            **({"Authorization": f"Bearer {access_token}"} if access_token else {}),
            "Fused-Recursion": f"{recursion_factor}",
        },
    )
    _realtime_raise_for_status(r)

    return _parse_realtime_response(r, content_type=r.headers["content-type"])


def run_file(
    email: str,
    id: Optional[str] = None,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    _client_id: Optional[str] = None,
    **params,
):
    if id is None:
        id = email
        email = context_get_user_email()

    url = f"{make_realtime_url(_client_id)}/api/v1/run/udf/saved/{email}/{id}"
    return _run_file(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        **params,
    )


def run_shared_file(
    token: str,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    **params,
):
    url = f"{make_shared_realtime_url(token)}/run/file"
    return _run_file(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        **params,
    )


async def _run_tile_async(
    url: str,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    **params,
):
    access_token = context_get_auth_token()
    recursion_factor = get_recursion_factor()

    req_params = {
        # TODO...
        "dtype_out_vector": _dtype_out_vector,
        "dtype_out_raster": _dtype_out_raster,
        **(params if params is not None else {}),
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=url,
            params=req_params,
            headers={
                **({"Authorization": f"Bearer {access_token}"} if access_token else {}),
                "Fused-Recursion": f"{recursion_factor}",
            },
            allow_redirects=False,
        ) as r:
            r = await _realtime_follow_redirect_async(session=session, r=r)
            _realtime_raise_for_status_async(r)

            return await _parse_realtime_response_async(
                r, content_type=r.headers["content-type"]
            )


async def run_tile_async(
    email: str,
    id: Optional[str] = None,
    *,
    x: int,
    y: int,
    z: int,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    _client_id: Optional[str] = None,
    **params,
):
    if id is None:
        id = email
        email = context_get_user_email()

    url = f"{make_realtime_url(_client_id)}/api/v1/run/udf/saved/{email}/{id}/tiles/{z}/{x}/{y}"
    return await _run_tile_async(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        **params,
    )


async def run_shared_tile_async(
    token: str,
    *,
    x: int,
    y: int,
    z: int,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    **params,
):
    url = f"{make_shared_realtime_url(token)}/run/tiles/{z}/{x}/{y}"
    return await _run_tile_async(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        **params,
    )


async def _run_file_async(
    url: str,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    **params,
):
    access_token = context_get_auth_token()
    recursion_factor = get_recursion_factor()

    req_params = {
        # TODO...
        "dtype_out_vector": _dtype_out_vector,
        "dtype_out_raster": _dtype_out_raster,
        **(params if params is not None else {}),
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=url,
            params=req_params,
            headers={
                **({"Authorization": f"Bearer {access_token}"} if access_token else {}),
                "Fused-Recursion": f"{recursion_factor}",
            },
            allow_redirects=False,
        ) as r:
            r = await _realtime_follow_redirect_async(session=session, r=r)
            _realtime_raise_for_status_async(r)

            return await _parse_realtime_response_async(
                r, content_type=r.headers["content-type"]
            )


async def run_file_async(
    email: str,
    id: Optional[str] = None,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    _client_id: Optional[str] = None,
    **params,
):
    if id is None:
        id = email
        email = context_get_user_email()

    url = f"{make_realtime_url(_client_id)}/api/v1/run/udf/saved/{email}/{id}"
    return await _run_file_async(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        **params,
    )


async def run_shared_file_async(
    token: str,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    **params,
):
    url = f"{make_shared_realtime_url(token)}/run/file"
    return await _run_file_async(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        **params,
    )
