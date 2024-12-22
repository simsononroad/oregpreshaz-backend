function en() {
    window.open("?l=en", "_self")
}
function de() {
    window.open("?l=de", "_self")
}
function hu() {
    window.open("?l=hu", "_self")

}

window.addEventListener("DOMContentLoaded", (event) => {
    let language = "hu"

    if (location.search.search("l=en") > 0) {
        language = "en"
    }
    else {
        if (location.search.search("l=de") > 0) {
            language = "de"
        }
    }
    if (location.search.search("l=2016") > 0) {
        alert("ÍSZTÖR EGG")
    }
    if (location.search.search("l=dani") > 0) {
        alert("2016, 2024, 2009, SZEKAI,")
    }
    if (location.search.search("l=how") > 0) {
        alert("only visual studio code")
    }
    for (let lang of ["en", "de", "hu"]) {
        if (lang == language) {
            console.log("Show: " + lang)
            for (let el of document.querySelectorAll('.'+lang)) {
                el.style.display = 'block';
            }
        } else {
            console.log("Hide: " + lang)
            for (let el of document.querySelectorAll('.'+lang)) {
                el.style.display = 'none';
            }
        }
    }
})