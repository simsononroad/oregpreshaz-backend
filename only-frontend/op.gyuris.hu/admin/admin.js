function send(){
    var nameid = document.getElementById("nameid").value
    var jelszo = document.getElementById("password").value
    if (nameid == "@mariann" || nameid == "1109"){
        if (jelszo == "Pecel.Hogyesz") {
            window.open("admindash.html")
            alert("asd")
        }
    }
    else{
        alert("Nincs ilyen felhasználó!")
    }
}
