function choice(ch){
    if (ch === "light") {
        light()
    } else if (ch === "dark") {
        dark()
    } else {
        console.log("How?")
    }
}

function light() {
   var element = document.body;
   element.className = ""
   element.classList.add("light")
}
function dark() {
   var element = document.body;
   element.className = ""
   element.classList.add("dark")
}

