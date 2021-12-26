let searchForm = document.getElementById('searchForm'); // get the search form
let pageLinks = document.getElementsByClassName('page-link'); // get the page links

if (searchForm) {
    for (let i = 0; pageLinks.length > i; i++) {
        const element = pageLinks[i];
        element.addEventListener('click', function (e) {
            e.preventDefault(); // prevent default page click functionality

            let page = this.dataset.page; // get the data-page attribute

            // append hidden search input to form
            searchForm.innerHTML += `<input value=${page} name="page" value="page" hidden>`;

            // now we can submit the form

            searchForm.submit();
        });
    }
}

let tags = document.getElementsByClassName('edit-tags');
// we are doing this by sending this data via API so that we dont need to send csrf token,
// we can also send this data through forms

for (let i = 0; i < tags.length; i++) {
    tags[i].addEventListener('click', e => {
        let tagId = e.target.dataset.tag;
        let projectId = e.target.dataset.project;
        console.log(tagId);
        console.log(projectId);

        fetch('http://127.0.0.1:8000/api/remove-tag/', {
            method: 'DELETE',
            headers: {
                'Content-type': 'application/json',
            },
            body: JSON.stringify({
                tag: tagId,
                project: projectId,
            }),
        })
            .then(response => response.json())
            .then(data => {
                e.target.remove();
            });
    });
}

document.querySelector('#dropDown').addEventListener('click', e => {
    document.querySelector('.drop-down').classList.toggle('drop-down--active');
});

let anonymous_sender = document.querySelector('.unknown_user');
anonymous_sender.addEventListener('click', e => {
    alert('This user is not registed with us');
});

