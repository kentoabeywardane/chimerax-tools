import os
import argparse
from pathlib import Path
import shlex
from chimerax.core.commands import run
from chimerax.core.models import Model

parser = argparse.ArgumentParser(description="Load and sync multi-track animation in ChimeraX for shepherd trajectories.")
parser.add_argument('dir', type=str, help='Directory containing the frame files.')
parser.add_argument('--nframes', type=int, default=400, help='Number of frames to load.')
parser.add_argument(
    '--x1-only',
    action='store_true',
    help='Load only the x1 atom trajectory (no x3 or x4 BILD files).',
)
args = parser.parse_args()

directory = Path(args.dir).resolve()
if not directory.is_dir():
    raise ValueError(f"The specified directory does not exist: {directory}")
print(directory.resolve())
num_frames = args.nframes
x1_only = args.x1_only

# 1. Build the model hierarchy
# Everything lives under a single top-level group model so the whole
# trajectory shows up as one row in the Models panel and can be hidden or
# shown with a single checkbox. Each track gets its own subgroup, and the
# individual frames are children of those subgroups.
top_group = Model(f"ShEPhERD trajectory ({directory.name})", session)
session.models.add([top_group])

x1_group = Model("x1 (atoms)", session)
session.models.add([x1_group], parent=top_group)

if x1_only:
    x3_group = x4_group = None
else:
    x3_group = Model("x3 (ESP)", session)
    x4_group = Model("x4 (pharmacophores)", session)
    session.models.add([x3_group, x4_group], parent=top_group)

x1_frames = []
x3_frames = []
x4_frames = []

if x1_only:
    print(f"Loading x1 animation into #{top_group.id_string}.")
    print(f"Loading {num_frames} files... please wait.")
else:
    print(f"Loading animation into #{top_group.id_string}.")
    print(f"Loading {num_frames * 3} files... please wait.")

def open_frame(path, parent, index):
    """Open a frame file and move it under the given group model."""
    models = run(session, f"open {shlex.quote(str(path))}", log=False)
    m = models[0]
    m.name = f"Frame {index}"
    m.display = False
    # Reparent so the frame becomes a child of its track group.
    session.models.add([m], parent=parent)
    return m

# 2. Silent Load Loop
with session.triggers.block_trigger('graphics update'):
    for i in range(num_frames):
        frame_str = f"{i:03d}"

        # --- Driver (x1) ---
        f_x1 = os.path.join(directory, f"{frame_str}_frame_x1.xyz")
        x1_frames.append(open_frame(f_x1, x1_group, i))

        if not x1_only:
            # --- Follower 1 (x3) ---
            f_x3 = os.path.join(directory, f"{frame_str}_frame_x3.bild")
            x3_frames.append(open_frame(f_x3, x3_group, i))

            # --- Follower 2 (x4) ---
            f_x4 = os.path.join(directory, f"{frame_str}_frame_x4.bild")
            x4_frames.append(open_frame(f_x4, x4_group, i))

# 3. Dynamic Sync Logic
last_frame_idx = -1

def sync_frames(trigger_name, data):
    global last_frame_idx

    try:
        # A. FIND DRIVER: whichever x1 frame the slider is currently showing
        current_frame_idx = None

        for idx, m in enumerate(x1_frames):
            if not m.deleted and m.display:
                current_frame_idx = idx
                break

        if current_frame_idx is None or current_frame_idx == last_frame_idx:
            return

        # B. UPDATE FOLLOWERS
        # Hide OLD followers
        if last_frame_idx != -1:
            for frames in (x3_frames, x4_frames):
                if last_frame_idx < len(frames) and not frames[last_frame_idx].deleted:
                    frames[last_frame_idx].display = False

        # Show NEW followers
        for frames in (x3_frames, x4_frames):
            if current_frame_idx < len(frames) and not frames[current_frame_idx].deleted:
                frames[current_frame_idx].display = True

        last_frame_idx = current_frame_idx

    except Exception:
        pass

# 4. Register Handler (only needed when x3/x4 follow x1)
if not x1_only:
    # We generate a unique handler name so this doesn't conflict with previous runs
    handler_name = f'sync_handler_{top_group.id_string.replace(".", "_")}'
    if hasattr(session, handler_name):
        session.triggers.remove_handler(getattr(session, handler_name))

    new_handler = session.triggers.add_handler('new frame', sync_frames)
    setattr(session, handler_name, new_handler)

print("Loading complete.")

# 5. Launch Slider
# Show first frame of driver to kickstart
if x1_frames:
    x1_frames[0].display = True

# The slider drives the x1 subgroup; its children are the frames.
run(session, f"mseries slider #{x1_group.id_string}")
