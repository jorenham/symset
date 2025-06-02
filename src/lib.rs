use pyo3::basic::CompareOp;
use pyo3::exceptions::PyTypeError;
use pyo3::types::PyFrozenSet;
use pyo3::{PyClass, prelude::*};

fn require_set<'py, T: PyClass, R>(
    slf: PyRef<'py, T>,
    other: Bound<'py, PyAny>,
    to_result: fn(PyRef<'py, T>, Bound<'py, PyAny>) -> PyResult<Bound<'py, R>>,
) -> PyResult<Bound<'py, R>> {
    let py = other.py();
    let abstract_set_type = PyModule::import(py, "typing")?.getattr("AbstractSet")?;
    if other.is_instance(&abstract_set_type)? {
        to_result(slf, other)
    } else {
        let error_msg = format!(
            "unsupported operand type: 'EmptySet' and '{}'",
            other.get_type().name()?
        );
        Err(PyTypeError::new_err(error_msg))
    }
}

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
    pub struct EmptySetType;

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

        /// Match the hash algorithm used by the builtin- frozenset type, for n=0
        /// https://github.com/python/cpython/blob/v3.13.3/Lib/_collections_abc.py#L669-L700
        fn _hash(&self) -> isize {
            static MASK: usize = usize::MAX;
            static H1: usize = 1_927_868_237 & MASK;
            static H2: usize = (H1 >> 11) ^ (H1 >> 25) ^ H1;
            static H3: usize = (H2 * 69_069 + 907_133_923) & MASK;
            static H4: isize = H3 as isize;
            static H5: isize = if H4 == -1 { 590_923_713 } else { H4 };
            H5
        }

        fn __hash__(&self) -> isize {
            self._hash()
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

        // TODO: implement the following `typing.AbstractSet` methods
        // isdisjoint: (Iterable[Any]) -> bool
    }

    #[pymodule_export]
    const EMPTY_SET: EmptySetType = EmptySetType;
}
