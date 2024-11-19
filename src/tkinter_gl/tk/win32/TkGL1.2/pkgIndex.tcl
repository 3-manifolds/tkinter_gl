if {[package vsatisfies [package provide Tcl] 9.0-]} { 
package ifneeded Tkgl 1.2 [list load [file join $dir tcl9Tkgl12.dll]] 
} else { 
package ifneeded Tkgl 1.2 [list load [file join $dir Tkgl12.dll]] 
} 
