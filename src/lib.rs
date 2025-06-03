use pyo3::basic::CompareOp;
use pyo3::exceptions::PyTypeError;
use pyo3::types::PyFrozenSet;
use pyo3::{PyClass, prelude::*};

/// The `hash(frozenset({}))` value, confirmed to be system-independent by inspecting the algorithm
const HASH_EMPTY: isize = 133146708735736;

fn is_set(other: &Bound<'_, PyAny>) -> PyResult<bool> {
    let abstract_set_type = PyModule::import(other.py(), "typing")?.getattr("AbstractSet")?;
    other.is_instance(&abstract_set_type)
}

fn require_set<'py, T: PyClass, R>(
    slf: PyRef<'py, T>,
    other: Bound<'py, PyAny>,
    to_result: fn(PyRef<'py, T>, Bound<'py, PyAny>) -> PyResult<Bound<'py, R>>,
) -> PyResult<Bound<'py, R>> {
    if is_set(&other)? {
        to_result(slf, other)
    } else {
        Err(PyTypeError::new_err("not a set"))
    }
}

#[pymodule]
mod _core {
    use super::*;

    #[pyclass(frozen)]
    struct NothingIterator;

    #[pymethods]
    impl NothingIterator {
        fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
            slf
        }

        fn __next__(&self) -> Option<PyObject> {
            None
        }
    }

    #[pyclass(frozen)]
    pub struct NothingType;

    #[pymethods]
    impl NothingType {
        fn __str__(&self) -> String {
            "∅".to_string()
        }

        fn __repr__(&self) -> String {
            "Nothing".to_string()
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

        fn __iter__(slf: PyRef<'_, Self>) -> PyResult<Py<NothingIterator>> {
            Py::new(slf.py(), NothingIterator)
        }

        fn _hash(&self) -> isize {
            HASH_EMPTY
        }

        fn __hash__(&self) -> isize {
            HASH_EMPTY
        }

        fn __richcmp__(&self, other: Bound<'_, PyAny>, op: CompareOp) -> PyResult<bool> {
            PyFrozenSet::empty(other.py())?
                .rich_compare(other, op)
                .and_then(|any| any.is_truthy())
        }

        fn __and__<'py>(
            slf: PyRef<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<Bound<'py, Self>> {
            require_set(slf, other, |slf_, other_| {
                Ok(slf_.into_pyobject(other_.py())?)
            })
        }

        fn __or__<'py>(
            slf: PyRef<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<Bound<'py, PyAny>> {
            require_set(slf, other, |slf_, other_| {
                Ok(if other_.is_truthy()? {
                    other_
                } else {
                    slf_.into_pyobject(other_.py())?.into_any()
                })
            })
        }

        fn __xor__<'py>(
            slf: PyRef<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<Bound<'py, PyAny>> {
            Self::__or__(slf, other)
        }

        fn __sub__<'py>(
            slf: PyRef<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<Bound<'py, Self>> {
            Self::__and__(slf, other)
        }

        fn __rsub__<'py>(
            slf: PyRef<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<Bound<'py, PyAny>> {
            Self::__or__(slf, other)
        }

        fn isdisjoint(&self, other: Bound<'_, PyAny>) -> PyResult<bool> {
            if other.try_iter().is_ok() {
                Ok(true)
            } else {
                Err(PyTypeError::new_err("not iterable"))
            }
        }
    }

    #[pymodule_export]
    #[allow(non_upper_case_globals)]
    const Nothing: NothingType = NothingType;
}
