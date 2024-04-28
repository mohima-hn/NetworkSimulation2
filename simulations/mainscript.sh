#!/bin/bash
# Filename: mainscript.sh
# shell script
# @author Mohima Hossain

# change our current directory to ~/Projects
cd /samples/mohima/NetworkSimulation2/simulations/

#print working directory
pwd
#-------------------------------------------------------------------------------------
#command to save the log in command.log
#exec 1> command.log 2>&1
#set -x
#-------------------------------------------------------------------------------------
python script_graph.py
echo creating config.xml
#=====================================================================================
#**********Get the value from the input text file and creating omnetpp.ini************
#=====================================================================================
echo ---------------------------------------------------------------------------------
echo Loading the input text file
echo ---------------------------------------------------------------------------------
python load_script.py
echo Creating omnetpp.ini with configuration
echo ---------------------------------------------------------------------------------
pwd
#======================================================================================
#***********************************Buid the project***********************************
#======================================================================================
echo -------------------------------------------------------------------------------------
echo Build the project
echo -------------------------------------------------------------------------------------
cd ../
make cleanall
make makefiles
make MODE=release all V=1


#23:48:22 **** Incremental Build of configuration release for project inet4.5 ****
#make MODE=release -j8 all
#make[1]: Entering directory '/c/Omnet+/omnetpp-6.0/samples/mohima/inet4.5/src'
#*** CCACHE not detected - using precompiled headers
#*** COMPILING with:
#clang++ -c  -O3 -DNDEBUG=1 -ffp-contract=off   -MMD -MP -MF .d    -isystem /mingw64/include -isystem /opt/mingw64/include -Wno-deprecated-register -Wno-unused-function -fno-omit-frame-pointer -DWITH_QTENV -DWITH_NETBUILDER -DWITH_OSG -DINET_EXPORT  -Wno-overloaded-virtual -include inet/common/precompiled_release.h -DOMNETPPLIBS_IMPORT -DINET_EXPORT -I. -I/c/Omnet+/omnetpp-6.0/include
#*** LINKING with:
#clang++ -shared  -o ../out/clang-release/src/libINET.dll  -Wl,--whole-archive  -Wl,--no-whole-archive -loppenvir -loppsim -lstdc++    -fuse-ld=lld  -L/usr/bin -L/mingw64/lib -L/opt/mingw64/lib -L/c/Omnet+/omnetpp-6.0/lib -Wl,--out-implib,../out/clang-release/src/libINET.dll.a -Wl,--output-def,../out/clang-release/src/libINET.def -lws2_32
#Building...


#=========================================================================================
#********************************Run the simulation***************************************
#=========================================================================================
echo -------------------------------------------------------------------------------------
echo Run the simulation
echo -------------------------------------------------------------------------------------
pwd
cd simulations/
pwd
opp_run -m -u Cmdenv -n .:../src:../../inet4.5/examples:../../inet4.5/showcases:../../inet4.5/src:../../inet4.5/tests/validation:../../inet4.5/tests/networks:../../inet4.5/tutorials -x inet.common.selfdoc:inet.linklayer.configurator.gatescheduling.z3:inet.emulation:inet.showcases.visualizer.osg:inet.examples.emulation:inet.showcases.emulation:inet.transportlayer.tcp_lwip:inet.applications.voipstream:inet.visualizer.osg:inet.examples.voipstream --image-path=../../inet4.5/images -l ../../inet4.5/src/INET omnetpp.ini
#=========================================================================================
#********************************Save the simulation result*******************************
#=========================================================================================
echo -------------------------------------------------------------------------------------
echo Save the Result
echo -------------------------------------------------------------------------------------
cd results/
pwd
#opp_scavetool x *.vec -o result_vector.csv
#opp_scavetool x *.vec -o result_vector.json
#opp_scavetool x *.sca -o result_scaler.csv
opp_scavetool x *.sca -o result_scaler.json
opp_scavetool x General-#0.sca -f module=~\"NetworkSimulation2.router**.ppp**.queue.fifo\" -o router.json
#strace



