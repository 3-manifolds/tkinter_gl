if {[package vsatisfies [package provide Tcl] 9.0-]} { 
package ifneeded Tkgl 1.0 [list load [file join $dir tcl9Tkgl10t.dll]] 
} else { 
package ifneeded Tkgl 1.0 [list load [file join $dir Tkgl10t.dll]] 
} 
