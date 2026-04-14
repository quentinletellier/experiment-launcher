from pathlib import Path
import argparse
from omegaconf import OmegaConf
from copy import deepcopy
import datetime

from experiment_launcher.configuration_sweeper import ConfigurationSweeper
from experiment_launcher.slurm_launcher import SlurmLauncher
from experiment_launcher.local_launcher import LocalLauncher

parser = argparse.ArgumentParser(prog="experiment_launcher")
parser.add_argument("--config", type=Path, required=True, help="the yaml configuration of the experiment")
parser.add_argument("--script", type=Path, required=True, help="the python script to run")
args = parser.parse_args()

config = dict(OmegaConf.to_object(OmegaConf.load(args.config)))
output_dir = (
    Path(config["launcher"]["output_dir"])
    / datetime.datetime.now().strftime("%m-%d-%y")
    / datetime.datetime.now().strftime("%H-%M-%S")
)
output_dir.mkdir(parents=True)
sweeper = ConfigurationSweeper()
configs, sweep_combinations = sweeper.get_sweeped_configs(config)

for config_idx, job_config in enumerate(configs):
    job_dir = output_dir / str(config_idx)
    job_dir.mkdir()
    OmegaConf.save(job_config, job_dir / "config.yaml")

device = config["launcher"]["device_launcher"]["device"]
if device == "slurm":
    launcher = SlurmLauncher()
elif device == "local":
    launcher = LocalLauncher()
else:
    raise ValueError(
        f'Device {device} is not a valid device. Supported devices: "slurm", "local"'
    )

device_launcher_config = deepcopy(config["launcher"]["device_launcher"])
device_launcher_config.pop("device")

print(f"######\nLaunching {len(configs)} processe(s):")
for sweep_combination in sweep_combinations:
    print(sweep_combination)
print("######\n")

launcher.submit(
    command=f"uv run {args.script}",
    num_jobs=len(configs),
    device_launcher_config=device_launcher_config,
    output_dir=output_dir,
)
