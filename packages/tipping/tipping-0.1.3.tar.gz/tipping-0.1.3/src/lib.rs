use std::collections::{HashMap, HashSet};

use pyo3::prelude::*;
use fancy_regex::Regex;


#[pyclass]
#[derive(Debug, Clone)]
struct TokenFilter {
    alphabetic: bool,
    numeric: bool,
    impure: bool,
}

#[pymethods]
impl TokenFilter {
    #[new]
    fn new(alphabetic: bool, numeric: bool, impure: bool) -> Self {
        Self {
            alphabetic,
            numeric,
            impure,
        }
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct Computations {
    template: bool,
    mask: bool,
}

#[pymethods]
impl Computations {
    #[new]
    fn new(template: bool, mask: bool) -> Self {
        Self { mask, template }
    }
}

type MessageClusters = Vec<Option<usize>>;
type ParameterMasks = Vec<String>;
type ClusterTemplates = Vec<HashSet<String>>;

#[pyfunction]
fn token_independency_clusters(
    messages: Vec<String>,
    threshold: f32,
    special_whites: Vec<String>,
    special_blacks: Vec<String>,
    symbols: String,
    filter: TokenFilter,
    comps: Computations,
) -> PyResult<(MessageClusters, ParameterMasks, ClusterTemplates)> {
    let special_blacks = special_blacks
        .into_iter()
        .map(compile_regex)
        .collect();
    let special_whites = special_whites
        .into_iter()
        .map(compile_regex)
        .collect();
    let symbols = symbols.chars().collect();

    let parser = tipping_rs::Parser::default()
        .with_threshold(threshold)
        .with_special_whites(special_whites)
        .with_special_blacks(special_blacks)
        .with_symbols(symbols)
        .with_filter_alphabetic(filter.alphabetic)
        .with_filter_numeric(filter.numeric)
        .with_filter_impure(filter.impure);
    Ok(match comps {
        Computations {
            template: false,
            mask: false,
        } => {
            let clusters = parser.parse(&messages);
            (clusters, Default::default(), Default::default())
        }
        Computations {
            template: false,
            mask: true,
        } => {
            let (clusters, masks) = parser.compute_masks().parse(&messages);
            (clusters, one_to_one_masks(&messages, masks), Default::default())
        }
        Computations {
            template: true,
            mask: false,
        } => {
            let (clusters, templates) = parser.compute_templates().parse(&messages);
            (clusters, Default::default(), templates)
        }

        Computations {
            template: true,
            mask: true,
        } => {
            let (clusters, templates, masks) =
                parser.compute_masks().compute_templates().parse(&messages);
                (clusters, one_to_one_masks(&messages, masks), templates)
        }
    })
}

/// A Python module implemented in Rust.
#[pymodule]
#[pyo3(name = "_lib_tipping")]
fn tipping(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(token_independency_clusters, m)?)?;
    m.add_class::<TokenFilter>()?;
    m.add_class::<Computations>()?;
    Ok(())
}

fn one_to_one_masks(messages: &[String], masks: HashMap<String, String>) -> Vec<String> {
    messages
        .iter()
        .map(|msg| masks.get(msg).map(ToOwned::to_owned).unwrap_or("0".repeat(msg.len())))
        .collect::<Vec<_>>()
}

fn compile_regex(re: impl AsRef<str>) -> Regex {
    match Regex::new(re.as_ref()) {
        Ok(regex) => regex,
        Err(err) => panic!("Error: {}, Regex: {}", err, re.as_ref()),
    }
}