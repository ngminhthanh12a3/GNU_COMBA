#!/bin/bash

# yosys -p 'read_verilog top.v; read_verilog -D ICE40_HX -lib -specify +/ice40/cells_sim.v; hierarchy -check; proc; stat'
/home/thanh/bin_tools/synlig/synlig -p 'read_systemverilog top.v; read_verilog -D ICE40_HX -lib -specify +/ice40/cells_sim.v; synth; tee -o out.json stat -json'