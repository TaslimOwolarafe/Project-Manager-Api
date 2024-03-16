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
                
                // Iterate through each project
                data.forEach(function(project) {
                    // Create HTML markup for each project
                    const projectHTML = `
                        <tr>
                            <td>
                                <div>
                                    <div>
                                        <img src="${project.display_photo}" alt="">
                                    </div>
                                    <div>
                                        <h4>${project.title}</h4>
                                        <p>${project.due_date}</p>
                                    </div>
                                </div>
                            </td>
                            <td>
                                <button disabled="disabled">${project.task_counts.total_tasks} tasks</button>
                            </td>
                            <td>
                                <div>
                                    <h3>${project.task_counts.completed_tasks}/${project.task_counts.total_tasks}</h3>
                                    <p>Tasks</p>
                                </div>
                            </td>
                            <td>
                                <div>
                                    <p>Progress</p>
                                </div>
                            </td>
                            <td>
                                ${project.members.map(member => `<div>${member.username}</div>`).join('')}
                            </td>
                        </tr>
                    `;
                    
                    // Append the project HTML to the table body
                    $('#project-tasks').append(projectHTML);
                });
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

    // // Search input event listener
    // $('#search-input').on('input', function () {
        
    // });

    // // Filter select change event listener
    // $('#status-filter').change(function () {
       
    // });
});
