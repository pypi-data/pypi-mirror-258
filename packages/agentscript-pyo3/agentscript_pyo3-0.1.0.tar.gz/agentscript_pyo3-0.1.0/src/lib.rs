use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use pyo3::Python;
use serde_json::Value;
use agentscript::InvokeParser;


#[pyclass]
struct Parser {
    parser: InvokeParser,
}

#[pymethods]
impl Parser {
    #[new]
    fn new() -> Self {
        Parser {
            parser: InvokeParser::new(),
        }
    }

    fn parse(&mut self, msg: String) {
        self.parser.parse(msg);
    }

    // Optionally expose a method to retrieve parsed data
    fn get_parsed_data(&self) -> PyResult<Vec<Py<InvokeData>>> {
        Python::with_gil(|py| {
            let data = self.parser.parsed_data.iter().map(|d| {
                Py::new(py, InvokeData {
                    tool: d.tool.clone(),
                    action: d.action.clone(),
                    parameters: d.parameters.clone(),
                }).unwrap()
            }).collect();
            Ok(data)
        })
    }
}


#[pyclass]
struct InvokeData {
    #[pyo3(get)]
    tool: String,
    #[pyo3(get)]
    action: String,
    parameters: Value,
}

#[pymethods]
impl InvokeData {
    fn get_parameters(&self, py: Python) -> PyObject {
        serde_json_value_to_pyobject(py, &self.parameters)
    }
}

fn serde_json_value_to_pyobject(py: Python, value: &Value) -> PyObject {
    match value {
        Value::Null => py.None(),
        Value::Bool(b) => b.into_py(py),
        Value::Number(n) => {
            if let Some(i) = n.as_i64() {
                i.into_py(py)
            } else if let Some(f) = n.as_f64() {
                f.into_py(py)
            } else {
                py.None()
            }
        },
        Value::String(s) => s.into_py(py),
        Value::Array(arr) => {
            let py_list = PyList::empty(py);
            for item in arr {
                let py_item = serde_json_value_to_pyobject(py, item);
                py_list.append(py_item).unwrap();
            }
            py_list.into_py(py)
        },
        Value::Object(obj) => {
            let py_dict = PyDict::new(py);
            for (key, value) in obj {
                let py_value = serde_json_value_to_pyobject(py, value);
                py_dict.set_item(key, py_value).unwrap();
            }
            py_dict.into_py(py)
        },
    }
}


#[pymodule]
fn agentscript_pyo3(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Parser>()?;
    m.add_class::<InvokeData>()?;
    Ok(())
}
