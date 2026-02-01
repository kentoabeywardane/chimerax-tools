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

[!NOTE] This ChimeraX script currently only handles trajectories that include x1, x3, *and* x4 files to animate (e.g., cannot handle trajectories with just x1 and x4).

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

This will load all the frames in the trajectory file.
