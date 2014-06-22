import QtQuick 2.1
import QtQuick.Window 2.1

RectWithCorner {
    id: rect
    radius: 6
    cornerDirection: "up"

    property int borderMargin: 10
    property int textMargin: 10
    
	property int windowPadding: 10
	property int windowOffsetX: -50
	property int windowOffsetY: 5
    property int minWindowWidth: 300
	
	property int mouseX: 0
	property int mouseY: 0
    property bool hideCorner: false
    
    function resetCorner() {
        hideCorner = false
    }
    
    function searchMode() {
        hideCorner = true
        windowView.clear_translate()
        toolbar.entry.activeFocus()
    }
    
	function adjustPosition() {
        var x = 0
        var pos = 0
        if (mouseX - windowView.width / 2 < 0) {
            x = windowPadding
            pos = mouseX - x
        } else if (mouseX + windowView.width / 2 > Screen.width) {
            x = Screen.width - windowView.width - windowPadding
            pos = mouseX - x
        } else {
            x = mouseX - windowView.width / 2
            pos = windowView.width / 2
        }
        cornerPos = pos
        if (qVersion == "5.1") {
            windowView.x = x + windowView.width / 2
        } else {
            windowView.x = x
        }
		
		var y = mouseY + windowOffsetY
		var direction = "up"
		if (y < 0) {
			y = windowPadding
		} else if (y + windowView.height > Screen.height) {
			y = mouseY - windowView.height - windowOffsetY
			direction = "down"
		}
        if (qVersion == "5.1") {
		    windowView.y = y + windowView.height / 2
        } else {
		    windowView.y = y
        }
        
        if (hideCorner) {
            cornerDirection = "none"
        } else {
		    cornerDirection = direction
        }
	}
}
