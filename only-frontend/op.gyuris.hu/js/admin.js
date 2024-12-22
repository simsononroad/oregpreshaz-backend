function send(){
    var nameid = document.getElementById("nameid").value
    var jelszo = document.getElementById("password").value
    if (nameid == "@mariann" || nameid == "1109"){
        if (jelszo == "Pecel.Hogyesz") {
            window.open("../admin/admindash.html")
        }
    }
    else{
        alert("Nincs ilyen felhasználó!")
    }
}