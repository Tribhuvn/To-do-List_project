from django.db import models
from django.http import Http404

# Create your models here.


class UserSession(models.Model):
    session_id = models.AutoField(primary_key=True)


def query_modify(request, query, auth_query):
    """
    Produce a new query set based on anonymous and authenticated user query sets
    :return:new query set object based on custom function
    """
    query.user = request.user
    query.save()
    return auth_query | query


def query_set_modify(request, query_set, auth_query_set):
    """
    Produce a new query set based on anonymous and authenticated user query sets
    :return:new query set object based on custom function
    """
    for query in query_set:
        query.user = request.user
        query.save()
    return auth_query_set | query_set


def get_query_object_or_404(request, model, **kwargs):
    """
    Return a query based on anonymous and authenticated user
    :param model: model name whose object is to be queried
    :return: query object
    """
    session_id = request.session.get('session_id', None)
    if session_id is not None:
        query = model.objects.get(session_id=session_id, **kwargs)

        # The user has recently logged in and has session data
        if query and request.user.is_authenticated:

            # if: User wants to associate his session data with his login user data
            auth_query = model.objects.get(user=request.user, **kwargs)

            if not auth_query:
                query.user = request.user
                query.save()

            # else: There is no login user data
            else:
                # delete session data for the login user
                query.session_id = None
                query.save()
                query = query_modify(request, query, auth_query)
                del request.session['session_id']

    # The user is logged in and has no session data
    elif request.user.is_authenticated:
        query = model.objects.get(user=request.user, **kwargs)
    else:
        raise Http404("No data found matching the query")
    return query


def get_query_set_or_404(request, model, **kwargs):
    """
    Return a query-set based on anonymous and authenticated user
    :param model: model name whose objects are to be queried
    :return: query-set object
    """
    session_id = request.session.get('session_id', None)
    if session_id is not None:
        query_set = model.objects.filter(session_id=session_id, **kwargs)

        # The user has recently logged in and has session data
        if query_set.exists() and request.user.is_authenticated:

            # if: User wants to associate his session data with his login user data
            auth_query_set = model.objects.filter(user=request.user, **kwargs)

            if not auth_query_set.exists():
                for query in query_set:
                    query.user = request.user
                    query.save()

            # else: There is no login user data
            else:
                # delete session data for the login user
                for query in query_set:
                    query.session_id = None
                    query.save()
                query_set = query_set_modify(request, query_set, auth_query_set)
                del request.session['session_id']

    # The user is logged in and has no session data
    elif request.user.is_authenticated:
        query_set = model.objects.filter(user=request.user, **kwargs)
    else:
        query_set = model.objects.none()
        raise Http404("No data found matching the query")
    return query_set


def create_object(request, model, **kwargs):
    """
    Create new model object based on authenticated and anonymous user
    :param model: model name whose objects is to be created
    :return:
    """
    session_id = request.session.get('session_id', None)
    if session_id is not None:
        session = UserSession.objects.get(session_id=session_id)
        obj = model.objects.create(session=session, **kwargs)
    elif request.user.is_authenticated:
        obj = model.objects.create(user=request.user, **kwargs)
    else:
        session = UserSession.objects.create()
        obj = model.objects.create(session=session, **kwargs)
        request.session['session_id'] = obj.session_id
        request.session.set_expiry(None)
    return obj

