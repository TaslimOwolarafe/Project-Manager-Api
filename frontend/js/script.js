function calculateDueTime(dueDate) {
    const now = new Date();
    const dueDateTime = new Date(dueDate);
    
    // Calculate the difference in milliseconds
    const difference = dueDateTime - now;
    
    // Calculate days and minutes
    const days = Math.floor(difference / (1000 * 60 * 60 * 24));
    const minutes = Math.floor((difference / (1000 * 60)) % 60);
    
    return `${days}d, ${minutes}m`;
  }

function formatDate(dateString) {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const date = new Date(dateString);
    const month = months[date.getMonth()];
    const day = date.getDate();
    const year = date.getFullYear();
    return `${month} ${day}, ${year}`;
  }

function toggleActive(button) {
    const buttons = document.querySelectorAll('.nav-item');
    buttons.forEach(btn => btn.classList.remove('active'));

    button.classList.add('active');
}


function createProgressBars() {
    const projectRows = document.querySelectorAll('.project-row');

    projectRows.forEach(row => {
        const completedTasksCell = row.querySelector('.task-ratio h3');
        const progressBarContainer = row.querySelector('.progress');
        const progressBar = document.createElement('div');
        progressBar.classList.add('progress-bar');
        progressBarContainer.appendChild(progressBar);

        const completedTasks = parseInt(completedTasksCell.textContent.split('/')[0]);
        const totalTasks = parseInt(completedTasksCell.textContent.split('/')[1]);
        const progress = (completedTasks / totalTasks) * 100;
        progressBar.style.width = `${progress}%`;
    });
}

$(document).ready(function () {
    const baseUrl = 'http://localhost:8000/';

    // Function to fetch projects based on search term and completion status
    function fetchProjects(searchTerm = '', completed = '') {
        const url = baseUrl + 'projects/?search=' + searchTerm + '&completed=' + completed;
        
        $.ajax({
            url: url,
            dataType: 'json',
            success: function (data) {
                // Clear existing table rows
                $('#project-tasks').empty();
                $('.project-count').empty()
                $('.project-count').append(`${data.length} results found`)
                // Iterate through each project
                data.forEach(function(project) {
                    const dueTime = calculateDueTime(project.due_date);
                    const formattedDateCreated = formatDate(project.date_created);

                    const projectHTML = `
                        <tr class="project-row">
                            <td>
                                <div class="project-title">
                                    <div class="img-container">
                                        <img width='55px' height='55px' id="project-photo-${project.id}" src="${project.display_photo ? project.display_photo : 'https://cdn.pixabay.com/photo/2016/07/07/16/46/dice-1502706_960_720.jpg'}" alt="">
                                    </div>
                                    <div class="title-date">
                                        <h4>${project.title}</h4>
                                        <p>${formattedDateCreated}</p>
                                    </div>
                                </div>
                            </td>
                            <td>
                                <button class="due-in" disabled="disabled">${dueTime}</button>
                            </td>
                            <td>
                                <div class="task-ratio">
                                    <h3>${project.task_counts.completed_tasks} / ${project.task_counts.total_tasks}</h3>
                                    <p>Tasks</p>
                                </div>
                            </td>
                            <td>
                                <div class="progress">
                                    <p><i class="fa-solid fa-bars-progress"></i> Progress</p>
                                    <div class="progress-bar-container">
                    
                                    </div>
                                </div>
                            </td>
                            <td>
                                ${project.members.map(member => `<div>${member.username}</div>`).join('')}
                            </td>
                        </tr>
                    `;
                    
                    $('#project-tasks').append(projectHTML);
                });

                createProgressBars();
            },
            error: function (error) {
                console.error("Error fetching projects:", error);
            }
        });
    }

    fetchProjects();

    // Function to handle Show button click
    $('#show').click(function () {
        const searchTerm = $('#search-input').val().trim();
        const completed = $('#status-filter').val();
        fetchProjects(searchTerm, completed);
    });

    $('.fa-magnifying-glass').click(function () {
        const searchTerm = $('#search-input').val().trim();
        const completed = $('#status-filter').val();
        fetchProjects(searchTerm, completed);
    });
    // // Search input event listener
    // $('#search-input').on('input', function () {
        
    // });

    // // Filter select change event listener
    // $('#status-filter').change(function () {
       
    // });
});
