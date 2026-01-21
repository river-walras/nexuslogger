"""Benchmark comparing NexusLogger vs Python's built-in logging vs picologging."""

import logging
import time
import tempfile
import os

# Number of log messages per benchmark
N_MESSAGES = 1_000_000


def bench_picologging(log_file: str) -> float:
    """Benchmark picologging."""
    import picologging

    pico_logger = picologging.Logger("pico_bench", picologging.INFO)
    handler = picologging.FileHandler(log_file, mode="w")
    handler.setFormatter(
        picologging.Formatter("[%(asctime)s %(filename)s %(lineno)d %(levelname)s] %(message)s")
    )
    pico_logger.addHandler(handler)

    start = time.perf_counter()
    for i in range(N_MESSAGES):
        pico_logger.info("Benchmark message number %d", i)
    handler.flush()
    elapsed = time.perf_counter() - start

    handler.close()
    return elapsed


def bench_python_logging(log_file: str) -> float:
    """Benchmark Python's built-in logging."""
    # Configure Python logging
    py_logger = logging.getLogger("python_bench")
    py_logger.setLevel(logging.INFO)
    py_logger.handlers.clear()
    handler = logging.FileHandler(log_file, mode="w")
    handler.setFormatter(
        logging.Formatter("[%(asctime)s %(filename)s %(lineno)d %(levelname)s] %(message)s")
    )
    py_logger.addHandler(handler)

    start = time.perf_counter()
    for i in range(N_MESSAGES):
        py_logger.info("Benchmark message number %d", i)
    handler.flush()
    elapsed = time.perf_counter() - start

    handler.close()
    py_logger.removeHandler(handler)
    return elapsed


def bench_rust_logger(log_file: str) -> float:
    """Benchmark NexusLogger."""
    import nexuslog as logging

    logging.basicConfig(log_file, level=logging.Level.Info)
    log = logging.getLogger("bench")

    start = time.perf_counter()
    for i in range(N_MESSAGES):
        log.info(f"Benchmark message number {i}")
    log.shutdown()  # Ensures all messages are flushed
    elapsed = time.perf_counter() - start

    return elapsed


def main():
    print(f"Benchmarking with {N_MESSAGES:,} log messages\n")
    print("-" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Benchmark Python logging
        py_log = os.path.join(tmpdir, "python.log")
        py_time = bench_python_logging(py_log)
        py_size = os.path.getsize(py_log)

        # Benchmark picologging
        pico_log = os.path.join(tmpdir, "pico.log")
        pico_time = bench_picologging(pico_log)
        pico_size = os.path.getsize(pico_log)

        # Benchmark NexusLogger
        # Note: NexusLogger adds date suffix, so we use a prefix
        rust_log_prefix = os.path.join(tmpdir, "rust")
        rust_time = bench_rust_logger(rust_log_prefix)
        # Find the actual log file (has date suffix)
        rust_files = [f for f in os.listdir(tmpdir) if f.startswith("rust")]
        rust_size = sum(os.path.getsize(os.path.join(tmpdir, f)) for f in rust_files)

        # Results
        print(f"{'Logger':<20} {'Time (s)':<12} {'Msgs/sec':<15} {'Log size':<12}")
        print("-" * 60)

        py_rate = N_MESSAGES / py_time
        print(f"{'Python logging':<20} {py_time:<12.3f} {py_rate:<15,.0f} {py_size:,} bytes")

        pico_rate = N_MESSAGES / pico_time
        print(f"{'picologging':<20} {pico_time:<12.3f} {pico_rate:<15,.0f} {pico_size:,} bytes")

        rust_rate = N_MESSAGES / rust_time
        print(f"{'NexusLogger':<20} {rust_time:<12.3f} {rust_rate:<15,.0f} {rust_size:,} bytes")

        print("-" * 60)
        print(f"\nNexusLogger is {py_time / rust_time:.2f}x faster than Python logging")
        print(f"NexusLogger is {pico_time / rust_time:.2f}x faster than picologging")


if __name__ == "__main__":
    main()
