use pyo3::basic::CompareOp;
use pyo3::exceptions::PyOverflowError;
use pyo3::exceptions::PyTypeError;
use pyo3::types::PyFrozenSet;
use pyo3::{PyClass, prelude::*};

/// The `hash(frozenset({}))` value, confirmed to be system-independent by inspecting the algorithm
const HASH_EMPTY: isize = 133146708735736;
const HASH_UNIVERSE: isize = (usize::MAX ^ HASH_EMPTY as usize) as isize;

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
    use pyo3::IntoPyObjectExt;

    use super::*;

    #[pyclass(frozen)]
    struct EmptyIterator;

    #[pymethods]
    impl EmptyIterator {
        fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
            slf
        }

        fn __next__(&self) -> Option<PyObject> {
            None
        }
    }

    #[pyclass(frozen)]
    pub struct EmptyType;

    #[pymethods]
    impl EmptyType {
        fn __str__(&self) -> String {
            "∅".to_string()
        }

        fn __repr__(&self) -> String {
            "Empty".to_string()
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

        fn __iter__(slf: PyRef<'_, Self>) -> PyResult<Py<EmptyIterator>> {
            Py::new(slf.py(), EmptyIterator)
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
                    slf_.into_bound_py_any(other_.py())?
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
            if other.try_iter().is_ok() || is_set(&other)? {
                Ok(true)
            } else {
                Err(PyTypeError::new_err("not iterable"))
            }
        }
    }

    #[pyclass(frozen)]
    pub struct UniverseType;

    #[pymethods]
    impl UniverseType {
        fn __str__(&self) -> String {
            "U".to_string()
        }

        fn __repr__(&self) -> String {
            "Universe".to_string()
        }

        fn __bool__(&self) -> bool {
            true
        }

        fn __len__(&self) -> PyResult<usize> {
            Err(PyOverflowError::new_err("infinite set"))
        }

        fn __iter__(&self) -> PyResult<Py<PyAny>> {
            Err(PyOverflowError::new_err("infinite set"))
        }

        fn __contains__(&self, _item: PyObject) -> bool {
            true
        }

        fn _hash(&self) -> isize {
            HASH_UNIVERSE
        }

        fn __hash__(&self) -> isize {
            HASH_UNIVERSE
        }

        fn __richcmp__(&self, other: Bound<'_, PyAny>, op: CompareOp) -> PyResult<bool> {
            let universe_py = Universe.into_bound_py_any(other.py())?.get_type();
            let err = Err(PyTypeError::new_err("not a set"));
            let eq = other.is_instance(&universe_py)?;
            match op {
                CompareOp::Eq => Ok(eq),
                CompareOp::Ne => Ok(!eq),
                CompareOp::Le => {
                    if is_set(&other)? {
                        Ok(eq)
                    } else {
                        err
                    }
                }
                CompareOp::Gt => {
                    if is_set(&other)? {
                        Ok(!eq)
                    } else {
                        err
                    }
                }
                CompareOp::Lt => {
                    if is_set(&other)? {
                        Ok(false)
                    } else {
                        err
                    }
                }
                CompareOp::Ge => {
                    if is_set(&other)? {
                        Ok(true)
                    } else {
                        err
                    }
                }
            }
        }

        fn __and__<'py>(
            slf: PyRef<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<Bound<'py, PyAny>> {
            require_set(slf, other, |_, other_| {
                Ok(if !other_.is_truthy()? {
                    Empty.into_bound_py_any(other_.py())?
                } else {
                    other_
                })
            })
        }

        fn __or__<'py>(
            slf: PyRef<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<Bound<'py, Self>> {
            require_set(slf, other, |slf_, other_| {
                Ok(slf_.into_pyobject(other_.py())?)
            })
        }

        fn __xor__<'py>(
            slf: PyRef<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<Bound<'py, PyAny>> {
            if !is_set(&other)? {
                return Err(PyTypeError::new_err("not a set"));
            }

            match other.len() {
                Err(_) => Empty.into_bound_py_any(slf.py()),
                Ok(0) => Universe.into_bound_py_any(slf.py()),
                Ok(_) => todo!("finite non-empty set complement"),
            }
        }

        fn __sub__<'py>(
            slf: PyRef<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<Bound<'py, PyAny>> {
            Self::__xor__(slf, other)
        }

        fn __rsub__<'py>(
            slf: PyRef<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<Bound<'py, EmptyType>> {
            require_set(slf, other, |_, other_| Empty.into_pyobject(other_.py()))
        }

        fn isdisjoint(&self, other: Bound<'_, PyAny>) -> PyResult<bool> {
            if is_set(&other)? {
                other.is_empty().or_else(|_| Ok(false))
            } else {
                Err(PyTypeError::new_err("not iterable"))
            }
        }
    }

    #[pymodule_export]
    #[allow(non_upper_case_globals)]
    const Empty: EmptyType = EmptyType;

    #[pymodule_export]
    #[allow(non_upper_case_globals)]
    const Universe: UniverseType = UniverseType;
}
