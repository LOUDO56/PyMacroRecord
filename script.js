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
const ageDoc = document.querySelector(".age");
if(ageDoc !== null){
    const dateNow = new Date();
    if(dateNow.getMonth() > 3){
        document.querySelector(".age").textContent = dateNow.getFullYear() - 2005;
    } else {
        document.querySelector(".age").textContent = (dateNow.getFullYear() - 2005) - 1;
    }
}


// To get the right version of the software without updating everytime the website
if(window.location.href.includes('download')){
    const downdloadLink = document.querySelector('.download')
    const downloadPortable = document.querySelector('.download-portable-link');
    const sourceLink = document.querySelector('.source-code')
    fetch('https://api.github.com/repos/LOUDO56/PyMacroRecord/releases/latest')
        .then(resp => resp.json())
        .then(ver => {
            const setupAsset = ver.assets.find(asset => asset.name.endsWith('_Setup.exe'));
            const portableAsset = ver.assets.find(asset => asset.name.endsWith('-portable.exe'));

            if (setupAsset) downdloadLink.href = setupAsset.browser_download_url;
            if (portableAsset) downloadPortable.href = portableAsset.browser_download_url;
            sourceLink.href = ver.zipball_url;
        })
}

fetch("/donors.txt")
    .then(res => res.text())
    .then(data => {
        const donors = data.split(";")
            .map(d => d.trim())
            .filter(d => d.length > 0)
            .reverse()
            .slice(0, 5);

        if (donors.length > 0) {
            const formatter = new Intl.ListFormat('en', { style: 'long', type: 'conjunction' });
            document.querySelector(".last-donators").textContent = formatter.format(donors);
            
            const label = donors.length === 1 ? "last donator: " : `${donors.length} last donators: `;
            document.querySelector(".nb-top-donators").textContent = label;
        }
    });
