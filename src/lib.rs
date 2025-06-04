use pyo3::IntoPyObjectExt;
use pyo3::basic::CompareOp;
use pyo3::exceptions::{PyNotImplementedError, PyOverflowError, PyTypeError};
use pyo3::prelude::*;
use pyo3::sync::GILOnceCell;
use pyo3::types::{PyFrozenSet, PyType};

/// The `hash(frozenset({}))` value, confirmed to be system-independent by inspecting the algorithm
const HASH_EMPTY: isize = 133_146_708_735_736;
const HASH_UNIVERSE: isize = (usize::MAX ^ HASH_EMPTY as usize) as isize;

/// mimics `pyo3::types::sequence::get_sequence_abc()`
fn get_set_abc(py: Python<'_>) -> PyResult<&Bound<'_, PyType>> {
    static SEQUENCE_ABC: GILOnceCell<Py<PyType>> = GILOnceCell::new();

    SEQUENCE_ABC.import(py, "collections.abc", "Set")
}

#[inline]
fn is_set(other: &Bound<'_, PyAny>) -> PyResult<bool> {
    other.is_instance(get_set_abc(other.py())?)
}

type PyEmpty = Py<_core::EmptyType>;
type PyUniverse = Py<_core::UniverseType>;

#[pymodule]
mod _core {
    use pyo3::PyTypeInfo;

    use super::*;

    #[pyclass(frozen, module = "symset")]
    pub struct EmptyType;

    #[pymethods]
    impl EmptyType {
        #[staticmethod]
        fn get(py: Python<'_>) -> Py<Self> {
            static CELL: GILOnceCell<PyEmpty> = GILOnceCell::new();

            CELL.get_or_try_init(py, || Py::new(py, Self))
                .unwrap()
                .clone_ref(py)
        }

        #[getter(C)]
        fn complement(slf: PyRef<'_, Self>) -> PyUniverse {
            UniverseType::get(slf.py())
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

        fn __contains__(&self, _item: &Bound<'_, PyAny>) -> bool {
            false
        }

        fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
            slf
        }

        fn __next__(&self) -> Option<PyObject> {
            None
        }

        fn _hash(&self) -> isize {
            HASH_EMPTY
        }

        fn __hash__(&self) -> isize {
            HASH_EMPTY
        }

        fn __richcmp__(&self, other: &Bound<'_, PyAny>, op: CompareOp) -> PyResult<bool> {
            PyFrozenSet::empty(other.py())?
                .rich_compare(other, op)
                .and_then(|any| any.is_truthy())
        }

        fn __and__(&self, other: &Bound<'_, PyAny>) -> PyResult<PyEmpty> {
            if is_set(other)? {
                Ok(EmptyType::get(other.py()))
            } else {
                Err(PyTypeError::new_err("not a set"))
            }
        }

        fn __sub__(&self, other: &Bound<'_, PyAny>) -> PyResult<PyEmpty> {
            self.__and__(other)
        }

        fn __or__<'py>(&self, other: Bound<'py, PyAny>) -> PyResult<Bound<'py, PyAny>> {
            if is_set(&other)? {
                if other.is_truthy()? {
                    Ok(other)
                } else {
                    EmptyType::get(other.py()).into_bound_py_any(other.py())
                }
            } else {
                Err(PyTypeError::new_err("not a set"))
            }
        }

        fn __xor__<'py>(&self, other: Bound<'py, PyAny>) -> PyResult<Bound<'py, PyAny>> {
            self.__or__(other)
        }

        fn __rsub__<'py>(&self, other: Bound<'py, PyAny>) -> PyResult<Bound<'py, PyAny>> {
            self.__or__(other)
        }

        fn isdisjoint(&self, other: &Bound<'_, PyAny>) -> PyResult<bool> {
            if other.try_iter().is_ok() || is_set(other)? {
                Ok(true)
            } else {
                Err(PyTypeError::new_err("not iterable"))
            }
        }
    }

    #[pyclass(frozen, module = "symset")]
    pub struct UniverseType;

    #[pymethods]
    impl UniverseType {
        #[staticmethod]
        fn get(py: Python<'_>) -> Py<Self> {
            static CELL: GILOnceCell<PyUniverse> = GILOnceCell::new();

            CELL.get_or_try_init(py, || Py::new(py, Self))
                .unwrap()
                .clone_ref(py)
        }

        #[getter(C)]
        fn complement(slf: PyRef<'_, Self>) -> PyEmpty {
            EmptyType::get(slf.py())
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

        fn __iter__(&self) -> PyResult<PyObject> {
            Err(PyOverflowError::new_err("infinite set"))
        }

        fn __contains__(&self, _item: &Bound<'_, PyAny>) -> bool {
            true
        }

        fn _hash(&self) -> isize {
            HASH_UNIVERSE
        }

        fn __hash__(&self) -> isize {
            HASH_UNIVERSE
        }

        fn __richcmp__(&self, other: &Bound<'_, PyAny>, op: CompareOp) -> PyResult<bool> {
            let universe_type = UniverseType::get(other.py()).bind(other.py()).get_type();
            let eq = other.is_instance(&universe_type)?;

            fn set_or_err(other: &Bound<'_, PyAny>, result: bool) -> PyResult<bool> {
                if is_set(other)? {
                    Ok(result)
                } else {
                    Err(PyTypeError::new_err("not a set"))
                }
            }

            match op {
                CompareOp::Eq => Ok(eq),
                CompareOp::Ne => Ok(!eq),
                CompareOp::Le => set_or_err(other, eq),
                CompareOp::Gt => set_or_err(other, !eq),
                CompareOp::Lt => set_or_err(other, false),
                CompareOp::Ge => set_or_err(other, true),
            }
        }

        fn __and__<'py>(&self, other: Bound<'py, PyAny>) -> PyResult<Bound<'py, PyAny>> {
            if is_set(&other)? {
                if other.is_truthy()? {
                    Ok(other)
                } else {
                    // coerce set-like to EmptyType
                    EmptyType::get(other.py()).into_bound_py_any(other.py())
                }
            } else {
                Err(PyTypeError::new_err("not a set"))
            }
        }

        fn __or__(&self, other: &Bound<'_, PyAny>) -> PyResult<Py<Self>> {
            if is_set(other)? {
                Ok(UniverseType::get(other.py()))
            } else {
                Err(PyTypeError::new_err("not a set"))
            }
        }

        fn __xor__(&self, other: &Bound<'_, PyAny>) -> PyResult<PyObject> {
            if !is_set(other)? {
                return Err(PyTypeError::new_err("not a set"));
            }

            let py = other.py();
            match other.len() {
                Err(e) => {
                    // TODO: separate OverflowError
                    if e.get_type(py).is(PyType::new::<PyOverflowError>(py)) {
                        Ok(EmptyType::get(py).into_any())
                    } else {
                        Err(e)
                    }
                }
                Ok(0) => Ok(UniverseType::get(py).into_any()),
                Ok(_) => Err(PyNotImplementedError::new_err(
                    "non-empty finite set complement is not supported yet",
                )),
            }
        }

        fn __sub__(&self, other: &Bound<'_, PyAny>) -> PyResult<PyObject> {
            self.__xor__(other)
        }

        fn __rsub__(&self, other: &Bound<'_, PyAny>) -> PyResult<PyEmpty> {
            if is_set(other)? {
                Ok(EmptyType::get(other.py()))
            } else {
                Err(PyTypeError::new_err("not a set"))
            }
        }

        fn isdisjoint(&self, other: &Bound<'_, PyAny>) -> PyResult<bool> {
            if is_set(other)? {
                other.is_empty().or_else(|_| Ok(false))
            } else if other.try_iter().is_ok() {
                Err(PyNotImplementedError::new_err(
                    "Universe.isdisjoint() does not support non-set iterables yet",
                ))
            } else {
                Err(PyTypeError::new_err("not iterable"))
            }
        }
    }

    #[pymodule_init]
    fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
        let py = m.py();

        // Register `EmptyType` and `UniverseType` as subclasses of `collections.abc.Set`
        let abc_set = get_set_abc(py)?;
        abc_set.call_method1("register", (EmptyType::type_object(py),))?;
        abc_set.call_method1("register", (UniverseType::type_object(py),))?;

        // Singletons for Empty and Universe
        m.add("Empty", EmptyType::get(py))?;
        m.add("Universe", UniverseType::get(py))?;

        Ok(())
    }
}
