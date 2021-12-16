let searchForm = document.getElementById('searchForm');         // get the search form
let pageLinks = document.getElementsByClassName('page-link');   // get the page links

if (searchForm) {
    for (let i = 0; pageLinks.length > i; i++) {
        const element = pageLinks[i];
        element.addEventListener('click', function (e) {
            e.preventDefault();                                 // prevent default page click functionality

            let page = this.dataset.page;                       // get the data-page attribute

            // append hidden search input to form
            searchForm.innerHTML += `<input value=${page} name="page" value="page" hidden>`;

            // now we can submit the form

            searchForm.submit();
        });
    }
}
