import time

def fibonacci_normal_python(n:int) -> int:
  if n <= 1:
    return n
  else:
    return fibonacci_normal_python(n - 1) + fibonacci_normal_python(n - 2)


def fibonacci_optimized_python(n:int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def measure_time_python(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time

if __name__ == "__main__":
    n = int(input("请输入 N 的值："))

    result_normal, time_normal = measure_time_python(fibonacci_normal_python, n)
    result_optimized, time_optimized = measure_time_python(fibonacci_optimized_python, n)

    print(f"常规实现: 第 {n} 项的值为: {result_normal}")
    print(f"常规实现: 运行时间: {time_normal} 秒")

    print(f"优化速度实现: 第 {n} 项的值为: {result_optimized}")
    print(f"优化速度实现: 运行时间: {time_optimized} 秒")

