#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = "__Jack__"

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from course import views

router = DefaultRouter()
router.register(prefix="viewsets", viewset=views.CourseViewSet)

urlpatterns = [
    # 认证接口
    path("auth/register/", views.RegisterView.as_view(), name="auth-register"),
    path("auth/login/", views.LoginView.as_view(), name="auth-login"),
    path("auth/logout/", views.LogoutView.as_view(), name="auth-logout"),
    path("auth/me/", views.CurrentUserView.as_view(), name="auth-me"),
    # Function Based View
    path("fbv/list/", views.course_list, name="fbv-list"),
    path("fbv/detail/<int:pk>/", views.course_detail, name="fbv-detail"),
    # Class Based View
    path("cbv/list/", views.CourseList.as_view(), name="cbv-list"),
    path("cbv/detail/<int:pk>/", views.CourseDetail.as_view(), name="cbv-detail"),
    # Generic Class Based View
    path("gcbv/list/", views.GCourseList.as_view(), name="gcbv-list"),
    path("gcbv/detail/<int:pk>/", views.GCourseDetail.as_view(), name="gcbv-detail"),
    # DRF viewsets
    # path("viewsets/", views.CourseViewSet.as_view(
    #     {"get": "list", "post": "create"}
    # ), name="viewsets-list"),
    # path("viewsets/<int:pk>/", views.CourseViewSet.as_view(
    #     {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    # ), name="viewsets-detail"),
    path("", include(router.urls)),
]
