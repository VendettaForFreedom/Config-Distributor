# Testing TeleTweet Bot

## Running Tests

1. Install test dependencies:

```bash
pip install pytest pytest-asyncio pytest-mock
```

2. Run tests:

```bash
python -m pytest tests/
```

## Manual Testing Guide

### Testing Attached Messages

1. Forward Message Test:

```
1. Forward a message from a channel to the bot
2. Reply to the forwarded message with additional text
3. Verify:
   - Both messages are stored
   - Length is calculated correctly
   - Source reference is preserved
```

2. Length Handling Test:

```
1. Forward a long message (>280 chars)
2. Add a reply (>100 chars)
3. Verify:
   - Length warning appears
   - Truncation options are offered
   - Split message option works
```

3. Media Test:

```
1. Forward a photo with caption
2. Reply with additional text
3. Verify:
   - Photo is preserved
   - Both captions are combined
   - Platform-specific formatting
```

### Test Cases

#### 1. Basic Message Combination

```python
Original: "Main message"
Attached: "Additional info"
Expected: "Main message\n\nAdditional info"
```

#### 2. Length Limits

```python
# Twitter (280 chars)
Original: "x" * 200
Attached: "y" * 100
Expected: Length warning + truncation options

# Telegram (4000 chars)
Original: "x" * 3000
Attached: "y" * 1500
Expected: Length warning + truncation options
```

#### 3. Source References

```python
Original: From channel @example_channel
Attached: "Additional context"
Expected: Proper channel reference preserved
```

### Edge Cases to Test

1. Empty Messages:

```
- Empty original, valid attached
- Valid original, empty attached
- Both empty
```

2. Special Characters:

```
- Unicode characters
- Emojis
- RTL text
```

3. Media Combinations:

```
- Photo + text reply
- Text + photo reply
- Multiple photos + text
```

4. Platform-Specific:

```
- Twitter hashtags in attached message
- Telegram formatting in both messages
- Links in either message
```

## Automated Test Coverage

Current test suite covers:

1. Message Utils:

- combine_messages()
- check_message_length()
- split_message()
- truncate_content()

2. Message Store:

- Storage operations
- Cleanup functionality
- Thread safety

3. Message Handling:

- Forwarded message processing
- Reply message handling
- Media handling

## Adding New Tests

1. Create test file:

```python
# tests/test_new_feature.py
import pytest
from unittest.mock import MagicMock

def test_new_functionality():
    # Test setup
    # Test execution
    # Assertions
```

2. Run specific test:

```bash
python -m pytest tests/test_new_feature.py -v
```

## Debugging Tests

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Using PDB

```python
def test_something():
    import pdb; pdb.set_trace()
    # Test code here
```

### Common Issues

1. Async Test Failures:

```python
@pytest.mark.asyncio
async def test_async_function():
    # Use await for async calls
```

2. Mock Dependencies:

```python
@patch('module.dependency')
def test_with_mock(mock_dep):
    mock_dep.return_value = 'expected'
```

3. Cleanup After Tests:

```python
@pytest.fixture(autouse=True)
def cleanup():
    yield
    MESSAGE_STORE.clear()
```

## Performance Testing

### Message Processing Speed

```python
import time

def test_processing_speed():
    start = time.time()
    # Process message
    duration = time.time() - start
    assert duration < 1.0  # Should process under 1 second
```

### Memory Usage

```python
import psutil
import os

def test_memory_usage():
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss
    # Run operations
    mem_after = process.memory_info().rss
    assert (mem_after - mem_before) < 10 * 1024 * 1024  # Less than 10MB increase
```

## Test Data

Sample message data is available in `tests/data/`:

- sample_messages.json
- sample_media.json
- sample_configs.json

Use these for consistent test scenarios.
