from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .supabase_client import supabase

# ----------------- API for Jiji -----------------

def index(request):
    return render(request, "index.html")

@api_view(["POST"])
def ask_jiji(request):
    """
    Accept a topic query, search Supabase topics table,
    and return a structured response including description,
    PPT link, and Video link.
    """
    query = request.data.get("question", "").strip()

    if not query:
        return Response(
            {"error": "Please provide a topic to explain."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Search for the topic in the 'topics' table
        result = supabase.table("topics") \
            .select("*") \
            .ilike("title", f"%{query}%") \
            .limit(1) \
            .execute()

        topic_data = result.data[0] if result.data else None
    except Exception as e:
        print("Supabase fetch error:", e)
        return Response(
            {"error": "Failed to fetch topic from Supabase."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    if topic_data:
        # Build response with one explanation paragraph and links
        response_data = {
            "answer": topic_data.get("description", f"Here's a brief overview of '{query}': Explore PPTs or videos to learn more."),
            "ppt": [{"title": topic_data["title"], "url": topic_data["ppt_url"]}] if topic_data.get("ppt_url") else [],
            "video": [{"title": topic_data["title"], "url": topic_data["video_url"]}] if topic_data.get("video_url") else []
        }
    else:
        # Fallback AI-like explanation
        response_data = {
            "answer": (
                f"I'm here to help! I couldn't find specific resources for '{query}', "
                "but here's a quick tip: Think about the key concepts of this topic and "
                "try searching online for PPTs or videos. You can also ask me for another topic!"
            ),
            "ppt": [],
            "video": []
        }

    return Response(response_data, status=status.HTTP_200_OK)

# ----------------- Web pages -----------------

def signup_user(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
            return redirect("index")

        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        login(request, user)
        return redirect("dashboard")

def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("index")

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

def logout_user(request):
    logout(request)
    return redirect("index")
