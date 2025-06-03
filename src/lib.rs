use pyo3::basic::CompareOp;
use pyo3::exceptions::{PyOverflowError, PyTypeError};
use pyo3::prelude::*;
use pyo3::types::PyFrozenSet;

/// The `hash(frozenset({}))` value, confirmed to be system-independent by inspecting the algorithm
const HASH_EMPTY: isize = 133_146_708_735_736;
const HASH_UNIVERSE: isize = (usize::MAX ^ HASH_EMPTY as usize) as isize;

fn is_set(other: &Bound<'_, PyAny>) -> PyResult<bool> {
    other.is_instance(&PyModule::import(other.py(), "typing")?.getattr("AbstractSet")?)
}

#[pymodule]
mod _core {
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

    #[pyclass(frozen, module = "symset")]
    pub struct EmptyType;

    #[pymethods]
    impl EmptyType {
        #[staticmethod]
        fn get(py: Python<'_>) -> Bound<'_, Self> {
            Empty.into_pyobject(py).unwrap()
        }

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
            if is_set(&other)? {
                Ok(slf.into_pyobject(other.py())?)
            } else {
                Err(PyTypeError::new_err("not a set"))
            }
        }

        fn __or__<'py>(
            slf: Bound<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<Bound<'py, PyAny>> {
            if is_set(&other)? {
                Ok(if other.is_truthy()? {
                    other
                } else {
                    slf.into_any()
                })
            } else {
                Err(PyTypeError::new_err("not a set"))
            }
        }

        fn __xor__<'py>(
            slf: Bound<'py, Self>,
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
            slf: Bound<'py, Self>,
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

        #[getter(C)]
        fn complement<'py>(&self, py: Python<'py>) -> Bound<'py, UniverseType> {
            UniverseType::get(py)
        }
    }

    #[pyclass(frozen, module = "symset")]
    pub struct UniverseType;

    #[pymethods]
    impl UniverseType {
        #[staticmethod]
        fn get(py: Python<'_>) -> Bound<'_, Self> {
            Universe.into_pyobject(py).unwrap()
        }

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

        fn __richcmp__<'py>(
            slf: Bound<'py, Self>,
            other: Bound<'py, PyAny>,
            op: CompareOp,
        ) -> PyResult<bool> {
            let universe_py = slf.get_type();
            let eq = other.is_instance(&universe_py)?;

            fn set_or_err(other_: &Bound<'_, PyAny>, result: bool) -> PyResult<bool> {
                if is_set(other_)? {
                    Ok(result)
                } else {
                    Err(PyTypeError::new_err("not a set"))
                }
            }

            match op {
                CompareOp::Eq => Ok(eq),
                CompareOp::Ne => Ok(!eq),
                CompareOp::Le => set_or_err(&other, eq),
                CompareOp::Gt => set_or_err(&other, !eq),
                CompareOp::Lt => set_or_err(&other, false),
                CompareOp::Ge => set_or_err(&other, true),
            }
        }

        fn __and__<'py>(&self, other: Bound<'py, PyAny>) -> PyResult<Bound<'py, PyAny>> {
            if is_set(&other)? {
                Ok(other)
            } else {
                Err(PyTypeError::new_err("not a set"))
            }
        }

        fn __or__<'py>(
            slf: PyRef<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<PyRef<'py, Self>> {
            if is_set(&other)? {
                Ok(slf)
            } else {
                Err(PyTypeError::new_err("not a set"))
            }
        }

        fn __xor__<'py>(
            slf: Bound<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<Bound<'py, PyAny>> {
            if !is_set(&other)? {
                return Err(PyTypeError::new_err("not a set"));
            }

            match other.len() {
                Err(_) => Ok(EmptyType::get(other.py()).into_any()),
                Ok(0) => Ok(slf.into_any()),
                Ok(_) => todo!("finite non-empty set complement"),
            }
        }

        fn __sub__<'py>(
            slf: Bound<'py, Self>,
            other: Bound<'py, PyAny>,
        ) -> PyResult<Bound<'py, PyAny>> {
            Self::__xor__(slf, other)
        }

        fn __rsub__<'py>(&self, other: Bound<'py, PyAny>) -> PyResult<Bound<'py, EmptyType>> {
            if is_set(&other)? {
                Ok(EmptyType::get(other.py()))
            } else {
                Err(PyTypeError::new_err("not a set"))
            }
        }

        fn isdisjoint(&self, other: Bound<'_, PyAny>) -> PyResult<bool> {
            if is_set(&other)? {
                other.is_empty().or_else(|_| Ok(false))
            } else {
                Err(PyTypeError::new_err("not iterable"))
            }
        }

        #[getter(C)]
        fn complement<'py>(&self, py: Python<'py>) -> Bound<'py, EmptyType> {
            EmptyType::get(py)
        }
    }

    #[pymodule_export]
    #[allow(non_upper_case_globals)]
    const Empty: EmptyType = EmptyType;

    #[pymodule_export]
    #[allow(non_upper_case_globals)]
    const Universe: UniverseType = UniverseType;
}
