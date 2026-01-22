# NexusLog

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11%20|%203.12%20|%203.13-blue)
![Version](https://img.shields.io/pypi/v/nexuslog?color=blue)

高性能异步日志库，兼容 Python 标准 logging API。

[English](README.md)

## 性能测试

<p align="center">
  <img src="assets/bench.png" width="720" alt="Benchmark chart" />
</p>

```
Benchmarking with 1,000,000 log messages

------------------------------------------------------------
Logger               Time (s)     Msgs/sec        Log size    
------------------------------------------------------------
Python logging       5.237        190,954         82,888,890 bytes
loguru               7.039        142,070         89,888,890 bytes
picologging          1.999        500,306         79,888,882 bytes
spdlog               0.298        3,358,706       79,888,890 bytes
NexusLogger          0.131        7,654,750       97,888,890 bytes
NexusLogger unix_ts  0.127        7,874,086       82,888,890 bytes
------------------------------------------------------------

NexusLogger is 40.09x faster than Python logging
NexusLogger is 53.88x faster than loguru
NexusLogger is 15.30x faster than picologging
NexusLogger is 2.28x faster than spdlog
NexusLogger unix_ts is 41.24x faster than Python logging
NexusLogger unix_ts is 55.42x faster than loguru
NexusLogger unix_ts is 15.74x faster than picologging
NexusLogger unix_ts is 2.34x faster than spdlog
```

## 安装

```bash
pip install nexuslog
```

## 快速开始

```python
import nexuslog as logging

logging.basicConfig(level=logging.INFO)

logging.info("Hello, world!")
logging.warning("This is a warning")
logging.error("This is an error")
```

## API

### 日志级别

```python
logging.TRACE
logging.DEBUG
logging.INFO
logging.WARNING
logging.ERROR
```

### 模块级函数

```python
logging.basicConfig(filename=None, level=logging.INFO, unix_ts=False)
logging.trace(message)
logging.debug(message)
logging.info(message)
logging.warning(message)
logging.error(message)
```

### Logger 类

```python
from nexuslog import Logger, Level

logger = Logger("myapp", path="/var/log/app", level=Level.Info)
logger.info("message")
logger.shutdown()
```

### getLogger

```python
import nexuslog as logging

logging.basicConfig(filename="/var/log/app.log", level=logging.DEBUG)
logger = logging.getLogger("myapp")
logger.info("message")
```

## License

MIT
