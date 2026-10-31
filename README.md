<!-- Davide Batic (Mathematics Department, Khalifa University of Science and Technology, Abu Dhabi, UAE), Alan S. Cornell (Department of Physics, University of Johannesburg, Auckland Park, South Africa), Dr. Denys Dutykh (Mathematics Department, Khalifa University of Science and Technology, Abu Dhabi, UAE) -->

# Schwarzschild–AdS quasinormal modes

Numerical data and high-precision Chebyshev spectral solvers for quasinormal
modes (QNMs) of four-dimensional Schwarzschild–anti-de Sitter (SAdS) black
holes.

This repository accompanies the paper
[*Scalar quasinormal modes of Schwarzschild–anti-de Sitter black holes: spectral analysis and a formal coefficient deformation*](https://doi.org/10.1140/epjc/s10052-026-16449-7)
by D. Batic, A. S. Cornell and D. Dutykh, published open access in
*Eur. Phys. J. C* **86**, 1252 (2026) (preprint:
[arXiv:2607.15731](https://arxiv.org/abs/2607.15731)). It contains Maple
worksheets for deriving and assembling the spectral matrix problem, Julia
programs for solving and post-processing it, and tabulated QNM spectra. The
PDF kept in `pdfs/` is the [preprint of 12 July 2026](pdfs/SCHWARZSCHILD_anti_de_SITTER_MASSLESS.pdf),
written under an earlier title; the journal version is the one to cite (see
[Citation and acknowledgement](#citation-and-acknowledgement)).

## Project status

The current release covers the **massless scalar perturbation sector**
(`s = 0`):

- the standard vanishing-field (Dirichlet) condition at the conformal AdS
  boundary;
- a generalized relation between the two independent scalar asymptotic
  coefficients; and
- benchmark and refinement data for small, intermediate, and large SAdS black
  holes.

The next part, covering **electromagnetic (`s = 1`) and gravitational
(`s = 2`) perturbations**, is currently in preparation. The completed
repository is intended to contain the data and code for all three perturbation
sectors: scalar, electromagnetic, and gravitational.

> [!IMPORTANT]
> Although the Julia programs contain common labels and validation logic for
> `s = 0, 1, 2`, the checked-in worksheets and numerical reports currently
> belong to the scalar sector only. Electromagnetic and gravitational results
> should not yet be inferred from the present data.

## Scientific problem and numerical method

The calculations use the dimensionless horizon radius and frequency

```text
x+ = r+/R,        Ω = ωR,
```

where `r+` is the event-horizon radius and `R` is the AdS radius. After the
exterior radial domain is compactified and the asymptotic QNM behavior is
factored out, Chebyshev collocation reduces the radial equation to the
quadratic matrix pencil

```text
M0 + i Ω M1 + Ω² M2 = 0.
```

The Maple assemblers construct `M0`, `M1`, and `M2` at three spectral
resolutions. The Julia programs linearize the pencil, solve the corresponding
generalized eigenvalue problems with arbitrary-precision arithmetic, filter
finite candidate eigenvalues, and match modes across all three resolutions.
The resolution-triplet comparison provides the numerical stability errors
reported with each accepted mode.

For the time convention

```text
exp(-i ω t),
```

the programs classify modes as follows:

| Frequency | Time behavior |
| --- | --- |
| `Im(Ω) < 0` | damped |
| `Im(Ω) > 0` | unstable |
| `Im(Ω) ≈ 0` within the configured tolerance | neutral |

The standard scalar calculation imposes vanishing field at the AdS boundary.
The generalized scalar calculation instead imposes

```text
A cos(θ) + B sin(θ) = 0,
```

where `A` and `B` are the two independent coefficients in the scalar's
large-radius expansion. This coefficient condition is the deformation studied
in the accompanying paper; it should not be confused with the usual
alternative quantization for a scalar in the Breitenlohner–Freedman window.

## Repository structure

```text
.
├── julia/
│   ├── SAdS_scalar_qnm_solver.jl
│   └── SAdS_scalar_qnm_solver_generalized_bc_fixed.jl
├── maple/
│   ├── 01-CASE-s0-SUPPLEMENTAL MATERIAL.mw
│   ├── 02-CASE-s0-SUPPLEMENTAL MATERIAL-General_BCs.mw
│   ├── Matrix_Assembler_s0_SAdS-Final Version.mw
│   └── Matrix_Assembler_s0_SAdS-Final Version-BC2.mw
├── pdfs/
│   └── SCHWARZSCHILD_anti_de_SITTER_MASSLESS.pdf
├── reports/
│   ├── s0-vanishing-AdS-boundary/
│   │   ├── L0/    # 15 files, x+ from 1/25 up to 100
│   │   ├── L1/    # 3 files:  x+ = 0.4, 1, 50
│   │   ├── L2/    # 3 files:  x+ = 0.4, 1, 50
│   │   └── L3/    # 3 files:  x+ = 0.4, 1, 50
│   └── s0-generalized BC/
│       └── L0/
│           ├── xp0_01/  xp0_01_refinement/   # θ = π/2…3π/8 ; π/16…3π/32
│           ├── xp1_0/   xp1_0_refinement/
│           └── xp50_0/  xp50_0_refinement/
├── .gitignore
├── LICENSE
└── README.md
```

### Maple worksheets

| File | Purpose |
| --- | --- |
| `01-CASE-s0-SUPPLEMENTAL MATERIAL.mw` | Scalar derivation and supplemental calculations for the standard AdS boundary condition |
| `02-CASE-s0-SUPPLEMENTAL MATERIAL-General_BCs.mw` | Scalar derivation and supplemental calculations for generalized coefficient boundary conditions |
| `Matrix_Assembler_s0_SAdS-Final Version.mw` | Builds the standard scalar quadratic-pencil matrices |
| `Matrix_Assembler_s0_SAdS-Final Version-BC2.mw` | Builds the generalized-boundary-condition scalar matrices |

The assemblers export matrix files with names of the form
`M0-N-<tag>.mat`, `M1-N-<tag>.mat`, and `M2-N-<tag>.mat`, where `N` is a
spectral resolution and `<tag>` records the sector, multipole, black-hole
size (as both the decimal `xp` value and the integer `a = 1000·x+` tag),
and, when relevant, the boundary angle.

### Julia solvers

- `SAdS_scalar_qnm_solver.jl` solves the standard vanishing-boundary problem.
- `SAdS_scalar_qnm_solver_generalized_bc_fixed.jl` solves the generalized
  coefficient-boundary problem and supports rational and decimal `x+` inputs
  and angle tags such as `th1over4pi`.

Both programs read three complete `M0/M1/M2` matrix triplets, determine a
compatible file tag, solve and compare the spectra, write readable and
full-precision tables, split stable modes by time behavior, and generate
plots.

### Numerical reports

The repository currently contains 48 scalar report files:

- `reports/s0-vanishing-AdS-boundary/` contains standard-boundary spectra for
  multipoles `ℓ = 0, 1, 2, 3` and several values of `x+`;
- `reports/s0-generalized BC/` contains `ℓ = 0` generalized-boundary spectra
  for representative `x+ = 0.01, 1, 50` cases and near-Dirichlet refinement
  angles.

Each report header records the background, sector, `ℓ`, `x+`, `epsilon`
(`= 1 − s²`), file tag, matrix pencil, time convention, and, where applicable,
`θ`. Each row gives an index `k`, the mode averaged over the three resolutions
(`Re(avg)`, `Im(avg)`), the three pairwise matching errors (`err12`, `err23`,
`err13`), and their maximum (`maxerr`). The committed reports are the concise
readable tables; additional detailed
and full-precision companion files are produced when the Julia solvers are run
locally.

## Requirements

- [Maple](https://www.maplesoft.com/products/Maple/) to inspect the worksheets
  and generate spectral matrices.
- [Julia](https://julialang.org/) to solve and post-process the matrix pencils.
- Julia packages:
  - [`GenericSchur.jl`](https://github.com/RalphAS/GenericSchur.jl)
  - [`Plots.jl`](https://docs.juliaplots.org/)
  - [`PlotlyJS.jl`](https://github.com/JuliaPlots/PlotlyJS.jl) for the default
    interactive plotting backend and HTML output. It is enabled by default
    (`SADS_USE_PLOTLYJS=true`); if it is unavailable the programs warn and fall
    back to the GR backend, so it remains optional.

`DelimitedFiles`, `Printf`, `LinearAlgebra`, and `Base.Threads` are provided by
Julia's standard library.

This repository does not currently include a `Project.toml` or a pinned Julia
environment. Install the required packages in an environment of your choice:

```bash
julia -e 'using Pkg; Pkg.add(["GenericSchur", "Plots", "PlotlyJS"])'
```

## Running the calculations

### 1. Generate the matrix data in Maple

Open the relevant matrix assembler in `maple/`, select the physical parameters
and three spectral resolutions, set an output directory, and execute the
worksheet. Use:

- `Matrix_Assembler_s0_SAdS-Final Version.mw` for the standard boundary
  condition;
- `Matrix_Assembler_s0_SAdS-Final Version-BC2.mw` for the generalized
  coefficient condition.

For every resolution listed in `SADS_N_VALS`, the output directory must contain
a matching `M0`, `M1`, and `M2` file. The Julia programs validate all nine
files before starting the expensive eigenvalue calculations.

> [!NOTE]
> The Maple-generated `.mat` inputs are not committed to this repository. The
> files under `reports/` are final QNM tables, not matrix inputs for the Julia
> programs.

### 2. Run the standard scalar solver

From the repository root, replace the example paths and parameters with those
used in Maple:

```bash
export SADS_DATA_DIR=/absolute/path/to/standard-matrices
export SADS_OUT_DIR="$PWD/output/standard-s0-L0-xp1"
export SADS_SPIN=0
export SADS_ELL=0
export SADS_XPLUS=1
export SADS_N_VALS=90,95,100

julia --threads=auto julia/SAdS_scalar_qnm_solver.jl
```

### 3. Run the generalized-boundary scalar solver

The following example requests `θ = π/4`. In this interface, `1/4` means the
rational multiple `π/4` for the boundary angle and its Maple filename tag.

```bash
export SADS_DATA_DIR=/absolute/path/to/generalized-bc-matrices
export SADS_OUT_DIR="$PWD/output/generalized-s0-L0-xp1-th1over4pi"
export SADS_SPIN=0
export SADS_ELL=0
export SADS_XPLUS=1
export SADS_THETA=1/4
export SADS_N_VALS=190,195,200

julia --threads=auto julia/SAdS_scalar_qnm_solver_generalized_bc_fixed.jl
```

The generalized solver also accepts forms such as `pi/4`, `1over4`, and
`th1over4pi`. Set `SADS_THETA_TAG` or the complete `SADS_FILETAG` explicitly
when automatic tag detection cannot match the filenames produced by Maple.

The source files contain author-machine Windows paths as historical defaults.
For portable use, always set `SADS_DATA_DIR` and preferably `SADS_OUT_DIR`.

## Configuration

The most commonly used environment variables are:

| Variable | Meaning | Standard default | Generalized default |
| --- | --- | --- | --- |
| `SADS_DATA_DIR` | Directory containing Maple-generated matrices | Author-machine path | Author-machine path |
| `SADS_OUT_DIR` | Directory for tables and plots | `<DATA_DIR>/Julia/<FILETAG>` | `<DATA_DIR>/Julia/<FILETAG>` |
| `SADS_SPIN` | Perturbation-sector label | `0` | `0` |
| `SADS_ELL` | Angular multipole `ℓ` | `0` | `3` |
| `SADS_XPLUS` | Dimensionless horizon radius `r+/R` | `50` | `50` |
| `SADS_N_VALS` | Exactly three spectral resolutions | `90,95,100` | `190,195,200` |
| `SADS_FILETAG` | Complete matrix filename tag | auto-detected | auto-detected |
| `SADS_XPLUS_TAG` | Override for the `x+` filename tag | derived | derived |
| `SADS_ATAG` | Override for the integer `a` filename tag (`a = round(1000·x+)`) | derived | derived |
| `SADS_THETA` | Generalized boundary angle | not used | `0` |
| `SADS_THETA_TAG` | Override for the angle filename tag | not used | derived |

Advanced controls include:

- precision and display: `SADS_FILE_DECIMAL_DIGITS`,
  `SADS_WORK_DECIMAL_DIGITS`, `SADS_DISPLAY_ZERO_TOL` (magnitude below which
  `Re`/`Im` values print as `0`);
- resolution matching: `SADS_STABLE_RELTOL`, `SADS_STABLE_ABSTOL`;
- zero-mode and time-behavior filters: `SADS_DISCARD_ZERO_MODE`,
  `SADS_ZERO_MODE_TOL`, `SADS_SEARCH_UNSTABLE`, `SADS_DAMPING_TOL`;
- symmetry and mode classification: `SADS_KEEP_REPRESENTATIVE_BRANCH`,
  `SADS_REPRESENTATIVE_RE_TOL`, `SADS_PURE_IMAG_RE_TOL`;
- plotting: `SADS_USE_PLOTLYJS`, `SADS_SAVE_HTML_PLOTS`,
  `SADS_PLOT_ZERO_TOL`;
- generalized boundary-row handling: `SADS_REDUCE_BOUNDARY_ROW`,
  `SADS_BOUNDARY_ROW_TOL`.

See the documented constant definitions near the beginning of each Julia file
for defaults and precise behavior.

## Output files

A solver run writes its results beneath `SADS_OUT_DIR`. Outputs include:

- finite and filtered candidate spectra for each resolution;
- `stable_modes-<tag>.txt`, plus detailed and full-precision companions;
- separate damped, unstable, neutral, oscillatory, and purely imaginary mode
  tables;
- all-mode and stable-mode plots, with additional category-specific plots when
  the corresponding mode set is nonempty;
- PNG plots and, when enabled and supported by the plotting backend, HTML
  plots.

Filename tags encode the parameters. For example,
`s0_L0_xp1_a1000_th1over4pi` denotes the scalar sector, `ℓ = 0`, `x+ = 1`,
the associated Maple `a` tag (`a = 1000·x+`), and `θ = π/4`.

## Authors

- **Davide Batic**, Mathematics Department, Khalifa University of Science
  and Technology, Abu Dhabi, United Arab Emirates.
- **Alan S. Cornell**, Department of Physics, University of Johannesburg,
  Auckland Park, South Africa.
- **Denys Dutykh**, Mathematics Department, Khalifa University of Science
  and Technology, Abu Dhabi, United Arab Emirates.

## Citation and acknowledgement

Anyone who uses the spectra, the matrices, the worksheets or the programs of
this repository in a paper, a thesis or a talk is asked to cite the published
paper and, whenever the data or the codes themselves were used, to name the
repository as well. The paper (version of record) is:

> D. Batic, A. S. Cornell and D. Dutykh, *Scalar quasinormal modes of
> Schwarzschild–anti-de Sitter black holes: spectral analysis and a formal
> coefficient deformation*, Eur. Phys. J. C **86**, 1252 (2026),
> [doi:10.1140/epjc/s10052-026-16449-7](https://doi.org/10.1140/epjc/s10052-026-16449-7).

The paper was received on 21 July 2026, accepted on 23 September 2026 and
published online on 29 October 2026, in issue 10 of volume 86. It is open
access under the Creative Commons Attribution 4.0 licence, and
[its page at the publisher](https://link.springer.com/article/10.1140/epjc/s10052-026-16449-7)
gives the full text and the citation formats. The preprint is
[arXiv:2607.15731](https://arxiv.org/abs/2607.15731) [gr-qc], submitted on
17 July 2026; its title ends with "generalized boundary conditions" instead of
"a formal coefficient deformation", so the journal reference above is the one
to use.

```bibtex
@article{batic2026scalar,
  author        = {Batic, Davide and Cornell, Alan S. and Dutykh, Denys},
  title         = {Scalar quasinormal modes of {Schwarzschild}--anti-de
                   {Sitter} black holes: spectral analysis and a formal
                   coefficient deformation},
  journal       = {Eur. Phys. J. C},
  volume        = {86},
  number        = {10},
  pages         = {1252},
  year          = {2026},
  doi           = {10.1140/epjc/s10052-026-16449-7},
  url           = {https://doi.org/10.1140/epjc/s10052-026-16449-7},
  eprint        = {2607.15731},
  archivePrefix = {arXiv},
  primaryClass  = {gr-qc}
}
```

The codes and the numerical data have their own reference:

> D. Batic, A. S. Cornell and D. Dutykh (2026), *Schwarzschild–AdS
> quasinormal modes: spectral codes and numerical data*, GitHub repository.

<https://github.com/dutykh/schwarzschild-ads>

```bibtex
@misc{batic2026sadsdata,
  author       = {Batic, Davide and Cornell, Alan S. and Dutykh, Denys},
  title        = {{Schwarzschild}--{AdS} quasinormal modes: spectral codes
                  and numerical data},
  year         = {2026},
  howpublished = {GitHub repository},
  url          = {https://github.com/dutykh/schwarzschild-ads}
}
```

A result, a formula or a figure taken from the paper needs the paper reference
alone. For frequencies read from the tables of `reports/`, or for calculations
run with the Maple worksheets or the Julia solvers, a sentence such as the
following in the acknowledgements or in the text is enough, where the bracketed
number stands for the paper in your list of references:

```text
The quasinormal frequencies were taken from the numerical data and the spectral
codes of Batic, Cornell and Dutykh [N], available at
https://github.com/dutykh/schwarzschild-ads.
```

Since the repository will grow with the electromagnetic and gravitational
sectors, please also quote the date of access or the commit that you used.

## Selected references

The accompanying paper contains the complete bibliography. Particularly
relevant references for the methods and benchmarks in this repository are:

1. G. T. Horowitz and V. E. Hubeny, *Phys. Rev. D* **62**, 024027 (2000).
2. A. Ishibashi and R. M. Wald, *Class. Quantum Grav.* **20**, 3815 (2003),
   [arXiv:gr-qc/0305012](https://arxiv.org/abs/gr-qc/0305012).
3. A. Ishibashi and R. M. Wald, *Class. Quantum Grav.* **21**, 2981 (2004),
   [arXiv:hep-th/0402184](https://arxiv.org/abs/hep-th/0402184).
4. V. Cardoso, R. Konoplya, and J. P. S. Lemos, *Phys. Rev. D* **68**, 044024
   (2003), [arXiv:gr-qc/0305037](https://arxiv.org/abs/gr-qc/0305037).
5. M. Wang, C. Herdeiro, and M. O. P. Sampaio, *Phys. Rev. D* **92**, 124006
   (2015), [arXiv:1510.04713](https://arxiv.org/abs/1510.04713).
6. R. G. Daghigh, M. D. Green, and J. C. Morey, *Phys. Rev. D* **107**, 024023
   (2023), [arXiv:2209.09324](https://arxiv.org/abs/2209.09324).

## License

This repository is distributed under the
[GNU Lesser General Public License, version 2.1](LICENSE). See `LICENSE` for
the complete terms.
