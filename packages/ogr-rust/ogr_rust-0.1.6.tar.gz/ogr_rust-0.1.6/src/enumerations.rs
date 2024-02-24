//! Functions for enumerating all of the potential golomb rulers

use std::collections::HashSet;
use std::vec;
use pyo3::prelude::*;

use thiserror::Error;

use crate::dist;
use crate::Ruler;
use crate::GInt;

#[derive(Error, Debug)]
pub enum GolombIterationError {
    #[error("The current golomb ruler index can't be contained in a u64")]
    IndexOverflow
}


/// Exhaustively enumerate all rulers up to length `max_length`
#[pyfunction]
#[pyo3(text_signature = "(max_length: usize)")]
pub fn enumerate_rulers(max_length: usize) -> Vec<GolombRuler> {
    let all_rulers: Vec<GolombRuler> = (2..max_length + 1).flat_map(|length| {
        RulerIterator::new(length)
    }).collect();

    all_rulers
}

#[pyfunction]
pub fn enumerate_rulers_with_length(length: usize) -> Vec<GolombRuler> {
    match length {
        0 => vec![GolombRuler::from_id(0)],
        1 => vec![GolombRuler::from_id(1)],
        _ => RulerIterator::new(length).collect()
    }
}

#[pyfunction]
pub fn enumerate_pruned_rulers(order: usize, length: usize) -> Vec<GolombRuler> {
    if order == 2 { return vec![GolombRuler::new(&[length as GInt])] }
    GolombRulerPrunedIterator::new(order, length).collect()
}

/// Get all rulers with `order` marks. They do not have to have the golomb property.
#[pyfunction]
pub fn enumerate_rulers_with_order(order: usize, length: usize) -> Vec<GolombRuler> {
    let rulers = enumerate_rulers(length);
    rulers.into_iter().filter(|r| r.order() == order).collect()
}

/// Print out every possible golomb ruler of order `order`
///
#[pyfunction]
#[pyo3(text_signature = "(order: int, max_length: ing)")]
pub fn enumerate_golomb_rulers(order: usize, max_length: usize) -> Vec<GolombRuler> {

    let all_rulers: Vec<GolombRuler> = (2..max_length + 1).flat_map(|length| {
        RulerIterator::new(length)
    }).collect();

    // all_rulers
    let filtered: Vec<GolombRuler> = all_rulers.into_iter().filter(|r| r.order() == order && r.is_golomb_ruler()).collect();
    // for ruler in filtered.clone().into_iter() {
    //     dbg!(ruler.length());
    // }

    filtered
}


#[pyfunction]
pub fn enumerate_golomb_rulers_with_length(order: usize, length: usize) -> Vec<GolombRuler> {
    let all_rulers: Vec<GolombRuler> = RulerIterator::new(length).collect();
    all_rulers.into_iter().filter(|r| r.order() == order && r.is_golomb_ruler() && r.length() == length as GInt).collect()
}

#[pyfunction]
pub fn enumerate_golomb_rulers_pruned(order: usize, max_length: usize) -> Vec<GolombRuler> {

    let all_rulers: Vec<GolombRuler> = (2..max_length + 1).flat_map(|length| {
        GolombRulerPrunedIterator::new(order, length)
    }).collect();

    // all_rulers
    // let filtered: Vec<GolombRuler> = all_rulers.into_iter().filter(|r| r.is_golomb_ruler()).collect();
    // for ruler in filtered.clone().into_iter() {
    //     dbg!(ruler.length());
    // }

    // filtered
    all_rulers.iter().filter(|g| g.is_golomb_ruler()).cloned().collect()
}

fn enumerate_golomb_rulers_pruned_with_length(order: usize, length: usize) -> Vec<GolombRuler> {
    GolombRulerPrunedIterator::new(order, length).collect()
}

/// For initial enumeration, check the golomb property at a depth of `depth`.
fn enumerate_golomb_rulers_depth(order: usize, max_length: usize, depth: usize) -> Vec<GolombRuler> {

    let all_rulers: Vec<GolombRuler> = (2..max_length + 1).flat_map(|length| {
        GolombRulerDepthIterator::new(order, length, depth)
    }).collect();

    all_rulers
}

