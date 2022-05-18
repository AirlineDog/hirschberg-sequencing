# Hirschberg Sequencing Algorithm

Let's say we got two DNA sequences `GATTACA` and `GCATGCA` and we want to get the optimal alignments of those two:
```
G-ATTACA | G-ATTACA | G-ATTACA
GCA-TGCG | GCAT-GCG | GCATG-CG
```

How are these alignments defined as optimal?
--
We calculate the alignment score as:

We begin we score 0
* If two letters are the same we add `m` (match) to the score 
* If two letters are different we subtract `d` (differ) to the score
* If we add a gap we subtract `g` (gap) to the score

To find all possible alignments:

1. Split the first sequence in half
2. Calculate the last line of the [Needleman-Wunsch matrix](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm) for the first half and the whole second sequence
3. Calculate the last line of the [Needleman-Wunsch matrix](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm) for the reversed second half and the whole reversed second sequence
4. Add the elements of `step 2` and reversed `step 3` together
5. Find the indexes of the elements equal to the max element of `step 4`

Then recursively split the first sequence in half and the second one at the index found in `step 5` until the length of a sequence is 0 or 1.
The reqursion terminates when you end up with a sequence of length 0 or 1. In the first case add gaps to the allignment. In the second one you have to aplly the [Needleman-Wunsch algorithm](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm), but this time the matrix will either have 2 rows or 2 columns

This is an efficient way to reduce space complexity of the [Needleman-Wunsch algorithm](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm) invented by [Dan Hirschberg](https://en.wikipedia.org/wiki/Dan_Hirschberg)

Needleman-Wunsch algorithm
---
* Time complexity: O(mn)
* Space complexity: O(mn)

Hirschberg algorithm
---
* Time complexity: O(mn)
* Space complexity: O(min{m, n})


More inforamation:
---
* [wikipedia](https://en.wikipedia.org/wiki/Hirschberg%27s_algorithm)
* [Hirschberg, D. S. 1975. “A Linear Space Algorithm for Computing Maximal Common
Subsequences.” ](https://doi.org/10.1145/360825.360861)
* [Needleman, Saul B., and Christian D. Wunsch. 1970. “A General Method Applicable to
the Search for Similarities in the Amino Acid Sequence of Two Proteins.”](https://doi.org/10.1016/0022-2836(70)90057-4)
