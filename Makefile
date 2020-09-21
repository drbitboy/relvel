########################################################################
### Run model near Closest Approach (CA) of ORX S/C
### & offset instrument for linear flyby of Bennu
###
### Usage:  make [run]      ### Run model around CA
###         make orx.bsp    ### Use SPICE PINPOINT utility to create SPK
###         make pinpoint   ### Download PINPOINT binary; see SPICE_OS
###         make clean      ### Remove SPK
###         make deepclean  ### Remove SPK and PINPOINT binary
########################################################################
### Edit SPICE_OS variable value for non-Linux and/or non-64-bit system
### - Cf. https://naif.jpl.nasa.gov/naif/utilities.html

SPICE_OS = PC_Linux_64bit

###
### End of configuration
########################################################################

run: orx.bsp
	python relvel.py orx.bsp defs.pinpoint

orx.bsp: Makefile defs.pinpoint pinpoint
	$(RM) $@
	./pinpoint -def defs.pinpoint -spk $@
	brief -t -c $@ | grep '[^ ]'

pinpoint:
	wget -nv naif.jpl.nasa.gov/pub/naif/utilities/$(SPICE_OS)/pinpoint
	chmod a+x pinpoint

deepclean: clean
	$(RM) pinpoint
clean:
	$(RM) orx.bsp relvel.json
