import fibonacciwangxiaoyanrustpython.fibonacci_python as fib_python
from fibonacciwangxiaoyanrustpython import fibonacciwangxiaoyanrustpython


if __name__ == "__main__":
    print(dir(fib_python))
    print(dir(fibonacciwangxiaoyanrustpython))
    n = int(input("请输入 N 的值："))

    result_normal, time_normal = fib_python.measure_time_python(fib_python.fibonacci_normal_python, n)
    result_optimized, time_optimized = fib_python.measure_time_python(fib_python.fibonacci_optimized_python, n)

    result_normal_rust, time_normal_rust = fib_python.measure_time_python(fibonacciwangxiaoyanrustpython.fibonacci_normal_rust, n)
    result_optimized_rust, time_optimized_rust = fib_python.measure_time_python(fibonacciwangxiaoyanrustpython.fibonacci_optimized_rust, n)

    print(f"常规实现: 第 {n} 项的值为: {result_normal}")
    print(f"常规实现: 运行时间: {time_normal} 秒")

    print(f"常规实现_rust: 第 {n} 项的值为: {result_normal_rust}")
    print(f"常规实现_rust: 运行时间: {time_normal_rust} 秒")


    print(f"优化速度实现: 第 {n} 项的值为: {result_optimized}")
    print(f"优化速度实现: 运行时间: {time_optimized} 秒")

    print(f"优化速度实现_rust: 第 {n} 项的值为: {result_optimized_rust}")
    print(f"优化速度实现_rust: 运行时间: {time_optimized_rust} 秒")