# symset

Symbolic Sets for Python, written in Rust

## Roadmap

Special sets

- [x] `Empty` - The *empty set* or *void set*, $\displaystyle\varnothing⁠ = \{ \}$
([wiki](https://w.wiki/EMr$))
- [x] `Universe` - *Universe set* $\displaystyle\mathbf{U}⁠$ containing everything, including itself
([wiki](https://w.wiki/EMs4))

Complement operations

- [ ] `Complement[A]` - *Absolute complement* $\displaystyle A^\complement⁠=\mathbf{U}\setminus A$
([wiki](https://w.wiki/ANo$))
- [ ] `Difference[A, B]` - *Relative complement* or *set-theoretic difference*
$\displaystyle A \setminus B$ ([wiki](https://w.wiki/ANo$#Relative_complement))

External operations

- [ ] `Subsets[A]` - *Power set* $\displaystyle\mathcal{P}(A)$; the set of all subsets of
$\displaystyle A$, with $\displaystyle \left|P(A)\right|$ ([wiki](https://w.wiki/FMZ))
- [ ] `Product[A, B]` - *Cartesian product* $\displaystyle A \times B$ with
$\displaystyle n_A \cdot n_B$ elements ([wiki](https://w.wiki/zus))
- [ ] `Sum[A, B]` - *Disjoint-* or *tagged union* (the *sum type* in type theory)
$\displaystyle A \sqcup B$ with $\displaystyle n_A + n_B$ elements

## Development

Install the [maturin import hook](https://www.maturin.rs/import_hook.html) in the uv project:

```shell
uv run -m maturin_import_hook site install --detect-uv
```

Linting, formatting, typechecking, and testing:

```shell
uv run ruff check
uv run ruff format
uv run basedpyright
uv run pytest
```

## More info

- [Set (mathematics) - Wikipedia](https://w.wiki/3ryH)
- [Algebra of sets - Wikipedia]([wiki](https://w.wiki/EMsH))
- [List of set identities and relations - Wikipedia](https://w.wiki/EMsU)
