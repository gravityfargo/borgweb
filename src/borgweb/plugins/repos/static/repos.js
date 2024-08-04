function openTab(tabId) {
    const triggerTabList = document.querySelectorAll('#RepoTabs button')
    triggerTabList.forEach(triggerEl => {
        const tabTrigger = new bootstrap.Tab(triggerEl)

        triggerEl.addEventListener('click', event => {
            event.preventDefault()
            tabTrigger.show()
        })
    })
    const triggerEl = document.querySelector('#RepoTabs button[data-bs-target="' + tabId + '"]')
    bootstrap.Tab.getInstance(triggerEl).show() // Select tab by name
}