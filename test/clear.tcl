# Fills a square with a solid color which changes with <Enter>
# or <Leave> events.

# Make sure that the tkGL and  tcl3dogl packares are in your auto_path!

package require Tkgl
if {[catch {package require tcl3dogl}]} {
    puts "This demo requires the package tcl3dogl, which is included with tcl3d."
    exit 1
}

set current_color blue

set draw {
    if {0 <= [winfo pointerx %W] < [winfo width %W] &&
	0 <= [winfo pointery %W] < [winfo height %W]} {
	draw_impl %W blue
	set current_color blue
    } else {
	draw_impl %W purple
	set current_color purple
    }
}

proc draw_impl {widget color} {
    $widget makecurrent
    if {$color == "blue"} {
	glClearColor 0.0 0.0 1.0 1.0
    } else {
	glClearColor 1.0 0.0 1.0 1.0
    }
    glClear GL_COLOR_BUFFER_BIT
    $widget swapbuffers
}

tkgl .w
bind .w <Enter> {draw_impl %W blue}
bind .w <Leave> {draw_impl %W purple}
bind .w <Map> $draw 
bind .w <Expose> $draw
puts "Using [.w glversion]"
pack .w -expand 1 -fill both -padx 50 -pady 50
