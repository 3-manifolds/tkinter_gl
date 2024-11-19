if {[package vsatisfies [package provide Tcl] 9.0-]} { 
package ifneeded Tkgl 1.2.1 [list load [file join $dir tcl9Tkgl121.dll]] 
} else { 
package ifneeded Tkgl 1.2.1 [list load [file join $dir Tkgl121t.dll]] 
} 
