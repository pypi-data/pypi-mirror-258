use pyo3::prelude::*;
use serde_json::Value;
use tokio_stream::{Stream, StreamExt};
use regex::Regex;
use pyo3::types::{PyDict, PyList};
use pyo3::Python;

pub struct InvokeParser {
    buffer: String,
    regex: Regex,
    pub parsed_data: Vec<ParsedInvokeData>,
}

pub struct ParsedInvokeData {
    pub tool: String,
    pub action: String,
    pub parameters: serde_json::Value, 
}


impl InvokeParser {
    pub fn new() -> Self {
        InvokeParser {
            buffer: String::new(),
            regex: Regex::new(r#"<invoke tool="(.*?)" action="(.*?)" parameters=(.*?)/>"#).unwrap(),
            parsed_data: Vec::new(),
        }
    }

    pub async fn parse_stream<S>(&mut self, mut stream: S)
    where
        S: Stream<Item = String> + Unpin,
    {
        while let Some(chunk) = stream.next().await {
            self.buffer.push_str(&chunk);

            while let Some(caps) = self.regex.captures(&self.buffer) {
                let tool = caps.get(1).map_or("", |m| m.as_str());
                let action = caps.get(2).map_or("", |m| m.as_str());
                let params_str = caps.get(3).map_or("{}", |m| m.as_str()); 
                let params: Value = serde_json::from_str(params_str)
                    .unwrap_or_else(|_| Value::Null);

                let invoke_data = ParsedInvokeData {
                    tool: tool.to_string(), 
                    action: action.to_string(),
                    parameters: params,
                };

                self.parsed_data.push(invoke_data);

                let match_end = caps.get(0).unwrap().end();
                self.buffer = self.buffer[match_end..].to_string();
            }
        }
    }

    pub fn parse(&mut self, msg: String) {
        self.buffer.push_str(&msg);

        while let Some(caps) = self.regex.captures(&self.buffer) {
            let tool = caps.get(1).map_or("", |m| m.as_str()).to_string();
            let action = caps.get(2).map_or("", |m| m.as_str()).to_string();
            let params_str = caps.get(3).map_or("{}", |m| m.as_str());
            let params: Value = serde_json::from_str(params_str)
                .unwrap_or_else(|_| Value::Null);

            let invoke_data = ParsedInvokeData {
                tool,
                action,
                parameters: params,
            };

            self.parsed_data.push(invoke_data);

            let match_end = caps.get(0).unwrap().end();
            self.buffer = self.buffer[match_end..].to_string();
        }
    }

    pub fn clear_buffer(&mut self) {
        self.buffer.clear();
    }
}


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
fn agentscript_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Parser>()?;
    m.add_class::<InvokeData>()?;
    Ok(())
}


#[tokio::test]
async fn parses_nested_parameter_object() {
    let input_stream = tokio_stream::iter(vec![
        String::from("<invoke tool=\"Translator\" action=\"translate\" parameters={\"text\": \"Hello\", \"options\": {\"from\": \"en\", \"to\": \"es\"}} />") 
    ]);

    let mut parser = InvokeParser::new();
    parser.parse_stream(input_stream).await;

    for data in &parser.parsed_data {
        println!("Tool: {}, Action: {} Params: {}", data.tool, data.action, data.parameters);
    }

    assert_eq!(parser.parsed_data.len(), 1); 
    let invoke_data = &parser.parsed_data[0];

    assert_eq!(invoke_data.tool, "Translator");
    assert_eq!(invoke_data.action, "translate");

    // Access nested parameters
    assert_eq!(invoke_data.parameters["text"].as_str(), Some("Hello")); 
    assert_eq!(invoke_data.parameters["options"]["from"].as_str(), Some("en"));
    assert_eq!(invoke_data.parameters["options"]["to"].as_str(), Some("es"));
}
