use std::{fmt::Display, ops::Add, str::FromStr};

use serde::{Deserialize, Serialize};

use crate::{
    error::{Context, CustomError},
    formula::MolecularFormula,
};

/// All possible neutral losses
#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Debug, Serialize, Deserialize, Hash)]
pub enum NeutralLoss {
    /// Gain of a specific formula
    Gain(MolecularFormula),
    /// Loss of a specific formula
    Loss(MolecularFormula),
}

impl NeutralLoss {
    /// Generate a nice HTML notation for this `NeutralLoss`
    pub fn hill_notation_html(&self) -> String {
        match self {
            Self::Loss(c) => format!("-{}", c.hill_notation_html()),
            Self::Gain(c) => format!("+{}", c.hill_notation_html()),
        }
    }
}

impl FromStr for NeutralLoss {
    type Err = CustomError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        if let Some(c) = s.chars().next() {
            match c {
                '+' => Ok(Self::Gain(MolecularFormula::from_pro_forma(&s[1..])?)),
                '-' => Ok(Self::Loss(MolecularFormula::from_pro_forma(&s[1..])?)),
                _ => Err(CustomError::error(
                    "Invalid neutral loss",
                    "A neutral loss can only start with '+' or '-'",
                    Context::line(0, s, 0, 1),
                )),
            }
        } else {
            Err(CustomError::error(
                "Invalid neutral loss",
                "A neutral loss cannot be an empty string",
                Context::None,
            ))
        }
    }
}

impl Display for NeutralLoss {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}",
            match self {
                Self::Loss(c) => format!("-{c}"),
                Self::Gain(c) => format!("+{c}"),
            }
        )
    }
}

impl std::ops::Add<&NeutralLoss> for &MolecularFormula {
    type Output = MolecularFormula;
    fn add(self, rhs: &NeutralLoss) -> Self::Output {
        match rhs {
            NeutralLoss::Gain(mol) => self + mol,
            NeutralLoss::Loss(mol) => self - mol,
        }
    }
}

impl_binop_ref_cases!(impl Add, add for MolecularFormula, NeutralLoss, MolecularFormula);
