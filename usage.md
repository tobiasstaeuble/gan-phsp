# Overview of Gate and GAGA installation #
main directory: `/home/ubuntu/gan-phsp`

## Locations
`/mac`              .mac files for Simulation
`/output`           generated files by Gate
`/plots`            plots from PHSP files
`/plots_gan`        plots from marginal distribution comparison
`/pth`              configuration files for GAN and generators 


-----------------------------------------------------------------
## Gate usage

`$ source ~/gan-phsp/gate_env.sh`
`$ Gate`                        To start Gate

`$ Gate mac/main.mac`           use Gate from power shell



### example:
`$ Gate mac/main.mac -a '[N,1e4] [JOB_ID,0] [TYPE,gaga]'`
    starts Gate Simulation with GAN generator, alternative 'analog'


### Exercises
`install/GateContrib/dosimetry/Radiotherapy/example3/main.mac`
see the documentation: https://opengate.readthedocs.io/en/latest/index.html

## compile Gate:
Gate was compiled with ccmake in

`$ cd ~/gan-phsp/install/builds/gate-9-build`
`$ ccmake ../gate-specific-build`


-----------------------------------------------------------------

## screen:
For long computation time and possible ssh time out use screen
    to start virtual sessions

`$ screen -S [ID]`              start a session with named [ID]
`$ screen -ls`                  see running screens

`$ 'ctrl' + 'a' + 'd'`                 exit screen
`$ exit`                        exit screen and terminate

`$ screen -r`                   resume screen (when only 1 is running)
                       





-----------------------------------------------------------------
## To convert .IAEAphsp into .root:

`$ source ~/gan-phsp/gate_env.sh`
`$ cd ~/gan-phsp/data/`
`$ ~/gan-phsp/src/phsp_iaea_to_root <input file>`




maybe `$ gt_phsp_convert_iaea` will be available
to directly convert .IAEAphsp to .npy


-----------------------------------------------------------------
## Gate Tools:
the scripts lie in `~/.local/bin`

show help with -h

do not source gate_env.sh -> instead start a new Terminal

`$ gt_gate_info`	            Display info about current Gate/G4 version
`$ gt_phsp_convert`	            Convert a phase space file from root to npy
`$ gt_phsp_info`                Display information about a phase space file
`$ gt_phsp_merge`	            Merge two phase space files (output in npy only)
`$ gt_phps_peaks`	            Try to detect photopeaks (experimental)
`$ gt_phsp_plot`	            Plot marginal distributions form a phase space file





-----------------------------------------------------------------
## GAGA Tools:

`$ gaga_train`                  Train a GAN on a phase space
`$ gaga_convert_pth_to_pt`     Convert pth to a pt and json file for Gate (also specify Z-coordinate)
`$ gaga_plot`                   Marignal Plots for phase space against a GAN

### example:
`$ gaga_convert_pth_to_pt pth/001.pth --no-gpu -k Z 267.0 -v`

Called functions (helper scripts) from these scripts lie in:
`/home/ubuntu/.local/lib/python3.6/site-packages/gaga/gaga_helpers.py`

