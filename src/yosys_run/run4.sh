#!/bin/bash

# yosys -p 'read_verilog top.v; read_verilog -D ICE40_HX -lib -specify +/ice40/cells_sim.v; hierarchy -check; proc; stat'
/home/nvmt/bin_tools/oss-cad-suite/bin/yosys -m slang -p 'read_slang top.v; hierarchy -simcheck -auto-top; tee -o out.json stat -json'