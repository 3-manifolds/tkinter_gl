# -*- tcl -*-
# Tcl package index file, version 1.1
#
if {[package vsatisfies [package provide Tcl] 9.0-]} {
    package ifneeded Tkgl 1.1 \
	    [list load [file join $dir libtcl9Tkgl1.1.dylib] [string totitle Tkgl]]
} else {
    package ifneeded Tkgl 1.1 \
	    [list load [file join $dir libTkgl1.1.dylib] [string totitle Tkgl]]
}
