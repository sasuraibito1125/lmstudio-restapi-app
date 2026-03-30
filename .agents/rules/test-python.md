---
trigger: always_on
---

# Python Test Rules (pytest)

## Framework

- pytest

---

## Unit Test

- 関数単位
- 外部依存はmock

---

## Fixture

- pytest.fixture を使用

---

## Example

```python
def test_should_return_value():
    assert func() == expected
```