fn enumerate_golomb_rulers_depth_with_length(order: usize, length: usize, depth: usize) -> Vec<GolombRuler> {
    GolombRulerDepthIterator::new(order, length, depth).collect()
}


// If we start with the smallest possible length, then the _very_ first ruler that we encounter
// is optional!

// Some facts about our object that we are working with:
// - there are an infinite number of golomb rulers
// - for a given length, there is only a certain number of golomb rulers possible


/// Iterator over all possible rulers with length `length`.
struct RulerIterator {
    state: Vec<bool>,
    length: usize
}

impl GolombRulerPrunedIterator {
    fn new(order: usize, length: usize) -> Self {
        // The initial state should return our starting point on next()
        // this pre-state accomplishes that
        let pre_state = vec![false; length - 2];
        GolombRulerPrunedIterator {
            state: pre_state,
            order,
            length,
        }
    }
}

/// Iterator that prunes the tree when the order has been hit or the golomb property is
#[derive(Debug)]
struct GolombRulerPrunedIterator {
    state: Vec<bool>,
    order: usize,
    length: usize
}

impl RulerIterator {
    fn new(length: usize) -> Self {
        // The initial state should return our starting point on next()
        // this pre-state accomplishes that
        let pre_state = vec![false; length - 2];
        RulerIterator {
            state: pre_state,
            length,
        }
    }
}

/// Iterator that initially only checks the golomb property up until a certain depth
#[derive(Debug)]
struct GolombRulerDepthIterator {
    state: Vec<bool>,
    order: usize,
    length: usize,
    depth: usize,
}

impl GolombRulerDepthIterator {
    fn new(order: usize, length: usize, depth: usize) -> Self {
        let pre_state = vec![false; length - 2];
        GolombRulerDepthIterator {
            state: pre_state,
            order,
            length,
            depth,
        }
    }
}

/// GolombRuler integer subtype

/// 0-implied GolombRuler.

#[derive(Clone, Debug)]
#[pyclass]
pub struct GolombRuler {
    marks: Vec<GInt>
}

#[derive(Debug, Clone)]
#[pyclass]
struct Distance {
    lhs: GInt,
    rhs: GInt,
    dist: GInt,
}

impl GolombRuler {

    pub fn new(marks: &[GInt]) -> Self {
        let marks = marks.to_vec();
        GolombRuler {
            marks
        }
    }
}

#[pymethods]
impl GolombRuler {

    fn __repr__(&self) -> String {
        self.to_string()
    }

    fn order(&self) -> usize {
        self.marks.len() + 1
    }

    fn length(&self) -> GInt {
        if self.marks.is_empty() {
            return 0
        }
        self.marks[self.marks.len() - 1]
    }

    /// Check if the data in `self.marks` actual admits the Golomb Property.
    fn is_golomb_ruler(&self) -> bool {
        Ruler::is_golomb_ruler(&self.marks)
    }

    /// Return the marks as a set
    fn as_set(&self) -> HashSet<GInt> {
        let mut out = HashSet::<GInt>::new();

        for m in &self.marks {
            out.insert(*m);
        }

        out
    }

    /// Return the next _RULER_ with order `order` and length `length`, not necessarily the next golomb ruler
    fn next_pruned(&self, order: usize, length: usize) -> Option<GolombRuler> {
        Some(self.to_state().next_pruned(order, length)?.to_ruler())
    }

    /// Used in enumeration algorithms. Check if the first order of distances are unique.
    ///
    /// Consider the following array
    ///
    /// `[1, 3, 4]`
    ///
    /// 0th order: `[1, 3, 4]`
    /// 1st order: `[2, 3]`
    /// 2nd order: `[1]`
    ///
    /// The idea is to prune our enumeration tree based on a O(2n) or O(n) check; n the number of marks on our ruler
    /// We can later iterate over the returned rulers to actually filter them.
    fn is_golomb_ruler_order_1(&self) -> bool {
        // start with the last element of our ruler and subtract every other element
        let set = self.as_set();
        let base = self.length(); // 0 is implied, our first element

        for m in &self.marks[0..(self.marks.len() - 1)] {
            let d = dist(*m, base);
            if set.contains(&d) {
                return false;
            }
        }
        true
    }

