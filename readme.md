# Installation of gan-phsp #

Author: Tobias Stäuble

The reference installation was done on a Windows machine using WSL 1 with an Ubuntu 18.04 distribution. You should however be able to follow these instruction for most Unix systems.

## Preparation
`sudo apt-get update`

### Dependencies 
`sudo apt-get install git dpkg-dev cmake g++ gcc binutils libx11-dev libxpm-dev libxft-dev libxext-dev libpng-dev liblzma-dev libjpeg-dev python python-dev mesa-utils libtool automake build-essential libssl-dev`

## Root
`cd install`  
`curl https://root.cern/download/root_v6.20.04.source.tar.gz | tar xvz`  
`mkdir builds`  
`cd builds && mkdir root`  
`cd root`  
`cmake ../../root-6.20.04/`  
`cmake --build .`  

Update path with: `source bin/thisroot.sh`

## Geant4
`cd install`  
`curl http://geant4-data.web.cern.ch/geant4-data/releases/geant4.10.06.p02.tar.gz | tar xvz`  
`cd builds && mkdir geant4 && geant4-build`  
`cd geant4-build`  
`cmake -DCMAKE_INSTALL_PREFIX=<PATH TO geant4 DIR IN BUILDS DIR> ../../geant4.10.06.p02/`  
`make -j4`  
`sudo make install`  

Geant4 is now installed at `<PATH TO geant4 DIR IN BUILDS DIR>`.

Update path with: `source <installdir>/bin/geant4.sh`

## Libtorch
On the pytorch website, select (Stable, Linux, LibTorch, C++/Java, None or CUDA depending on whether a GPU is available) and download the cxx11 ABI file.  
Note: I downloaded 1.3.1 and not the newest version as it seems to have compatiblity issues with gcc.  
Extract the ZIP contents to `install/libtorch/` folder.  


## Gate
Download and extract Gate 9.0 to the `install` folder.  
`cd Gate-9.0`  
`sudo apt-get install cmake-curses-gui qt5-default libxmu-dev`  
`cd builds && mkdir gate-9-build && mkdir gate-9`  
`cd gate-9-build`  
`ccmake ../../Gate-9.0 -DCMAKE_INSTALL_PREFIX=/mnt/c/Users/mlsostt/Documents/gan-phsp/install/builds/gate-9`  

Hit `c` to configure, then enable `GATE_USE_TORCH`. Hit `c` again. Now an error shows up, but if you go to the variable definitions again, you can now configure `Torch_DIR`.

Set `Torch_DIR` to `<PATH TO installdir>/libtorch/share/cmake/Torch`. Hit `c` again. If it succeeds, hit `g`. 

`make -j4`
`sudo make install`

`export PATH=/<PATH TO gate-9 dir in install folder>/bin:$PATH`


## GAN 4 Gate (GAGA)
`sudo apt-get install python3-pip`
`pip3 install gaga-phsp`
`pip3 install gatetools`
`pip3 install torch===1.5.1 torchvision===0.6.1 -f https://download.pytorch.org/whl/torch_stable.html`


To be continued.