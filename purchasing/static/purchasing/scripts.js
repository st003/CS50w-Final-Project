document.addEventListener('DOMContentLoaded', () => {

    // side bar nav active styling
    if (document.querySelector('.sideBar')) {

        const contentArea = document.querySelector('.page');
        document.querySelectorAll('.sideBarLink').forEach( (link) => {
            if (link.dataset.nav == contentArea.dataset.page)
                link.classList.add('sideBarLinkActive');
        });

    }

});