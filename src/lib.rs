use pyo3::basic::CompareOp;
use pyo3::prelude::*;
use pyo3::types::PyFrozenSet;

#[pymodule]
mod _core {

    use super::*;

    #[pyclass(frozen)]
    struct EmptySetType;

    #[pymethods]
    impl EmptySetType {
        fn __str__(&self) -> String {
            "∅".to_string()
        }

        fn __repr__(&self) -> String {
            "EmptySet".to_string()
        }

        fn __bool__(&self) -> bool {
            false
        }

        fn __len__(&self) -> usize {
            0
        }

        fn __contains__(&self, _item: &str) -> bool {
            false
        }

        fn __hash__<'py>(slf: Bound<'py, Self>) -> isize {
            PyFrozenSet::empty(slf.py()).unwrap().hash().unwrap()
        }

        // fn __hash__<'py>(slf: Bound<'py, Self>) -> PyResult<isize> {
        //     let builtins = slf.py().import("builtins")?;
        //     builtins.getattr("frozenset")?.call1(())?.hash()
        // }

        fn __richcmp__<'py>(&self, other: Bound<'py, PyAny>, op: CompareOp) -> PyResult<bool> {
            let empty = PyFrozenSet::empty(other.py()).unwrap();
            match op {
                CompareOp::Lt => empty.lt(other),
                CompareOp::Le => empty.le(other),
                CompareOp::Eq => empty.eq(other),
                CompareOp::Ne => empty.ne(other),
                CompareOp::Gt => empty.gt(other),
                CompareOp::Ge => empty.ge(other),
            }
        }
    }

    #[pymodule_export]
    const EMPTY_SET: EmptySetType = EmptySetType;
}
