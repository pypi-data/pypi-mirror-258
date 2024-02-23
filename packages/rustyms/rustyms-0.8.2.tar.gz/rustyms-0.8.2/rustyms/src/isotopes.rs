use crate::{element::Element, system::da, system::Mass, MolecularFormula};
use probability::distribution::{Binomial, Discrete};
use std::collections::HashMap;

impl MolecularFormula {
    #[allow(clippy::fn_params_excessive_bools, clippy::missing_panics_doc)]
    fn isotopic_distribution(
        &self,
        threshold: f64,
        use_h: bool,
        use_c: bool,
        use_n: bool,
        use_o: bool,
    ) -> Vec<(Self, f64, String)> {
        let h = Element::H.isotopes();
        let c = Element::C.isotopes();
        let n = Element::N.isotopes();
        let o = Element::O.isotopes();
        let additional_mass: Self = self
            .elements()
            .iter()
            .filter(|i| {
                i.1.is_none()
                    && (i.0 != Element::H
                        && i.0 != Element::C
                        && i.0 != Element::N
                        && i.0 != Element::O)
            })
            .fold(Self::default(), |mut acc, s| {
                assert!(acc.add(*s));
                acc
            });
        let mut isotopes = Vec::new();
        let present_h = self
            .elements()
            .iter()
            .find(|i| i.0 == Element::H && i.1.is_none())
            .map_or(0, |i| i.2);
        let present_c = self
            .elements()
            .iter()
            .find(|i| i.0 == Element::C && i.1.is_none())
            .map_or(0, |i| i.2);
        let present_n = self
            .elements()
            .iter()
            .find(|i| i.0 == Element::N && i.1.is_none())
            .map_or(0, |i| i.2);
        let present_o = self
            .elements()
            .iter()
            .find(|i| i.0 == Element::O && i.1.is_none())
            .map_or(0, |i| i.2);
        let max_h = if use_h { present_h } else { 0 };
        let max_c = if use_c { present_c } else { 0 };
        let max_n = if use_n { present_n } else { 0 };
        let max_o = if use_o { present_o } else { 0 };

        for num_h in 0..=max_h {
            let h_chance = binom(num_h, max_h, h[1].2);
            if h_chance < threshold {
                continue;
            }
            for num_c in 0..=max_c {
                let c_chance = binom(num_c, max_c, c[1].2);
                if h_chance * c_chance < threshold {
                    continue;
                }
                for num_n in 0..=max_n {
                    let n_chance = binom(num_n, max_n, n[1].2);
                    if h_chance * c_chance * n_chance < threshold {
                        continue;
                    }
                    for num_o_1 in 0..=max_o {
                        let o_1_chance = binom(num_o_1, max_o, o[1].2);
                        if h_chance * c_chance * n_chance * o_1_chance < threshold {
                            continue;
                        }
                        for num_o_2 in 0..=max_o - num_o_1 {
                            let o_2_chance = binom(num_o_2, max_o, o[2].2);
                            let chance = h_chance * c_chance * n_chance * o_1_chance * o_2_chance;
                            if chance < threshold {
                                continue;
                            }
                            // Do the calc
                            let formula = Self::new(&[
                                (Element::H, Some(1), present_h - num_h),
                                (Element::H, Some(2), num_h),
                                (Element::C, Some(12), present_c - num_c),
                                (Element::C, Some(13), num_c),
                                (Element::N, Some(14), present_n - num_n),
                                (Element::N, Some(15), num_n),
                                (Element::O, Some(16), present_o - num_o_1 - num_o_2),
                                (Element::O, Some(17), num_o_1),
                                (Element::O, Some(18), num_o_2),
                            ]);
                            isotopes.push((
                                &formula.unwrap() + &additional_mass,
                                chance,
                                format!("[2H{num_h}][13C{num_c}][15N{num_n}][17O{num_o_1}][18O{num_o_2}]"),
                            ));
                        }
                    }
                }
            }
        }
        isotopes.sort_unstable_by(|a, b| b.1.total_cmp(&a.1));
        isotopes
    }
}

