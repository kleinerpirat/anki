// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

use super::{NoteFieldConfig, NoteFieldProto};
use crate::{
    backend_proto::UInt32,
    error::{AnkiError, Result},
};

#[derive(Debug, PartialEq, Clone)]
pub struct NoteField {
    pub ord: Option<u32>,
    pub name: String,
    pub config: NoteFieldConfig,
}

impl From<NoteField> for NoteFieldProto {
    fn from(f: NoteField) -> Self {
        NoteFieldProto {
            ord: f.ord.map(|n| UInt32 { val: n }),
            name: f.name,
            config: Some(f.config),
        }
    }
}

impl From<NoteFieldProto> for NoteField {
    fn from(f: NoteFieldProto) -> Self {
        NoteField {
            ord: f.ord.map(|n| n.val),
            name: f.name,
            config: f.config.unwrap_or_default(),
        }
    }
}

impl NoteField {
    pub fn new(name: impl Into<String>) -> Self {
        NoteField {
            ord: None,
            name: name.into(),
            config: NoteFieldConfig {
                sticky: false,
                rtl: false,
                font_name: "Arial".into(),
                font_size: 20,
                other: vec![],
            },
        }
    }

    /// Fix the name of the field if it's valid. Otherwise explain why it's not.
    pub(crate) fn fix_name(&mut self) -> Result<()> {
        if self.name.is_empty() {
            return Err(AnkiError::invalid_input("Empty field name"));
        }
        let bad_chars = |c| c == ':' || c == '{' || c == '}' || c == '"';
        if self.name.contains(bad_chars) {
            self.name = self.name.replace(bad_chars, "");
        }
        // and leading/trailing whitespace and special chars
        let bad_start_chars = |c: char| c == '#' || c == '/' || c == '^' || c.is_whitespace();
        let trimmed = self.name.trim().trim_start_matches(bad_start_chars);
        if trimmed.is_empty() {
            return Err(AnkiError::invalid_input(
                "Field name: ".to_owned() + &self.name,
            ));
        }
        if trimmed.len() != self.name.len() {
            self.name = trimmed.into();
        }
        Ok(())
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn name() {
        let mut field = NoteField::new("  # /^ t:e{s\"t} field name #/^  ");
        assert_eq!(field.fix_name(), Ok(()));
        assert_eq!(&field.name, "test field name #/^");
    }
}
