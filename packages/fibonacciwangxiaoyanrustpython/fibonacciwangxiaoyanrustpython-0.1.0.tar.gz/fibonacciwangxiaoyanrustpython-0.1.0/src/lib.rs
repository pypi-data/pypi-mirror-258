use pyo3::prelude::*;


#[pyfunction]
fn fibonacci_normal_rust(n: u64) -> u64 {
    if n <= 1 {
      n
    } else {
        fibonacci_normal_rust(n - 1) + fibonacci_normal_rust(n - 2)
    }
  }



  #[pyfunction]
  fn fibonacci_optimized_rust(n: u64) -> u64 {
    let mut a = 0;
    let mut b = 1;
    for _ in 0..n {
        let temp = a;
        a = b;
        b += temp;
    }
    a
}



#[pymodule]
fn fibonacciwangxiaoyanrustpython(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fibonacci_normal_rust, m)?)?;
    m.add_function(wrap_pyfunction!(fibonacci_optimized_rust, m)?)?;

    Ok(())
}