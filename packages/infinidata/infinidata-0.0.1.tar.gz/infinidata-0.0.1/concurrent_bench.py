import numpy as np
import concurrent.futures
from infinidata import TableView

tbl_dict = {"foo": np.random.uniform(size=(451, 80)).astype(np.float32), "bar": np.arange(451 * 1024).reshape((451, 1024)) }

tv = TableView(tbl_dict)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=16)

def bench_loop():
    for _ in range(1_000):
        tv[:]

concurrent.futures.wait([executor.submit(bench_loop) for _ in range(16)])