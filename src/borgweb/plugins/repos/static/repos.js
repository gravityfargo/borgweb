
function set_active_tab(tabId) {
    const all_tabs = document.getElementsByClassName("nav-item");
    for (let i = 0; i < all_tabs.length; i++) {
        all_tabs[i].classList.remove("active");
    }
    document.getElementById(tabId).classList.add("active");
    
}