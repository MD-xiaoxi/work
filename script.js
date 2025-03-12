document.addEventListener('DOMContentLoaded', function() {
    const postButton = document.getElementById('post-button');
    const postContentInput = document.getElementById('post-content');
    const postList = document.querySelector('.post-list');

    postButton.addEventListener('click', function() {
        const content = postContentInput.value.trim();
        if (content !== '') {
            const post = document.createElement('div');
            post.classList.add('post');
            post.innerHTML = `
                <div class="content">${content}</div>
            `;
            postList.appendChild(post);
            postContentInput.value = '';
        }
    });
});
