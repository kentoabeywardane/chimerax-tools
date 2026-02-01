# ChimeraX Tips & Examples

A curated, copy‑paste‑friendly collection of ChimeraX command‑line tips for common structural biology visualization tasks.

---

## Quick recipes (copy–paste friendly)

### Clean publication-style cartoon (single model)

```bash
set bgColor white; select #1 & C; color sel light steel blue; lighting shadows false; graphics silhouettes true; lighting flat; select clear
```

### Fade most of a structure, keep region opaque

```bash
set bgColor white; select #1.2-100 & C; color sel light steel blue; select #1.2-100; transparency sel 90 target a; lighting shadows false; graphics silhouettes true; lighting flat; select clear
```

### Binding site interactions (ligand-focused)

```bash
hbonds #1 & ligand reveal true log true
```

```bash
contacts #1 & ligand makePseudobonds false reveal true log true
```

```bash
show solvent & #2-9 :<5.5
```

### Binding-site-only view

```bash
select ligand :<4.5 & protein; hide ~sel target ar; sel clear; show ligand
```

### Transparent context + focused ligand

```bash
transparency 75 target r
```

```bash
transparency 75 target a
```

```bash
sel ligand; transparency sel 0 target a; sel clear
```

### Surface around ligand

```bash
surface zone #1 near ligand dist 8 max 1; surface transparency 50
```

---

## Coloring tips and examples

### Color ligand or specific selections

```bash
select #1 & ligand & C
color sel light steel blue
select clear
```

```bash
color sel dark slate grey
```

### Color by element / heteroatoms

```bash
color #1 byhetero
color C dark slate grey
```

### Color only a single chain

```bash
color /A sky blue
```

---

## Binding site visualization tips

### Show only the binding site region

```bash
select ligand :<4.5 & protein
hide ~sel target ar
sel clear
show ligand
```

### Surface around ligand only

```bash
surface protein & ligand :<5 visiblePatches 1
```

### Hydrophobic and electrostatic surfaces

```bash
mlp   # hydrophobic surface
coulombic   # electrostatic potential surface
```

### Zoning surface around ligand

```bash
surface zone #1 near ligand dist 8 max 1
surface transparency 50
```

---

## Binding site interaction tips

### Hydrogen bonds

```bash
hbonds #1 & ligand reveal true log true
```

### Contacts (non‑H‑bond)

```bash
contacts #1 & ligand makePseudobonds false reveal true log true
```

### Waters near binding site

```bash
show solvent & #2-9 :<5.5
```

### Create custom pseudobonds

Likely hydrogen bond:

```bash
pbond /A:614@O /A:901@NAU reveal true color yellow radius 0.075 dashes 7 name likely_hbond
```

Likely salt bridge:

```bash
pbond /A:901@NBI /A:618@CD reveal true color magenta radius 0.075 dashes 12 name likely_saltbridge
```

---

## Highlighting tips

### Transparency tricks

Transparent ribbons:

```bash
transparency 75 target r
```

Transparent atoms:

```bash
transparency 75 target a
```

Make ligand opaque again:

```bash
sel ligand
transparency sel 0 target a
sel clear
```

### Highlight specific regions manually

(Select atoms interactively with Shift + Ctrl)

```bash
transparency #12 50 target ac
transparency sel 0 target ac
```

### Outline selection

```bash
graphics sel col black width 6
```

More advanced outlining:

* [https://www.jameslingford.com/blog/chimerax-outlines/](https://www.jameslingford.com/blog/chimerax-outlines/)

---

## PDB / protein tips

### Delete a chain

```bash
delete /B
```

### Align structures

```bash
mmaker #2 to #1
```

### Color residues by heteroatoms

```bash
sel /R
color sel byhetero
sel clear
```

---

## Extra resources links

* ChimeraX tutorials (comparative structures):
  [https://rbvi.github.io/chimera-tutorials/presentations/modules/chimerax-comp-structures/index.html](https://rbvi.github.io/chimera-tutorials/presentations/modules/chimerax-comp-structures/index.html)

* ChimeraX tutorial PDF:
  [https://dasher.wustl.edu/bio5357/software/chimerax/tutorial.pdf](https://dasher.wustl.edu/bio5357/software/chimerax/tutorial.pdf)

* Binding site tutorial (official docs):
  [https://www.cgl.ucsf.edu/chimerax/docs/user/tutorials/binding-sites.html](https://www.cgl.ucsf.edu/chimerax/docs/user/tutorials/binding-sites.html)

* Binding site tutorial (RBVI mirror):
  [https://www.rbvi.ucsf.edu/chimerax/docs/user/tutorials/binding-sites.html](https://www.rbvi.ucsf.edu/chimerax/docs/user/tutorials/binding-sites.html)