fn combined_pattern(
    isotopes: &[(MolecularFormula, f64, String)],
) -> Vec<(Mass, f64, usize, String)> {
    let mut combined: Vec<(Mass, f64, usize, String)> = Vec::new();

    for isotope in isotopes {
        let isotope_mass = isotope.0.monoisotopic_mass().value.round();
        if let Some(entry) = combined
            .iter_mut()
            .find(|i| (i.0.value - isotope_mass).abs() < f64::EPSILON)
        {
            entry.1 += isotope.1;
            entry.2 += 1;
            entry.3 += &format!(",{}", isotope.2);
        } else {
            combined.push((da(isotope_mass), isotope.1, 1, isotope.2.clone()));
        }
    }
    combined.sort_unstable_by(|a, b| b.1.total_cmp(&a.1));
    combined
}

fn binom(tries: i16, total: i16, p: f64) -> f64 {
    Binomial::new(total as usize, p).mass(tries as usize)
}

fn memoized_f64_factorial(num: u16, cache: &mut HashMap<u16, f64>) -> f64 {
    *cache
        .entry(num)
        .or_insert_with(|| stupid_f64_factorial(num))
}

fn stupid_f64_factorial(num: u16) -> f64 {
    (2..=num).fold(1.0, |acc, i| acc * f64::from(i))
}

#[cfg(test)]
#[allow(clippy::missing_panics_doc)]
mod tests {
    use super::*;
    use std::{
        fs::File,
        io::{BufWriter, Write},
    };

    //#[test]
    fn simple_isotope_pattern() {
        // EVQLVESGGGLVQPGG start 16 AA of herceptin
        let peptide = MolecularFormula::new(&[
            (Element::H, None, 108),
            (Element::C, None, 65),
            (Element::N, None, 18),
            (Element::O, None, 24),
        ])
        .unwrap();
        let isotopes = peptide.isotopic_distribution(1e-6, true, true, true, true);
        save_combinations(
            &combined_pattern(&isotopes),
            "target/peptide_combined_all.tsv",
        );
        save_combinations(
            &combined_pattern(&peptide.isotopic_distribution(1e-5, true, false, false, false)),
            "target/peptide_combined_only_H.tsv",
        );
        save_combinations(
            &combined_pattern(&peptide.isotopic_distribution(1e-5, false, true, false, false)),
            "target/peptide_combined_only_C.tsv",
        );
        save_combinations(
            &combined_pattern(&peptide.isotopic_distribution(1e-5, false, false, true, false)),
            "target/peptide_combined_only_N.tsv",
        );
        save_combinations(
            &combined_pattern(&peptide.isotopic_distribution(1e-5, false, false, false, true)),
            "target/peptide_combined_only_O.tsv",
        );
        println!(
            "MonoIsotopic mass: {} average mass: {}",
            peptide.monoisotopic_mass().value,
            peptide.average_weight().value
        );
    }

