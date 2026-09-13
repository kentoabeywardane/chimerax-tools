# Scripts and tips to help manipulate ChimeraX programmatically

## File structure
```
├── animate
│   └── shepherd_traj.py
├── LICENSE
├── TIPS.md
└── README.md
```

## [`TIPS.md`](TIPS.md)
Look at TIPS.md for quick copy-and-paste commands for ChimeraX

## Animation

### ShEPhERD trajectories: `animate/shepherd_traj.py`
This script loads a ShEPhERD trajectory and creates an `mseries` slider to animate x1, x3, and x4 together. It is impossible to natively use `mseries` to bundle multiple objects and animate them together without the help of this script.

By default, the script expects x1, x3, and x4 files. Use `--x1-only` to
construct a trajectory containing only the x1 atoms.

1. Generate ShEPhERD sample and save trajectory:
```python
from shepherd.inference import generate
samples = generate(
    ...
    store_trajectories=True
)
```

2. Create a folder and save x1, x3, and x4 in the following formats:
```
<trajctory_dir>
├── 000_frame_x1.xyz
├── 000_frame_x3.bild
├── 000_frame_x4.bild
├── ...
├── XXX_frame_x1.xyz
├── XXX_frame_x3.bild
└── XXX_frame_x4.bild
```

This can be done with `shepherd-score`:
```python
from shepherd_score.visualize import chimera_from_sample

nframes = 400               # number of frames in trajectory
sample_idx = 0              # ShEPhERD sample index of interest
save_dir = 'trajctory_dir'  # directory to save trajectory
# Loop through trajectory and save x1, x3, x4
for i in range(nframes - 1):
    frame_name = f'{i:03d}_frame'
    chimera_from_sample(
        samples[sample_idx]['trajectories'][i],
        frame_name,
        save_dir
    )

# Save final frame
chimera_from_sample(
    samples[sample_idx],
    f'{i+1:03d}_frame',
    save_dir
)
```


3. In the ChimeraX window, run:
```
runscript <path/to/repo>/animate/shepherd_traj.py <dir>
```
Optionally use the --nframes flag to choose the number of frames. Default is 400.

To load only the x1 atom trajectory, the directory needs only the
`XXX_frame_x1.xyz` files:
```
runscript <path/to/repo>/animate/shepherd_traj.py <dir> --x1-only
```

This will load all the frames in the trajectory file.

All frames are grouped under a single top-level model in the Models panel, with
one subgroup per track, so the whole trajectory can be hidden or shown with a
single checkbox:
```
#1    ShEPhERD trajectory (<dir>)
├── #1.1  x1 (atoms)
│   ├── #1.1.1  Frame 0
│   └── ...
├── #1.2  x3 (ESP)
└── #1.3  x4 (pharmacophores)
```
