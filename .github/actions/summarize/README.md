## Usage

```yaml
on:
  pull_request:

jobs:
  my-job:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/actions/summarize
        with:
          header: '## Display `vars` context'
          json: ${{ toJSON(vars) }}
```

Output:

```md
## Display vars context

```json
{
    "foo": "bar",
    "number": 42
}
```

---

```