    //#[test]
    fn sars_cov_2_spike_isotope_pattern() {
        // MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFSNVTWFHAIHVSGTNGTKRFDNPVLPFNDGVYFASTEKSNIIRGWIFGTTLDSKTQSLLIVNNATNVVIKVCEFQFCNDPFLGVYYHKNNKSWMESEFRVYSSANNCTFEYVSQPFLMDLEGKQGNFKNLREFVFKNIDGYFKIYSKHTPINLVRDLPQGFSALEPLVDLPIGINITRFQTLLALHRSYLTPGDSSSGWTAGAAAYYVGYLQPRTFLLKYNENGTITDAVDCALDPLSETKCTLKSFTVEKGIYQTSNFRVQPTESIVRFPNITNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPCNGVEGFNCYFPLQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVNFNFNGLTGTGVLTESNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCSFGGVSVITPGTNTSNQVAVLYQDVNCTEVPVAIHADQLTPTWRVYSTGSNVFQTRAGCLIGAEHVNNSYECDIPIGAGICASYQTQTNSPRRARSVASQSIIAYTMSLGAENSVAYSNNSIAIPTNFTISVTTEILPVSMTKTSVDCTMYICGDSTECSNLLLQYGSFCTQLNRALTGIAVEQDKNTQEVFAQVKQIYKTPPIKDFGGFNFSQILPDPSKPSKRSFIEDLLFNKVTLADAGFIKQYGDCLGDIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPAICHDGKAHFPREGVFVSNGTHWFVTQRNFYEPQIITTDNTFVSGNCDVVIGIVNNTVYDPLQPELDSFKEELDKYFKNHTSPDVDLGDISGINASVVNIQKEIDRLNEVAKNLNESLIDLQELGKYEQYIKWPWYIWLGFIAGLIAIVMVTIMLCCMTSCCSCLKGCCSCGSCCKFDEDDSEPVLKGVKLHYT
        let spike = MolecularFormula::new(&[
            (Element::H, None, 9770),
            (Element::C, None, 6336),
            (Element::N, None, 1656),
            (Element::O, None, 1894),
            (Element::S, None, 54),
        ])
        .unwrap();
        let isotopes = spike.isotopic_distribution(1e-5, true, true, true, true);
        let file_handler = File::create("target/spike_isotopes.tsv").unwrap();
        let mut writer = BufWriter::new(file_handler);
        writeln!(writer, "Name\tMass\tProbability").unwrap();
        for isotope in &isotopes {
            writeln!(writer, "{}\t{}\t{}", isotope.2, isotope.0, isotope.1).unwrap();
        }
        let combined = combined_pattern(&isotopes);
        save_combinations(&combined, "target/spike_combined_all.tsv");
        save_combinations(
            &combined_pattern(&spike.isotopic_distribution(1e-5, true, false, false, false)),
            "target/spike_combined_only_H.tsv",
        );
        save_combinations(
            &combined_pattern(&spike.isotopic_distribution(1e-5, false, true, false, false)),
            "target/spike_combined_only_C.tsv",
        );
        save_combinations(
            &combined_pattern(&spike.isotopic_distribution(1e-5, false, false, true, false)),
            "target/spike_combined_only_N.tsv",
        );
        save_combinations(
            &combined_pattern(&spike.isotopic_distribution(1e-5, false, false, false, true)),
            "target/spike_combined_only_O.tsv",
        );
        println!(
            "MonoIsotopic mass: {} average mass: {}",
            spike.monoisotopic_mass().value,
            spike.average_weight().value
        );
    }

    fn save_combinations(data: &[(Mass, f64, usize, String)], name: &str) {
        let file_handler = File::create(name).unwrap();
        let mut writer = BufWriter::new(file_handler);
        writeln!(writer, "Name\tMass\tProbability\tTotalIsotopes").unwrap();
        for isotope in data {
            writeln!(
                writer,
                "{}\t{}\t{}\t{}",
                isotope.3, isotope.0.value, isotope.1, isotope.2
            )
            .unwrap();
        }
    }

    //#[test]
    fn herceptin_v_heavy_isotope_pattern() {
        // EVQLVESGGGLVQPGGSLRLSCAASGFNIKDTYIHWVRQAPGKGLEWVARIYPTNGYTRYADSVKGRFTISADTSKNTAYLQMNSLRAEDTAVYYCSRWGGDGFYAMDYWGQGTLVTVSSASTK
        let herceptin = MolecularFormula::new(&[
            (Element::H, None, 915),
            (Element::C, None, 602),
            (Element::N, None, 165),
            (Element::O, None, 185),
            (Element::S, None, 4),
        ])
        .unwrap();
        let isotopes = herceptin.isotopic_distribution(1e-5, true, true, true, true);
        let file_handler = File::create("target/herceptin_isotopes.tsv").unwrap();
        let mut writer = BufWriter::new(file_handler);
        writeln!(writer, "Name\tMass\tProbability").unwrap();
        for isotope in &isotopes {
            writeln!(writer, "{}\t{}\t{}", isotope.2, isotope.0, isotope.1).unwrap();
        }
        let combined = combined_pattern(&isotopes);
        save_combinations(&combined, "target/herceptin_combined_all.tsv");
        save_combinations(
            &combined_pattern(&herceptin.isotopic_distribution(1e-5, true, false, false, false)),
            "target/herceptin_combined_only_H.tsv",
        );
        save_combinations(
            &combined_pattern(&herceptin.isotopic_distribution(1e-5, false, true, false, false)),
            "target/herceptin_combined_only_C.tsv",
        );
        save_combinations(
            &combined_pattern(&herceptin.isotopic_distribution(1e-5, false, false, true, false)),
            "target/herceptin_combined_only_N.tsv",
        );
        save_combinations(
            &combined_pattern(&herceptin.isotopic_distribution(1e-5, false, false, false, true)),
            "target/herceptin_combined_only_O.tsv",
        );
        println!(
            "MonoIsotopic mass: {} average mass: {}",
            herceptin.monoisotopic_mass().value,
            herceptin.average_weight().value
        );
    }
}
