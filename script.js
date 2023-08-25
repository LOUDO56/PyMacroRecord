const hamburger_icon = document.querySelector('.hambuger-icon');
const close_menu_icon = document.querySelector('.close-icon');
const mobile_menu = document.querySelector('.links-mobile-menu')

hamburger_icon.addEventListener('click', () => {
    mobile_menu.style.right = "0";
})

close_menu_icon.addEventListener('click', () => {
    mobile_menu.style.right = "-300px";
})


// To get the right version of the software without updating everytime the website
if(window.location.href.includes('download')){
    const downdloadLink = document.querySelector('.download')
    fetch('https://api.allorigins.win/get?url=https://pastebin.com/raw/8YAjs4Pc')
        .then(resp => resp.json())
        .then(ver => {
            const versionToDl = 'https://github.com/LOUDO56/PyMacroRecord/releases/download/'+ver.contents+'/PyMacroRecord_'+ver.contents+'_Setup.exe'
            downdloadLink.href = versionToDl;
        })
}