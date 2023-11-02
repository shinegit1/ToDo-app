# wrtie test here for all view classes

import pytest
from todo.views import HomePageView
from pytest_django.asserts import assertRedirects
from todo.models import CustomUser, TodoTask
from django.urls import reverse_lazy
from django.db.models import Q


# Test for HomeView
@pytest.mark.integration
def test_home_page_view(rf, client):
    home_page_url = '/'
    request1 = rf.get(home_page_url)
    view = HomePageView()
    view.setup(request1)
    response = client.get(home_page_url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.integration
def test_urls_with_login_required(client):
    url_list = ["/todoboard/", "/create-task/", "/logout/", "/update-task/1/", '/delete-task/1/']

    # default user is anonymous
    # assert that the anonymous user is redirected to login page

    for url in url_list:
        response = client.get(url)
        expected_url = '/login/' + "?next="+ url
        assertRedirects(response, expected_url=expected_url, status_code=302, fetch_redirect_response=False)


@pytest.mark.django_db
@pytest.mark.integration
def test_signup_view(client):
    signup_page_url = "/signup/"

    response1 = client.get(signup_page_url)
    assert response1.status_code == 200
    # write user's data to create a new account
    data1 = {
        "first_name": "Todo", 
        "last_name":"Task", 
        "email": "todotaskuser@gmail.com", 
        "password1":"password@123",
        "password2":"password@123"
    }
    response2 = client.post(signup_page_url, data1)
    # assert that a user data saved in the database if user redirect to todoboard page
    assertRedirects(response2, expected_url="/todoboard/", status_code=302)
    # assert that the user is authenticated if user data exist in database 
    assert CustomUser.objects.filter(email="todotaskuser@gmail.com").exists()
    # write user's data to create a new account
    data2 = {
        "first_name": "Todo", 
        "last_name":"Task", 
        "email": "dannysmith1@gmail.com", 
        "password1":"Password@123",
        "password2":"Password@123"
    }
    # this time we assert that it raise Exception for user's email ID if email ID already exist in the database
    with pytest.raises(Exception):
        response3 = client.post(signup_page_url, data2)
        assert response3.status_code != 200


@pytest.mark.django_db
def test_logout_view(client):
    redirect_url = reverse_lazy('todo:HomePage')
    user = CustomUser.objects.get(email="dannysmith1@gmail.com")
    # client user is authenticated
    client.force_login(user)

    # assert that the client user is unauthenticated if the page is redirected
    response1 = client.get("/logout/")
    assertRedirects(response1, status_code=301, expected_url=redirect_url)


@pytest.mark.django_db
@pytest.mark.integration
def test_create_todotask_view(client):
    todotask_page_url = reverse_lazy("todo:CreateTodoTask")
    client.login(email="dannysmith1@gmail.com", password="Password@123")
    # write a new task data
    data = {
        'description':"This is my new Task",
        "status": "INPROGRESS",
        "end_date": "2023-11-01",
        "time": "01:40:00"
    }
    response = client.post(todotask_page_url, data)
    # assert that the authenticated user created a new todo task if the user redirect to taskboard page
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.integration
def test_todoboard_view(client):
    todoboard_page_url = reverse_lazy("todo:TodoboardPage")
    client.login(email="dannysmith1@gmail.com", password="Password@123")
    user = CustomUser.objects.get(email="dannysmith1@gmail.com")

    # get all tasks created by an authenticated user
    tasks = TodoTask.objects.filter(user=user)

    # assert that the user's todo tasks redirect to the expected url
    response = client.get(todoboard_page_url, {"object_list":tasks})
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.integration
def test_update_todotask_view(client):
    user = CustomUser.objects.get(email="dannysmith1@gmail.com")
    # get a task of an authenticated user
    task = TodoTask.objects.get(Q(id=1), Q(user=user))
    
    update_task_url = f"/update-task/{task.id}/"
    # authenticate the user to this view
    client.login(email="dannysmith1@gmail.com", password="Password@123")
    update_data = {
        'description':"Update my new Task",
        "status": "COMPLETE",
        "end_date": "2023-11-01",
        "time": "01:40:00"
    }
    # assert that the user is updated task data if the user is redirect to todoboard page (302) success
    response = client.post(update_task_url, update_data)
    assert response.status_code == 302
    


@pytest.mark.django_db
@pytest.mark.integration
def test_delete_todotask_view(client):
    user = CustomUser.objects.get(email="dannysmith1@gmail.com")
    # get a task of an authenticated user
    task = TodoTask.objects.get(Q(id=1), Q(user=user))
    delete_url = f"/delete-task/{task.id}/"
    # authenticate the user to this view
    client.login(email="dannysmith1@gmail.com", password="Password@123")

    # assert that user's task is deleted if authenticated user is redirected
    response = client.get(delete_url)
    assert response.status_code == 302

    task.delete()
    # assert that the given task is not exist in the database if task is deleted
    assert TodoTask.objects.filter(id=task.id, user=user).exists() is False


@pytest.mark.integration
def test_about_page_view(client):
    about_page_url = reverse_lazy("todo:AboutPage")
    response = client.get(about_page_url)
    # assert that the response's status code is matched with 200 (success)
    assert response.status_code == 200
