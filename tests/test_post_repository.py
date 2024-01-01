import pytest
from datetime import datetime
from lib.posts import Post
from lib.post_repository import PostRepository
from lib.database_connection import DatabaseConnection

# Test case for adding a new post
def test_add_post(db_connection):

    db_connection.seed('seeds/post.sql')
    repository = PostRepository(db_connection)

    content = "Test Post Content"
    user_id = 1
    post_id = repository.add_post(content, user_id)
    
    assert post_id is not None

# Test case for getting a post by ID
def test_get_post_by_id(db_connection):

    db_connection.seed('seeds/post.sql')
    repository = PostRepository(db_connection)

    # Arrange: Add a post
    content = "Test Post Content"
    user_id = 1
    post_id = repository.add_post(content, user_id)
    
    # Act: Retrieve the post by ID
    retrieved_post = repository.get_post_by_id(post_id)
    
    # Assert: Check post details
    assert retrieved_post is not None
    assert retrieved_post.id == post_id
    assert retrieved_post.message == content
    assert retrieved_post.user_id == user_id

# Test case for getting all posts
def test_get_all_posts(db_connection):

    
    db_connection.seed('seeds/post.sql')
    repository = PostRepository(db_connection)

    # Arrange: Add some test posts
    repository.add_post("Post 1", 1)
    repository.add_post("Post 2", 2)
    
    # Act: Retrieve all posts
    all_posts = repository.get_all_posts()
    
    # Assert: Check the number of posts
    assert len(all_posts) >= 2

# Test case for deleting a post
def test_delete_post(db_connection):

        
    db_connection.seed('seeds/post.sql')
    repository = PostRepository(db_connection)
    # Arrange: Add a post
    content = "Test Post Content"
    user_id = 1
    post_id = repository.add_post(content, user_id)
    
    # Act: Delete the post
    repository.delete_post(post_id)
    
    # Assert: Attempt to get the deleted post
    deleted_post = repository.get_post_by_id(post_id)
    assert deleted_post is None

# Test case for updating a post
def test_update_post(db_connection):
    db_connection.seed('seeds/post.sql')
    repository = PostRepository(db_connection)
    # Arrange: Add a post
    content = "Test Post Content"
    user_id = 1
    post_id = repository.add_post(content, user_id)
    
    # Arrange: Create an updated post
    updated_content = "Updated Post Content"
    updated_user_id = 2
    updated_post = Post(post_id, updated_content, updated_user_id, datetime.now().timestamp())
    
    # Act: Update the post
    repository.update_post(updated_post)
    
    # Assert: Check if the post is updated
    retrieved_post = repository.get_post_by_id(post_id)
    assert retrieved_post is not None
    assert retrieved_post.id == post_id
    assert retrieved_post.message == updated_content
    assert retrieved_post.user_id == updated_user_id

# Test case for getting posts by user ID
def test_get_posts_by_user_id(db_connection):
    db_connection.seed('seeds/post.sql')
    repository = PostRepository(db_connection)
    # Arrange: Add posts for a user
    user_id = 1
    repository.add_post("Post 1", user_id)
    repository.add_post("Post 2", user_id)
    
    # Act: Retrieve posts by user ID
    posts = repository.get_posts_by_user_id(user_id)
    
    # Assert: Check the number of posts
    assert len(posts) >= 2
