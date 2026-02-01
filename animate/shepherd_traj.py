import os
import argparse
from pathlib import Path
import shlex
from chimerax.core.commands import run

parser = argparse.ArgumentParser(description="Load and sync multi-track animation in ChimeraX for shepherd trajectories.")
parser.add_argument('dir', type=str, help='Directory containing the frame files.')
parser.add_argument('--nframes', type=int, default=400, help='Number of frames to load.')
args = parser.parse_args()

directory = Path(args.dir).resolve()
if not directory.is_dir():
    raise ValueError(f"The specified directory does not exist: {directory}")
print(directory.resolve())
num_frames = args.nframes

# 1. Determine Next Available ID
# We scan existing models to find the highest ID used so far.
existing_ids = [m.id[0] for m in session.models]
if existing_ids:
    start_id = max(existing_ids) + 1
else:
    start_id = 1

# Define our three tracks based on the start_id
# If start_id is 2 (because #1 exists), tracks will be #2, #3, #4
DRIVER_ID = start_id
FOLLOWER_1_ID = start_id + 1
FOLLOWER_2_ID = start_id + 2

print(f"Detected existing models. Loading animation into #{DRIVER_ID}, #{FOLLOWER_1_ID}, #{FOLLOWER_2_ID}.")
print(f"Loading {num_frames * 3} files... please wait.")

# 2. Silent Load Loop
with session.triggers.block_trigger('graphics update'):
    for i in range(num_frames):
        frame_str = f"{i:03d}"
        
        # --- Driver (x1) ---
        f_x1 = os.path.join(directory, f"{frame_str}_frame_x1.xyz")
        models = run(session, f"open {shlex.quote(str(f_x1))}", log=False)
        m1 = models[0]
        m1.id = (DRIVER_ID, i)
        m1.name = f"Frame {i}"
        m1.display = False 
        
        # --- Follower 1 (x3) ---
        f_x3 = os.path.join(directory, f"{frame_str}_frame_x3.bild")
        models = run(session, f"open {shlex.quote(str(f_x3))}", log=False)
        m2 = models[0]
        m2.id = (FOLLOWER_1_ID, i)
        m2.display = False 

        # --- Follower 2 (x4) ---
        f_x4 = os.path.join(directory, f"{frame_str}_frame_x4.bild")
        models = run(session, f"open {shlex.quote(str(f_x4))}", log=False)
        m3 = models[0]
        m3.id = (FOLLOWER_2_ID, i)
        m3.display = False 

# 3. Dynamic Sync Logic
last_frame_idx = -1

def sync_frames(trigger_name, data):
    global last_frame_idx, DRIVER_ID, FOLLOWER_1_ID, FOLLOWER_2_ID
    
    try:
        # A. FIND DRIVER: Check the specific DRIVER_ID we calculated
        current_frame_idx = None
        
        for m in session.models:
            if m.id[0] == DRIVER_ID and m.display:
                current_frame_idx = m.id[1]
                break
        
        if current_frame_idx is None or current_frame_idx == last_frame_idx:
            return

        # B. UPDATE FOLLOWERS
        # Hide OLD followers
        if last_frame_idx != -1:
            old_models = [m for m in session.models if (m.id == (FOLLOWER_1_ID, last_frame_idx) or m.id == (FOLLOWER_2_ID, last_frame_idx))]
            for m in old_models:
                m.display = False

        # Show NEW followers
        new_models = [m for m in session.models if (m.id == (FOLLOWER_1_ID, current_frame_idx) or m.id == (FOLLOWER_2_ID, current_frame_idx))]
        for m in new_models:
            m.display = True
        
        last_frame_idx = current_frame_idx

    except Exception:
        pass

# 4. Register Handler
# We generate a unique handler name so this doesn't conflict with previous runs
handler_name = f'sync_handler_{DRIVER_ID}'
if hasattr(session, handler_name):
    session.triggers.remove_handler(getattr(session, handler_name))

# Attach handler
new_handler = session.triggers.add_handler('new frame', sync_frames)
setattr(session, handler_name, new_handler)

print("Loading complete.")

# 5. Launch Slider
# Show first frame of driver to kickstart
start_model = [m for m in session.models if m.id == (DRIVER_ID, 0)]
if start_model:
    start_model[0].display = True

run(session, f"mseries slider #{DRIVER_ID}")