    fn distances(&self) -> Vec<Distance> {

        let mut out: Vec<Distance> = Vec::new();

        for (idx, lhs) in self.marks.iter().enumerate() {
            out.push(Distance {
                lhs: 0,
                rhs: *lhs,
                dist: *lhs
            });
            for rhs in &self.marks[idx + 1..] {
                out.push(Distance {
                    lhs: *lhs,
                    rhs: *rhs,
                    dist: GInt::abs(rhs - lhs)
                });
            }
        }

        out
    }

    fn to_id(&self) -> Option<usize> {

        // [0]
        if self.marks.is_empty() {
            Some(0)
        } else if self.length() == 1 {
        // [0, 1]
            Some(1)
        } else if self.length() > 64 {
            None
        } else {
            let mut val = 1 << (self.length() - 1);
            // println!("Starting value: {}", val);
            let state = self.to_state();
            self.marks[0..self.marks.len() - 1].iter().for_each(|m| if state[(*m - 1) as usize] { val += 1 << (m - 1)} );

            Some(val)
        }
    }

    #[staticmethod]
    fn from_id(id: usize) -> GolombRuler {

        if id == 0 {
            GolombRuler {
                marks: vec![],
            }
        } else if id == 1 {
            GolombRuler {
                marks: vec![1]
            }
        } else {

            // Break the id into binary
            // for bit in id.view_bits() {

            // }
            let length = id.ilog2() as usize + 1;

            // Now that's the _length_ of our bit vector!
            // println!("Magnitude: {}", magnitude);
            let mut state = vec![false; length - 1];

            for (i, b) in state.iter_mut().enumerate().take(length - 1) {

                let mask = 1usize << i;
                if (id & mask) == mask {
                    *b = true
                }
            }

            state.to_ruler()
        }
    }

    #[staticmethod]
    fn from_ids(start_idx: usize, end_idx: usize) -> Vec<GolombRuler> {
        (start_idx..end_idx).map(GolombRuler::from_id).collect::<Vec<GolombRuler>>()
    }


    fn to_state(&self) -> Vec<bool> {

        let l = self.length();

        if self.order() == 1 || self.length() == 1 {
            return vec![]
        }


        // if self.
        // if self.length() == 0 {
        //     return vec![]
        // }

        // if self.length()

        // Initialize with all false, dropping the 0 and length
        let mut state = vec![false; (l - 1) as usize];

        // Drop the 0
        for m in &self.marks[0..self.marks.len() - 1] {
            state[*m as usize - 1] = true;
        }

        state
    }

}

impl std::fmt::Display for GolombRuler {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {

        // prepend a zero to our vector
        let mut out: Vec<GInt> = vec![0];
        out.append(&mut self.marks.clone());
        write!(f, "{:?}", out)
    }
}

/// Simple trait to convert a vector of booleans to a u64
trait RulerState {
    fn jump_back(&self) -> Vec<bool>;
    fn to_u64(&self) -> Option<u64>;
    /// Count the number of true values in this iterator state
    fn count_marks(&self) -> usize;
    /// Return the next state with max number of marks `order` and max length `length`
    fn next(&self, length: usize) -> Option<Vec<bool>>;
    /// Test if every bool is true in this RulerState
    fn all(&self) -> bool;
    /// Append a false to the end of this vector
    fn go_left(&self) -> Vec<bool>;
    /// Bounce back one level of ancestry, then go right
    fn back_one_then_right(&self) -> Vec<bool>;
    /// Traverse upwards until we've reached an untouched node
    fn backtrack(&self) -> Vec<bool>;
    fn to_string(&self) -> String;
    /// Convert the current state into a golomb ruler
    fn to_ruler(&self) -> GolombRuler;
    fn total_marks(&self) -> usize;
    fn next_pruned(&self, order: usize, length: usize) -> Option<Vec<bool>>;
    fn next_golomb_depth_1(&self, order: usize, length: usize) -> Option<Vec<bool>>;
    fn contains(&self, value: GInt) -> bool;
    fn is_golomb_ruler_order_1(&self) -> bool;
    fn add_mark(&self) -> Option<Vec<bool>>;
    fn pruned_propose_next(&self, order: usize) -> Option<Vec<bool>>;
}

