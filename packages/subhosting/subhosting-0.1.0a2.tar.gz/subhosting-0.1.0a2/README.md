# Deno Deploy Subhosting REST API client for Python

[![PyPI version](https://img.shields.io/pypi/v/subhosting.svg)](https://pypi.org/project/subhosting/)

This library provides convenient access to the
[Deno Deploy Subhosting](https://deno.com/subhosting) REST API, which allows you
to programmatically deploy untrusted, third-party code into the cloud, from
server-side Python.

The REST API documentation can be found
[on apidocs.deno.com](https://apidocs.deno.com/). The full API of this library
can be found in
[api.md](https://github.com/denoland/subhosting-python/blob/main/api.md).

To learn more about Subhosting,
[check out our documentation](https://docs.deno.com/subhosting/manual).

## Installation

```sh
pip install --pre subhosting
```

## Usage

Before you begin, you'll need to have a Deno Deploy access token and an ID for
the Deno Deploy organization you're using for Subhosting.

- You can find or create a personal access token
  [in the dashboard here](https://dash.deno.com/account#access-tokens)
- Your org ID can be found near the top of the page on your Deno Deploy
  dashboard [as described here](https://docs.deno.com/subhosting/api)

The code examples below assume your access token is stored in a
`DEPLOY_ACCESS_TOKEN` environment variable and your Deno Deploy org ID is stored
in a `DEPLOY_ORG_ID` environment variable.

```python
import os
from subhosting import Subhosting

client = Subhosting(
    # This is the default and can be omitted
    bearer_token=os.environ.get("DEPLOY_ACCESS_TOKEN"),
)

organization = client.organizations.get(
    "DEPLOY_ORG_ID",
)
print(organization.id)
```

While you can provide a `bearer_token` keyword argument, we recommend using
[python-dotenv](https://pypi.org/project/python-dotenv/) to add
`DEPLOY_ACCESS_TOKEN="My Bearer Token"` to your `.env` file so that your Bearer
Token is not stored in source control.

## Async usage

Simply import `AsyncSubhosting` instead of `Subhosting` and use `await` with
each API call:

```python
import os
import asyncio
from subhosting import AsyncSubhosting

client = AsyncSubhosting(
    # This is the default and can be omitted
    bearer_token=os.environ.get("DEPLOY_ACCESS_TOKEN"),
)


async def main() -> None:
    organization = await client.organizations.get(
        "DEPLOY_ORG_ID",
    )
    print(organization.id)


asyncio.run(main())
```

Functionality between the synchronous and asynchronous clients is otherwise
identical.

## Using types

Nested request parameters are
[TypedDicts](https://docs.python.org/3/library/typing.html#typing.TypedDict).
Responses are [Pydantic models](https://docs.pydantic.dev), which provide helper
methods for things like:

- Serializing back into JSON,
  `model.model_dump_json(indent=2, exclude_unset=True)`
- Converting to a dictionary, `model.model_dump(exclude_unset=True)`

Typed requests and responses provide autocomplete and documentation within your
editor. If you would like to see type errors in VS Code to help catch bugs
earlier, set `python.analysis.typeCheckingMode` to `basic`.

## Handling errors

When the library is unable to connect to the API (for example, due to network
connection problems or a timeout), a subclass of `subhosting.APIConnectionError`
is raised.

When the API returns a non-success status code (that is, 4xx or 5xx response), a
subclass of `subhosting.APIStatusError` is raised, containing `status_code` and
`response` properties.

All errors inherit from `subhosting.APIError`.

```python
import subhosting
from subhosting import Subhosting

client = Subhosting()

try:
    client.organizations.get(
        "DEPLOY_ORG_ID",
    )
except subhosting.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except subhosting.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except subhosting.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
```

Error codes are as followed:

| Status Code | Error Type                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `APIConnectionError`       |

### Retries

Certain errors are automatically retried 2 times by default, with a short
exponential backoff. Connection errors (for example, due to a network
connectivity problem), 408 Request Timeout, 409 Conflict, 429 Rate Limit, and
>=500 Internal errors are all retried by default.

You can use the `max_retries` option to configure or disable retry settings:

```python
from subhosting import Subhosting

# Configure the default for all requests:
client = Subhosting(
    # default is 2
    max_retries=0,
)

# Or, configure per-request:
client.with_options(max_retries=5).organizations.get(
    "DEPLOY_ORG_ID",
)
```

### Timeouts

By default requests time out after 1 minute. You can configure this with a
`timeout` option, which accepts a float or an
[`httpx.Timeout`](https://www.python-httpx.org/advanced/#fine-tuning-the-configuration)
object:

```python
from subhosting import Subhosting

# Configure the default for all requests:
client = Subhosting(
    # 20 seconds (default is 1 minute)
    timeout=20.0,
)

# More granular control:
client = Subhosting(
    timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
)

# Override per-request:
client.with_options(timeout=5 * 1000).organizations.get(
    "DEPLOY_ORG_ID",
)
```

On timeout, an `APITimeoutError` is thrown.

Note that requests that time out are [retried twice by default](#retries).

## Advanced

### Logging

We use the standard library
[`logging`](https://docs.python.org/3/library/logging.html) module.

You can enable logging by setting the environment variable `SUBHOSTING_LOG` to
`debug`.

```shell
$ export SUBHOSTING_LOG=debug
```

### How to tell whether `None` means `null` or missing

In an API response, a field may be explicitly `null`, or missing entirely; in
either case, its value is `None` in this library. You can differentiate the two
cases with `.model_fields_set`:

```py
if response.my_field is None:
  if 'my_field' not in response.model_fields_set:
    print('Got json like {}, without a "my_field" key present at all.')
  else:
    print('Got json like {"my_field": null}.')
```

### Accessing raw response data (e.g. headers)

The "raw" Response object can be accessed by prefixing `.with_raw_response.` to
any HTTP method call, e.g.,

```py
from subhosting import Subhosting

client = Subhosting()
response = client.organizations.with_raw_response.get(
    "DEPLOY_ORG_ID",
)
print(response.headers.get('X-My-Header'))

organization = response.parse()  # get the object that `organizations.get()` would have returned
print(organization.id)
```

These methods return an
[`APIResponse`](https://github.com/denoland/subhosting-python/tree/main/src/subhosting/_response.py)
object.

The async client returns an
[`AsyncAPIResponse`](https://github.com/denoland/subhosting-python/tree/main/src/subhosting/_response.py)
with the same structure, the only difference being `await`able methods for
reading the response content.

#### `.with_streaming_response`

The above interface eagerly reads the full response body when you make the
request, which may not always be what you want.

To stream the response body, use `.with_streaming_response` instead, which
requires a context manager and only reads the response body once you call
`.read()`, `.text()`, `.json()`, `.iter_bytes()`, `.iter_text()`,
`.iter_lines()` or `.parse()`. In the async client, these are async methods.

```python
with client.organizations.with_streaming_response.get(
    "DEPLOY_ORG_ID",
) as response:
    print(response.headers.get("X-My-Header"))

    for line in response.iter_lines():
        print(line)
```

The context manager is required so that the response will reliably be closed.

### Configuring the HTTP client

You can directly override the
[httpx client](https://www.python-httpx.org/api/#client) to customize it for
your use case, including:

- Support for proxies
- Custom transports
- Additional [advanced](https://www.python-httpx.org/advanced/#client-instances)
  functionality

```python
import httpx
from subhosting import Subhosting

client = Subhosting(
    # Or use the `SUBHOSTING_BASE_URL` env var
    base_url="http://my.test.server.example.com:8083",
    http_client=httpx.Client(
        proxies="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

### Managing HTTP resources

By default the library closes underlying HTTP connections whenever the client is
[garbage collected](https://docs.python.org/3/reference/datamodel.html#object.__del__).
You can manually close the client using the `.close()` method if desired, or
with a context manager that closes when exiting.

## Versioning

This package generally follows [SemVer](https://semver.org/spec/v2.0.0.html)
conventions, though certain backwards-incompatible changes may be released as
minor versions:

1. Changes that only affect static types, without breaking runtime behavior.
2. Changes to library internals which are technically public but not intended or
   documented for external use. _(Please open a GitHub issue to let us know if
   you are relying on such internals)_.
3. Changes that we do not expect to impact the vast majority of users in
   practice.

We take backwards-compatibility seriously and work hard to ensure you can rely
on a smooth upgrade experience.

We are keen for your feedback; please open an
[issue](https://www.github.com/denoland/subhosting-python/issues) with
questions, bugs, or suggestions.

## Requirements

Python 3.7 or higher.
