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


function getOS() {
    const ua = navigator.userAgent;
    if (/windows/i.test(ua)) return 'windows';
    if (/linux/i.test(ua) && !/android/i.test(ua)) return 'linux';
    return 'other';
}

const os = getOS();

fetch('https://api.github.com/repos/LOUDO56/PyMacroRecord/releases/latest')
    .then(resp => resp.json())
    .then(release => {
        const setupAsset    = release.assets.find(a => a.name.endsWith('-setup.exe'));
        const portableAsset = release.assets.find(a => a.name.endsWith('-portable.exe'));
        const appImageAsset = release.assets.find(a => a.name.endsWith('.AppImage'));

        const heroBtn = document.getElementById('hero-download-btn');
        const hint    = document.getElementById('download-os-hint');
        if (!heroBtn) return;

        if (os === 'windows' && setupAsset) {
            heroBtn.href = setupAsset.browser_download_url;
            let hintHTML = 'for Windows — Setup';
            if (portableAsset)
                hintHTML += ` · <a href="${portableAsset.browser_download_url}" class="linked">portable version</a>`;
            hint.innerHTML = hintHTML;
        } else if (os === 'linux' && appImageAsset) {
            heroBtn.href = appImageAsset.browser_download_url;
            hint.textContent = 'for Linux — AppImage';
        } else {
            heroBtn.href = 'https://github.com/LOUDO56/PyMacroRecord/releases/latest';
            hint.textContent = 'view all releases on GitHub';
        }
    });

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