const TWO: u64 = 2;



impl RulerState for Vec<bool> {

    fn to_u64(&self) -> Option<u64> {

        let n = self.len();
        if n > 64 {
            None
        } else {
            let mut int: u64 = 0;
            for i in 0..n {
                if self[n - 1 - i] {
                    int += TWO.pow((i).try_into().unwrap())
                }
            }
            Some(int)
        }
    }

    /// Used in enumeration algorithms. Check if the first order of distances are unique.
    ///
    /// Consider the following array
    ///
    /// `[1, 3, 4]`
    ///
    /// 0th order: `[1, 3, 4]`
    /// 1st order: `[2, 3]`
    /// 2nd order: `[1]`
    ///
    /// The idea is to prune our enumeration tree based on a O(2n) or O(n) check; n the number of marks on our ruler
    /// We can later iterate over the returned rulers to actually filter them.
    fn is_golomb_ruler_order_1(&self) -> bool {
        // start with the first element of our ruler and subtract every other element
        let ruler = self.to_ruler();
        let base = ruler.marks[ruler.marks.len() - 1]; // 0 is implied, our first element

        if ruler.marks.is_empty() || ruler.marks.len() == 1 {
            return true
        }

        for m in &ruler.marks[0..(ruler.marks.len() - 1)] {
            let d = dist(*m, base);
            if self.contains(d) {
                return false;
            }
        }
        true
    }

    fn count_marks(&self) -> usize {
        let mut count = 0;
        self.iter().for_each(|b| if *b { count += 1 });
        count
    }

    /// Return the total number of marks (including the implied start and end points).
    fn total_marks(&self) -> usize {
        self.count_marks() + 2
    }

    fn all(&self) -> bool {
        for b in self {
            if !b { return false }
        }
        true
    }

    fn go_left(&self) -> Vec<bool> {
        let mut out = self.clone();
        out.push(false);
        out
    }

    fn back_one_then_right(&self) -> Vec<bool> {
        let mut out = self.clone();
        out[self.len() - 1] = true;
        out
    }

    /// 0111 -> 1000
    fn backtrack(&self) -> Vec<bool> {

        let mut out = self.clone();
        // Iterate backwards
        for i in (0..self.len()).rev() {
            if out[i] {
                out[i] = false;
            } else {
                out[i] = true;
                break;
            }
        }

        out
    }

    fn to_string(&self) -> String {
        self.iter().map(|b| if *b { '1' } else { '0' } ).collect()
    }

    /// Convert the current RulerState into a full-fledged GolombRuler
    fn to_ruler(&self) -> GolombRuler {
        // 0 is implied and the final element is implied as well!
        let length_of_ruler = self.len() + 1;
        let mut marks: Vec<GInt> = self.iter().enumerate().filter_map(|(idx, b)| {
            if *b {
                Some((idx + 1) as GInt)
            } else {
                None
            }
        }).collect();
        marks.push(length_of_ruler as GInt);

        GolombRuler {
            marks,
        }
    }

    fn next(&self, length: usize) -> Option<Vec<bool>> {

        if self.len() > length - 1 {
            return None
        }

        if self.len() < length - 1 {

            // Always 'go to the left'
            let mut left = self.go_left();
            while left.len() != length - 1 {
                left = left.go_left();
            }
            Some(left)

        } else {

            // If our final element is 0, then we simply bounce back one and go to the right
            if !self[self.len() - 1] {
                Some(self.back_one_then_right())
            } else {
                // We need to back track!
                // .. unless we should end iteration!
                if self.all() {
                    None
                } else {
                    Some(self.backtrack())
                }
            }
        }
    }

