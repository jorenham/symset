use pyo3::basic::CompareOp;
use pyo3::exceptions::PyTypeError;
use pyo3::prelude::*;
use pyo3::types::PyFrozenSet;
use std::sync::OnceLock;

#[pymodule]
mod _core {
    use super::*;

    #[pyclass(frozen)]
    struct EmptySetIterator;

    #[pymethods]
    impl EmptySetIterator {
        fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
            slf
        }

        fn __next__(&self) -> Option<PyObject> {
            None
        }
    }

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

        fn __contains__(&self, _item: PyObject) -> bool {
            false
        }

        fn __iter__(slf: PyRef<'_, Self>) -> PyResult<Py<EmptySetIterator>> {
            Py::new(slf.py(), EmptySetIterator)
        }

        fn _hash(slf: PyRef<'_, Self>) -> PyResult<isize> {
            PyFrozenSet::empty(slf.py())?.hash()
        }

        fn __hash__(slf: PyRef<'_, Self>) -> isize {
            static HASH_CELL: OnceLock<isize> = OnceLock::new();
            *HASH_CELL.get_or_init(|| Self::_hash(slf).unwrap())
        }

        fn __richcmp__(&self, other: Bound<'_, PyAny>, op: CompareOp) -> PyResult<bool> {
            let empty = PyFrozenSet::empty(other.py())?;
            match op {
                CompareOp::Lt => empty.lt(other),
                CompareOp::Le => empty.le(other),
                CompareOp::Eq => empty.eq(other),
                CompareOp::Ne => empty.ne(other),
                CompareOp::Gt => empty.gt(other),
                CompareOp::Ge => empty.ge(other),
            }
        }

        fn __and__<'py>(
            slf: PyRef<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<Bound<'py, Self>> {
            let py = other.py();
            let abstract_set_type = PyModule::import(py, "typing")?.getattr("AbstractSet")?;
            if other.is_instance(&abstract_set_type)? {
                Ok(slf.into_pyobject(py).unwrap())
            } else {
                Err(PyTypeError::new_err(
                    "Expected an instance of typing.AbstractSet",
                ))
            }
        }

        fn __rand__<'py>(
            slf: PyRef<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<Bound<'py, Self>> {
            Self::__and__(slf, other)
        }

        // TODO: implement the following `typing.AbstractSet` methods
        // __[r]and__: (AbstractSet[?]) -> Self
        // __[r]or__: (S @ AbstractSet[?]]) -> S
        // __[r]xor__: (S @ AbstractSet[?]]) -> S
        // __sub__: (AbstractSet[?]) -> Self
        // __rsub__: (S @ AbstractSet[?]) -> S
        // isdisjoint: (Iterable[Any]) -> bool
    }

    #[pymodule_export]
    const EMPTY_SET: EmptySetType = EmptySetType;
}
