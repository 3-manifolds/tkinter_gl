if {[package vsatisfies [package provide Tcl] 9.0-]} { 
package ifneeded Tkgl 1.1 [list load [file join $dir tcl9Tkgl11.dll]] 
} else { 
package ifneeded Tkgl 1.1 [list load [file join $dir Tkgl11.dll]] 
} 
