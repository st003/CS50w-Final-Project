const MEDIUMBREAKPOINT = 768;

document.addEventListener('DOMContentLoaded', () => {

    // main nav scripts
    if (document.querySelector('#mainNav')) {

        const navCollapse = document.querySelector('#navCollapse');
        const contentArea = document.querySelector('.contentArea');
        
        // set mobile optimizations onload 
        if (window.innerWidth <= MEDIUMBREAKPOINT) {
            navCollapse.classList.remove('show');
            contentArea.style.height = 'auto';
        }

        // update mobile optimzations on window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth > MEDIUMBREAKPOINT) {
                navCollapse.classList.add('show');
                contentArea.style.height = 'calc(100vh - 4em)';
                contentArea.style.overflowY = 'scroll';
            } else if (window.innerWidth <= MEDIUMBREAKPOINT) {
                navCollapse.classList.remove('show');
                contentArea.style.height = 'auto';
                contentArea.style.overflowY = none;
            }
        });

        // side bar nav active styling
        const page = document.querySelector('.page');
        document.querySelectorAll('.sideBarLink').forEach( (link) => {
            if (link.dataset.nav == page.dataset.page)
                link.classList.add('sideBarLinkActive');
        });

    }

});