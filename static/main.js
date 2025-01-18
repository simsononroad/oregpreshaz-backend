window.addEventListener("DOMContentLoaded", (event) => {
	const toggleButton = document.getElementsByClassName('toggle-button')[0]
	const navbarLinks = document.getElementsByClassName('navbar-links')[0]
	const BrandTitle = document.getElementsByClassName('brand-title')[0]

	toggleButton.addEventListener('click', () => {
		navbarLinks.classList.toggle('active')
	})
	BrandTitle.addEventListener('click', () => {
		window.open("/")
	})
})



function element(){
	const element_btn = document.getElementsByClassName('element-button')[0]
	const element_btn_del = document.getElementsByClassName('element-button-del')[0]
	element_btn.classList.toggle('active')
	element_btn_del.classList.toggle('active')
	var text = document.getElementById("element-text").innerHTML="Felhasználónév: @dani:oregpreshaz.eu"
}

function element_del(){
	const element_btn = document.getElementsByClassName('element-button')[0]
	const element_btn_del = document.getElementsByClassName('element-button-del')[0]
	element_btn.classList.toggle('active')
	element_btn_del.classList.toggle('active')
	var text = document.getElementById("element-text").innerHTML=""
}

function select_message(message){
	var inp = document.getElementById("delete_msg")
	inp.innerText=message
	
}

function del(){
	window.open ('/dashboard#chat-box','_self',false)
}
