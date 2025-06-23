// Function that runs once the window is fully loaded
window.onload = function() {
    loadPosts();
}

// Function to fetch all the posts from the API and display them on the page
function loadPosts() {
    fetch('/api/posts')
        .then(response => response.json())
        .then(data => {
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `
                  <h2>${post.title}</h2>
                  <p>${post.content}</p>
                  <p><strong>Author:</strong> ${post.author || 'Unknown'}</p>
                  <p><strong>Date:</strong> ${post.date || 'N/A'}</p>
                  <button onclick="deletePost(${post.id})">Delete</button>
                `;
                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error loading posts:', error));
}

// Function to send a POST request to add a new post
function addPost() {
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;
    var postAuthor = document.getElementById('post-author').value;

    fetch('/api/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: postTitle, content: postContent, author: postAuthor })
    })
    .then(response => response.json())
    .then(post => {
        console.log('Post added:', post);
        loadPosts();
    })
    .catch(error => console.error('Error adding post:', error));
}

// Function to send a DELETE request to delete a post
function deletePost(postId) {
    fetch('/api/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('Post deleted:', postId);
        loadPosts();
    })
    .catch(error => console.error('Error deleting post:', error));
}