    /// Attempt to add one mark to this state vector.
    ///
    /// If we can't increase the order tally, return None.
    fn add_mark(&self) -> Option<Vec<bool>> {

        let mut out = self.clone();

        // Iterating backwards, find the first zero
        for i in (0..self.len()).rev() {
            if !self[i] {
                out[i] = true;
                return Some(out);
            }
        }

        // And return None if our state is full of ones
        None
    }

    /// Improved implementation of `next` by pruning trees that have too many points
    fn next_pruned(&self, order: usize, length: usize) -> Option<Vec<bool>> {

        if self.len() > length - 1 {
            return None
        }

        if self.len() < length - 1 {
            return self.go_left().next_pruned(order, length);
        }

        let mut next = self.pruned_propose_next(order)?;

        while next.total_marks() != order {
            next = next.pruned_propose_next(order)?;
        }

        Some(next)
        // // If our final element is 0, then we simply bounce back one and go to the right
        // if !self[self.len() - 1] {

        //     let n_marks = self.total_marks();

        //     // If we have too many marks, we can't continue to the right.
        //     if n_marks == order {

        //         // If our vector starts with 1, then we are totally done.
        //         // This condition needs to change to: if the first (order - 2) elements are 1
        //         if self.iter().take(order - 2).all(|b| *b) {
        //         // if self[0] {
        //             None
        //         } else {
        //             let next = self.jump_back();
        //             if next.total_marks() == order {
        //                 Some(next)
        //             } else {
        //                 next.next_pruned(order, length)
        //             }
        //         }
        //     } else {
        //         let next = self.add_mark()?;

        //         if next.total_marks() == order {
        //             Some(next)
        //         } else {
        //             next.next_pruned(order, length)
        //         }
        //     }

        // } else {
        //     // We need to back track!
        //     // .. unless we should end iteration!
        //     if self.all() {
        //         None
        //     } else {
        //         let next = self.backtrack();
        //         if next.total_marks() == order {
        //             Some(next)
        //         } else {
        //             next.next_pruned(order, length)
        //         }
        //     }
        // }
    }

    fn next_golomb_depth_1(&self, order: usize, length: usize) -> Option<Vec<bool>> {
        // First get next ruler
        let mut next_pruned = self.next_pruned(order, length)?;
        // if next_pruned.to_ruler().

        while !next_pruned.is_golomb_ruler_order_1() {
            next_pruned = next_pruned.next_pruned(order, length)?;
        }

        Some(next_pruned)
    }

    /// Skip over elements who are saturated
    ///
    /// With 2 total true values, send 010 -> 100 (instead of 011)
    ///
    /// This function should be called when we are about to add an additional mark
    /// but we actually already have enough marks
    /// The caller must protect against the case where the first boolean is 1.
    fn jump_back(&self) -> Vec<bool> {

        // Just roll back the first one that we encounter
        let mut out = self.clone();
        let mut j: usize = 0;
        for i in (0..out.len()).rev() {
            if out[i] {
                out[i] = false;
                j = i;
                // out[i - 1] = true;
                break
            }
        }

        // Now go through consecutive ones
        for i in (0..j).rev() {
            // If our consecutive ones have ended,
            if !out[i] {
                out[i] = true;
                break
            } else {
                out[i] = false;
            }
        }

        out
    }


    /// Given a vector of booleans, propose the next pruned ruler.
    ///
    /// This function helps us implement an iterative version of `next_pruned` that doesn't use recursion
    fn pruned_propose_next(&self, order: usize) -> Option<Vec<bool>> {

        // If our final element is 0, then we simply bounce back one and go to the right
        if !self[self.len() - 1] {

            let n_marks = self.total_marks();

            // If we have too many marks, we can't continue to the right.
            if n_marks == order {

                // If our vector starts with 1, then we are totally done.
                // This condition needs to change to: if the first (order - 2) elements are 1
                if self.iter().take(order - 2).all(|b| *b) {
                // if self[0] {
                    None
                } else {
                    Some(self.jump_back())
                }
            } else {
                self.add_mark()
            }

        } else {
            // We need to back track!
            // .. unless we should end iteration!
            if self.all() {
                None
            } else {
                Some(self.backtrack())
            }
        }
    }

