'use strict';
let baseURL = 'http://127.0.0.1:8000';
let ProjectsURL = 'http://127.0.0.1:8000/api/projects/';

let token = localStorage.getItem('TOKEN');
if (token) {
    document.querySelector('.btn-primary').style.display = 'none';
} else {
    document.querySelector('.btn-danger').style.display = 'none';
}

let getProjects = () => {
    fetch(ProjectsURL)
        .then(response => response.json())
        .then(data => {
            // console.log(data);
            buildProjects(data);
        });
};

let buildProjects = projects => {
    let projectWrapper = document.querySelector('#projects_wrapper');
    projectWrapper.innerHTML = '';
    for (let index = 0; index < projects.length; index++) {
        const project = projects[index];
        let projectCard = `
                <div class="project--card">
                    <img src="http://127.0.0.1:8000${project.featured_image}" />
                    
                    <div>
                        <div class="card--header">
                            <h3>${project.title}</h3>
                            <strong class="vote--option" data-vote="up" data-project="${project.id}" >&#43;</strong>
                            <strong class="vote--option" data-vote="dn" data-project="${project.id}"  >&#8722;</strong>
                        </div>
                        <i>${project.vote_ratio}% Positive feedback </i>
                        <p>${project.description.substring(0, 150)}</p>
                    </div>
                
                </div>
        `;
        projectWrapper.innerHTML += projectCard;
    }
    addVotes();
};

let addVotes = () => {
    let voteButton = document.querySelectorAll('.vote--option');

    voteButton.forEach(element => {
        element.addEventListener('click', e => {
            let vote = e.target.dataset.vote;
            let project = e.target.dataset.project;
            // token stored in localStorage Chrome->Application->storage->local Storage as key value pair
            token = localStorage.getItem('TOKEN');
            if (!token) {
                alert('You must be logged in to vote')
            }

            // POST request using fetch()
            fetch(`${baseURL}/api/projects/${project}/vote/`, {
                method: 'POST',
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                    Authorization: `Bearer ${token}`,
                },

                body: JSON.stringify({
                    value: vote,
                }),
            })
                // Converting to JSON
                .then(response => response.json())

                // Displaying results to console
                .then(data => {
                    // console.log('SUCCESS ', data);
                    getProjects();
                });
        });
    });
};
getProjects();
