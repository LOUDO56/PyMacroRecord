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
    const downdloadLink = document.querySelector('.download');
    const sourceLink = document.querySelector('.source-code');
    const portableLink = document.querySelector('.download-portable-link');
    fetch('https://api.allorigins.win/get?url=https://pastebin.com/raw/8YAjs4Pc')
        .then(resp => resp.json())
        .then(ver => {
            const versionToDl = 'https://github.com/LOUDO56/PyMacroRecord/releases/download/v'+ver.contents+'/PyMacroRecord_'+ver.contents+'_Setup.exe'
            const portableToDl = 'https://github.com/LOUDO56/PyMacroRecord/releases/download/v'+ver.contents+'/PyMacroRecord_'+ver.contents+'-portable.exe'
            const sourcetoDl = 'https://github.com/LOUDO56/PyMacroRecord/archive/refs/tags/v'+ver.contents+'.zip'
            downdloadLink.href = versionToDl;
            sourceLink.href = sourcetoDl;
            portableLink.href = portableToDl;
        });
}