    /// Check if self contains the value `value`
    fn contains(&self, value: GInt) -> bool {

        let length = self.len() + 1;

        if value < 0 {
            return false
        }

        if value == 0 || value == length as GInt {
            true
        } else if value as usize > length  {
            false
        } else {
            self[(value - 1) as usize]
        }
    }

}


impl Iterator for RulerIterator {
    type Item = GolombRuler;

    fn next(&mut self) -> Option<Self::Item> {

        let next_state = self.state.next(self.length);
        self.state = next_state?;
        Some(self.state.to_ruler())
    }
}

impl Iterator for GolombRulerPrunedIterator {
    type Item = GolombRuler;

    fn next(&mut self) -> Option<Self::Item> {

        let next_state = self.state.next_pruned(self.order, self.length);
        self.state = next_state?;
        Some(self.state.to_ruler())
    }
}

impl Iterator for GolombRulerDepthIterator {
    type Item = GolombRuler;

    fn next(&mut self) -> Option<Self::Item> {
        let next_state = self.state.next_golomb_depth_1(self.order, self.length);
        self.state = next_state?;
        Some(self.state.to_ruler())
    }
}


fn count_permutations(n: GInt, r: GInt) -> GInt {
    (n - r + 1..=n).product()
}


/* -------------------------------------------------------------------------- */
/*                              Public functions                              */
/* -------------------------------------------------------------------------- */
#[pymethods]
impl Ruler {

    /// Create a new ruler from a given id.
    #[staticmethod]
    #[pyo3(text_signature = "(id: int)")]
    fn from_id(id: usize) -> GolombRuler {
        GolombRuler::from_id(id)
    }

}


#[cfg(test)]
mod tests {

    use super::*;

    #[test]
    fn test() {

        let my_bool: Vec<bool> = vec![true, true, false];
        dbg!(my_bool.to_u64());
        assert_eq!(my_bool.count_marks(), 2);
        dbg!(my_bool.to_string());

    }


    #[test]
    fn test_enum() {

        // let my_bool: Vec<bool> = vec![true, true, false];
        // dbg!(my_bool.to_u64());
        // assert_eq!(my_bool.count_marks(), 2);
        // dbg!(my_bool.to_string());

        // dbg!(my_bool.to_ruler());


        // dbg!(enumerate_golomb_rulers(3, 4));

        let order = 3;

        // let len_1 = enumerate_golomb_rulers(order, 1);

        // dbg!(len_1);

        // let len_2 = enumerate_golomb_rulers(order, 2);
        // dbg!(len_2);

        // let len_3 = enumerate_golomb_rulers(order, 3);
        // dbg!(len_3);


        let r_o3_l3 = enumerate_golomb_rulers(2, 3);

        for r in r_o3_l3 {
            println!("{}", r);
            // dbg!(r.distances());
        }

        let rulers_2_3 = enumerate_rulers(3);
        for r in rulers_2_3 {
            println!("{}", r);
        }


        let r2 = enumerate_rulers_with_length(2);
        println!("========= Length 2 ===========");
        for r in r2 {
            println!("{}", r);
        }


        // let r_o2_3 = enumerate_golomb_rulers(2, 3);
        let r3 = enumerate_rulers_with_length(3);
        println!("========= Length 3 ===========");
        for r in r3 {
            println!("{}", r);
        }

        let r4 = enumerate_rulers_with_length(4);
        println!("========= Length 4 ===========");
        for r in r4 {
            println!("{}", r);
        }


        println!("========= G 3_10 ===========");
        let g4 = enumerate_golomb_rulers(3, 10);
        for r in g4 {
            println!("{}", r)
        }

        println!("======== Ruler 3_10 ========");
        let r_3_10 = enumerate_rulers_with_order(3, 10);
        for r in r_3_10.iter() {
            println!("{}", r);
        }

        // println!("Num rulers: {}", r_3_10.len());
        // println!("10 choose 3: {}", count_permutations(10, 3));

        // println

        // for r in r_o2_3 {
        //     println!("{}", r);
        //     dbg!(r.distances());
        // }


        // For a single length, let's count the number of values at each order

        let mut lengths: Vec<(usize, usize)> = Vec::new();
        let order_range = 2..10;
        for order in order_range.clone() {
            lengths.push((order, enumerate_golomb_rulers(order, 20).len()));
        }


        for r in lengths {
            println!("{:?}", r)
        }
        // dbg!(lengths);

    }

