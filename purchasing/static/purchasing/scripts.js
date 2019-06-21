const MEDIUMBREAKPOINT = 768;

document.addEventListener('DOMContentLoaded', () => {

    // main nav scripts
    if (document.querySelector('#mainNav')) {

        // set mobile menu to be collaped onload 
        if (window.innerWidth <= MEDIUMBREAKPOINT) {
            document.querySelector('#navCollapse').classList.remove('show');
        }

        // close mobile menu or show deskop menu on window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth > MEDIUMBREAKPOINT) {
                document.querySelector('#navCollapse').classList.add('show');
            } else if (window.innerWidth <= MEDIUMBREAKPOINT) {
                document.querySelector('#navCollapse').classList.remove('show');
            }
        });

        // side bar nav active styling
        const contentArea = document.querySelector('.page');
        document.querySelectorAll('.sideBarLink').forEach( (link) => {
            if (link.dataset.nav == contentArea.dataset.page)
                link.classList.add('sideBarLinkActive');
        });

    }

});