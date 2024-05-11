const hamburger_icon = document.querySelector('.hambuger-icon');
const close_menu_icon = document.querySelector('.close-icon');
const mobile_menu = document.querySelector('.links-mobile-menu')

hamburger_icon.addEventListener('click', () => {
    mobile_menu.style.right = "0";
})

close_menu_icon.addEventListener('click', () => {
    mobile_menu.style.right = "-300px";
})

document.querySelector(".current-year").textContent = new Date().getFullYear();


// To get the right version of the software without updating everytime the website
if(window.location.href.includes('download')){
    const downdloadLink = document.querySelector('.download')
    const downloadPortable = document.querySelector('.download-portable-link');
    const sourceLink = document.querySelector('.source-code')
    fetch('https://api.github.com/repos/LOUDO56/PyMacroRecord/releases/latest')
        .then(resp => resp.json())
        .then(ver => {
            const setupToDl = 'https://github.com/LOUDO56/PyMacroRecord/releases/download/'+ver.tag_name+'/PyMacroRecord_'+ver.tag_name.replace('v', '')+'_Setup.exe'
            const portableToDl = 'https://github.com/LOUDO56/PyMacroRecord/releases/download/'+ver.tag_name+'/PyMacroRecord_'+ver.tag_name.replace('v', '')+'-portable.exe'
            const sourcetoDl = 'https://github.com/LOUDO56/PyMacroRecord/archive/refs/tags/'+ver.tag_name+'.zip'
            downdloadLink.href = setupToDl;
            downloadPortable.href = portableToDl
            sourceLink.href = sourcetoDl;
        })
}

fetch("/donors.txt")
    .then(res => res.text())
    .then(data => {
        let lastDonators = "";
        maxDonators = 5
        data = data.split(";")
        if(data.length < 5){
            maxDonators = data.length
        }
        for(let i = 0; i < maxDonators; i++){
            if(i == maxDonators - 1 && i != 0) lastDonators += " and " + data[data.length - 1 - i]
            else lastDonators += data[data.length - 1  - i]
            if(i < maxDonators - 1 && maxDonators != 1 && i < maxDonators - 2){
                lastDonators += ","
            }
        }
        document.querySelector(".last-donators").textContent = lastDonators;
        if(maxDonators == 1) document.querySelector(".nb-top-donators").textContent = "last donator: ";
        else document.querySelector(".nb-top-donators").textContent = maxDonators += " last donators: ";
    });