    /// Verify that all rulers are being enumerated
    #[test]
    fn gen_rulers() {

        let length = 10;
        let rulers = enumerate_rulers_with_length(length);

        let rulers: Vec<&GolombRuler> = rulers.iter().filter(|r| r.is_golomb_ruler()).collect();


        for r in &rulers {
            println!("{}", r)
        }
        println!("N rulers: {}", rulers.len());

    }

    #[test]
    fn gen_pruned() {

        let length = 5;
        let order = 3;
        let rulers = enumerate_pruned_rulers(order, length);

        for r in &rulers {
            println!("{}", r);
        }

        // let iter = GolombRulerPrunedIterator::new(order, length);




        // dbg!(iter.take(1).collect::<Vec<GolombRuler>>());


    }

    #[test]
    fn test_jump_back() {

        let test: Vec<bool> = vec![false, true, false];

        dbg!(&test);
        dbg!(test.jump_back());


    }

    #[test]
    fn test_ruler() {

        let rulers_3 = enumerate_rulers_with_length(3);
        for r in rulers_3 {
            println!("{}", r);
        }

    }


    #[test]
    fn test_ids() {

        let rulers_3 = enumerate_rulers(3);
        for r in rulers_3 {
            println!("[{:?}] Ruler: {};", r.to_id().unwrap(), r);
        }
    }

    #[test]
    fn test_from_id() {

        let first = GolombRuler::from_id(0);
        println!("{}", first);

        let second = GolombRuler::from_id(1);
        println!("{}", second);

        let third = GolombRuler::from_id(2);
        println!("{}", third);

        let third = GolombRuler::from_id(3);
        println!("{}", third);

        let fourth = GolombRuler::from_id(4);
        println!("{}", fourth);

        // let test = GolombRuler::from_id(1000234);
        // println!("{}", test);

        for i in 0..10 {
            println!("[{:02}] {}", i, GolombRuler::from_id(i));
        }

    }

    #[test]
    fn sample_rulers() {

        let max_range = 1000;

        let rulers = (0..max_range).map(GolombRuler::from_id).collect::<Vec<GolombRuler>>();
        let rulers_is_golom: Vec<(&GolombRuler, bool)> = rulers.iter().map(|r| (r, r.is_golomb_ruler())).collect();

        let mut golomb_rulers: Vec<usize> = Vec::new();

        for (idx, pair) in rulers_is_golom.iter().enumerate() {
            println!("{}, {:?}", idx, pair);
            if pair.1 {
                golomb_rulers.push(idx)
            }
        }

        println!("Only {} golomb rulers out of {}!", golomb_rulers.len(), max_range);

        println!("Golomb Rulers: {:?}", golomb_rulers);

    }

    #[test]
    fn stats() {

        let max_range = 100;
        let rulers = GolombRuler::from_ids(0, max_range);
        let golomb_rulers = rulers.iter().filter(|r| r.is_golomb_ruler()).collect::<Vec<&GolombRuler>>();

        // Find the average order?
        // Actually I just want the _distribution_ of heights.

        println!("Num golomb rulers {}/{}", golomb_rulers.len(), max_range);
        println!("{:?}", golomb_rulers);

        for g in golomb_rulers {
            println!("g: {}, order: {}", &g, g.order());
        }



    }

    /// Verify that our `contains` function for `Vec<bool>` works properly
    #[test]
    fn test_contains() {

        let ruler = GolombRuler::from_id(10);
        println!("Ruler: {}", ruler);

        let state = ruler.to_state();
        assert!(state.contains(0));
        assert!(state.contains(2));
        assert!(state.contains(4));
        assert!(!state.contains(5));
        assert!(!state.contains(10));
        assert!(!state.contains(200));
        assert!(!state.contains(-2));

    }

    #[test]
    fn test_propery_order_1() {

        let ruler = GolombRuler::from_id(10);
        println!("Ruler: {}", ruler);

        let r_09 = GolombRuler::from_id(9);
        println!("Ruler: {}", r_09);

        assert!(!ruler.is_golomb_ruler_order_1());
        assert!(r_09.is_golomb_ruler_order_1());

    }

    #[test]
    fn add_mark_unit() {

        let ruler = GolombRuler::from_id(22528);

        // dbg!(ruler.to_state());
        // dbg!(ruler.to_state().next_pruned(4, 15).unwrap());

        // println!("====");

        // dbg!(ruler.to_string());
        // dbg!(ruler.to_state().next_pruned(4, 15).unwrap().to_ruler().to_string());
    }

    #[test]
    fn add_mark() {

        // let ruler = GolombRuler::from_id(18432);
        // let ruler = GolombRuler::from_id(576);

        // println!("R.state: {:?}, r: {}", ruler.to_state(), ruler);
        // let next = ruler.to_state().next_pruned(4, 15).unwrap().to_ruler();

        // let np = ruler.to_state().next_pruned(4, 15).unwrap();
        // dbg!(np);

        // println!("R.state.next(): {:?}, r: {}", next.to_state(), next);

        let rulers = enumerate_golomb_rulers_pruned_with_length(4, 15);
        for r in rulers {
            println!("{}", r);
        }

    }

    #[test]
    fn more_enums() {

        use itertools::*;
        let order = 2;
        let length = 11;
        let depth = 1;

        let rulers = enumerate_rulers_with_length(length);
        println!("N rulers: {} length: {}", rulers.len(), length);

        let rulers_pruned = enumerate_golomb_rulers_pruned_with_length(order, length);
        println!("N pruned rulers: {} (order: {}, length: {})", rulers_pruned.len(), order, length);

        let ruler_pruned_g = rulers_pruned.iter().filter(|r| r.is_golomb_ruler()).collect_vec();

        let rulers_depth = enumerate_golomb_rulers_depth_with_length(order, length, depth);
        println!("N depth rulers: {} (order: {}, length: {})", rulers_depth.len(), order, length);

        let golomb_rulers = enumerate_golomb_rulers_with_length(order, length);
        println!("N golomb rulers: {} (order: {}, length: {})", golomb_rulers.len(), order, length);

        for r in &rulers_pruned {
            println!("{}", r);
        }

        println!("========");

        for r in rulers_depth {
            println!("{}", r);
        }

        println!("=======");

        for r in golomb_rulers {
            println!("{}", r);
        }

        println!("=======");

        for r in ruler_pruned_g {
            println!("{}", r);
        }


    }

    #[test]
    fn tnp() {
        // Test next pruned
        // Generate all rulers then filter
        use itertools::*;

        fn test_pruned(length: usize) {

            let all_rulers = enumerate_rulers_with_length(length);

            for order in 1..length {

                // Generate all rulers then filter
                let filtered = all_rulers.iter().filter(|r| r.order() == order).collect_vec();
                let pruned = enumerate_pruned_rulers(order, length);

                assert_eq!(filtered.len(), pruned.len())
            }
        }

        test_pruned(10);
        test_pruned(12);
        test_pruned(20);
    }

    #[test]
    fn timing_tnp() {

        enumerate_pruned_rulers(10, 20);
    }

    #[test]
    fn timing_all() {

        // enumerate_pruned_rulers(10, 20);
        enumerate_rulers_with_order(10, 20);
    }


}